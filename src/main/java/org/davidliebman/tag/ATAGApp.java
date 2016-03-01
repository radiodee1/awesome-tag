package org.davidliebman.tag;

import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;

/**
 * Hello world!
 *
 */
public class ATAGApp
{
    static ATAGShowImage image = null;

    public static void main( String[] args )
    {

        ATAG val = new ATAG();

        ATAGProcCsv proc = new ATAGProcCsv(val);

        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                try {

                    if (image != null ) {
                        ATAGCnn cnnThread = image.getCnnThread();
                        if(cnnThread != null && cnnThread.isAlive()) {
                            cnnThread.setExitEarly(true);
                            System.out.println("thread told to stop.");
                            if (!cnnThread.getModelSaved()) cnnThread.saveModel(cnnThread.getModel());
                        }
                    }



                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });


        //ATAGShowImage
        image = new ATAGShowImage(val,proc);


    }
}
