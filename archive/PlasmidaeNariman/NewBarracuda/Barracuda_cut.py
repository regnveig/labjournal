import os
import subprocess
 
def Bash(Command):
	Shell = subprocess.Popen(Command, shell=True, executable="/bin/bash", stdout=open(os.devnull, 'w'), stderr=subprocess.PIPE)
	Error = Shell.communicate()[1]
	if Shell.returncode != 0: raise OSError(f"Bash fucked up because of architecture proёb")

Input_R1 = "/dev/datasets/ngs_data/Battulin_BGI_20200918/demult/AS_A23_1.fq.gz"
Input_R2 = "/dev/datasets/ngs_data/Battulin_BGI_20200918/demult/AS_A23_2.fq.gz"
Output_R1 = "/dev/datasets/ngs_data/Battulin_BGI_20200918/demult/AS_A23_Cut_1.fq.gz"
Output_R2 = "/dev/datasets/ngs_data/Battulin_BGI_20200918/demult/AS_A23_Cut_2.fq.gz"

SearchLength = 15
ErrorRate = 0.2
Threads = 10

CutFragment = {
	"F": "CATGAGCGGATACATATTTGAATGTATTTAGAAAAATAAACAAATAGGGGTTCCGCGCACATTTCCCCGAAAAGTGCCACCTGGGCATGCG^NNCGANNACTNNATGNNACGNNCTGNNTCANN$TCGGTACCGAGAACCGGGCAGGTCACGCATCCCCCCCTTCCCTCCCACCCCCTGCCAAGCTCTCCCTCCCAGGATCCTCTCTGGCTCCATCGTAAGCAAACCTTAGAGGTTCTGGCAAGGAGAGAGATGGCTCCAGGAAATGGGGGTGTGTCACCAGATAAGGAATCTGCCTAACAGGAGGTGGGGGTTAGACCCAATATCAGGAGACTAGGAAGGAGGAGGCCTAAGGATGGGGCTTTTCTGTCACCAATCCTGTCCCTAGTGGCCCCACTGTGGGGTGGAGGGGACAGATAAAAGTACCCAGAACCAGAGCCACATTAACCGGCCCTGGGAATATAAGGTGGTCCCAGCTCGGGGACACAGGATCCCTGGAGGCAGCAAACATGCTGTCCTGAAGTGGACATAGGGGCCCGGGTTGGAGGAAGAAGACTAGCTGAGCTCTCGGACCCCTGGAAGATGCCATGACAGGGGGCTGGAAGAGCTAGGGTACCAC^NNTACNNCGANNTAGNNACGNNTTCNNGAGNN$CGCTAGCAACGTAGGAGCGACATTGATTATTGACTAG",
	"R": "CTAGTCAATAATCAATGTCGCTCCTACGTTGCTAGCG$NNCTCNNGAANNCGTNNCTANNTCGNNGTANN^GTGGTACCCTAGCTCTTCCAGCCCCCTGTCATGGCATCTTCCAGGGGTCCGAGAGCTCAGCTAGTCTTCTTCCTCCAACCCGGGCCCCTATGTCCACTTCAGGACAGCATGTTTGCTGCCTCCAGGGATCCTGTGTCCCCGAGCTGGGACCACCTTATATTCCCAGGGCCGGTTAATGTGGCTCTGGTTCTGGGTACTTTTATCTGTCCCCTCCACCCCACAGTGGGGCCACTAGGGACAGGATTGGTGACAGAAAAGCCCCATCCTTAGGCCTCCTCCTTCCTAGTCTCCTGATATTGGGTCTAACCCCCACCTCCTGTTAGGCAGATTCCTTATCTGGTGACACACCCCCATTTCCTGGAGCCATCTCTCTCCTTGCCAGAACCTCTAAGGTTTGCTTACGATGGAGCCAGAGAGGATCCTGGGAGGGAGAGCTTGGCAGGGGGTGGGAGGGAAGGGGGGGATGCGTGACCTGCCCGGTTCTCGGTACCGA$NNTGANNCAGNNCGTNNCATNNAGTNNTCGNN^CGCATGCCCAGGTGGCACTTTTCGGGGAAATGTGCGCGGAACCCCTATTTGTTTATTTTTCTAAATACATTCAAATATGTATCCGCTCATG" 
	}

CutSeqs = {}
for Strand in ['F', 'R']:
	Begin = '^' if Strand == 'F' else '$'
	End = '^' if Strand == 'R' else '$'
	CutSeqs[f"1{Strand}"] = CutFragment[Strand].split(Begin)[0][-SearchLength:]
	CutSeqs[f"2{Strand}"] = CutFragment[Strand].split(End)[1][0:SearchLength]
	CutSeqs[f"L{Strand}"] = len(CutFragment[Strand].split(Begin)[1].split(End)[0])
	CutSeqs[f"Pos{Strand}"] = len(CutFragment[Strand].split(Begin)[0])

Command = f"set -o pipefail; cutadapt -j {str(Threads)} -e {str(ErrorRate)} -g {CutSeqs['1R']} -g {CutSeqs['1F']} -G {CutSeqs['1R']} -G {CutSeqs['1F']} -O {str(SearchLength)} -o {Output_R1} -p {Output_R2} {Input_R1} {Input_R2}"
#Bash(Command)
print(CutSeqs)