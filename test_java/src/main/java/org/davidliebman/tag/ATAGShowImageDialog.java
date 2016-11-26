package org.davidliebman.tag;

import javafx.scene.control.ProgressBar;

import javax.swing.*;
import java.awt.*;

/**
 * Created by dave on 3/5/16.
 */
public class ATAGShowImageDialog extends JDialog {

    public ATAGShowImageDialog (JFrame parentFrame) {
        JProgressBar progressBar = new JProgressBar(0,500);
        progressBar.setIndeterminate(true);
        this.add(BorderLayout.CENTER, progressBar);
        this.add(BorderLayout.NORTH, new JLabel("Thread is working. wait several minutes..."));
        this.setTitle("Progress: Please Wait!");
        this.setDefaultCloseOperation(JDialog.DO_NOTHING_ON_CLOSE);
        this.setSize(300, 75);
        this.setLocationRelativeTo(parentFrame);
        this.setModal(false);
        this.pack();
        this.setIconImage(Toolkit.getDefaultToolkit().getImage("bigsmilered.png"));
        this.setVisible(true);

    }


}
