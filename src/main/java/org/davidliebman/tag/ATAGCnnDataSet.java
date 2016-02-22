package org.davidliebman.tag;


        import org.nd4j.linalg.api.ndarray.INDArray;
        import org.nd4j.linalg.dataset.DataSet;
        import org.nd4j.linalg.dataset.SplitTestAndTrain;
        import org.nd4j.linalg.dataset.api.DataSetPreProcessor;
        import org.nd4j.linalg.dataset.api.iterator.DataSetIterator;
        import org.nd4j.linalg.factory.Nd4j;

        import javax.imageio.ImageIO;
        import java.awt.*;
        import java.awt.image.BufferedImage;
        import java.io.File;
        import java.io.IOException;
        import java.nio.file.*;
        import java.nio.file.attribute.BasicFileAttributes;
        import java.util.*;
        import java.util.List;

/**
 * Created by dave on 1/21/16.
 */
public class ATAGCnnDataSet  implements DataSetIterator {



    //ArrayList<String> list = new ArrayList<String>();

    int searchType = 0;
    long seed = 0;
    int cursor = 0;
    int cursorSize = 0;

    float percentForTesting = 0.20f;

    boolean trainWithThisSet = true;

    double [][] featureMatrix;
    double [][] labels;
    private ArrayList<ATAGProcCsv.CsvLine> listLocal;
    private ATAG var;



    public ATAGCnnDataSet(ArrayList<ATAGProcCsv.CsvLine >  list , ATAG v, int type, boolean train, float split, long seed) throws Exception {
        super();
        searchType = type;
        this.seed = seed;
        trainWithThisSet = train;
        percentForTesting = split;

        listLocal = list;
        var = v;


        //randomizeList() ;
        splitList();
    }



    /*
    public static INDArray convert28x28(INDArray in) {
        return convert28x28(in, 2.0d);
    }


    public static INDArray convert28x28 (INDArray in , double modifier) {
        double magx = modifier * 28/128.0d;
        double magy = modifier * 28/128.0d;
        int transx = -(int)(28/modifier), transy = -(int)(28/ modifier);
        double outArray[][] = new double[28][28];

        for (int i  = 0; i < Math.sqrt(in.length()); i ++) {
            for (int j = 0; j < Math.sqrt(in.length()); j ++) {
                if (in.getRow(i).getDouble(j) > 0.5d) {
                    if (i*magx + transx >=0 && i*magx + transx< 28 && j * magy+transy >=0 && j * magy+ transy < 28) {
                        outArray[(int)(j*magy)+transy][(int)(i*magx) + transx] = 1.0d;
                    }
                }
            }
        }
        INDArray out = Nd4j.create(outArray);
        //out.transpose();
        //System.out.println(out.toString());
        return out.linearView();
    }
    */

    public static INDArray convertSIDExSIDE(INDArray in) { return convertSIDExSIDE(in, 0, 0) ;}

    public static INDArray convertSIDExSIDE(INDArray in, double x_start, double y_start ) {
        int transx = (int)(x_start), transy = (int)(y_start);

        if (transx < 0) transx = 0;
        if (transy < 0) transy = 0;

        double outArray[][] = new double[ATAG.CNN_DIM_SIDE][ATAG.CNN_DIM_SIDE];
        for (int i  = 0; i < ATAG.CNN_DIM_SIDE; i ++) {
            for (int j = 0; j < ATAG.CNN_DIM_SIDE; j ++) {

                if (i + transx >=0 && i + transx< in.rows() && j +transy >=0 && j + transy < in.columns()) {
                    if (in.getRow(i+transx).getDouble(j+ transy) > 0.5d) {

                        outArray[(j)][(i)] = 1.0d;
                    }

                }

            }
        }

        INDArray out = Nd4j.create(outArray);
        return out.linearView();
    }

    public  INDArray loadImageBMP ( File file) throws Exception {
        //System.out.println(file.toString());
        BufferedImage image = ImageIO.read(file);

        double[][] array2D = new double[image.getWidth()][image.getHeight()];

        for (int xPixel = 0; xPixel < image.getWidth(); xPixel++)
        {
            for (int yPixel = 0; yPixel < image.getHeight(); yPixel++)
            {
                int color = image.getRGB(xPixel, yPixel);
                if (color== Color.BLACK.getRGB()) {
                    array2D[xPixel][yPixel] = 1;
                } else {
                    array2D[xPixel][yPixel] = 0; // ?
                }
            }
        }
        return Nd4j.create(array2D);
    }

    /*
    public void randomizeList() {

        Random r = new Random(seed);
        ArrayList<String> newList = new ArrayList<String>();

        OneHotOutput output = new OneHotOutput(searchType);
        int startConst = 6, stopConst = 4;

        for (int i = 0; i < list.size(); i ++) {
            String num = list.get(i).substring(list.get(i).length() - startConst, list.get(i).length()-stopConst);
            //System.out.println(num);
            if (output.getMemberNumber(num) != -1) {
                newList.add(list.get(i));
            }
        }

        list = newList;
        newList = new ArrayList<String>();
        int size = list.size();
        for (int i = 0; i < size; i ++) {

            //System.out.println(list.get(i));
            int choose = r.nextInt(list.size());
            newList.add(list.get(choose));
            list.remove(choose);
        }

        list = newList;


    }
    */
    public void showSquare(INDArray in) {
        INDArray show = in.linearView();
        for (int i = 0; i < ATAG.CNN_DIM_SIDE; i ++) {
            for (int j = 0; j < ATAG.CNN_DIM_SIDE; j ++) {
                if (show.getDouble(i * ATAG.CNN_DIM_SIDE + j) > 0.5d) {
                    System.out.print("#");
                }
                else {
                    System.out.print(" ");
                }
            }
            System.out.println("--");
        }
        System.out.println("------------ rows " + show.rows() + " -- cols " + show.columns() + " -------");
    }


    public void splitList() {
        ArrayList<ATAGProcCsv.CsvLine>  newList = new ArrayList<ATAGProcCsv.CsvLine>();

        if (trainWithThisSet) {
            newList.addAll(listLocal.subList(0,(int)(listLocal.size() * (1.0 - percentForTesting))));
        }
        else {
            newList.addAll(listLocal.subList(1 + (int)(listLocal.size() * (1.0 - percentForTesting)),listLocal.size()));
        }

        listLocal = newList;
        cursorSize = (int)listLocal.size()/ATAG.CNN_BATCH_SIZE;

        System.out.println(listLocal.size() + " size after split");

    }

    public void limitList(int num ) {
        if (cursorSize > num) cursorSize = num;
    }

    public void fillArrays(int cursor) throws Exception {


        featureMatrix = new double[ ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE][ ATAG.CNN_BATCH_SIZE];
        labels = new double[ATAG.CNN_LABELS][ATAG.CNN_BATCH_SIZE];

        for(int i = 0; i < ATAG.CNN_BATCH_SIZE; i ++) {
            //System.out.println(list.get(i));
            String filename = var.configRootDatabase + File.separator + listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getFileLocation();
            double xcoord = listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_APPROACH_X);
            double ycoord = listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_APPROACH_Y);


            System.out.println(filename + " name " + xcoord + "  " + ycoord + " " + ( i + cursor * ATAG.CNN_BATCH_SIZE));

            INDArray arr = loadImageBMP(new File(filename));
            arr.linearView();
            //System.out.println(arr.toString());

            INDArray out = convertSIDExSIDE(arr, xcoord, ycoord);
            out.linearView();

            showSquare(out);

            for (int j = 0; j < (ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE); j ++) {
                featureMatrix[j][i] = out.getDouble(j);
                //System.out.print("."+ i + "." + j);
            }
            double [] label = new double[4]; // max possible labels... probably will use less!
            label[0] =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_1);
            label[1] =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_2);
            label[2] =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_3);
            label[3] =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_4);
            double labelnooutput =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_NO_OUTPUT);


            for(int j = 0; j < ATAG.CNN_LABELS -1 ; j ++) {
                labels [j][i] = label[j];
                System.out.print(" label ");
            }

            labels[ATAG.CNN_LABELS -1 ][i] = labelnooutput;
        }


    }

    /*
    public int getCharFromFilename(String in) {
        int startConst = 6, stopConst = 4;

        String num = in.substring(in.length() - startConst, in.length()-stopConst);
        int out = Integer.parseInt(num,16);
        return out;
    }
    */

    @Override
    public String toString() {
        return super.toString();
    }



    public DataSet next(int i) {
        cursor = i;
        return next();
    }

    public int totalExamples() {
        return listLocal.size();
    }

    public int inputColumns() {
        return ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE;// 28*28;
    }

    public int totalOutcomes() {
        //OneHotOutput output = new OneHotOutput(searchType);
        //return output.length();
        return ATAG.CNN_LABELS;
    }

    public void reset() {
        cursor = 0;
    }

    public int batch() {
        return 0;
    }

    public int cursor() {
        return cursor;
    }

    public int numExamples() {
        return listLocal.size();
    }

    public void setPreProcessor(DataSetPreProcessor dataSetPreProcessor) {

    }

    public List<String> getLabels() {
        return null;
    }

    public int length() { return listLocal.size();}

    public boolean hasNext() {
        boolean hasnext = false;
        if (cursor <= cursorSize ) hasnext = true;
        return hasnext;
    }

    public DataSet next() {
        DataSet temp = new DataSet();

        try {
            //create dataset with cursor here.
            fillArrays(cursor);
            temp.setFeatures(Nd4j.create(featureMatrix).transpose());
            temp.setLabels(Nd4j.create(labels).transpose());
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        cursor ++;
        return temp;
    }

    public void remove() {

    }
}
