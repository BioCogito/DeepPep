# output: sparseData2: target.csv, metaInfo.csv, *.txt
# input-verify-against: sigma_49_reference.csv
# input-protein-reference:  Sigma_49_sequence.fasta  
# input-peptides: ~/data/protein/sigma_49/Sigma_49.txt
#a) 

import sys
import os
sys.path.append('../..')
import prepLib

in_strFastaFilename = '{!s}/data/protein/sigma_49/Sigma_49_sequence.fasta'.format(os.environ.get('HOME'))
in_strPeptideFilename = '{!s}/data/protein/sigma_49/Sigma_49.txt'.format(os.environ.get('HOME'))
in_strProtRefsDir = './protRefs'
out_strOutputBaseDir = './sparseData2'

prepLib.breakFasta(in_strFastaFilename, in_strProtRefsDir)
# load peptide probabilities
#prepLib.genSparse(in_.strFastaFilename, out_.strOutputBaseDir)
