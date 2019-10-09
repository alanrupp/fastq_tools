## Add custom genes to GTF file based on user input


# input GTF information
gtf_stash = list()
while True:
    seqname = str(input('seqname (no default): '))
    while len(seqname) == 0:
        seqname = str(input('seqname (no default): '))
    source = str(input('source (default = AddedGenes): ') or 'AddedGenes')
    feature = str(input('feature (default = exon): ') or 'exon')
    start = str(input('start (default = 1): ') or '1')
    end = str(input('end (no default): '))
    while len(end) == 0:
        end = str(input('end (no default): '))
    score = str(input('score (default = .): ') or '.')
    strand = str(input('strand (default = +): ') or '+')
    frame = str(input('frame (default = 0): ') or '0')
    attributes = str(input('attributes (default = seqname): ') or 'gene_id "'+seqname+'"; '+'gene_name "'+seqname+'"; '+'transcript_id "'+seqname+'"; '+'transcript_name "'+seqname+'";')
    gtf = seqname + '\t'+source+'\t'+feature+'\t'+start+'\t'+end+'\t' + score + '\t' + strand + '\t' + frame + '\t' + attributes + '\n'
    gtf_stash.append(gtf)
    ask = input('Done! To finish, type "exit". To add another, hit ENTER: ')
    if ask == 'exit' : break


# ask if appending custom genes to existing GTF
fname = input('Existing GTF file to append ("n" to generate new file): ')
if fname != 'n':
    gtf = list()
    with open(fname, 'r') as f:
        for line in f:
            gtf.append(line)
    for line in gtf_stash:
        gtf.append(line)
else:
    gtf = gtf_stash


# write to file
fname = input('GTF filename: ')
with open(fname, 'w') as f:
    for line in gtf:
        f.write(line)
