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
/**
 * Created by agibsonccc on 9/16/15.
 */
public class ATAGCnn extends  Thread {
    private static final Logger log = LoggerFactory.getLogger(ATAGCnn.class);

    private boolean exitEarly = false;
    MultiLayerNetwork model;
    String name = "lenet_example_faces";
    String homeDir = "";
    String fileName = "";
    private ATAG var;
    private ATAGProcCsv proc;

    private boolean doFit = false;
    private boolean doTest = true;
    private boolean doLoadSave = true;
    private boolean doSaveCursor = true;

    private int cursor = 0;

    public   ATAGCnn (ATAG var, ATAGProcCsv proc) throws Exception {
        this.var = var;
        this.proc = proc;
        homeDir = var.configLocalRoot;
    }

    public void run() {


        Nd4j.ENFORCE_NUMERICAL_STABILITY =  true;

        homeDir = var.configLocalRoot;

        int nChannels = ATAG.CNN_CHANNELS;
        int outputNum = ATAG.CNN_LABELS;
        int batchSize = ATAG.CNN_BATCH_SIZE;
        int nEpochs = 1;// 10
        int iterations = 1;
        int seed = 123;
        float testSplit = 0.12f;

        int inputDim = ATAG.CNN_DIM_SIDE;//80 or 90

        log.info("Load data....");

        DataSetIterator mnistTrain = null;
        DataSetIterator mnistTest = null;
        try {
            mnistTrain = new ATAGCnnDataSet(proc.getLocalList(), var, 0, true, 1.0f - testSplit, seed, 0, true);
            mnistTest = new ATAGCnnDataSet(proc.getLocalList(), var, 0, false, testSplit, seed , 0, false);
        }
        catch (Exception e) {
            e.printStackTrace();
        }

        log.info("Build model....");
        MultiLayerConfiguration.Builder builder = new NeuralNetConfiguration.Builder()
                .seed(seed)
                .iterations(iterations)
                .regularization(true).l2(0.0005)
                .learningRate(0.01)
                .weightInit(WeightInit.XAVIER)
                .optimizationAlgo(OptimizationAlgorithm.STOCHASTIC_GRADIENT_DESCENT)
                .updater(Updater.NESTEROVS).momentum(0.9)
                .list(4)
                .layer(0, new ConvolutionLayer.Builder(5, 5)
                        .nIn(nChannels)
                        .stride(1, 1)
                        .nOut(20) //20
                        .dropOut(0.5)
                        .activation("relu")
                        .build())
                .layer(1, new SubsamplingLayer.Builder(SubsamplingLayer.PoolingType.MAX)
                        .kernelSize(2,2)
                        .stride(2,2)
                        .build())
                .layer(2, new DenseLayer.Builder().activation("relu")
                        .nOut(1000).build()) // 500
                .layer(3, new OutputLayer.Builder(LossFunctions.LossFunction.NEGATIVELOGLIKELIHOOD)
                        .nOut(outputNum)
                        .activation("softmax")
                        .build())
                .backprop(true).pretrain(false);
        new ConvolutionLayerSetup(builder,inputDim,inputDim, nChannels);

        MultiLayerConfiguration conf = builder.build();
        final MultiLayerNetwork model = new MultiLayerNetwork(conf);
        model.init();

        this.model = model;
        setFileName(this.name);

        loadModel(model);


        try {

            if(!doFit) nEpochs = 1;

            model.setListeners(new ScoreIterationListener(1));
            for (int i = 0; i < nEpochs; i++) {
                if (exitEarly) return;

                if (doFit) {
                    log.info("Train model.... " + mnistTrain.numExamples());

                    cursor = Integer.valueOf(var.configLastCursor);
                    if (cursor > ((ATAGCnnDataSet)mnistTrain).cursorSize()) cursor = 0;

                    ((ATAGCnnDataSet) mnistTrain).setCursor(cursor);

                    while(mnistTrain.hasNext()) {
                        model.fit(mnistTrain.next(cursor));
                        cursor ++;
                    }

                    //model.fit(mnistTrain);
                    //saveModel(model); // not needed because of shutdown hook

                    log.info("*** Completed epoch {} ***", i);
                }

                if (doTest) {
                    log.info("Evaluate model.... " + mnistTest.numExamples());

                    cursor = 0;
                    doSaveCursor = false;

                    Evaluation eval = new Evaluation(outputNum);
                    while (mnistTest.hasNext()) {
                        DataSet ds = mnistTest.next();
                        INDArray output = model.output(ds.getFeatureMatrix());
                        eval.eval(ds.getLabels(), output);
                    }
                    log.info(eval.stats());
                    mnistTest.reset();
                }
            }
            log.info("****************Example finished********************");
        }

        catch (Exception e) {
            //e.printStackTrace(); // this prints stack trace when thread is interrupted!!
        }
    }

    public MultiLayerNetwork getModel() {return model;}
    public void setModel(MultiLayerNetwork m) {model = m;}

    public void setFileName(String name) {
        this.name = name;

        fileName = homeDir + File.separator + name +".bin";
    }


    public void loadModel(MultiLayerNetwork m ) {
        try {
            model = m;
            File filePath = new File(fileName);

            System.out.println("model " + fileName);
            if (!filePath.exists() || !doLoadSave) return;

            DataInputStream dis = new DataInputStream(new FileInputStream(filePath));
            INDArray newParams = Nd4j.read(dis);
            dis.close();
            model.setParameters(newParams);
            System.out.println("done load model");
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void saveModel(MultiLayerNetwork m)  {
        try {
            if (!doLoadSave) return;
            model = m;
            //Write the network parameters:
            System.out.println("start model save, please wait...");
            File filePointer = new File(fileName);
            //OutputStream fos = Files.newOutputStream(Paths.get(fileName));
            FileOutputStream fos = new FileOutputStream(filePointer);
            DataOutputStream dos = new DataOutputStream(fos);
            Nd4j.write(model.params(), dos);
            dos.flush();
            dos.close();

            if (doSaveCursor || doFit) var.writeConfigText(ATAG.DOTFOLDER_SAVED_CURSOR, new Integer(cursor).toString());

            System.out.println("done save model");
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void setExitEarly(boolean in) {exitEarly = in;}
    public boolean getDoFit() {return doFit;}

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
                        cnn.interrupt();

                        if (fit) {

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
            //e.printStackTrace();
        }
    }

}