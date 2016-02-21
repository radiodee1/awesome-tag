package org.davidliebman.tag;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;

/**
 * Created by dave on 2/20/16.
 */
public class ATAGPanel extends JPanel{

    private String filename = "";
    private BufferedImage image;

    private ArrayList<ATAGProcCsv.CsvLine> listFaces;

    private double fx,fy,fheight,fwidth;
    private boolean addOutline = false;

    public ATAGPanel() {
    }

    public ATAGPanel(String im) {
        setFilename(im);
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

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (image != null) {
            g.drawImage(image, 0, 0, null);

            if(addOutline) {
                for (int i = 0; i < listFaces.size(); i ++) {
                    fx = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_X);
                    fy = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_Y);
                    fwidth = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_WIDTH);
                    fheight = listFaces.get(i).getSpecifications().get(ATAGProcCsv.FACE_HEIGHT);
                    g.setColor(Color.blue);
                    g.drawRect((int) fx, (int) fy, (int) fwidth, (int) fheight);
                    System.out.println("add line.");

                }


            }
        }
    }
}
