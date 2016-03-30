package org.davidliebman.tag;

import org.deeplearning4j.eval.Evaluation;
import org.deeplearning4j.nn.api.OptimizationAlgorithm;
import org.deeplearning4j.nn.conf.MultiLayerConfiguration;
import org.deeplearning4j.nn.conf.NeuralNetConfiguration;
import org.deeplearning4j.nn.conf.Updater;
import org.deeplearning4j.nn.conf.layers.ConvolutionLayer;
import org.deeplearning4j.nn.conf.layers.DenseLayer;
import org.deeplearning4j.nn.conf.layers.OutputLayer;
import org.deeplearning4j.nn.conf.layers.SubsamplingLayer;
import org.deeplearning4j.nn.conf.layers.setup.ConvolutionLayerSetup;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.deeplearning4j.nn.weights.WeightInit;
import org.deeplearning4j.optimize.listeners.ScoreIterationListener;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.dataset.api.iterator.DataSetIterator;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.lossfunctions.LossFunctions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;


public class ATAGCnn extends  Thread {
    private static final Logger log = LoggerFactory.getLogger(ATAGCnn.class);

    private boolean exitEarly = false;
    MultiLayerNetwork model;
    String name = ATAG.DEFAULT_BIASES_NAME;
    String homeDir = "";
    String fileName = "";
    private ATAG var;
    private ATAGProcCsv proc;
    private ATAGCnnDataSet predictData;
    private INDArray output;

    private boolean doFit = false;
    private boolean doTest = true;
    private boolean doPredict = false;
    private boolean doLoadSaveModel = true;
    private boolean doSaveCursor = true;
    private boolean doLoadData = true;
    private boolean doGenerateNewModel = true;
    private boolean doScheduledLearningChange = false;
    private boolean doUseSerializerLoad = false;
    private boolean modelSaved = false;

    private double learningRate = 0.01;

    private int cursor = 0;
    private int split = 0;

    public   ATAGCnn (ATAG var, ATAGProcCsv proc) throws Exception {
        this.var = var;
        this.proc = proc;
        homeDir = var.configLocalRoot;
    }

    public void run() {
        //System.setProperty("java.library.path","/usr/local/cuda/lib64");

        String pathAddition = ":/usr/local/cuda/lib64:/usr/local/cuda/bin";
        String oldPath = System.getProperty("java.library.path");

        if (! oldPath.endsWith(pathAddition)) {
            String newPath = oldPath + pathAddition;
            System.setProperty("java.library.path", newPath);
        }
        System.out.println(System.getProperty("java.library.path"));

        Nd4j.ENFORCE_NUMERICAL_STABILITY =  true;

        homeDir = var.configLocalRoot;

        int nChannels = ATAG.CNN_CHANNELS;
        int outputNum = ATAG.CNN_LABELS;
        int batchSize = ATAG.CNN_BATCH_SIZE;
        int nEpochs = 1;// 10
        int iterations = 1;
        int seed = 123;
        float testSplit = 0.025f;

        split = Integer.valueOf(var.configLastSplit);

        int inputDim = ATAG.CNN_DIM_SIDE;//60 or 56

        setFileName(this.name);

        DataSetIterator mnistTrain = null;
        DataSetIterator mnistTest = null;

        if(doLoadData) {
            log.info("Load csv data....");


            try {
                mnistTrain = new ATAGCnnDataSet(proc.getLocalList(split), var, 0, true, 1.0f - testSplit, seed, 0, true);
                mnistTest = new ATAGCnnDataSet(proc.getLocalList(1), var, 0, false, testSplit, seed, 0, false);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        ////
        if (doGenerateNewModel) {

            if (doScheduledLearningChange) scheduleLearningRate();

            System.out.println("Build model....");

            MultiLayerConfiguration.Builder builder = new NeuralNetConfiguration.Builder()
                    .seed(seed)
                    .iterations(iterations)
                    .regularization(true)
                    .l2(0.0005)
                    .learningRate(learningRate) // 0.01 or 0.0005
                    .weightInit(WeightInit.XAVIER)
                    .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                    //.optimizationAlgo(OptimizationAlgorithm.LBFGS)

                    .updater(Updater.ADAGRAD)
                    .momentum(0.9)
                    .list(4)
                    .layer(0, new ConvolutionLayer.Builder(5, 5)
                            .nIn(nChannels)
                            .stride(1, 1)
                            .nOut(80) //80
                            .dropOut(0.5)
                            .activation("relu")
                            .build())

                    .layer(1, new SubsamplingLayer.Builder(SubsamplingLayer.PoolingType.MAX)
                            .kernelSize(2, 2)
                            .stride(2, 2)
                            .build())


                    .layer(2, new DenseLayer.Builder()
                            .activation("relu")
                            .nOut(600) // 600
                            .build())

                    /*
                    .layer(3, new RBM.Builder(RBM.HiddenUnit.RECTIFIED, RBM.VisibleUnit.GAUSSIAN)//, RBM.VisibleUnit.GAUSSIAN)
                            .k(1)
                            .lossFunction(LossFunctions.LossFunction.RMSE_XENT)//mcxent
                            //.updater(Updater.ADAGRAD)
                            .dropOut(0.5)
                            .activation("relu")
                            .nIn(600) // 600
                            .nOut(200) // 250
                            .build())


                    .layer(4, new DenseLayer.Builder() //(RBM.HiddenUnit.RECTIFIED, RBM.VisibleUnit.GAUSSIAN)
                            //.k(1)
                            //.lossFunction(LossFunctions.LossFunction.NEGATIVELOGLIKELIHOOD)
                            //.updater(Updater.ADAGRAD)
                            .dropOut(0.5)
                            .activation("relu")
                            .nIn(700) // 500
                            .nOut(100) // 250
                            .build())
                    */

                    .layer(3, new OutputLayer.Builder(LossFunctions.LossFunction.NEGATIVELOGLIKELIHOOD)
                            .nIn(600) // 250
                            .nOut(outputNum)
                            .activation("softmax")
                            .build())
                    .backprop(true).pretrain(false);
            new ConvolutionLayerSetup(builder, inputDim, inputDim, nChannels);

            MultiLayerConfiguration conf = builder.build();
            final MultiLayerNetwork modelNew = new MultiLayerNetwork(conf);

            this.model = modelNew;

            model.init();

            //setFileName(this.name);

            if (exitEarly) return;


            for (int ii = 0; ii < model.getnLayers(); ii++)
                System.out.println(ii + " layer dim=" + model.getLayer(ii).numParams());//+ " = " + model.getLayer(ii).getParam("bias").toString() );

            loadModel(model);

        }
        ////
        try {

            if(!doFit) nEpochs = 1;


            model.setListeners(new ScoreIterationListener(1));

            for (int i = 0; i < nEpochs; i++) {
                if (exitEarly) throw new Exception();

                if (doFit) {

                    System.out.println("Train model.... " + mnistTrain.numExamples());

                    modelSaved = false;
                    cursor = Integer.valueOf(var.configLastCursor);
                    if (cursor > ((ATAGCnnDataSet)mnistTrain).cursorSize()) cursor = 0;

                    ((ATAGCnnDataSet) mnistTrain).setCursor(cursor);

                    while(mnistTrain.hasNext()) {
                        System.out.print(split + " split -- ");

                        model.fit(mnistTrain.next(cursor));

                        //System.out.println(model.f1Score(mnistTrain.next(cursor)));

                        cursor ++;
                        if (exitEarly) throw new Exception();

                    }

                    split ++;
                    cursor = 0;

                    //model.fit(mnistTrain);
                    //saveModel(model); // not needed because of shutdown hook

                    System.out.println("*** Completed split ***");
                }

                if (doTest) {
                    log.info("Evaluate model.... " + mnistTest.numExamples());

                    ((ATAGCnnDataSet)mnistTest).setDoMirrorTrain(false);

                    cursor = 0;
                    doSaveCursor = false;

                    Evaluation eval = new Evaluation(outputNum);
                    while (mnistTest.hasNext()) {

                        DataSet ds = mnistTest.next();
                        if (exitEarly) throw new Exception();

                        INDArray output = model.output(ds.getFeatureMatrix());
                        eval.eval(ds.getLabels(), output);
                        if (exitEarly) throw new Exception();

                    }
                    log.info(eval.stats());
                    mnistTest.reset();

                    System.out.println("end of cnn op");

                }

                if(doPredict) {
                    System.out.println("predict...");

                    predictData.reset();

                    double [][] smallArray = new double[predictData.cursorSize() * ATAG.CNN_BATCH_SIZE][2];

                    INDArray small = null;

                    while (predictData.hasNext()) {
                        DataSet ds = predictData.next();
                        small = model.output(ds.getFeatureMatrix());

                        //System.out.println("len="+ small.shape().length);
                        //for (int ii = 0; ii < small.shape().length; ii ++) {System.out.println("num=" + small.shape()[ii]);}

                        for (int jj = 0; jj < small.rows(); jj ++) {
                            //System.out.println(jj + " jj " + (predictData.cursor()-1));
                            smallArray[jj + small.rows() * (predictData.cursor()-1)][0] = small.getDouble(jj,0);
                            smallArray[jj + small.rows() * (predictData.cursor()-1)][1] = small.getDouble(jj,1);
                        }

                    }
                    output = Nd4j.create(smallArray);
                    //output = small;
                }
                saveModel(model);
            }
        }

        catch (Exception e) {
            //e.printStackTrace(); // this prints stack trace when thread is interrupted!!
            saveModel(model);
        }
    }

    public MultiLayerNetwork getModel() {return model;}
    public INDArray getPredictOutput () {return output;}
    public void setModel(MultiLayerNetwork m) {model = m;}
    public void setPredictData( ATAGCnnDataSet d ) {predictData = d;}

    public void setDoFit(boolean d ) {doFit = d;}
    public void setDoTest( boolean d) {doTest = d;}
    public void setDoLoadData(boolean d) {doLoadData = d;}
    public void setDoLoadSaveModel( boolean d) { doLoadSaveModel = d;}
    public void setDoPredict( boolean d) {doPredict = d;}
    public void setDoGenerateNewModel( boolean d) {doGenerateNewModel = d;}
    public void init() {
        //model.init();
    }

    public void setFileName(String name) {
        this.name = name;
        fileName = homeDir + File.separator + name +".bin";
    }

    private void scheduleLearningRate () {
        if (split > 1 ) learningRate =  0.0005;
        else learningRate = 0.01;
    }

    public void loadModel(MultiLayerNetwork m ) {
        try {
            model = m;
            File filePath = new File(fileName);

            System.out.println("model " + fileName);
            if (!filePath.exists() || !doLoadSaveModel) return;

            if (doUseSerializerLoad) {
                //model = org.deeplearning4j.util.ModelSerializer.restoreMultiLayerNetwork(filePath);
            }
            else {
                DataInputStream dis = new DataInputStream(new FileInputStream(filePath));
                INDArray newParams = Nd4j.read(dis);
                dis.close();
                model.setParameters(newParams);

                model.setListeners(new ScoreIterationListener(1));

                ///// updater /////
                ObjectInputStream ois = new ObjectInputStream(new FileInputStream(homeDir + File.separator + this.name + ".updater.bin"));
                org.deeplearning4j.nn.api.Updater updater;
                updater = (org.deeplearning4j.nn.api.Updater) ois.readObject();
                ois.close(); //??
                model.setUpdater(updater);


            }
            System.out.println("done load model");
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void saveModel(MultiLayerNetwork m)  {
        try {
            if (!doLoadSaveModel || !doFit) return;
            model = m;
            //Write the network parameters:
            System.out.println("start model save, please wait...");

            File filePointer = new File(fileName);
            if(doUseSerializerLoad) {
                //org.deeplearning4j.util.ModelSerializer.writeModel(model, filePointer,true);
            }
            else {
                FileOutputStream fos = new FileOutputStream(filePointer);
                DataOutputStream dos = new DataOutputStream(fos);
                Nd4j.write(model.params(), dos);
                dos.flush();
                dos.close();

                ///// updater /////
                ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(homeDir + File.separator + this.name + ".updater.bin"));
                oos.writeObject(model.getUpdater());
                oos.flush();
                oos.close();
            }
            modelSaved = true;

            if (doSaveCursor || doFit) {
                var.configLastCursor = new Integer(cursor).toString();
                var.configLastSplit = new Integer(split).toString();
                var.writeConfigText(ATAG.DOTFOLDER_SAVED_CURSOR, new Integer(cursor).toString());
                var.writeConfigText(ATAG.DOTFOLDER_SAVED_SPLIT, new Integer(split).toString());
            }

            System.out.println("done save model");
            System.out.println();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void setExitEarly(boolean in) {exitEarly = in;}
    public boolean getDoFit() {return doFit;}
    public boolean getModelSaved() {return modelSaved;}

    public static void main(String [] args) {

        ATAG var = new ATAG();
        ATAGProcCsv proc = new ATAGProcCsv(var);
        proc.loadCsvStart(); // assume list has already been modded
        proc.clearUnusedList();


        try {
            final ATAGCnn cnn = new ATAGCnn(var,proc);
            cnn.start();

            Runtime.getRuntime().addShutdownHook(new Thread() {
                public void run() {
                    try {
                        cnn.setExitEarly(true);
                        MultiLayerNetwork m = cnn.getModel();
                        boolean fit = cnn.getDoFit();
                        //cnn.interrupt();

                        if (fit) {
                            cnn.setExitEarly(true);
                            cnn.saveModel(m);//(cnn.getModel());
                        }
                        //System.exit(0);


                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
        }
        catch (InterruptedException i) {

        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

}