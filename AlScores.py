import os
from Bio import SeqIO
import argparse

#HERE BEGINS THE INPUT ARGUMENTS DEFINITION
usage = "A program that aligns FASTA files using mafft and evaluates the alignments using Gblocks. It returns a score that indicates each alignment's quality  \n"
toolname = "AlScore"
footer = "Who \n Paschalis Natsidis (p.natsidis@ucl.ac.uk); \n \nWhere \n Telford Lab, UCL;\n\
 ITN IGNITE; \n  \nWhen\n September 2019; \n\n"

parser = argparse.ArgumentParser(description = usage, prog = toolname, epilog = footer, formatter_class=argparse.RawDescriptionHelpFormatter,)
parser.add_argument('-c', metavar = 'filename', dest = 'config', required = True,
                    help = 'full path to config file')
parser.add_argument('-t', metavar = 'str', dest = 'type', required = True, choices=['protein', 'dna'],
                    help = 'type of molecules [protein, dna]')

#parser.print_help()

args = parser.parse_args()

#READ USER INPUT
config_file = args.config
type_of_seq = args.type


################################################################################################################
#READ CONFIG FILE

config = open(config_file, 'r')
config_lines = config.readlines()

proper_lines = []
for line in config_lines:
    if "=" in line:
        proper_lines.append(line.strip())

for line in proper_lines:
    if "fastas_dir" in line:
        fastas_dir = line.split("=")[1]
    if "mafft_path" in line:
        mafft_path = line.split("=")[1]
    if "Gblocks_path" in line:
        gblocks_path = line.split("=")[1]

################################################################################################################
#CREATE LIST WITH FASTAS
os.system("ls " + fastas_dir + "* > " + fastas_dir + "all_fasta_files.txt")

#RUN MAFFT FOR EACH FASTA
fastas_names = open(fastas_dir + "all_fasta_files.txt", "r")
fastas_names_lines = fastas_names.readlines()
fastas_names_stripped = [x.strip() for x in fastas_names_lines]

for fastas_name in fastas_names_stripped:
    os.system(mafft_path + " --auto " + fastas_name + " > " + fastas_name + ".aln")

################################################################################################################
#CREATE LIST WITH ALIGNMENT FILENAMES
os.system("ls " + fastas_dir + "*aln > " + fastas_dir + "all_aln_files.txt")

#RUN GBLOCKS FOR EACH ALIGNMENT
aln_names = open(fastas_dir + "all_aln_files.txt", "r")
aln_names_lines = aln_names.readlines()
aln_names_stripped = [x.strip() for x in aln_names_lines]

for aln_name in aln_names_stripped:
    f = SeqIO.parse(aln_name, "fasta")
    number_of_seqs = 0
    for record in f:
        number_of_seqs += 1
    half = int(number_of_seqs/2)
    os.system(gblocks_path + " " + aln_name + " -t=" + type_of_seq[0] + " -b5=h -b4=5 -b3=20 -b1=" + str(half+1) + " -b2=" + str(half+1))


################################################################################################################
# CALCULATE SCORE FOR EACH ALIGNMENT AND WRITE OUTPUT FILE

result = []

for aln_name in aln_names_stripped:
    open_aln = SeqIO.parse(aln_name, "fasta")
    open_gb = SeqIO.parse(aln_name + "-gb", "fasta")
    
    for i in open_aln:
        aln_length = len(i.seq)
        
    for i in open_gb:
        gb_length = len(i.seq)    
        
    score = round(1 - ((aln_length - gb_length) / aln_length), 3)
    result.append([aln_name.split("/")[-1][:-4], score])
    
output = open(fastas_dir + "final_scores.tsv", "w")

for entry in result:
    output.write(entry[0] + "\t" + str(entry[1]) + "\n")
