package org.davidliebman.tag;

/**
 * Hello world!
 *
 */
public class ATAGApp
{
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );

        ATAG val = new ATAG();

        ATAGProcCsv proc = new ATAGProcCsv(val);
        ATAGShowImage image = new ATAGShowImage(val,proc);


    }
}
