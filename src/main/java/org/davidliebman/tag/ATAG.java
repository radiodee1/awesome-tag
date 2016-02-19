package org.davidliebman.tag;

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

    public String configRootDatabase = "";
    public String configSplitFolderName = "";
    public String configCsvFileSingle = "";

    public String configCsvSecond = "";
    public String configLocalRoot = "";
    public String configCsvLocal = "";

    public String configHomeDirectory = "";

    public static final String DEFAULT_ROOT_DATABASE = "workspace";
    public static final String DEFAULT_SPLIT_FOLDERNAME = "split10";
    public static final String DEFAULT_SINGLE_CSV_FILENAME = "some.csv";
    public static final String DEFAULT_SECOND_CSV_FILENAME = "second.csv";
    public static final String DEFAULT_LOCAL_DATA_FOLDERNAME = "local";
    public static final String DEFAULT_LOCAL_DATA_CSV = "my.csv";

    public String configRootLocal = "";


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

    public void writeConfigText(String textName, String contents) throws Exception {
        if (configHomeDirectory.contentEquals("") || textName.contentEquals("")){
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
    }
}
