import sys, os, argparse, json, glob

############### for exporting #################
# fileGlobList 
def readExisting(fileGlobList, keyfield):
    existing = set()
    fixture_files = []
    for pattern in fileGlobList:
        fixture_files.extend(glob.glob(pattern))

    for fil in fixture_files:
        print 'Reading file ' + fil + '...'
        with open(fil) as f:
            content = json.load(f)
            for item in content:
                existing.add(item['fields'][keyfield])

    return existing

memoed_genomes = {}
memoed_upper_genomes = {}
# return the original name as well
def containedIn(fileGlob, gene, **kwargs):
    if fileGlob not in memoed_genomes:
        genome = (readExisting([fileGlob], 'name'))
        memoed_genomes[fileGlob] = genome
        memoed_upper_genomes[fileGlob] = [m for m in genome if m.upper() != m]

    full_genome = memoed_genomes[fileGlob]
    upper_genome = memoed_upper_genomes[fileGlob]

    if gene in full_genome:
        return True, gene
    elif not kwargs['case_sensitive']:
        matches = [m for m in upper_genome if m.upper() == gene.upper()]
        if matches:
            return True, matches[0]
        else:
            return False, None

    return False, None

def newEntry(gene_name):
    return dict(model = 'annotations.gene', fields = dict(
        name = gene_name))

###############

# sample: python annotations/fixtures/genomeToFixture.py -gf ../magi/data/genome/hg19_genes_list.tsv -o annotations/fixtures/hg19
if __name__ == '__main__':
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

