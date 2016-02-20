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

    public ATAGPanel() {
    }

    public ATAGPanel(String im) {
        setFilename(im);
    }

    public void setFilename(String im) {
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


    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (image != null) {
            g.drawImage(image, 0, 0, null);

        }
    }
}
