package org.davidliebman.tag;

import java.io.*;
import java.util.ArrayList;
import java.util.Random;

/**
 * Created by dave on 2/20/16.
 */
public class ATAGProcCsv {

    public static final int CSV_POSITION_FILE_LOCATION = 2;

    public static final int NUM_OF_APPROACHES = 2;
    public static final int APPROACH_IS_CLOSE = 70;

    public static final int FACE_X = 6;
    public static final int FACE_Y = 7;
    public static final int FACE_WIDTH = 8;
    public static final int FACE_HEIGHT = 9;
    public static final int FACE_APPROACH_X = 10;
    public static final int FACE_APPROACH_Y = 11;
    public static final int FACE_APPROACH_DIST = 12;
    public static final int FACE_LABEL_1 = 13;
    public static final int FACE_LABEL_2 = 14;
    public static final int FACE_LABEL_3 = 15;
    public static final int FACE_LABEL_4 = 16;
    public static final int FACE_LABEL_NO_OUTPUT = 17;

    public static final double FACE_MOD_AVG = 1.0d;//3.0d/5.0d;

    public static final double FACE_4 = 3000;
    public static final double FACE_3 = 60;//90
    public static final double FACE_2 = 30;//45
    public static final double FACE_1 = 15;//22

    private ATAG var;
    private ArrayList<CsvLine> listSingle;
    private ArrayList<CsvLine> listLocal;
    private ArrayList<CsvLine> listSecond;

    private ArrayList<String> headingSingle;
    private ArrayList<String> headingLocal;
    private ArrayList<String> headingSecond;

    private Random r;
    private double avg_approach_dist = 0;
    private double max_size_vertical = 0;
    private boolean grossImageChoice = true;

    private boolean debugMessages = false;

    public ATAGProcCsv (ATAG v) {
        var = v;
        r = new Random(System.currentTimeMillis());
    }

    public void loadCsvStart() {
        loadCsvSingle();
        loadCsvLocal();
        System.out.println("load done.");
    }

    public ArrayList<CsvLine> getLocalList() { return listLocal;}

    public void clearUnusedList() { listSingle = new ArrayList<CsvLine>();}

    private void loadCsvSingle() {
        if (debugMessages) System.out.println( "Hello World! -- " + var.configCsvFileSingle );

        if (!(new File(var.configCsvFileSingle)).exists()) {
            return;
        }

        listSingle = new ArrayList<CsvLine>();
        headingSingle = new ArrayList<String>();
        loadAnyCsv(var.configCsvFileSingle, listSingle,headingSingle, CSV_POSITION_FILE_LOCATION);
    }

    private void loadCsvLocal() {
        if (debugMessages) System.out.println( "Hello World! -- " + var.configCsvLocal );

        if (!(new File(var.configCsvLocal)).exists()) {
            return;
        }

        listLocal = new ArrayList<CsvLine>();
        headingLocal = new ArrayList<String>();
        loadAnyCsv(var.configCsvLocal, listLocal, headingLocal, CSV_POSITION_FILE_LOCATION);


    }

    public void saveCsvLocal() {
        processFile(listSingle,headingSingle);

        saveAnyCsv(var.configCsvLocal, listLocal,headingLocal,  CSV_POSITION_FILE_LOCATION);
    }


    private void loadAnyCsv(String name, ArrayList<CsvLine> csv, ArrayList<String> heading, int filePosition) {

        long num = 0;
        try {
            BufferedReader in = new BufferedReader(new FileReader(name));
            String str;

            while ((str = in.readLine()) != null) {
                if (debugMessages) System.out.println("out " + str);
                CsvLine line = new CsvLine();
                if (num > 0) {
                    String [] arr = str.split(",");
                    for (int i = 0; i < arr.length; i ++) {
                        if (i == filePosition) {
                            line.setFileLocation(arr[i].trim());
                            line.getSpecifications().add(0.0d);
                        }
                        else {

                            if (!arr[i].trim().contentEquals("")) {
                                line.getSpecifications().add(Double.parseDouble(arr[i]));
                            }
                            else {
                                line.getSpecifications().add(0.0d);
                            }
                        }
                    }
                    csv.add(line);
                }
                else {
                    String [] arr = str.split(",");
                    for (int i = 0; i < arr.length; i ++) {
                        heading.add(arr[i].trim());
                    }
                }
                num ++;
            }
            in.close();
        } catch (IOException e) {
            System.out.println("File Read Error");
        }

        if (debugMessages) {
            System.out.println(num + " " + csv.size() + "  " + name);
            for (int i = 0; i < heading.size(); i++) {
                System.out.print(heading.get(i) + " - ");
            }
            System.out.println();
        }
    }

    private void saveAnyCsv(String name, ArrayList<CsvLine> csv,ArrayList<String> heading, int filePosition) {
        try {
            String out = "";

            FileWriter fileWriter = new FileWriter(name);
            BufferedWriter writer = new BufferedWriter(fileWriter);

            if (heading != null) {

                for (int j = 0; j < heading.size(); j++) {
                    writer.append(heading.get(j));
                    if (j < heading.size() - 1) {
                        writer.append(",");
                    }
                }
                writer.append("\n");
            }

            for (int i = 0; i < csv.size(); i ++) {
                for (int j = 0; j < csv.get(0).getSpecifications().size(); j ++) {
                    out = String.valueOf(csv.get(i).getSpecifications().get(j));
                    if (j == filePosition) {
                        out = csv.get(i).getFileLocation();
                    }
                    writer.append(out);
                    if (j < csv.get(0).getSpecifications().size() - 1) {
                        writer.append(",");
                    }
                }

                writer.append("\n");
            }

            writer.close();
        }
        catch (Exception e) {
            e.printStackTrace();
        }


        System.out.println("done save");
    }

    private void processFile(ArrayList<CsvLine> csv, ArrayList<String> labels) {
        avg_approach_dist = 0;
        listLocal = new ArrayList<CsvLine>();
        for (int i = 0; i < csv.size(); i ++ ) {
            processLine(csv.get(i));
        }

        avg_approach_dist = avg_approach_dist / (listLocal.size());

        if (debugMessages) {
            System.out.println("average approach dist " + avg_approach_dist);
            System.out.println("max face height " + max_size_vertical);
        }
    }

    private void processLine(CsvLine line) {

        double fx = line.getSpecifications().get(FACE_X);
        double fy = line.getSpecifications().get(FACE_Y);
        double fheight = line.getSpecifications().get(FACE_HEIGHT);
        double fwidth = line.getSpecifications().get(FACE_WIDTH);
        double approachx = 0;
        double approachy = 0;
        double approachdist = 0;
        double approachavg = 0;



        if(fheight > max_size_vertical) max_size_vertical = fheight;



        ArrayList<CsvLine> list = new ArrayList<CsvLine>();

        for (int i = 0; i < NUM_OF_APPROACHES; i ++) {

            CsvLine out = new CsvLine();
            out.setFileLocation(line.getFileLocation());
            for (int j = 0; j < line.getSpecifications().size(); j ++) {
                out.getSpecifications().add(line.getSpecifications().get(j));
            }

            if (i != 0) {
                double changex =  r.nextInt((int) fwidth) - fwidth / 2.0d;
                double changey =  r.nextInt((int) fheight) - fheight / 2.0d;

                if (grossImageChoice) {
                    changex = fwidth * (r.nextInt(2) -1 );
                    if(changex == 0) changex = fwidth;
                }

                approachx = fx + changex;
                approachy = fy + changey;
                approachdist = Math.sqrt(Math.pow(fx - approachx, 2) + Math.pow(fy - approachy, 2));
            }
            else {
                approachx = fx;
                approachy = fy;
                approachdist = 0;
            }

            avg_approach_dist += approachdist;
            approachavg += approachdist;



            out.getSpecifications().add(approachx);
            out.getSpecifications().add(approachy);
            out.getSpecifications().add(approachdist);
            //out.getSpecifications().add(labelOutput);

            list.add(out);
        }

        approachavg = approachavg / NUM_OF_APPROACHES;

        for (int i = 0; i< NUM_OF_APPROACHES; i ++) {

            approachdist = list.get(i).getSpecifications().get(FACE_APPROACH_DIST);

            double labelsize1 = 0,labelsize2 = 0, labelsize3 = 0, labelsize4 = 0, labelnooutput = 0;

            ////////////////////////////
            if ((fheight <= FACE_1 && fheight > 0) || (fheight > FACE_1 && ATAG.CNN_LABELS -1 == 1))  {
                labelsize1 = 1;
                labelsize2 = 0;
                labelsize3 = 0;
                labelsize4 = 0;
            }
            else if((fheight <= FACE_2 && fheight > FACE_1) || (fheight > FACE_2 && ATAG.CNN_LABELS -1 == 2)) {
                labelsize1 = 0;
                labelsize2 = 1;
                labelsize3 = 0;
                labelsize4 = 0;
            }
            else if ((fheight <= FACE_3 && fheight > FACE_2) || (fheight > FACE_3 && ATAG.CNN_LABELS -1 == 3)) {
                labelsize1 = 0;
                labelsize2 = 0;
                labelsize3 = 1;
                labelsize4 = 0;
            }
            else if ( fheight > FACE_3){
                labelsize1 = 0;
                labelsize2 = 0;
                labelsize3 = 0;
                labelsize4 = 1;
            }

            if (approachdist < approachavg / FACE_MOD_AVG) {
                labelnooutput = 0;


            }
            else {
                labelnooutput = 1;
                labelsize1 = 0;
                labelsize2 = 0;
                labelsize3 = 0;
                labelsize4 = 0;
            }
            ///////////////////////////

            list.get(i).getSpecifications().add(labelsize1);
            list.get(i).getSpecifications().add(labelsize2);
            list.get(i).getSpecifications().add(labelsize3);
            list.get(i).getSpecifications().add(labelsize4);
            list.get(i).getSpecifications().add(labelnooutput);

            listLocal.add(list.get(i));
        }


    }

    public ArrayList<CsvLine> getFirstMatchByName() {
        ArrayList<CsvLine> list = new ArrayList<CsvLine>();

        CsvLine line = new CsvLine();
        for (int i = 0; i < listLocal.size(); i ++) {
            if(var.configLastImage.toLowerCase().endsWith(listLocal.get(i).getFileLocation().toLowerCase())) {
                line = listLocal.get(i);
                list.add(line);
            }
        }
        return list;
    }

    public void getNextFilename() {
        //CsvLine line = new CsvLine();
        if (listLocal == null) return;

        CsvLine next = new CsvLine();
        boolean found = false;
        boolean atmargin = false;

        for (int i = 0; i < listLocal.size(); i ++) {
            if(var.configLastImage.toLowerCase().endsWith(listLocal.get(i).getFileLocation().toLowerCase())) {
                if (i == listLocal.size() - 1) atmargin = true;
                found = true;
            }
            else {
                if (found == true) {
                    next = listLocal.get(i);
                    found = false;
                }
            }
        }
        if (!atmargin) {
            var.configLastImage = var.getStartFolder() + File.separator + next.getFileLocation();
        }
        if (debugMessages) System.out.println(var.configLastImage + " next");
    }

    public void getPreviousFilename() {

        if (listLocal == null) return;

        CsvLine next = new CsvLine();
        boolean found = false;
        boolean atmargin = false;

        for (int i = listLocal.size() - 1; i >=0; i --) {
            if(var.configLastImage.toLowerCase().endsWith(listLocal.get(i).getFileLocation().toLowerCase())) {
                if (i == 0) atmargin = true;
                found = true;
            }
            else {
                if (found == true) {
                    next = listLocal.get(i);
                    found = false;
                }
            }
        }
        if (!atmargin) {
            var.configLastImage = var.getStartFolder() + File.separator + next.getFileLocation();
        }
        if (debugMessages) System.out.println(var.configLastImage + " prev");
    }

    class CsvLine {
        String fileLocation;
        ArrayList<Double> specifications = new ArrayList<Double>();

        public String getFileLocation() {
            return fileLocation;
        }

        public void setFileLocation(String fileLocation) {
            this.fileLocation = fileLocation;
        }

        public ArrayList<Double> getSpecifications() {
            return specifications;
        }

        public void setSpecifications(ArrayList<Double> specifications) {
            this.specifications = specifications;
        }
    }
}
