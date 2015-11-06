__author__ = 'Safyre'

'''
Part 1.1 Grab files from S3 and store in collection titled db_tweets

'''

import os, pymongo, json, gzip
from boto.s3.key import Key
from boto.s3.connection import S3Connection
print "Paste your own AWS keys before using\n"
print "connecting to S3 via boto \n"

conn = S3Connection('AKIAJGEMM7IGTP4NTZCQ', 'k/Gi2aBpO5l/7+Y27peHU1bB/oiWyFR9ZbgYdxQG')
#bucket = conn.create_bucket('1000genomes')  # sub-datasets bucket already exists
myBucket = conn.get_bucket('1000genomes')

#for key in myBucket.list():
#    print key.name.encode('utf-8')

wkdir = '/Users/Safyre/Documents/'
#bucket = conn.create_bucket('w205_hw2bucket')  # sub-datasets bucket already exists
myKey = Key(myBucket)
bucket_list = myBucket.list()
# awesomeness http://www.laurentluce.com/posts/upload-and-download-files-tofrom-amazon-s3-using-pythondjango/


#print " Open MongoDB connection\n"
#try:
 #   conn=pymongo.MongoClient()
  #  print "Connected!"
#except pymongo.errors.ConnectionFailure, e:
#    print "Connection failed : %s" % e

#tweets_db = conn['db_tweets']


print "downloading new files locally\n"
#print "like this: s3_oldfilename.fastq.gz"
count =0
while count < 10:
    for l in bucket_list: # this indexing doesn't seem to work, still prints everything
        print l.name.encode('utf-8')
            #if str(l.key).endswith(".fastq.gz"):
        if str(l.key).endswith(".vcf.gz") or str(l.key).endswith(".vcf.gz.tbi"):
            keyString = str(l.key).split('/', )[-1]
            if not os.path.exists(wkdir + "s3_" + keyString):
                fname = wkdir + "s3_" + keyString
                print "Saving ", fname, "\n"
                l.get_contents_to_filename(fname)
                count +=1
                print "Number of files downloaded: ", count


print "Finished!"