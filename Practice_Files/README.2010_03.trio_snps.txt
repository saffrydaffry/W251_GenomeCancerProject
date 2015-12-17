
README file for 1000 Genomes Pilot 2 SNP calls

The 1000 Genomes Pilot 2 SNP calls are based on deep coverage 
whole genome DNA sequence data collected in 2008 using high 
throughput sequencing on two family trios in the CEPH Utah and 
HapMap sample collections.  The DNA for each individual comes 
from lymphoblastoid cell lines distributed by Coriell Institute, 
Camden, NJ.  

Average fold coverage by sequencing technology:

	 	 	   Illumina    AB SOLiD    LS 454
    (CEU family # 1463)
    NA12892 (mother)	    26.7 x
    NA12891 (father)	    32.4 x
    NA12878 (daughter)	    33.2 x	16.6 x	   13.5 x

    (YRI family # Y117)
    NA19238 (mother)	    21.8 x
    NA19239 (father)	    26.4 x
    NA19240 (daughter)	    34.7 x	24.9 x	    5.6 x

All sequence reads are mapped against the NCBI build 36.3 human 
genome reference sequence of March, 2006.  The pseudo-autosomal 
regions on the Y chromosome are replaced with Ns for males;  the 
Y chromosome is omitted for females.  Read mapping uses MAQ for 
Illumina data, Corona_lite 4.01 for AB SOLiD data and SSAHA2 for 
LS 454 data.  In Illumina and LS 454 data, PCR duplicates are 
removed using Picard MarkDuplicates and base call quality values 
are recalibrated using GATK.  Both mapped and unmapped sequence 
reads are freely available in the 1000 Genomes ftp archive.

The SNP and genotype calls released for each trio in March 2010 
are the intersection of results from two separate computational 
analyses applied to the same mapped sequence reads in the .bam 
files available from the 1000 Genomes ftp archive.  Both analyses 
are likelihood-based.  They differ in some details of pre-processing 
and modeling, and in the thresholds applied afterward to exclude 
marginal sites.  

At Broad Institute, a pre-processing step uses GATK to locally 
realign all sequence reads which cover either an indel or a cluster 
of apparent polymorphisms.  The likelihood based SNP calling treats 
each trio as three unrelated females.  The criterion to include 
a potential polymorphic site in the set of final Broad calls is:

    Consistent with Mendelian inheritance   	AND
    SNP call quality score (QUAL) >= 50,       	AND 
    Allele balance (AB) <= 75% reference, 	AND 
    Depth of coverage (DP) <= 360,   	     	AND
    Strand bias (SB) <= -0.10, 	      	     	AND
    (Number of covering reads with mapping quality score zero (MQ0) 
      <= 0.1 * depth of coverage  OR  (MQ0 < 4)).

At University of Michigan, no local realignment is done.  
The likelihood procedure makes use of known gender and family 
relationships.  Genotypes are phased where possible using 
transmission among family members, otherwise reported as 
"unphased".  A potential polymorphic site must satisfy:  

    (a)	For some sequencing technology, the depth of coverage combined 
	across all trio members at this site is between 50% and 150% 
	of the average depth, and the root mean squared (RMS) mapping 
	quality score of covering reads is at least 30.
    (b)	Sequence data passing (a) is present for each person in the trio 
	(although perhaps not from the same sequencing technology).  
    (c)	The posterior probability for at least one non-reference 
	allele exceeds 0.999  (SNP call quality score > 30).  
    (d)	Away from a potential indel detected by local realignment.  

The current release set consists of all sites which are called by 
both analyses, including passing the criteria shown above.  


