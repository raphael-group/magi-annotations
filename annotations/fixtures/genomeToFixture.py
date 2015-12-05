import sys, os, argparse, json

# sample: python annotations/fixtures/genomeToFixture.py -gf ../magi/data/genome/hg19_genes_list.tsv -o annotations/fixtures/hg19

parser = argparse.ArgumentParser()
parser.add_argument('-gf', '--genome_file', type=str, required=True)
parser.add_argument('-o', '--output_prefix', type=str, required=True)

args = parser.parse_args(sys.argv[1:])
genes = list()

print "Reading genome file " + args.genome_file + "..."
with open(args.genome_file) as f:
    # load file, but skip header
    arrs = [ l.rstrip('\n').split('\t') for l in f if not l.startswith('#') ]
    for idx, (gene, chromosome, start, end) in enumerate(arrs):
        gene = dict(model='annotations.gene', fields = dict(
            name = gene,
            chromosome = chromosome,
            locus_begin = int(start),
            locus_end = int(end)))
        genes.append(gene)

with open(args.output_prefix + '-genome.json', 'w') as out:
    json.dump( genes, out, sort_keys=True, indent=4 )
