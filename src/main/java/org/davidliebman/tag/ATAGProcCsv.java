package org.davidliebman.tag;

import java.io.*;
import java.util.ArrayList;
import java.util.Random;

/**
 * Created by dave on 2/20/16.
 */
public class ATAGProcCsv {

    public static final int CSV_POSITION_FILE_LOCATION = 2;

    public static final int NUM_OF_APPROACHES = 4;
    public static final int APPROACH_IS_CLOSE = 70;

    public static final int FACE_X = 6;
    public static final int FACE_Y = 7;
    public static final int FACE_WIDTH = 8;
    public static final int FACE_HEIGHT = 9;

    private ATAG var;
    private ArrayList<CsvLine> listSingle;
    private ArrayList<CsvLine> listLocal;
    private ArrayList<CsvLine> listSecond;

    private ArrayList<String> headingSingle;
    private ArrayList<String> headingLocal;
    private ArrayList<String> headingSecond;

    private Random r;
    private double avg_approach_dist = 0;

    public ATAGProcCsv (ATAG v) {
        var = v;
        r = new Random(System.currentTimeMillis());
    }

    public void loadCsvStart() {
        loadCsvSingle();
        loadCsvLocal();
    }

    public ArrayList<CsvLine> getLocalList() { return listLocal;}

    private void loadCsvSingle() {
        System.out.println( "Hello World! -- " + var.configCsvFileSingle );

        if (!(new File(var.configCsvFileSingle)).exists()) {
            return;
        }

        listSingle = new ArrayList<CsvLine>();
        headingSingle = new ArrayList<String>();
        loadAnyCsv(var.configCsvFileSingle, listSingle,headingSingle, CSV_POSITION_FILE_LOCATION);
    }

    private void loadCsvLocal() {
        System.out.println( "Hello World! -- " + var.configCsvLocal );

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
                System.out.println("out " + str);
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

        System.out.println(num + " " + csv.size() + "  " + name);
        for (int i = 0; i < heading.size(); i ++) {
            System.out.print(heading.get(i) + " - ");
        }
        System.out.println();

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
        System.out.println("average approach dist " + avg_approach_dist);
    }

    private void processLine(CsvLine line) {
        double fx = line.getSpecifications().get(FACE_X);
        double fy = line.getSpecifications().get(FACE_Y);
        double fheight = line.getSpecifications().get(FACE_HEIGHT);
        double fwidth = line.getSpecifications().get(FACE_WIDTH);
        double approachx = 0;
        double approachy = 0;
        double approachdist = 0;
        double labelOutput = 0;

        for (int i = 0; i < NUM_OF_APPROACHES; i ++) {

            CsvLine out = new CsvLine();
            out.setFileLocation(line.getFileLocation());
            for (int j = 0; j < line.getSpecifications().size(); j ++) {
                out.getSpecifications().add(line.getSpecifications().get(j));
            }

            approachx = fx + r.nextInt((int)fwidth * 2) - fwidth;
            approachy = fy + r.nextInt((int)fheight * 2) - fheight;
            approachdist = Math.sqrt(Math.pow(fx - approachx,2)+Math.pow(fy - approachy,2));
            avg_approach_dist += approachdist;
            if (approachdist < APPROACH_IS_CLOSE) {
                labelOutput = 1;
            }
            else {
                labelOutput = 0;
            }

            out.getSpecifications().add(approachx);
            out.getSpecifications().add(approachy);
            out.getSpecifications().add(approachdist);
            out.getSpecifications().add(labelOutput);

            listLocal.add(out);
        }

    }

    public CsvLine getFirstMatchByName() {
        CsvLine line = new CsvLine();
        for (int i = 0; i < listLocal.size(); i ++) {
            if(var.configLastImage.endsWith(listLocal.get(i).getFileLocation())) {
                line = listLocal.get(i);
            }
        }
        return line;
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
