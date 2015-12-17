import sys, os, argparse, json

# sample: python annotations/fixtures/genomeToFixture.py -gf ../magi/data/genome/hg19_genes_list.tsv -o annotations/fixtures/hg19

parser = argparse.ArgumentParser()
parser.add_argument('-gf', '--genome_file', type=str, required=True)
parser.add_argument('-o', '--output_prefix', type=str, required=True)

args = parser.parse_args(sys.argv[1:])

# genome has gene, chromosome, 
def parse_line_to_gene(line):
    gene, chromosome, locus_start, locus_end = line.rstrip('\n').split('\t')
    return dict(model = 'annotations.gene', fields = dict(
        name = gene,
        chromosome = chromosome,
        start_pos = int(locus_start),
        end_pos = int(locus_end)))

print "Reading genome file " + args.genome_file + "..."
with open(args.genome_file) as f:
    # load file, but skip header with cmment lines
    genome = [ parse_line_to_gene(l) for l in f if not l.startswith('#') ]

# write as a json file
with open(args.output_prefix + '-genome.json', 'w') as out:
    json.dump( genome, out, sort_keys=True, indent=4 )
