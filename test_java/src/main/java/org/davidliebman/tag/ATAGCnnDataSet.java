package org.davidliebman.tag;


        import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.dataset.api.DataSetPreProcessor;
import org.nd4j.linalg.dataset.api.iterator.DataSetIterator;
import org.nd4j.linalg.factory.Nd4j;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

//import java.nio.file.attribute.BasicFileAttributes;

/**
 * Created by dave on 1/21/16.
 */
public class ATAGCnnDataSet  implements DataSetIterator {


    int searchType = 0;
    long seed = 0;
    int cursor = 0;
    int cursorSize = 0;

    float percentForTesting = 0.20f;


    double [][] featureMatrix;
    double [][] labels;
    private ArrayList<ATAGProcCsv.CsvLine> listLocal;
    private ATAG var;

    private boolean debugMessages = false;
    private static boolean debugByteOrder = false;
    private boolean debugDontCenter = true; // only if we are restricting the size of face to ATAG.CNN_DIM_PIXELS !!
    private static boolean debugNoThreshold = true;
    private boolean debugDoNotSplit = false;
    private static boolean orderAsAlternate = true;
    private static boolean debugOneChannelForDisplay = true;
    private boolean doMirrorTrain = ATAG.CNN_MIRROR_TRAIN;

    boolean trainWithThisSet = true;

    private int globalOutputCount = 0;

    public ATAGCnnDataSet(ArrayList<ATAGProcCsv.CsvLine >  list , ATAG v, int type, boolean train, float split, long seed, int savedCursor, boolean doNotSplit) throws Exception {
        super();
        searchType = type;
        this.seed = seed;
        trainWithThisSet = train;
        percentForTesting = split;

        debugDoNotSplit = doNotSplit;
        listLocal = list;
        var = v;

        globalOutputCount = 0;

        cursor = savedCursor;
        if (cursor > cursorSize) cursor = 0;
        //randomizeList() ;
        splitList();
    }

    public INDArray loadImageBMP (File file, double x, double y ) throws Exception {
        return loadImageBMP(file, x, y, ATAG.CNN_DIM_PIXELS);
    }



    public  static INDArray loadImageBMP ( File file, double x_start, double y_start, double dim_side) throws Exception {

        double[] array1D = new double[ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE * ATAG.CNN_CHANNELS];

        if (!file.exists()) return Nd4j.create(array1D);

        int transx = (int)(x_start) , transy = (int)(y_start);
        int threshold = 128;//128
        float colordiv = 255.0f; // produce a num between 0 and 2... change to 255.0f for num between 0 and 1
        float mag = (float) dim_side /(float) ATAG.CNN_DIM_SIDE;
        //mag = (float)ATAG.CNN_DIM_SIDE /(float) dim_side;// /(float) ATAG.CNN_DIM_SIDE;

        if (false) System.out.println("mag " + mag + " dim-side "+ dim_side);

        BufferedImage image = ImageIO.read(file);

        double[][][] array2D = new double[ATAG.CNN_DIM_SIDE][ATAG.CNN_DIM_SIDE ][ATAG.CNN_CHANNELS];

        for (int yPixel = 0; yPixel < ATAG.CNN_DIM_SIDE; yPixel++)
        {
            for (int xPixel = 0; xPixel < ATAG.CNN_DIM_SIDE; xPixel++)
            {
                if (xPixel * mag + transx >=0 && xPixel* mag + transx< image.getWidth() && yPixel * mag +transy >=0 && yPixel * mag + transy < image.getHeight()) {

                    int color = image.getRGB((int)(xPixel *mag +transx ), (int)(yPixel * mag + transy));

                    int arrayPos1D = yPixel * ATAG.CNN_DIM_SIDE  * ATAG.CNN_CHANNELS + xPixel * ATAG.CNN_CHANNELS ;


                    int alpha = (color >> 24) & 0xff;
                    int red = (color >> 16) & 0xff;
                    int green = (color >> 8) & 0xff;
                    int blue = (color) & 0xff;

                    if ((red) < threshold) { // ...dark enough??
                        array2D[yPixel][xPixel][0] = 1;
                    } else {
                        array2D[yPixel][xPixel][0] = 0; // ?
                    }
                    if ((green) < threshold) { // ...dark enough??
                        array2D[yPixel][xPixel][1] = 1;
                    } else {
                        array2D[yPixel][xPixel][1] = 0; // ?
                    }

                    if ((blue) < threshold) { // ...dark enough??
                        array2D[yPixel][xPixel][2] = 1;
                    } else {
                        array2D[yPixel][xPixel][2] = 0; // ?
                    }

                    if (!debugNoThreshold) {
                        if (!orderAsAlternate) {
                            array1D[arrayPos1D + 0] = array2D[yPixel][xPixel][0];

                            array1D[arrayPos1D + 1] = array2D[yPixel][xPixel][1];

                            array1D[arrayPos1D + 2] = array2D[yPixel][xPixel][2];
                        }
                        else {
                            array1D[ 0 * ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE + yPixel * ATAG.CNN_DIM_SIDE + xPixel] = array2D[yPixel][xPixel][0];//array2D[yPixel][xPixel][0];

                            array1D[ 1 * ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE + yPixel * ATAG.CNN_DIM_SIDE + xPixel] = array2D[yPixel][xPixel][1];//array2D[yPixel][xPixel][1];

                            array1D[ 2 * ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE + yPixel * ATAG.CNN_DIM_SIDE + xPixel] = array2D[yPixel][xPixel][2];//array2D[yPixel][xPixel][2];
                        }
                    }
                    else {
                        if (!orderAsAlternate) {
                            array1D[arrayPos1D + 0] = red / colordiv;// here R,G, and B are side by side.

                            array1D[arrayPos1D + 1] = green / colordiv;

                            array1D[arrayPos1D + 2] = blue / colordiv;
                        }
                        else {
                            array1D[ 0 * ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE + yPixel * ATAG.CNN_DIM_SIDE + xPixel] = red / colordiv;//

                            array1D[ 1 * ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE + yPixel * ATAG.CNN_DIM_SIDE + xPixel] = green / colordiv;//

                            array1D[ 2 * ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE + yPixel * ATAG.CNN_DIM_SIDE + xPixel] = blue / colordiv;//
                        }
                    }

                    if (debugByteOrder) {
                        for (int x = 0; x < ATAG.CNN_CHANNELS; x ++) {
                            array1D[arrayPos1D + x] = x;
                        }
                    }
                }
            }
        }
        return Nd4j.create(array1D);//
    }


    private INDArray mirrorTrain(INDArray in) {
        in.linearView();

        double [] zarray = new double[ATAG.CNN_DIM_SIDE*ATAG.CNN_DIM_SIDE*ATAG.CNN_CHANNELS];


        for(int c = 0; c < ATAG.CNN_CHANNELS; c ++) {
            for (int i = 0; i < ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE; i ++) {
                int frame = c * ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE;
                zarray[frame + i] = in.getDouble(frame + (ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE) - i - 1 );
            }
        }

        //System.out.println("mirror");
        INDArray out = Nd4j.create(zarray);
        return out;
    }


    public static void showSquare(INDArray in) {
        INDArray show = in.linearView();
        boolean noOutput = true;
        int channelsForDisplay = 0;
        if (debugOneChannelForDisplay) {
            channelsForDisplay = 1;
        }
        else {
            channelsForDisplay = ATAG.CNN_CHANNELS;
        }
        for (int i = 0; i < ATAG.CNN_DIM_SIDE ; i ++) {
            for (int j = 0; j < ATAG.CNN_DIM_SIDE ; j ++) {

                for (int k = 0; k < channelsForDisplay; k ++ ) {
                    if (show.getDouble(i * ATAG.CNN_DIM_SIDE * channelsForDisplay + j * channelsForDisplay + k) > 0.5d) {
                        if (!debugByteOrder) {
                            System.out.print("#");
                        }
                        else {
                            //System.out.print((int)(show.getDouble( i * ATAG.CNN_DIM_SIDE * ATAG.CNN_CHANNELS+ j * ATAG.CNN_CHANNELS + k)));
                        }
                        noOutput = false;
                    } else {
                        System.out.print(" ");
                    }
                }
            }
            System.out.println("--");
        }
        //System.out.println("------------ rows " + show.rows() + " -- cols " + show.columns() + " ---------");
        int testout = (ATAG.CNN_DIM_SIDE - 1 ) * ATAG.CNN_DIM_SIDE * ATAG.CNN_CHANNELS + (ATAG.CNN_DIM_SIDE - 1) * ATAG.CNN_CHANNELS + ATAG.CNN_CHANNELS - 1;
        if (!noOutput) System.out.println("dimensions here. " + in.columns() + "  " + testout);
    }


    public void splitList() {
        ArrayList<ATAGProcCsv.CsvLine>  newList = new ArrayList<ATAGProcCsv.CsvLine>();

        if (!debugDoNotSplit) {
            if (trainWithThisSet) {
                newList.addAll(listLocal.subList(0, (int) (listLocal.size() * (1.0 - percentForTesting))));
            } else {
                newList.addAll(listLocal.subList(1 + (int) (listLocal.size() * (1.0 - percentForTesting)), listLocal.size()));
            }
            listLocal = newList;

        }
        cursorSize = (int)listLocal.size()/ATAG.CNN_BATCH_SIZE;

        if (debugMessages ) System.out.println(listLocal.size() + " size after split");

    }

    public void limitList(int num ) {
        if (cursorSize > num) cursorSize = num;
    }

    public void fillArrays(int cursor) throws Exception {
        globalOutputCount = 0;
        double[] array1D = new double[ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE * ATAG.CNN_CHANNELS];

        featureMatrix = new double[ ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE * ATAG.CNN_CHANNELS][ ATAG.CNN_BATCH_SIZE];
        labels = new double[ATAG.CNN_LABELS][ATAG.CNN_BATCH_SIZE];

        for(int i = 0; i < ATAG.CNN_BATCH_SIZE; i ++) {
            //System.out.println(list.get(i));
            String location = listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getFileLocation();
            String filename = var.configRootDatabase + File.separator + listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getFileLocation();

            if (location.startsWith("/")) filename = location;

            double facew = listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_WIDTH);
            double faceh = listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_HEIGHT);

            double xcoord = listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_APPROACH_X);
            double ycoord = listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_APPROACH_Y);

            if (faceh > facew) {
                // ...center cnn over image of face ??
                xcoord = xcoord - (faceh - facew) / 2;
                //ycoord = ycoord - (ATAG.CNN_DIM_PIXELS - faceh) / 2;
            }

            double [] label = new double[4]; // max possible labels... probably will use less!
            label[0] =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_1);
            label[1] =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_2);
            label[2] =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_3);
            label[3] =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_4);
            double labelnooutput =listLocal.get(i + cursor * ATAG.CNN_BATCH_SIZE).getSpecifications().get(ATAGProcCsv.FACE_LABEL_NO_OUTPUT);



            if(debugMessages) System.out.println(filename + " name  x=" + xcoord + "  y=" + ycoord + " height=" + faceh + " i=" + ( i + cursor * ATAG.CNN_BATCH_SIZE));

            File file = new File(filename);

            INDArray out = Nd4j.create(array1D);
            if (file.exists() && !file.isDirectory()) {
                //System.out.println(filename);
                //INDArray
                out = loadImageBMP(file, xcoord, ycoord, faceh);
                if (labelnooutput > ATAGPanel.SURENESS && doMirrorTrain) {
                    out = mirrorTrain(out);
                }
            }
            out = out.linearView();
            //System.out.println(arr.toString());

            //INDArray out = convertSIDExSIDE(arr, xcoord, ycoord);
            //out.linearView();

            if (debugMessages) showSquare(out);

            for (int j = 0; j < (ATAG.CNN_DIM_SIDE * ATAG.CNN_DIM_SIDE * ATAG.CNN_CHANNELS); j ++) {
                featureMatrix[j][i] = out.getDouble(j);
                //System.out.print("."+ i + "." + j);
            }

            for(int j = 0; j < ATAG.CNN_LABELS -1 ; j ++) {
                labels [j][i] = label[j];
                if (debugMessages) System.out.print(" label=" + label[j]);
            }

            if (debugMessages) System.out.println(" no-out="+ labelnooutput);

            labels[ATAG.CNN_LABELS -1 ][i] = labelnooutput;


            if(labelnooutput > 0.5d) {
                //System.out.println("no-out");
            }
            else {
                //System.out.println("here detection");
                globalOutputCount ++;
            }

        }

        //if (globalOutputCount != ATAG.CNN_BATCH_SIZE / ATAG.CNN_LABELS && globalOutputCount != ATAG.CNN_BATCH_SIZE)  Thread.currentThread().interrupt();//System.exit(0);

        if(debugMessages || true) System.out.println("batch totals " + globalOutputCount +"/" + (ATAG.CNN_BATCH_SIZE) + " size="+ listLocal.size() + " cursor=" + cursor + "/"+ cursorSize);

    }

    public void setDoMirrorTrain ( boolean m ) {doMirrorTrain = m;}


    @Override
    public String toString() {
        return super.toString();
    }


    public void setCursor (int c) {
        cursor = c;
        cursorSize = listLocal.size() / ATAG.CNN_BATCH_SIZE;
        System.out.println("c=" + cursor + " c-size=" + cursorSize);
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

    public int cursorSize() {return cursorSize;}

    public void setPreProcessor(DataSetPreProcessor dataSetPreProcessor) {

    }

    public List<String> getLabels() {
        return null;
    }

    public int length() { return listLocal.size();}

    public boolean hasNext() {
        boolean hasnext = false;
        if (cursor < cursorSize ) hasnext = true;
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
