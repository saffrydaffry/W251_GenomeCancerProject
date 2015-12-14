#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import re

# insert path to parent directory
path = '/root/tcga/tcga_data'

#read input from 1000 genomes file
tgfilename = "/root/tcga/vcf_1sample_cast.csv"
tgfile = pd.read_csv(tgfilename, sep = ',', engine = 'python', header = 0)
print tgfile.shape

# Read the cancer type from the folder name
for folder in os.listdir(path):
    cancer_type = folder.split('_')[1]
    print cancer_type
    path2 = path + "/" + folder

    for filename in os.listdir(path2):
        print filename

        input_maf = path2 + "/" + filename
        #input_maf = "/root/tcga/tcga_data/Data_BRCA/genome.wustl.edu_BRCA.IlluminaGA_DNASeq.Level_2.3.2.0.somatic.maf"
        maf_ex = pd.read_csv(input_maf, sep = "\t", engine = 'python', skiprows = 1, index_col=False)
        maf_ex = pd.DataFrame(maf_ex)
        
        # get column names
        colnames = list(maf_ex.columns.values)      

        # Filter by Variant_type = SNP, select only first column
        maf_ex_sub = maf_ex.loc[maf_ex.Variant_Type == "SNP", ['Hugo_Symbol', 'Tumor_Sample_Barcode' ]].copy()
        print maf_ex_sub.shape
        

        # Tumour Samples are the first 12 characters of the whole barcode
        maf_ex_sub['Tumor_Sample_Barcode'] = maf_ex_sub['Tumor_Sample_Barcode'].str[0:12]

        # Select only Tumors and Genes, each row is one mutation
        maf_gb = maf_ex_sub.groupby(['Tumor_Sample_Barcode', 'Hugo_Symbol'])

        # Reset the indices to fill the columns with Sample Names
        maf_gb_df = pd.DataFrame(maf_gb.size().reset_index())

        # Grouping counts by tumour sample and gene
        maf_gb_df.rename(columns = {0:'Count'}, inplace = True)
        maf_gb_df.columns = ['Idx', 'Gene', 'Count']

        # Cast the table into a sparse matrix insert column for label and sample
        pivoted = maf_gb_df.pivot(index = 'Idx', columns ='Gene', values = 'Count')
        print pivoted.shape
        pivoted.insert(4,'Label', cancer_type, allow_duplicates='TRUE')
        pivoted.insert(0,'Sample',pivoted.index)

        # Convert NaNs to 0s
        print pivoted.shape
        outfile = "/root/tcga/tcga_processed/"+filename+".csv"
        pivoted.fillna(0).to_csv(outfile)

        # Combine TCGA data matrix. If gene columns don't exist then create them
        tgfile = tgfile.append(pivoted)
        print tgfile.shape
        tg_outfile = "tcga_output.csv"
        tgfile.fillna(0).to_csv(tg_outfile)
