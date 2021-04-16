package org.ejprd.hpomapping;

import java.io.File;

public class Main {

    public static void main(String[] args) throws Exception
    {
        if(args.length != 2)
        {
            throw new Exception("You must specify 2 arguments: input file, output file");
        }

        File input = new File(args[0]);
        if(!input.exists())
        {
            throw new Exception("Input file not found at " + input.getAbsolutePath());
        }

        File output = new File(args[1]);
        if(output.exists())
        {
            throw new Exception("Output file already present, please delete at " + output.getAbsolutePath());
        }

        FindHPOCodes FHC = new FindHPOCodes(input, output);
        FHC.start();

        System.out.println("Finished!");
    }

}
