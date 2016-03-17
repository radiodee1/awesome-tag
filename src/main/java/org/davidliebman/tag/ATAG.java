package org.davidliebman.tag;


import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.io.*;


/**
 * Created by dave on 2/19/16.
 */
public class ATAG {
    public static final String DOTFOLDER = ".atag";
    public static final String DOTFOLDER_ROOT_DATABASE_NAME = "root_database";
    public static final String DOTFOLDER_SPLIT_FOLDER_NAME = "split_folder_name";
    public static final String DOTFOLDER_SINGLE_CSV_FILENAME = "csv_file_single";
    public static final String DOTFOLDER_SECOND_CSV_FILENAME = "csv_file_second";
    public static final String DOTFOLDER_LOCAL_DATA_FOLDERNAME = "local_database";
    public static final String DOTFOLDER_LOCAL_DATA_CSV = "my_csv_name";
    public static final String DOTFOLDER_LAST_IMAGE = "image_name";
    public static final String DOTFOLDER_SAVED_CURSOR = "saved_cursor";
    public static final String DOTFOLDER_SAVED_SPLIT = "saved_split";

    public static final String DOTFOLDER_SPLIT_START = "split_start";
    public static final String DOTFOLDER_SPLIT_END = "split_end";
    public static final String DOTFOLDER_SPLIT_CURRENT = "split_current";
    public static final String DOTFOLDER_BASENAME = "base_name";

    public String configRootDatabase = "";
    public String configSplitFolderName = "";
    public String configCsvFileSingle = "";

    public String configCsvSecond = "";
    public String configLocalRoot = "";
    public String configCsvLocal = "";

    public String configLastImage = "";

    public String configHomeDirectory = "";

    public String configLastCursor = "";
    public String configLastSplit = "";

    public String configSlpitStartNum = "";
    public String configSplitStopNum = "";
    public String configSplitCurrentNum = "";
    public String configSplitCSVBasename = "";

    public static final String DEFAULT_ROOT_DATABASE = "workspace";
    public static final String DEFAULT_SPLIT_FOLDERNAME = "split10";
    public static final String DEFAULT_SINGLE_CSV_FILENAME = "some.csv";
    public static final String DEFAULT_SECOND_CSV_FILENAME = "second.csv";
    public static final String DEFAULT_LOCAL_DATA_FOLDERNAME = "local";
    public static final String DEFAULT_LOCAL_DATA_CSV = "my.csv";
    public static final String DEFAULT_LAST_IMAGE = "image.png";
    public static final String DEFAULT_BIASES_NAME = "lenet-conv1-rbm1-rc38_faces";


    public String configRootLocal = "";


    public static final int CNN_LABELS = 2;
    public static final int CNN_DIM_SIDE = 56; //60
    public static final int CNN_BATCH_SIZE = 32; //64
    public static final int CNN_CHANNELS = 3;
    public static final int CNN_DIM_PIXELS = 56; //60

    public static final int THREAD_TRAIN = 1;
    public static final int THREAD_TEST = 2;
    public static final int THREAD_PREDICT = 3;
    public static final int THREAD_NONE = 0;

    public ATAG () {

        try {
            setupHomeFolder();
            setupDotFolder();
            readDotFolder();
        }
        catch (Exception e) {
            e.printStackTrace();
        }

    }

    public void setupHomeFolder () {
        configHomeDirectory = System.getProperty("user.home");
    }


    public void setupDotFolder() throws Exception {

        if (configHomeDirectory.contentEquals("")){
            throw new Exception();
        }

        String pathDotFolder = configHomeDirectory + File.separator + DOTFOLDER;
        File fileDotFolder = new File(pathDotFolder);

        if (!fileDotFolder.exists()) fileDotFolder.mkdirs();
    }

    public String readConfigText(String textName) throws Exception {
        return readConfigText(textName, "");
    }

    public String readConfigText( String textName , String defaultText) throws Exception {

        String line = null;
        int count = 0;
        String output = null;

        if (configHomeDirectory.contentEquals("") || textName.contentEquals("")){
            throw new Exception();
        }
        String pathDotFolderFile = configHomeDirectory + File.separator + DOTFOLDER + File.separator + textName;

        File dotFile = new File(pathDotFolderFile);

        if (!dotFile.exists()) {
            writeConfigText(textName,defaultText);
        }

        FileReader fileReader = new FileReader(dotFile);
        BufferedReader bufferedReader = new BufferedReader(fileReader);

        System.out.print(pathDotFolderFile);

        while((line = bufferedReader.readLine()) != null) {
            if (line.contentEquals("")) {
                throw new Exception();
            }
            else {
                count = count + 1;
                System.out.println(" " + line);
                output = line;
            }
        }
        bufferedReader.close();

        return output;
    }

    public void writeConfigText(String textName, String contents)  {

        try {
            if (configHomeDirectory.contentEquals("") || textName.contentEquals("")) {
                throw new Exception();
            }
            String pathDotFolderFile = configHomeDirectory + File.separator + DOTFOLDER + File.separator + textName;
            File dotFile = new File(pathDotFolderFile);

            String newline = System.getProperty("line.separator");

            FileWriter fw = new FileWriter(dotFile);
            BufferedWriter writer = new BufferedWriter(fw);

            writer.write(contents + newline);
            writer.close();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void readDotFolder()throws Exception {
        configRootDatabase = this.readConfigText(DOTFOLDER_ROOT_DATABASE_NAME , DEFAULT_ROOT_DATABASE);
        configSplitFolderName = this.readConfigText(DOTFOLDER_SPLIT_FOLDER_NAME , DEFAULT_SPLIT_FOLDERNAME);
        configCsvFileSingle = this.readConfigText(DOTFOLDER_SINGLE_CSV_FILENAME,  DEFAULT_SINGLE_CSV_FILENAME);

        if (configRootDatabase.contentEquals("") || configSplitFolderName.contentEquals("") || configCsvFileSingle.contentEquals("")) {
            throw new Exception();
        }

        configCsvSecond = this.readConfigText(DOTFOLDER_SECOND_CSV_FILENAME, DEFAULT_SECOND_CSV_FILENAME);
        configLocalRoot = this.readConfigText(DOTFOLDER_LOCAL_DATA_FOLDERNAME, DEFAULT_LOCAL_DATA_FOLDERNAME);
        configCsvLocal = this.readConfigText(DOTFOLDER_LOCAL_DATA_CSV,DEFAULT_LOCAL_DATA_CSV);

        if (configCsvSecond.contentEquals("") || configLocalRoot.contentEquals("") || configCsvLocal.contentEquals("")) {
            throw new Exception();
        }

        configLastImage = this.readConfigText(DOTFOLDER_LAST_IMAGE, DEFAULT_LAST_IMAGE);

        if (configLastImage.contentEquals("")) {
            throw new Exception();
        }
        configLastCursor = this.readConfigText(DOTFOLDER_SAVED_CURSOR, "0");
        configLastSplit = this.readConfigText(DOTFOLDER_SAVED_SPLIT, "1");

        if(configLastCursor.contentEquals("") || configLastSplit.contentEquals("")) {
            throw new Exception();
        }

        configSlpitStartNum = this.readConfigText(DOTFOLDER_SPLIT_START,"1");
        configSplitStopNum = this.readConfigText(DOTFOLDER_SPLIT_END,"10");
        configSplitCurrentNum = this.readConfigText(DOTFOLDER_SPLIT_CURRENT,"1");
        configSplitCSVBasename = this.readConfigText(DOTFOLDER_BASENAME,"my");

        if(configSlpitStartNum.contentEquals("") || configSplitStopNum.contentEquals("") || configSplitCurrentNum.contentEquals("") || configSplitCSVBasename.contentEquals("")) {
            throw new Exception();
        }
    }

    public String selectFolder(String description) {
        UIManager.put("FileChooser.readOnly", Boolean.TRUE);

        String returnString = "";

        JFileChooser chooser = new JFileChooser();

        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        int returnVal = chooser.showOpenDialog(null);
        if (returnVal == JFileChooser.APPROVE_OPTION) {
            returnString = chooser.getSelectedFile().getAbsolutePath();
        }

        return returnString;
    }

    public String selectFile(String description )  {
        UIManager.put("FileChooser.readOnly", Boolean.TRUE);

        String returnString = "";

        JFileChooser chooser = new JFileChooser();
        FileNameExtensionFilter filter = new FileNameExtensionFilter(description,"csv");
        chooser.setFileFilter(filter);
        int returnVal = chooser.showOpenDialog(null);
        if (returnVal == JFileChooser.APPROVE_OPTION) {
            returnString = chooser.getSelectedFile().getAbsolutePath();
        }

        return returnString;

    }

    public String selectImage(String description )  {
        UIManager.put("FileChooser.readOnly", Boolean.TRUE);

        String returnString = "";

        JFileChooser chooser = new JFileChooser(getStartFolder());
        FileNameExtensionFilter filter = new FileNameExtensionFilter(description,"png","bmp","jpg","jpeg");
        chooser.setFileFilter(filter);
        int returnVal = chooser.showOpenDialog(null);
        if (returnVal == JFileChooser.APPROVE_OPTION) {
            returnString = chooser.getSelectedFile().getAbsolutePath();
        }

        return returnString;

    }

    public String getStartFolder() {
        String returnString = configHomeDirectory;

        if (configRootDatabase.contains(File.separator)) {
            returnString = configRootDatabase;
        }

        //System.out.println(configRootDatabase + " " + File.separator);

        return returnString;
    }

    public String getUserInputString(JFrame frame, String title, String description, String def) {

        String in = (String)JOptionPane.showInputDialog(
                frame,
                description,
                title,
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                def);

        return in;
    }

    public String getSplitFolderFromNumber(String num) {
        String out = "";
        out = configRootDatabase + File.separator + "split" + num + File.separator + "train_" + num + ".csv";
        return out;
    }

    public String getMyCsvFilenameFromBaseString(String name, String num) {
        String out = configLocalRoot + File.separator + name.trim() + "_" + num.trim() + ".csv";
        return out;
    }


}
