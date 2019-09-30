# AlScores
A script that aligns fasta files using mafft and evaluates the alignments using Gblocks. It returns a score that indicates each alignment's quality based on Gblocks result.


This script depends on the following software to run:
- [mafft](https://mafft.cbrc.jp/alignment/software/) 
- [Gblocks](http://molevol.cmima.csic.es/castresana/Gblocks.html) 
<br>

The local paths to these tools **must** be defined in the config file.
 <br> 

 All the above tools and packages can be easily installed via the ```conda``` environment.
 
 <br> 
 <br>  

## Arguments
Argument    |  Description             
:-------------:|:-----------------------
`-c` | (full) path to config file
`-t` | type of sequences used [protein, dna]

## Example Usage

AlScore needs a config file to run. This file will contain the paths to required tools (mafft, Gblocks) as well as the  path to directory that contains the fasta files to be analysed. Note that all fasta files **must** end with the suffix `.fasta`
<br>
Please change the provided `config.txt` file accordingly before running your own analysis.

```
python AlScore.py -c config.txt -t dna
```

<br>
The output file will be called `final_scores.tsv` and will contain two columns: filename and score. <br>
The score can range from 0 to 1, with higher score meaning better aligment quality.
 
<br>
Who<br> 
 Paschalis Natsidis, PhD candidate (p.natsidis@ucl.ac.uk); <br>
<br>
Where<br>
 Telford Lab, UCL;<br>
 ITN IGNITE; 
<br>
<br>
When<br> 
 October 2019; 
