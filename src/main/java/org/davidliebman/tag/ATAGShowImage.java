package org.davidliebman.tag;



import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * Created by dave on 2/19/16.
 */
public class ATAGShowImage {
    private JLabel databaseRoot;
    private JLabel splitFolderName;
    private JLabel csvFileSingle;
    private JLabel csvFileSecond;
    private JLabel localDatabase;
    private JLabel csvFileLocal;
    private JLabel programName;
    private JPanel imagePanel;
    private JPanel formPanel; // do not instantiate!!
    private JButton buttonImage;
    private JButton buttonRoot;
    private JButton buttonSplit;
    private JButton buttonCsvSingle;
    private JButton buttonCsvSecond;
    private JButton buttonDBLocal;
    private JButton buttonCsvLocal;



    private ATAG var;

    //JFrame frame ;//= new JFrame("ATAGShowImage");


    private void createUIComponents() {
        // TODO: place custom component creation code here
        databaseRoot = new JLabel();
        splitFolderName = new JLabel();
        csvFileSingle = new JLabel();
        csvFileSecond = new JLabel();
        csvFileLocal = new JLabel();
        localDatabase = new JLabel();
        programName = new JLabel();
        imagePanel = new JPanel();
        //formPanel = new JPanel();

        buttonImage = new JButton();
        buttonRoot = new JButton();
        buttonSplit = new JButton();
        buttonCsvSingle = new JButton();
        buttonCsvSecond = new JButton();
        buttonDBLocal = new JButton();
        buttonCsvLocal = new JButton();

        buttonImage.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String out = var.selectImage("Image");
                if (!out.contentEquals("")) {
                    var.configLastImage = out;
                    var.writeConfigText(ATAG.DOTFOLDER_LAST_IMAGE, var.configLastImage);
                    setDisplayText();
                }
            }
        });

        buttonRoot.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String out = var.selectFolder("Folder");
                if (!out.contentEquals("")) {
                    var.configRootDatabase = out;
                    var.writeConfigText(ATAG.DOTFOLDER_ROOT_DATABASE_NAME, var.configRootDatabase);
                    setDisplayText();
                }
            }
        });

        buttonSplit.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String out = var.selectFolder("Folder");
                if (!out.contentEquals("")) {
                    var.configSplitFolderName = out;
                    var.writeConfigText(ATAG.DOTFOLDER_SPLIT_FOLDER_NAME, var.configSplitFolderName);
                    setDisplayText();
                }
            }
        });

        buttonCsvSingle.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String out = var.selectFile("CSV");
                if (!out.contentEquals("")) {
                    var.configCsvFileSingle = out;
                    var.writeConfigText(ATAG.DOTFOLDER_SINGLE_CSV_FILENAME, var.configCsvFileSingle);
                    setDisplayText();
                }
            }
        });

        buttonCsvSecond.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String out = var.selectFile("CSV");
                if (!out.contentEquals("")) {
                    var.configCsvSecond = out;
                    var.writeConfigText(ATAG.DOTFOLDER_SECOND_CSV_FILENAME, var.configCsvSecond);
                    setDisplayText();
                }
            }
        });

        buttonDBLocal.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String out = var.selectFolder("Folder");
                if (!out.contentEquals("")) {
                    var.configLocalRoot = out;
                    var.writeConfigText(ATAG.DOTFOLDER_LOCAL_DATA_FOLDERNAME, var.configLocalRoot);
                    setDisplayText();
                }
            }
        });

        buttonCsvLocal.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String out = var.selectFile("CSV");
                if (!out.contentEquals("")) {
                    var.configCsvLocal = out;
                    var.writeConfigText(ATAG.DOTFOLDER_LOCAL_DATA_CSV, var.configCsvLocal);
                    setDisplayText();
                }
            }
        });
    }

    private void setDisplayText() {
        if(var == null) return;
        databaseRoot.setText(var.configRootDatabase);
        splitFolderName.setText(var.configSplitFolderName);
        csvFileSingle.setText(var.configCsvFileSingle);
        csvFileSecond.setText(var.configCsvSecond);
        csvFileLocal.setText(var.configCsvLocal);
        localDatabase.setText(var.configLocalRoot);
        programName.setText(var.configLastImage);
        System.out.println(databaseRoot.getText());
    }




    public   ATAGShowImage(ATAG v) {
        JFrame frame = new JFrame("ATAGShowImage");
        frame.setContentPane(formPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);

        var = v;
        setDisplayText();
    }




}
