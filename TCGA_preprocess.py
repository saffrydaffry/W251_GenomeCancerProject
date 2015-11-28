

import pandas as pd
import numpy as np
#from pandas import DataFrame

input_maf = "Practice_Files/genome.wustl.edu_BRCA.IlluminaGA_DNASeq.Level_2.5.3.0.somatic.maf"
maf_ex = pd.read_csv(input_maf, sep = r'\t', engine = 'python', skiprows = 1)
maf_ex = pd.DataFrame(maf_ex)

# check to see if everything split nicely
print maf_ex.head(), maf_ex.shape

# get column names
colnames = list(maf_ex.columns.values)
print colnames
# Number of unique genes
print len(maf_ex.Hugo_Symbol.unique())

# index columns of interest:

# Filter by Variant_type = SNP, select only first column
maf_ex_sub = maf_ex.loc[maf_ex.Variant_Type=='SNP', ['Hugo_Symbol', 'Tumor_Sample_Barcode' ]].copy()
print maf_ex_sub.head()

maf_ex_sub['Tumor_Sample_Barcode'] = maf_ex_sub['Tumor_Sample_Barcode'].str[0:12]

print maf_ex_sub.head()
print len(maf_ex_sub.Tumor_Sample_Barcode.unique())

maf_gb = maf_ex_sub.groupby(['Tumor_Sample_Barcode', 'Hugo_Symbol'])
maf_gb_df = pd.DataFrame(maf_gb.size().reset_index())
print "Grouping counts by tumor sample and gene\n", maf_gb_df.head()
maf_gb_df.rename(columns = {0:'Count'}, inplace = True)
print maf_gb_df.shape, maf_gb_df.columns.values
pivoted = maf_gb_df.pivot('Tumor_Sample_Barcode', 'Hugo_Symbol')


print pivoted.head()

print pivoted.loc[:,['Count']].fillna(0).head()
#print pivoted.loc[:,['Count']].fillna(0).reset_index().head()

outfile = "processed_MAF.csv"

#pivoted.loc[:,['Count']].fillna(0).to_csv(outfile, header=0, chunksize = 5)
pivoted.fillna(0).to_csv(outfile, header=0, chunksize = 5)

'''
# trying to change NaNs to 0, but have to access under multiIndex
# this gets the job done, but then have to put back together into one DF?

for sample, sub_df in pivoted.groupby(level=0):
    print sub_df.fillna(0)
'''

#pivoted.fillna(0)
#print pivoted.head()


#print pivoted.where(pivoted ==1)

# Are any greater than one?

#print maf_ex.shape, maf_ex_sub.shape

#df[['col1', 'col2', 'col3', 'col4']].groupby(['col1', 'col2']).agg(['mean', 'count'])




'''
import csv
input_maf = "Practice_Files/genome.wustl.edu_BRCA.IlluminaGA_DNASeq.Level_2.5.3.0.somatic.maf"

with open(input_maf, 'rb') as f:
    fread = csv.reader(f)
    for line in fread:
        print line
'''
