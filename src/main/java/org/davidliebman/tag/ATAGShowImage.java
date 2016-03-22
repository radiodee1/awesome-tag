package org.davidliebman.tag;



import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.nd4j.linalg.api.ndarray.INDArray;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
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
    private JButton buttonPredict;

    private ArrayList<ATAGProcCsv.CsvLine> listFaces;

    private ATAG var;
    private ATAGProcCsv proc;

    JFrame frame ;

    private boolean debugConsecOutput = false;
    private boolean debugReuseModel = false;
    private boolean debugShowRawPredictList = false;

    private ATAGShowImageDialog dialog = null;

    private SwingWorker<Object,Object> dialogThread = null;

    private ATAGCnn cnnThread = null;
    private int threadType = 0;
    private ArrayList<ATAGProcCsv.CsvLine> predictList;

    private MultiLayerNetwork model = null;

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

        buttonPredict = new JButton();

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
                    var.configLastCursor = "0";
                    var.configLastSplit = var.configSlpitStartNum;
                    var.writeConfigText(ATAG.DOTFOLDER_SAVED_CURSOR, var.configLastCursor);
                    var.writeConfigText(ATAG.DOTFOLDER_SAVED_SPLIT, var.configLastSplit);

                    Object[] options = {"ERASE", "KEEP"};
                    int n = JOptionPane.showOptionDialog(frame,
                            "The cursor has been reset. Do you want to erase the biases?",
                            "Clear Previous Data",
                            JOptionPane.YES_NO_CANCEL_OPTION,
                            JOptionPane.QUESTION_MESSAGE,
                            null,
                            options,
                            options[1]);

                    if (n == 0) {
                        File file = new File(var.configLocalRoot + File.separator + ATAG.DEFAULT_BIASES_NAME + ".bin");
                        if (file.exists()) file.delete();
                        File file2 = new File(var.configLocalRoot + File.separator + ATAG.DEFAULT_BIASES_NAME + ".updater.bin");
                        if (file2.exists()) file2.delete();
                    }
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
                if (cnnThread != null && (! cnnThread.isAlive() ||cnnThread.getState() == Thread.State.WAITING)) {
                    ((ATAGPanel)imagePanel).standardOutReset();
                    cnnThread = null;
                    setDisplayText();
                    imagePanel.repaint();
                }
                if (proc.getLocalList() != null) {
                    listFaces = proc.getFirstMatchByName();
                    ((ATAGPanel)imagePanel).setExtraDataFaces(listFaces);
                    ((ATAGPanel)imagePanel).setShowPredictBoxes(false);
                    imagePanel.repaint();

                    Object[] options = {"PRINT", "SKIP"};
                    int n = JOptionPane.showOptionDialog(frame,
                            "The square for face outlines can be printed to text output.",
                            "Show Data",
                            JOptionPane.YES_NO_CANCEL_OPTION,
                            JOptionPane.QUESTION_MESSAGE,
                            null,
                            options,
                            options[1]);

                    if (n == 0) {
                        proc.printListToStandardOut(listFaces);
                    }


                }
            }
        });

        buttonPrevious.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (cnnThread != null && (! cnnThread.isAlive() ||cnnThread.getState() == Thread.State.WAITING)) {
                    ((ATAGPanel)imagePanel).standardOutReset();
                    cnnThread = null;
                    setDisplayText();
                }
                proc.getPreviousFilename();
                var.writeConfigText(ATAG.DOTFOLDER_LAST_IMAGE, var.configLastImage);
                setDisplayText();
                imagePanel.repaint();
            }
        });

        buttonNext.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (cnnThread != null && (! cnnThread.isAlive() ||cnnThread.getState() == Thread.State.WAITING)) {
                    ((ATAGPanel)imagePanel).standardOutReset();
                    cnnThread = null;
                    setDisplayText();
                }
                proc.getNextFilename();
                var.writeConfigText(ATAG.DOTFOLDER_LAST_IMAGE, var.configLastImage);
                setDisplayText();
                imagePanel.repaint();
            }
        });

        buttonPredict.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                //
                threadType = ATAG.THREAD_PREDICT;
                frame.setTitle("Please Wait...");
                if (cnnThread != null && (! cnnThread.isAlive() ||cnnThread.getState() == Thread.State.WAITING)) {
                    ((ATAGPanel)imagePanel).standardOutReset();
                    cnnThread = null;
                    setDisplayText();
                }
                waitDialogShow();
                predictList = proc.getPredictListFromImage(var.configLastImage);
                try {
                    ATAGCnnDataSet predictData = new ATAGCnnDataSet(predictList, var, 0, true, 0.0f, 0, 0, true);

                    //MultiLayerNetwork model = null;
                    ((ATAGPanel) imagePanel).setShowPredictBoxes(true);

                    cnnThread = new ATAGCnn(var,proc);
                    if (model != null) {
                        cnnThread.setDoGenerateNewModel(false);
                        cnnThread.setModel(model);
                        //cnnThread.init();
                        cnnThread.setDoLoadSaveModel(false);
                    }
                    else {
                        cnnThread.setDoLoadSaveModel(true);
                    }
                    cnnThread.setDoFit(false); // ensure 'run()' does no training
                    cnnThread.setDoTest(false); // ensure 'run()' does no training
                    cnnThread.setDoLoadData(false); // ensure 'run()' does no training
                    //cnnThread.setDoLoadSaveModel(true); // ... must load!!
                    cnnThread.setExitEarly(false);
                    cnnThread.setDoPredict(true);
                    cnnThread.setPredictData(predictData);
                    cnnThread.start(); // create model and load biases... on this thread!!

                        //model = cnn.getModel();
                    dialogThread = new StartDialog();
                    dialogThread.execute();


                }
                catch (Exception i ) {i.printStackTrace();}
            }
        });

        buttonTrainCNN.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                threadType = ATAG.THREAD_TRAIN;
                if (cnnThread != null&& cnnThread.isAlive()) {
                    // TERMINATE AND SET TO NULL
                    frame.setTitle("Wait...");
                    buttonTrainCNN.setText("Wait");
                    cnnThread.setExitEarly(true);
                    waitDialogShow();

                    dialogThread = new StartDialog();
                    dialogThread.execute();

                }
                else if ( threadType == ATAG.THREAD_TRAIN && cnnThread != null && (! cnnThread.isAlive() ||cnnThread.getState() == Thread.State.WAITING)) {
                    ((ATAGPanel)imagePanel).standardOutReset();
                    cnnThread = null;
                    frame.setTitle("Awesome Tag");
                    setDisplayText();
                }
                else
                {
                    // CREATE INSTANCE AND RUN
                    ((ATAGPanel)imagePanel).standardOutDisplay();
                    frame.setTitle("TRAIN");
                    buttonTrainCNN.setText("Interrupt");

                    try {

                        cnnThread = new ATAGCnn(var, proc);
                        cnnThread.setDoGenerateNewModel(true);
                        cnnThread.setDoLoadData(true); //ATAGCnnDataSet.java
                        cnnThread.setDoTest(false);
                        cnnThread.setDoFit(true);
                        cnnThread.setDoLoadSaveModel(true);
                        cnnThread.setExitEarly(false);
                        cnnThread.start();
                    }
                    catch (Exception i) {i.printStackTrace();}

                }
            }
        });

        buttonTestCNN.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                threadType = ATAG.THREAD_TEST;


                if (cnnThread != null && cnnThread.isAlive()) {
                    // TERMINATE AND SET TO NULL
                    frame.setTitle("Wait...");
                    buttonTestCNN.setText("Wait");
                    cnnThread.setExitEarly(true);
                    waitDialogShow();
                    dialogThread = new StartDialog();
                    dialogThread.execute();

                }
                else if ( threadType == ATAG.THREAD_TEST && cnnThread != null && (! cnnThread.isAlive() ||cnnThread.getState() == Thread.State.WAITING)) {
                    ((ATAGPanel)imagePanel).standardOutReset();
                    cnnThread = null;
                    frame.setTitle("Awesome Tag");
                    setDisplayText();

                }
                else  {
                    // CREATE INSTANCE AND RUN
                    ((ATAGPanel)imagePanel).standardOutDisplay();
                    frame.setTitle("TEST");
                    buttonTestCNN.setText("Interrupt");

                    try {


                        cnnThread = new ATAGCnn(var, proc);
                        if(model != null) {
                            cnnThread.setDoGenerateNewModel(false);
                            cnnThread.setModel(model);
                            //cnnThread.init();
                            cnnThread.setDoLoadSaveModel(false);
                        }
                        else {
                            cnnThread.setDoLoadSaveModel(true);
                        }
                        cnnThread.setDoLoadData(true); //ATAGCnnDataSet.java
                        cnnThread.setDoTest(true);
                        cnnThread.setDoFit(false);
                        //cnnThread.setDoLoadSaveModel(true); // load and save!
                        cnnThread.setExitEarly(false);
                        cnnThread.start();
                    }
                    catch (Exception i) {i.printStackTrace();}

                }
            }
        });
    }

    private void renderPredictionOnScreen( INDArray output) {

        ArrayList<ATAGProcCsv.CsvLine> list = predictList;
        //output.linearView();

        int i = 0, j = 0;
        if (list == null || list.size() < 1) return;

        for (int jj = 0; jj < ATAG.CNN_LABELS; jj ++) {
            for (int ii = 0; ii < predictList.size(); ii ++) {
                int labelIndexNumbered = 0;
                int location = ii;// (ATAG.CNN_BATCH_SIZE - 1) - ii;

                if (debugConsecOutput) {
                    labelIndexNumbered = ii * ATAG.CNN_LABELS + jj;
                    i = ii;
                    j = jj;

                }
                else {
                    labelIndexNumbered = jj * predictList.size() + ii;
                    i = ii;
                    j = jj;

                }
                if (jj < ATAG.CNN_LABELS - 1) {
                    switch (jj) {
                        case 0:
                            list.get(location).getSpecifications().remove(ATAGProcCsv.FACE_LABEL_1);
                            list.get(location).getSpecifications().add(ATAGProcCsv.FACE_LABEL_1, output.getDouble(i,j));
                            break;
                        case 1:
                            list.get(location).getSpecifications().remove(ATAGProcCsv.FACE_LABEL_2);
                            list.get(location).getSpecifications().add(ATAGProcCsv.FACE_LABEL_2, output.getDouble(i,j));
                            break;
                        case 3:
                            list.get(location).getSpecifications().remove(ATAGProcCsv.FACE_LABEL_3);
                            list.get(location).getSpecifications().add(ATAGProcCsv.FACE_LABEL_3, output.getDouble(i,j));
                            break;
                        case 4:
                            list.get(location).getSpecifications().remove(ATAGProcCsv.FACE_LABEL_4);
                            list.get(location).getSpecifications().add(ATAGProcCsv.FACE_LABEL_4, output.getDouble(i,j));
                            break;
                        default:
                            //nothing
                            break;
                    }
                }
                else {
                    list.get(location).getSpecifications().remove(ATAGProcCsv.FACE_LABEL_NO_OUTPUT);
                    list.get(location).getSpecifications().add(ATAGProcCsv.FACE_LABEL_NO_OUTPUT, output.getDouble(i,j));
                }
            }


        }
        proc.saveAnyCsv(var.configLocalRoot + File.separator + "predict.csv",list,null, ATAGProcCsv.CSV_POSITION_FILE_LOCATION);


        ((ATAGPanel)imagePanel).setShowPredictBoxes(true);
        if (debugShowRawPredictList) {

            predictList = proc.getPredictListFromImage(var.configLastImage);
            ((ATAGPanel)imagePanel).setShowAllLines(true);
            ((ATAGPanel)imagePanel).setExtraDataFaces(predictList);
        }
        else {
            ((ATAGPanel)imagePanel).setExtraDataFaces(list);

        }
        imagePanel.repaint();
        frame.setTitle("Awesome Tag");
        waitDialogHide();
    }

    private void waitDialogShow() {

        //dialogThread = new StartDialog();
        //dialogThread.execute();
        if (dialog == null) dialog = new ATAGShowImageDialog(frame);
        dialog.setVisible(true);

    }

    private void waitDialogHide() {
        if (dialogThread != null && dialogThread.getState() == SwingWorker.StateValue.STARTED) {
            dialog.setVisible(false);
            dialogThread.cancel(true);
            dialogThread = null;
        }

        if (dialog != null) {
            dialog.setVisible(false);

            dialog = null;
        }
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

        buttonLoadCsv.setText("Reset Cursor");

        buttonTestCNN.setText("Test CNN");
        buttonTrainCNN.setText("Train CNN");

        buttonNext.setText("Next Pic");
        buttonPrevious.setText("Prev Pic");

        ((ATAGPanel)imagePanel).setFilename(var.configLastImage);


    }

    public ATAGCnn getCnnThread() {return cnnThread;}


    public   ATAGShowImage(ATAG v, ATAGProcCsv p) {
        frame = new JFrame("Awesome Tag");
        frame.setContentPane(formPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        /*
        Dimension preferredSize = new Dimension(-1,-1);
        imagePanel.setPreferredSize(preferredSize);
        ((ATAGPanel)imagePanel).standardOutDisplay();
        */
        
        frame.pack();
        frame.setVisible(true);

        var = v;
        proc = p;
        proc.loadCsvStart();
        setDisplayText();
        imagePanel.repaint();

        frame.setIconImage(Toolkit.getDefaultToolkit().getImage("bigsmilered.png"));
        frame.setName("Awesome Tag");
    }

    class StartDialog extends SwingWorker<Object,Object> {

        @Override
        protected Object doInBackground() throws Exception {

            try {
                cnnThread.join();
                System.out.println("just joined");



            }
            catch (Exception i) {i.printStackTrace();}
            return null;
        }

        @Override
        protected void done() {
            super.done();

            if(threadType == ATAG.THREAD_PREDICT) {
                INDArray output = cnnThread.getPredictOutput();
                renderPredictionOnScreen(output);
            }
            else if (threadType == ATAG.THREAD_TRAIN) {
                ((ATAGPanel) imagePanel).standardOutReset(false);
                //((ATAGPanel) imagePanel).setShowPredictBoxes(false);
                buttonTrainCNN.setText("Clear");
            }
            else if (threadType == ATAG.THREAD_TEST){
                ((ATAGPanel) imagePanel).standardOutReset();
                //((ATAGPanel) imagePanel).setShowPredictBoxes(false);
                buttonTestCNN.setText("Clear");
            }

            MultiLayerNetwork mod = cnnThread.getModel();
            if(debugReuseModel && mod != null) {
                model = mod;
            }

            frame.setTitle("Awesome Tag");
            waitDialogHide();

        }


    }


}
