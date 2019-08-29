#!/bin/bash

THREADS=1
B2_INDEX="/dev/datasets/FairWind/_db/hg19/hg19_small/hg19"
INPUT_PATH="/dev/datasets/FairWind/_results/cut_and_split/splitted"
OUTPUT_PATH="/dev/datasets/FairWind/"
SORTED_PATH="/dev/datasets/FairWind/_results/bowtie/bam"

 bowtie2 -x $B2_INDEX \
 	-U $INPUT_PATH/sample-1-3_R1_SplitLeft.fastq \
 	-U $INPUT_PATH/sample-1-3_R1_SplitRight.fastq \
 	-U $INPUT_PATH/sample-1-3_R2_SplitLeft.fastq \
 	-U $INPUT_PATH/sample-1-3_R2_SplitRight.fastq \
 	-U $INPUT_PATH/sample-1-4_R1_SplitLeft.fastq \
 	-U $INPUT_PATH/sample-1-4_R1_SplitRight.fastq \
 	-U $INPUT_PATH/sample-1-4_R2_SplitLeft.fastq \
 	-U $INPUT_PATH/sample-1-4_R2_SplitRight.fastq \
 	--very-sensitive -p $THREADS | tee $OUTPUT_PATH/sample-1-3-4.sam | samtools view -bS \
 	-@ $THREADS - | samtools sort -@ $THREADS -O BAM - > $SORTED_PATH/sample-1-3-4_sorted.bam;

 echo 1-3-4 is ready.


 bowtie2 -x $B2_INDEX \
 	-U $INPUT_PATH/sample-1-7_R1_SplitLeft.fastq \
 	-U $INPUT_PATH/sample-1-7_R1_SplitRight.fastq \
 	-U $INPUT_PATH/sample-1-7_R2_SplitLeft.fastq \
 	-U $INPUT_PATH/sample-1-7_R2_SplitRight.fastq \
 	-U $INPUT_PATH/sample-1-8_R1_SplitLeft.fastq \
 	-U $INPUT_PATH/sample-1-8_R1_SplitRight.fastq \
 	-U $INPUT_PATH/sample-1-8_R2_SplitLeft.fastq \
 	-U $INPUT_PATH/sample-1-8_R2_SplitRight.fastq \
 	--very-sensitive -p $THREADS | tee $OUTPUT_PATH/sample-1-7-8.sam | samtools view -bS \
 	-@ $THREADS - | samtools sort -@ $THREADS -O BAM - > $SORTED_PATH/sample-1-7-8_sorted.bam;

 echo 1-7-8 is ready.
