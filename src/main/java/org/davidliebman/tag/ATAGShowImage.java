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
    private JButton buttonLoadCsv;
    private JButton buttonModCsv;
    private JButton buttonTrainCNN;
    private JButton buttonTestCNN;
    private JPanel buttonBar;
    private JButton buttonAddLine;

    private ATAGProcCsv.CsvLine line;

    private ATAG var;
    private ATAGProcCsv proc;

    JFrame frame ;


    private void createUIComponents() {
        // TODO: place custom component creation code here
        databaseRoot = new JLabel();
        splitFolderName = new JLabel();
        csvFileSingle = new JLabel();
        csvFileSecond = new JLabel();
        csvFileLocal = new JLabel();
        localDatabase = new JLabel();
        programName = new JLabel();
        imagePanel =  new ATAGPanel();
        //formPanel = new JPanel();

        buttonImage = new JButton();
        buttonRoot = new JButton();
        buttonSplit = new JButton();
        buttonCsvSingle = new JButton();
        buttonCsvSecond = new JButton();
        buttonDBLocal = new JButton();
        buttonCsvLocal = new JButton();

        buttonLoadCsv = new JButton();
        buttonModCsv = new JButton();
        buttonTrainCNN = new JButton();
        buttonTestCNN = new JButton();
        buttonAddLine = new JButton();

        buttonImage.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String out = var.selectImage("Image");
                if (!out.contentEquals("")) {
                    var.configLastImage = out;
                    var.writeConfigText(ATAG.DOTFOLDER_LAST_IMAGE, var.configLastImage);
                    setDisplayText();
                    imagePanel.repaint();

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

        buttonLoadCsv.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (proc != null) {
                    proc.loadCsvStart();
                }
            }
        });

        buttonModCsv.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (proc != null) {
                    proc.saveCsvLocal();
                }
            }
        });

        buttonAddLine.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (proc.getLocalList() != null) {
                    line = proc.getFirstMatchByName();
                    ((ATAGPanel)imagePanel).setExtraData(line);
                    imagePanel.repaint();
                }
            }
        });
    }

    private void setDisplayText() {
        if(var == null) return;
        databaseRoot.setText(var.configRootDatabase);
        databaseRoot.setToolTipText(var.configRootDatabase);

        splitFolderName.setText(var.configSplitFolderName);
        splitFolderName.setToolTipText(var.configSplitFolderName);

        csvFileSingle.setText(var.configCsvFileSingle);
        csvFileSingle.setText(var.configCsvFileSingle);

        csvFileSecond.setText(var.configCsvSecond);
        csvFileSecond.setToolTipText(var.configCsvSecond);

        csvFileLocal.setText(var.configCsvLocal);
        csvFileLocal.setToolTipText(var.configCsvLocal);

        localDatabase.setText(var.configLocalRoot);
        localDatabase.setToolTipText(var.configLocalRoot);

        programName.setText(var.configLastImage);
        programName.setToolTipText(var.configLastImage);

        ((ATAGPanel)imagePanel).setFilename(var.configLastImage);


    }




    public   ATAGShowImage(ATAG v, ATAGProcCsv p) {
        frame = new JFrame("ATAGShowImage");
        frame.setContentPane(formPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);

        var = v;
        proc = p;
        setDisplayText();
        imagePanel.repaint();
    }




}
