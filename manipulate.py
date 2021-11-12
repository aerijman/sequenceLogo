import numpy as np
import sys


'''
input file should be list of sequences that align. 
should come from something like this:

cat R1.subsampled.fastq | grep "CGACCTCGGGTGGGAACAC" |\
sed 's/.*CGACCTCGGGTGGGAACAC\(.\{15\}\).*$/\1/' | sort

'''
info_content=False # default do not include information content.

for n,i in enumerate(sys.argv):
    if i in ['--input','--in','--table']:
        filename = sys.argv[n+1]
    if i in ['--info-content', '--info']:
        info_content=True


nt =   {'A':0, 'T':1, 'C':2, 'G':3, 'N':4}
nt_r = {v:k for k,v in nt.items()}

sequences = {}
with open(filename, 'r') as f:
    while True:
        try:
            seq = next(f).strip().upper()
            
            if seq not in sequences:
                sequences[seq] = 1
            else:
                sequences[seq]+=1

        except StopIteration:
            break

lens = {len(k) for k in sequences.keys()}
assert len(lens)==1, "oops... not all sequences are the same length..."

length = list(lens)[0]

FPM = np.zeros(shape=(5, length)) # 5 includes "N"

for seq,howmany in sequences.items():
    for j,i in enumerate(seq):
        FPM[nt[i]][j] += howmany


PPM = FPM / np.sum(FPM, axis=0)

# not including N!!
en = 1/np.log(2) * (PPM.shape[0]-1)/2*len(sequences)
IC = np.log2(PPM.shape[0]) + np.sum(PPM * np.log2(PPM+0.001), axis=0)#.reshape(-1,1)
PWM = PPM * IC

from plot_logo import *
scores = []
for i in range(PWM.shape[1]):
    scores.append( [(nt_r[n], PWM[n,i]) for n in range(PWM.shape[0])] )

f,ax = plt.subplots(1, figsize=(25,5))
plot_logo(ax, scores)
plt.title(filename)
plt.savefig(filename+'.png', dpi=300)
#plt.show()
plt.close()
