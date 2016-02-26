package org.davidliebman.tag;



import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

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
    private JButton buttonPrevious;
    private JButton buttonNext;

    private ArrayList<ATAGProcCsv.CsvLine> listFaces;

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

        buttonPrevious = new JButton();
        buttonNext = new JButton();

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
                //String out = var.selectFolder("Folder");
                String outNum = var.getUserInputString(frame,"Split Number","Enter a starting 'split' number (1 - 10):","1");
                String out = var.getSplitFolderFromNumber(outNum.trim());
                if (!outNum.contentEquals("")) {
                    var.configSlpitStartNum = outNum.trim();
                    var.writeConfigText(ATAG.DOTFOLDER_SPLIT_START, var.configSlpitStartNum);
                }
                if (!out.contentEquals("")) {
                    var.configSplitFolderName = out;
                    var.writeConfigText(ATAG.DOTFOLDER_SPLIT_FOLDER_NAME, var.configSplitFolderName);
                    setDisplayText();
                }
            }
        });

        buttonCsvSingle.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                //String out = var.selectFile("CSV");
                String outNum = var.getUserInputString(frame,"Split Number","Enter a current 'split' number (1 - 10):","1");
                String out = var.getSplitFolderFromNumber(outNum.trim());
                if(!outNum.contentEquals("")) {
                    var.configSplitCurrentNum = outNum.trim();
                    var.writeConfigText(ATAG.DOTFOLDER_SPLIT_CURRENT, var.configSplitCurrentNum);
                }
                if (!out.contentEquals("")) {
                    var.configCsvFileSingle = out;
                    var.writeConfigText(ATAG.DOTFOLDER_SINGLE_CSV_FILENAME, var.configCsvFileSingle);
                    setDisplayText();
                }
            }
        });

        buttonCsvSecond.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                //String out = var.selectFile("CSV");
                String outNum = var.getUserInputString(frame,"Split Number","Enter a ending 'split' number (1 - 10):","10");
                String out = var.getSplitFolderFromNumber(outNum.trim());
                if(!outNum.contentEquals("")) {
                    var.configSplitStopNum = outNum.trim();
                    var.writeConfigText(ATAG.DOTFOLDER_SPLIT_END, var.configSplitStopNum);
                }
                if (!out.contentEquals("")) {
                    var.configCsvSecond = out.trim();
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
                String outBasename = var.getUserInputString(frame,"Base Name","Enter a string for a file base name:","my");
                String out = var.getMyCsvFilenameFromBaseString(outBasename, "#");
                //String out = var.selectFile("CSV");
                if(!outBasename.contentEquals("")) {
                    var.configSplitCSVBasename = outBasename;
                    var.writeConfigText(ATAG.DOTFOLDER_BASENAME, var.configSplitCSVBasename);
                }

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
                    //proc.saveCsvLocal();
                    try {
                        int start = Integer.valueOf(var.configSlpitStartNum.trim());
                        int stop = Integer.valueOf(var.configSplitStopNum.trim());
                        int keep = Integer.valueOf(var.configSplitCurrentNum.trim());
                        proc.saveCsvLocal(start,stop,keep);
                    }
                    catch (Exception i) {
                        //do nothing
                    }


                }
            }
        });

        buttonAddLine.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (proc.getLocalList() != null) {
                    listFaces = proc.getFirstMatchByName();
                    ((ATAGPanel)imagePanel).setExtraDataFaces(listFaces);
                    imagePanel.repaint();
                }
            }
        });

        buttonPrevious.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                proc.getPreviousFilename();
                var.writeConfigText(ATAG.DOTFOLDER_LAST_IMAGE, var.configLastImage);
                setDisplayText();
                imagePanel.repaint();
            }
        });

        buttonNext.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                proc.getNextFilename();
                var.writeConfigText(ATAG.DOTFOLDER_LAST_IMAGE, var.configLastImage);
                setDisplayText();
                imagePanel.repaint();
            }
        });
    }

    private void setDisplayText() {
        if(var == null) return;
        databaseRoot.setText(var.configRootDatabase);
        databaseRoot.setToolTipText(var.configRootDatabase);

        splitFolderName.setText(var.configSplitFolderName);
        splitFolderName.setToolTipText(var.configSplitFolderName);
        buttonSplit.setText("Split Start Num");

        csvFileSingle.setText(var.configCsvFileSingle);
        csvFileSingle.setText(var.configCsvFileSingle);
        buttonCsvSingle.setText("Current Split Num");

        csvFileSecond.setText(var.configCsvSecond);
        csvFileSecond.setToolTipText(var.configCsvSecond);
        buttonCsvSecond.setText("Split End Num");

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
