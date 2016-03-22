package org.davidliebman.tag;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.ArrayList;
import java.util.Random;

/**
 * Created by dave on 2/20/16.
 */
public class ATAGProcCsv {

    public static final int CSV_POSITION_FILE_LOCATION = 2;

    public static final int NUM_OF_APPROACHES = 2; //2
    public static final int APPROACH_IS_CLOSE = 70;
    public static final int NUM_OF_SKIPPED_CONSECUTIVE_NO_OUTPUT = 1;
    public static final double SIZE_TOO_BIG = 4.0d;//1.25d;

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
    public static final int FACE_LIST_TOTAL = 18;

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
    private int num_positive_output = 0;
    private boolean grossImageChoice = true;
    private int num_of_skipped_no_output = 0;

    private boolean debugMessages = false;
    private boolean doSkipOnHeight = true;

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

    public ArrayList<CsvLine> getLocalList(int split) {
        if (split < Integer.valueOf(var.configSlpitStartNum) || split > Integer.valueOf(var.configSplitStopNum)) split = 1;

        listLocal = new ArrayList<CsvLine>();
        headingLocal = new ArrayList<String>();
        String filename = var.getMyCsvFilenameFromBaseString(var.configSplitCSVBasename, String.valueOf(split));
        loadAnyCsv(filename, listLocal,headingLocal,CSV_POSITION_FILE_LOCATION);
        return listLocal;
    }


    public void clearUnusedList() { listSingle = new ArrayList<CsvLine>();}

    private void loadCsvSingle() {
        loadCsvSingle(var.configSplitCurrentNum);
    }

    private void loadCsvSingle(String num) {

        String filename = var.getSplitFolderFromNumber(num);

        if (debugMessages || true) System.out.println( "Hello World! -- " + filename );

        if (!(new File(filename)).exists()) {
            return;
        }

        listSingle = new ArrayList<CsvLine>();
        headingSingle = new ArrayList<String>();
        loadAnyCsv(filename, listSingle,headingSingle, CSV_POSITION_FILE_LOCATION);
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

    public void saveCsvLocal(int start, int stop, int keep) {
        ArrayList<CsvLine> list = new ArrayList<CsvLine>();
        for (int i = start ; i <= stop; i ++) {
            loadCsvSingle(new Integer(i).toString());
            processFile(listSingle, headingSingle);
            if (i == keep ) {
                list = listLocal;
            }
            String filename = var.getMyCsvFilenameFromBaseString(var.configSplitCSVBasename, new Integer(i).toString());
            saveAnyCsv(filename,listLocal,headingLocal, CSV_POSITION_FILE_LOCATION);
            System.out.println(i + " " + filename);
        }
        listLocal = list;

        //clear saved cursor and split num
        var.configLastCursor = "0";
        var.configLastSplit = "1";
        var.writeConfigText(ATAG.DOTFOLDER_SAVED_CURSOR, var.configLastCursor);
        var.writeConfigText(ATAG.DOTFOLDER_SAVED_SPLIT, var.configLastSplit);
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

    public void saveAnyCsv(String name, ArrayList<CsvLine> csv,ArrayList<String> heading, int filePosition) {
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


        System.out.println("done save csv");
    }

    private void processFile(ArrayList<CsvLine> csv, ArrayList<String> labels) {
        avg_approach_dist = 0;
        num_positive_output = 0;

        listLocal = new ArrayList<CsvLine>();

        listSecond = new ArrayList<CsvLine>();
        for (int i = 0; i < csv.size(); i ++ ) {
            System.out.print("i=" + i + " ");
            processLine(csv.get(i));
        }
        for (int i = 0; i < listSecond.size(); i ++) {
            //listLocal.add(listSecond.get(i));
        }
        int num_held = listSecond.size();
        listSecond = null;

        avg_approach_dist = avg_approach_dist / (listLocal.size());

        if (debugMessages) {
            System.out.println("average approach dist " + avg_approach_dist);
            System.out.println("max face height " + max_size_vertical);
            System.out.println("num positive outputs " + num_positive_output + " / " + listLocal.size());
            System.out.println("num held " + num_held);
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

        double dim_size = fheight;

        double skipOnHeight = 0;

        boolean aproachNeedsRepeat = true;

        if (fheight > max_size_vertical) max_size_vertical = fheight;
        if (fheight > ATAG.CNN_DIM_PIXELS * SIZE_TOO_BIG && doSkipOnHeight) skipOnHeight = 1.0d;


        ArrayList<CsvLine> list = new ArrayList<CsvLine>();


        if (skipOnHeight < 0.5d) { // note: num_of_approaches must be greater than 1!! (2 is good)
            for (int i = 0; i < NUM_OF_APPROACHES; i++) {

                CsvLine out = new CsvLine();
                out.setFileLocation(line.getFileLocation());
                for (int j = 0; j < line.getSpecifications().size(); j++) {
                    out.getSpecifications().add(line.getSpecifications().get(j));
                }

                if (i != 0) {

                    aproachNeedsRepeat = true;

                    int j = 0;
                    while (aproachNeedsRepeat && j< 100) { // 20

                        double changex = r.nextInt((int) dim_size) - dim_size / 2.0d;
                        double changey = r.nextInt((int) dim_size * 2) - dim_size ;

                        if (grossImageChoice) {
                            changex = (dim_size + r.nextInt((int)dim_size * 2)  ) * (r.nextInt(2) - 1);
                            if (changex == 0) changex = dim_size + 2;
                        }

                        approachx = fx + changex;
                        approachy = fy + changey;
                        approachdist = Math.sqrt(Math.pow(fx - approachx, 2) + Math.pow(fy - approachy, 2));

                        //check if approach is good...
                        aproachNeedsRepeat =  getApproachNeedsRepeat( (int)approachx,(int) approachy,(int)dim_size, line.getFileLocation());
                        j++;
                        if (debugMessages || true) System.out.println(j + " a=" + aproachNeedsRepeat);
                    }

                } else {
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


            for (int i = 0; i < NUM_OF_APPROACHES; i++) {

                approachdist = list.get(i).getSpecifications().get(FACE_APPROACH_DIST);

                double labelsize1 = 0, labelsize2 = 0, labelsize3 = 0, labelsize4 = 0, labelnooutput = 0;

                ////////////////////////////
                if ((fheight <= FACE_1 && fheight > 0) || (fheight > FACE_1 && ATAG.CNN_LABELS - 1 == 1)) {
                    labelsize1 = 1;
                    labelsize2 = 0;
                    labelsize3 = 0;
                    labelsize4 = 0;
                } else if ((fheight <= FACE_2 && fheight > FACE_1) || (fheight > FACE_2 && ATAG.CNN_LABELS - 1 == 2)) {
                    labelsize1 = 0;
                    labelsize2 = 1;
                    labelsize3 = 0;
                    labelsize4 = 0;
                } else if ((fheight <= FACE_3 && fheight > FACE_2) || (fheight > FACE_3 && ATAG.CNN_LABELS - 1 == 3)) {
                    labelsize1 = 0;
                    labelsize2 = 0;
                    labelsize3 = 1;
                    labelsize4 = 0;
                } else if (fheight > FACE_3) {
                    labelsize1 = 0;
                    labelsize2 = 0;
                    labelsize3 = 0;
                    labelsize4 = 1;
                }

                if ((approachdist <= approachavg / FACE_MOD_AVG || (ATAG.CNN_LABELS == 1 && approachdist < 1)) && fheight <= ATAG.CNN_DIM_PIXELS * SIZE_TOO_BIG) {
                    labelnooutput = 0;
                    num_positive_output++;

                } else {
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


                if (num_of_skipped_no_output < NUM_OF_SKIPPED_CONSECUTIVE_NO_OUTPUT && labelnooutput > 0.5d) {
                    listLocal.add(list.get(i));
                    num_of_skipped_no_output++;//= 0;
                } else if (labelnooutput < 0.5d) {
                    if (num_of_skipped_no_output == NUM_OF_SKIPPED_CONSECUTIVE_NO_OUTPUT) {
                        listLocal.add(list.get(i));
                        num_of_skipped_no_output = 0;
                    } else {
                        listSecond.add(list.get(i));
                    }
                } else if (num_of_skipped_no_output >= NUM_OF_SKIPPED_CONSECUTIVE_NO_OUTPUT && listSecond.size() > 0) {
                    listLocal.add(listSecond.get(0));
                    listSecond.remove(0);
                    num_of_skipped_no_output = 0;
                }
            }

        }
    }

    private boolean getApproachNeedsRepeat( int x, int y, String name) {
        return  getApproachNeedsRepeat(x,y,  ATAG.CNN_DIM_PIXELS, name);
    }

    private boolean getApproachNeedsRepeat( int x, int y,int dim_side, String name) {

        boolean test = false;

        ArrayList<CsvLine> listCheck = getFirstMatchByName( name,listSingle );

        BoundingBox a = new BoundingBox(x,y, dim_side, dim_side);

        int i = 0;
        for (i = 0; i < listCheck.size(); i ++) {
            double xx =  listCheck.get(i).getSpecifications().get(FACE_X);
            double yy =  listCheck.get(i).getSpecifications().get(FACE_Y);

            double width = listCheck.get(i).getSpecifications().get(FACE_WIDTH);
            double height = listCheck.get(i).getSpecifications().get(FACE_HEIGHT);

            double changex = (dim_side - width ) / 2.0f;
            double changey = (dim_side - height) / 2.0f;

            xx = xx - changex;
            yy = yy - changey;

            if (((int) xx) != x && ((int) yy) != y) {
                BoundingBox b = new BoundingBox((int) xx, (int) yy, (int) height, (int) height);
                boolean out = collisionSimple(a, b);

                if (debugMessages) System.out.println(name + " " + xx + " " + yy + " " + out);
                if (out) {
                    test = true;
                    i = listCheck.size();
                }
            }
        }

        return test;
    }

    public  ArrayList<CsvLine> getFirstMatchByName() {
        return getFirstMatchByName(var.configLastImage, listLocal);
    }

    public ArrayList<CsvLine> getFirstMatchByName( String name, ArrayList<CsvLine> chosenList) {
        ArrayList<CsvLine> list = new ArrayList<CsvLine>();

        CsvLine line = new CsvLine();
        for (int i = 0; i < chosenList.size(); i ++) {
            if(name.toLowerCase().endsWith(chosenList.get(i).getFileLocation().toLowerCase())) {
                line = chosenList.get(i);
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

    public ArrayList<CsvLine> getPredictListFromImage(String filename) {
        ArrayList<CsvLine> listPredict = new ArrayList<CsvLine>();
        BufferedImage image = null;
        try {
            image = ImageIO.read(new File(filename));

        }
        catch (Exception e) {e.printStackTrace();}

        int top = 0;
        int bot = image.getHeight();
        int left = 0;
        int right = image.getWidth();

        int spanHorizontal = ((right - left) - ATAG.CNN_DIM_PIXELS) / 7;//ATAG.CNN_DIM_SIDE;
        int spanVertical = ((bot - top) - ATAG.CNN_DIM_PIXELS) / 7;//ATAG.CNN_DIM_SIDE;

        for (int x = 0; x < 8; x ++) {
            for (int y = 0; y < 8; y ++) {
                ///////////////////////
                CsvLine row = new CsvLine();
                for (int i = 0; i < FACE_LIST_TOTAL; i ++) {
                    row.getSpecifications().add(0.0d);
                }
                row.setFileLocation(filename);

                row.getSpecifications().remove(FACE_APPROACH_X);
                row.getSpecifications().add(FACE_APPROACH_X,(double) x * spanHorizontal);

                row.getSpecifications().remove(FACE_APPROACH_Y);
                row.getSpecifications().add(FACE_APPROACH_Y, (double) y * spanVertical);

                row.getSpecifications().remove(FACE_HEIGHT);
                row.getSpecifications().add(FACE_HEIGHT, (double) ATAG.CNN_DIM_PIXELS);

                row.getSpecifications().remove(FACE_WIDTH);
                row.getSpecifications().add(FACE_WIDTH, (double) ATAG.CNN_DIM_PIXELS);
                ///////////////////////

                listPredict.add(row);
            }
        }

        saveAnyCsv(var.configLocalRoot + File.separator + "predict.csv",listPredict,null, CSV_POSITION_FILE_LOCATION);

        return  listPredict;
    }


    private boolean collisionSimple(BoundingBox boxA, BoundingBox boxB) {
        int x[] = {0,0,0,0};
        int y[]= {0,0,0,0};
        int i, j;
        boolean test = false;
        boolean outsideTest, insideTest;

        x[0] = boxA.left;
        y[0] = boxA.top;

        x[1] = boxA.right;
        y[1] = boxA.top;

        x[2] = boxA.left;
        y[2] = boxA.bottom;

        x[3] = boxA.right;
        y[3] = boxA.bottom;
        for (i = 0; i < 4; i ++) {
            // is one point inside the other bounding box??
            if (x[i] <= boxB.right && x[i] >= boxB.left && y[i] <= boxB.bottom && y[i] >= boxB.top ) {
                // are all other points outside the other bounding box??
                outsideTest = false;

                for (j = 0; j < 4 ; j ++) {
                    if (j != i ) {
                        if (!(x[j] <= boxB.right && x[j] >= boxB.left && y[j] <= boxB.bottom && y[j] >= boxB.top) ) {
                            outsideTest = true;

                        }
                    }
                }
                if(outsideTest) {
                    test = true;

                }
                // is a second point inside the bounding box??
                insideTest = false;
                for (j = 0; j < 4 ; j ++) {
                    if (j != i ) {
                        if ((x[j] <= boxB.right && x[j] >= boxB.left && y[j] <= boxB.bottom && y[j] >= boxB.top) ) {
                            insideTest = true;

                        }
                    }
                }
                if(insideTest) {
                    test = true;

                }

                /////////////////////////
            }
        }
        if (!test) return collisionHelper(boxA, boxB);
        else return true;
    }

    /**
     *	Used for overall collision testing.
     */

    private boolean collisionHelper(BoundingBox boxA, BoundingBox boxB) {
        int x[] = {0,0,0,0};
        int y[] = {0,0,0,0};
        int i,j;
        boolean test = false;
        boolean outsideTest, insideTest;

        x[0] = boxB.left;
        y[0] = boxB.top;

        x[1] = boxB.right;
        y[1] = boxB.top;

        x[2] = boxB.left;
        y[2] = boxB.bottom;

        x[3] = boxB.right;
        y[3] = boxB.bottom;
        for (i = 0; i < 4; i ++) {
            // is one point inside the other bounding box??
            if (x[i] <= boxA.right && x[i] >= boxA.left && y[i] <= boxA.bottom && y[i] >= boxA.top ) {


                // are all other points outside the other bounding box??
                outsideTest = false;

                for (j = 0; j < 4 ; j ++) {
                    if (j != i ) {
                        if (!(x[j] <= boxA.right && x[j] >= boxA.left && y[j] <= boxA.bottom && y[j] >= boxA.top) ) {
                            outsideTest = true;

                        }
                    }
                }
                if(outsideTest) {
                    test = true;

                }
                // is a second point inside the bounding box??
                insideTest = false;
                for (j = 0; j < 4 ; j ++) {
                    if (j != i ) {
                        if ((x[j] <= boxA.right && x[j] >= boxA.left && y[j] <= boxA.bottom && y[j] >= boxA.top) ) {
                            insideTest = true;

                        }
                    }
                }
                if(insideTest) {
                    test = true;

                }


                //////////////////////////
            }
        }

        return test;
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

    class BoundingBox {
        public int left,right,top,bottom;

        public BoundingBox ( int x, int y, int width, int height) {
            left = x;
            right = x + width;
            top = y;
            bottom = y + height;
        }
    }
}
