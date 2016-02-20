package org.davidliebman.tag;

/**
 * Hello world!
 *
 */
public class ATAGApp
{
    public static void main( String[] args )
    {

        ATAG val = new ATAG();

        ATAGProcCsv proc = new ATAGProcCsv(val);
        ATAGShowImage image = new ATAGShowImage(val,proc);


    }
}
