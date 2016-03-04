package org.davidliebman.tag;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.ArrayList;

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

    private Thread textThread = null;

    //private double fx,fy,fheight,fwidth;
    private boolean addOutline = false;
    private boolean showBlueFaceBox = false;
    private boolean showPredictBoxes = false;
    private boolean showStandartOut = false;

    private int textSizeW = 44, textSizeH = 27;

    public ATAGPanel() {
    }

    public ATAGPanel(String im) {
        setFilename(im);
    }

    public void standardOutDisplay() {
        showStandartOut = true;
        baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        textField = new JTextArea("text", textSizeH,textSizeW);
        textField.setLineWrap(true);
        textField.setWrapStyleWord(true);
        //textField.setPreferredSize(null);
        scrollPane = new JScrollPane( textField,ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED,ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);


        add(scrollPane,BorderLayout.WEST);
        scrollPane.setBackground(Color.WHITE);


        textThread = new Thread() {
            public void run() {
                // do stuff
                int len = 0;// baos.size();


                while ( true) {
                    try {
                        if (len != baos.size()) {
                            textField.setText(baos.toString());
                            len = baos.size();
                            //System.out.println("x");
                            System.out.flush();
                            baos.flush();
                            revalidate();
                            scrollPane.getVerticalScrollBar().setValue((int) ATAGPanel.this.getPreferredSize().getHeight());
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
            }
        };
        textThread.start();

        try {
            baos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        //textField.setText(baos.toString());
        revalidate();


    }

    public void standardOutReset() {
        showStandartOut = false;
        if (textThread != null && textThread.isAlive()) textThread.interrupt();

        System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out)));
        this.remove(scrollPane);
        revalidate();
        repaint();
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
                    fx = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_X);
                    fy = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_Y);
                    fwidth = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_WIDTH);
                    fheight = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_HEIGHT);

                    if(showBlueFaceBox) {
                        g.setColor(Color.blue);
                        g.drawRect((int) fx, (int) fy, (int) fwidth, (int) fheight);
                    }
                    System.out.println("add line.");

                    g.setColor(Color.GREEN);
                    if (listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_LABEL_NO_OUTPUT) >= 0.5d) {
                        g.setColor(Color.RED);
                    }
                    else {
                        //foundOutput = true;
                    }
                    if (listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_LABEL_1) >= 0.5d) {
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
