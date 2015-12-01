
import pandas as pd
import numpy as np
from cruzdb import Genome
#import PyMySQL
#PyMySQL.install_as_MySQLdb()
#import MySQLdb

'''
To install cruzdb into anaconda, go to pkgs dir within anaconda
wget https://conda.anaconda.org/travis/linux-64/cruzdb-0.5.4-py27_0.tar.bz2
conda install cruzdb-0.5.4-py27_0.tar.bz2

# cruzdb relies on MySQLdb:
sudo pip install MySQL-python
# On conda:
conda install -c https://conda.anaconda.org/chuongdo mysql-python

# fix .dylib error from mysql.so by fixing path variables
lib /usr/local/mysql/lib/libmysqlclient.18.dylib /Library/Python/2.7/site-packages/_mysql.so
'''

input_vcf = "Practice_Files/VariantCallFile10prc.vcf"

vcf_ex = pd.read_csv(input_vcf, sep = r'\t', engine = 'python', skiprows = 55)
vcf_ex = pd.DataFrame(vcf_ex)
print vcf_ex.head()

names = vcf_ex.columns.values
new_names = ['CHROM']
new_names.extend(names[1:])
print "\n", new_names
vcf_ex.columns = new_names

# If QUAL > 0.5, sample passes
vcf_ex_sub = vcf_ex.loc[vcf_ex.QUAL > 0.5, ['CHROM', 'POS']].copy()
print vcf_ex_sub.head()

hg19 = Genome('hg19')
genes = pd.Series(np.zeros(vcf_ex_sub.shape[0]))
#gene = hg19.bin_query('refGene', vcf_ex_sub.CHROM[1], vcf_ex_sub.POS[1], vcf_ex_sub.POS[1])
#print vcf_ex_sub.POS.iloc[0]


for i in range(0, vcf_ex_sub.shape[0]):
     genes[i] = hg19.bin_query('refGene', vcf_ex_sub.CHROM.iloc[i], vcf_ex_sub.POS.iloc[i], vcf_ex_sub.POS.iloc[i])
vcf_ex_sub['Hugo_Symbol'] = genes

#hg19.bin_query('refGene', vcf_ex_sub.CHROM, vcf_ex_sub.POS, vcf_ex_sub.POS)
print vcf_ex_sub.head()
print genes[0:5]

#vcf_ex['Gene'] = hg19.query('refGene', vcf_ex.C)

'''
for i, line in enumerate(open('dat.txt')):
    toks = line.split()
    if i == 0:
        print "\t".join(['gene'] + toks)
    else:
        chrom, posns = toks[0].split(":")
        start, end = map(int, posns.rstrip("|").split("-"))
        genes = hg19.bin_query('refGene', chrom, start, end)
        print "\t".join(["|".join(set(g.name2 for g in genes))] + toks)
'''