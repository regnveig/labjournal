import time

chrom = 'huita'
print(f"{chrom} is started ... ", end="")
f = open("/dev/datasets/FairWind/_results/bowtie/coverage/grep_coverage_exoc/.txt", 'wt')
start_time = time.time()

for line in open('/dev/datasets/FairWind/_results/bowtie/coverage/1-2_hg19_coverage_each.txt', 'rt'):
    
    lst = line.split('\t')
    
    if lst[0] != chrom:
        chrom = lst[0]
        f.close()
        print(f"Done [%.2f sec]" % (time.time() - start_time), end="\n")
        f = open("/dev/datasets/FairWind/_results/bowtie/coverage/grep_coverage_exoc/" + chrom + ".txt", 'wt')
        print(f"{chrom} is started ... ", end="")
        start_time = time.time()
    
    coverage = lst[-1]
    f.write(coverage)

f.close()
print(f"Done [%.2f sec]" % (time.time() - start_time), end="\n")