

import pandas as pd
import numpy as np
import os

# insert path to parent directory
path = '/root/tcga'
# this will print the part of the directory name after the _
for name in os.listdir(path):
    print name.split('_')[1]
input_maf = "Practice_Files/genome.wustl.edu_BRCA.IlluminaGA_DNASeq.Level_2.5.3.0.somatic.maf"

maf_ex = pd.read_csv(input_maf, sep = r'\t', engine = 'python', skiprows = 1)
maf_ex = pd.DataFrame(maf_ex)

# get column names
colnames = list(maf_ex.columns.values)

# Filter by Variant_type = SNP, select only first column
maf_ex_sub = maf_ex.loc[maf_ex.Variant_Type=='SNP', ['Hugo_Symbol', 'Tumor_Sample_Barcode' ]].copy()

# Tumor Samples are the first 12 characters of the whole barcode
maf_ex_sub['Tumor_Sample_Barcode'] = maf_ex_sub['Tumor_Sample_Barcode'].str[0:12]

# Select only Tumors and Genes, each row is one mutation
maf_gb = maf_ex_sub.groupby(['Tumor_Sample_Barcode', 'Hugo_Symbol'])

# Reset the indices to fill the columns with Sample Names
maf_gb_df = pd.DataFrame(maf_gb.size().reset_index())

# Grouping counts by tumor sample and gene
maf_gb_df.rename(columns = {0:'Count'}, inplace = True)
    #print maf_gb_df.shape, maf_gb_df.columns.values

# Cast the table into a sparse matrix
pivoted = maf_gb_df.pivot(index = 'Tumor_Sample_Barcode', columns ='Hugo_Symbol', values = 'Count')
pivoted['label'] = ['BRCA']*pivoted.shape[0]

# Print out the sparse matrix
# Convert NaNs to 0s
outfile = "processed_MAF.csv"
pivoted.fillna(0).to_csv(outfile)
