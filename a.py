import sys


length_of_output = 20 # default
for n,i in enumerate(sys.argv):
    if i in ['--fastq','--fastq-file']:
        filename = sys.argv[n+1]
    elif i in ['--pattern','--sequence','--primer']:
        primer = sys.argv[n+1]
    elif i in ['--length','--outputLength']:
        length_of_output = sys.argv[n+1]


if len( {'primer','filename'}.intersection(locals().keys()) )<2:
    print("Dont forget fastq and patern")



sequences = []
with open(filename,'r') as f:
    while True:
        try:
            h,s,p,q = next(f),next(f),next(f),next(f)
            sequences.append(s.strip())
        except StopIteration:
            break


def find_fuzzy(pattern, string):
    l = len(pattern)//4
    patterns = [pattern[l*n:l*(n+1)] for n in range(4)] 
    
    for n,p in enumerate(patterns):
        f = [i.span()[0] for i in re.finditer(p, string)]
        # generate edit distance of entire pattern 
        # for each partial match



from fuzzysearch import find_near_matches

n=0
for k,seq in enumerate(sequences):

    a = find_near_matches(primer, seq, max_l_dist=0)

    if len(a)>0:
        end = a[0].end
        print(seq[end:end+length_of_output])
        n+=1

sys.stderr.write("{}, {}\n".format(n,k))
