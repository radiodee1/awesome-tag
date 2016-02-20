package org.davidliebman.tag;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;

/**
 * Created by dave on 2/20/16.
 */
public class ATAGPanel extends JPanel{

    private String filename = "";
    private BufferedImage image;

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

    public void setExtraData(ATAGProcCsv.CsvLine line) {
        if (line.getSpecifications().size() < ATAGProcCsv.FACE_HEIGHT) return;

        fx = line.getSpecifications().get(ATAGProcCsv.FACE_X);
        fy = line.getSpecifications().get(ATAGProcCsv.FACE_Y);
        fheight = line.getSpecifications().get(ATAGProcCsv.FACE_HEIGHT);
        fwidth = line.getSpecifications().get(ATAGProcCsv.FACE_WIDTH);
        addOutline = true;

    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (image != null) {
            g.drawImage(image, 0, 0, null);

            if(addOutline) {
                g.setColor(Color.blue);
                g.drawRect((int) fx, (int) fy, (int) fwidth, (int) fheight);
                System.out.println("add line.");
            }
        }
    }
}
