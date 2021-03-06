from lib.Liebe import *

genome = "/dev/datasets/FairWind/_db/hg19/hg19.fa"
exome = "/dev/datasets/FairWind/_db/MedExome_hg19_capture_targets.sorted.bed"
THREADS_NUM = 12
EXP = "DP>10 & %QUAL>15 & ((DP4[2]+DP4[3])/DP)>0.2"

def the_thread(block, output_dir):
	index, input_filename = block
	
	output_filename = Blister.Output(input_filename, output_dir, f"FilterCalls_DP10-QUAL15-ALT02", "vcf", rewrite=True)
	if not output_filename: return

	with Blister.Timestamp("FILTER BAM", input_filename, output_filename) as start_time:
		
		#command = f"bcftools mpileup -f {genome} {input_filename} | bcftools call -cv -Ou | bcftools filter -i \"{EXP}\" | vcftools --vcf - --recode --recode-INFO-all --bed {exome} --out {output_filename}"
		command = f"bcftools mpileup -f {genome} {input_filename} | bcftools call -cv -Ou | bcftools filter -i \"{EXP}\" > {output_filename}"
		sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = sp.communicate()
		if err != b'': print(f"BamFilter: Shell: {str(err)}", end='\n')

Blister.EachFile(f"BamFilter", ["/dev/datasets/FairWind/_results/bowtie/dupless/sample-1-9_dupless.bam"], "/dev/datasets/FairWind/_results/bowtie/", THREADS_NUM)(the_thread)()
