import sys, os, argparse, json, re
import genomeToFixture as genome
import fixture_utils as django_fixtures
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_prefix', type=str, required=True)
    parser.add_argument('-gf', '--genome_fixture', type=str, required=False)
    parser.add_argument('-nf', '--network_files', type=str, required=True, nargs='*')

    args = parser.parse_args(sys.argv[1:])
    previousGenome = "genome_fixture" in args
    if previousGenome:
        newGenes = []

    interactions = list()
    references = list()
    interxnCounter = 1
    refCounter = 1

    for network_file in args.network_files:
        print "Reading network file " + network_file

        with open(network_file) as f:

            arrs = [ l.rstrip('\n').split('\t') for l in f if not l.startswith('#') ]
            # each row contains the following fields
            for idx, (source, target, weight, network, PMIDlist) in enumerate(arrs, interxnCounter):
                # check to see whether source/target genes are correctly named
                if previousGenome:
                    isContained, source_name = genome.containedIn(args.genome_fixture, source, case_sensitive=False)                        
                    if not isContained:
#                        print "Adding new gene", source
                        newGenes.append(source)
                    else:
#                        if source != source_name:
#                            print "Source corrected from %s->%s" % (source, source_name) 
                        source = source_name

                    isContained, target_name = genome.containedIn(args.genome_fixture, target, case_sensitive=False)                        
                    if not isContained:
#                        print "Adding new gene", target
                        newGenes.append(target)
                    else:
#                        if target != target_name:
#                            print "Target corrected from %s->%s" % (target, target_name) 
                        target = target_name
    
                # compile interactions for the relation anotations.interaction
                interxn = dict(model='annotations.interaction', pk = idx, fields = dict(
                    source = source,
                    target = target,
                    input_source = network))
                interactions.append(interxn)
                
                # references should be added to a separate relation annotations.interactionreference
                if PMIDlist:
                    for pmid in set(PMIDlist.split(',')):
                        ref = dict(model='annotations.interactionreference', pk=refCounter, fields = dict(
                            identifier = pmid,
                            interaction = idx,
                            db = 'PMID' # database is always PMID for these 
                        ))
                        refCounter += 1
                        references.append(ref)
                        
            interxnCounter += len(arrs)

    # export to JSON
    newGenes = list(set(newGenes))
    django_fixtures.export_fileset(args.output_prefix, {'-ppinetwork.json': interactions,
                                    '-ppirefs.json': references,
                                    '-newgenes.json': map(genome.newEntry, newGenes)})
