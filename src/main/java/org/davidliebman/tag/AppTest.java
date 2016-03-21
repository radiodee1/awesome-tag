package org.davidliebman.tag;

/**
 * Created by dave on 3/20/16.
 */
public class AppTest {
    public static void main(String[] args){

        //System.setProperty("java.library.path","/usr/lib/");

        System.out.println(System.getProperty("java.library.path"));
        System.loadLibrary("nd4j");
    }
}
