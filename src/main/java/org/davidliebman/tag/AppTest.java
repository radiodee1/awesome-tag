package org.davidliebman.tag;

import org.nd4j.linalg.factory.Nd4j;

/**
 * Created by dave on 3/20/16.
 */
public class AppTest {
    public static void main(String[] args){

        //System.setProperty("java.library.path","/usr/lib/");
        String newPath = System.getProperty("java.library.path") + ":/usr/local/cuda/lib64:/usr/local/cuda/bin";
        System.setProperty("java.library.path", newPath);
        System.out.println(System.getProperty("java.library.path"));

        Nd4j.ENFORCE_NUMERICAL_STABILITY =  true;

        //System.out.println(System.getProperty("java.library.path"));
        //System.loadLibrary("nd4j");
    }
}
