package org.davidliebman.tag;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.*;
import java.util.List;

/**
 * Created by dave on 2/20/16.
 */
public class ATAGPanel extends JPanel{

    private String filename = "";
    private BufferedImage image;

    private ArrayList<ATAGProcCsv.CsvLine> listFaces;
    private ByteArrayOutputStream baos = null;
    private JTextArea textField = null;
    private JScrollPane scrollPane = null;
    //private JScrollBar scrollBar = null;


    private SwingWorker<Object,Object> worker = null;

    //private double fx,fy,fheight,fwidth;
    private boolean addOutline = false;
    private boolean showBlueFaceBox = true;
    private boolean showPredictBoxes = false;
    private boolean showStandartOut = false;

    private int textSizeW = 44, textSizeH = 27;

    public static final double SURENESS = 0.7d;

    public ATAGPanel() {
    }

    public ATAGPanel(String im) {
        setFilename(im);
    }

    public void standardOutDisplay() {
        showStandartOut = true;


        textField = new JTextArea("text output here...", textSizeH,textSizeW);
        textField.setLineWrap(true);
        textField.setWrapStyleWord(true);


        scrollPane = new JScrollPane( textField,ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS,ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
        baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));

        add(scrollPane,BorderLayout.WEST);
        scrollPane.setBackground(Color.WHITE);


        worker = new SwingWorker<Object, Object>() {
            @Override
            protected Object doInBackground() throws Exception {
                int len = 0;// baos.size();

                boolean loop = true;

                while ( loop) {
                    try {
                        if (len != baos.size()) {
                            //textField.setText(baos.toString());
                            len = baos.size();
                            //System.out.println("x");
                            System.out.flush();
                            baos.flush();
                            //revalidate();
                            //scrollPane.getVerticalScrollBar().setValue( (int) (ATAGPanel.this.getPreferredSize().getHeight() + textField.getPreferredSize().getHeight()));
                            publish();

                        }
                        Thread.sleep(2000);
                    }
                    catch (InterruptedException e) {
                        //e.printStackTrace();

                    }
                    catch (Exception e) {
                        standardOutReset();
                        e.printStackTrace();
                    }
                }
                return null;
            }

            @Override
            protected void process(List<Object> chunks) {
                super.process(chunks);
                textField.setText(baos.toString());
                scrollPane.getVerticalScrollBar().setValue( (int) (ATAGPanel.this.getPreferredSize().getHeight() + textField.getPreferredSize().getHeight()));
                revalidate();
            }
        };

        worker.execute();
        /*
        try {
            baos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        */
        //textField.setText(baos.toString());
        revalidate();


    }

    public void standardOutReset() {
        standardOutReset(true);
    }

    public void standardOutReset( boolean repaint) {
        showStandartOut = false;
        if (worker != null ) worker.cancel(true);// .interrupt();

        //baos = null;//new ByteArrayOutputStream();
        System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out)));
        if (scrollPane != null) this.remove(scrollPane);
        revalidate();
        if (repaint) repaint();
        //this.remove(0);
    }

    public void setFilename(String im) {
        addOutline = false;
        filename = im;
        if (!filename.contentEquals("")) {
            try {
                image = ImageIO.read(new File(filename));
                System.out.println(filename + " filename");
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public void setExtraDataFaces(ArrayList<ATAGProcCsv.CsvLine> list) {
        listFaces = list;

        if ( listFaces.isEmpty() || listFaces.get(0).getSpecifications().size() < ATAGProcCsv.FACE_HEIGHT) return;


        addOutline = true;

    }

    public void setShowPredictBoxes( boolean p ) {showPredictBoxes = p;}

    public void showSizes(ATAGProcCsv.CsvLine line) {
        for (int i = 0; i < line.getSpecifications().size(); i ++) {
            if ( i >= ATAGProcCsv.FACE_LABEL_1){
                System.out.print(line.getSpecifications().get(i) + "  --  ");
            }
        }
        System.out.println(line.getSpecifications().get(ATAGProcCsv.FACE_HEIGHT));

    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        boolean foundOutput = false;
        if (image != null && ! showStandartOut) {
            setBackground(Color.LIGHT_GRAY);
            g.drawImage(image, 0, 0, null);

            if(addOutline) {
                for (int i = 0; i < listFaces.size(); i ++) {
                    foundOutput = false;
                    double fx,fy,fwidth, fheight;

                    fwidth = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_WIDTH);
                    fheight = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_HEIGHT);

                    double xcoord = 0, ycoord = 0;
                    if (showBlueFaceBox && !showPredictBoxes) {
                        // ...center cnn over image of face ??
                        xcoord = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_APPROACH_X);
                        ycoord = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_APPROACH_Y);

                        xcoord = xcoord - (ATAG.CNN_DIM_PIXELS - fwidth) / 2;
                        ycoord = ycoord - (ATAG.CNN_DIM_PIXELS - fheight) / 2;

                        g.setColor(Color.blue);
                        g.drawRect((int) xcoord, (int) ycoord, (int) ATAG.CNN_DIM_PIXELS, (int) ATAG.CNN_DIM_PIXELS);
                    }
                    System.out.println("add line.");

                    g.setColor(Color.GREEN);
                    if (listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_LABEL_NO_OUTPUT) >= SURENESS) {
                        g.setColor(Color.RED);
                    }
                    else {
                        //foundOutput = true;
                    }
                    if (listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_LABEL_1) >= SURENESS) {
                        g.setColor(Color.GREEN);
                        foundOutput = true;
                    }
                    fx = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_APPROACH_X);
                    fy = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_APPROACH_Y);

                    if (foundOutput || !showPredictBoxes) {
                        g.drawRect((int) fx, (int) fy, (int) fwidth, (int) fheight);
                    }
                    showSizes(listFaces.get(i));
                }
                if (showPredictBoxes) System.out.println("list length " + listFaces.size());


            }
        }
        else {
            setBackground(Color.WHITE);
        }

    }
}
