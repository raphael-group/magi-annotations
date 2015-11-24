import sys, os, argparse, json, re

parser = argparse.ArgumentParser()
parser.add_argument('-nf', '--network_files', type=str, required=True, nargs='*')
parser.add_argument('-o', '--output_prefix', type=str, required=True)

args = parser.parse_args(sys.argv[1:])

class CounterSet:
    counterDict = dict()
    counter = 1
    def lookupOrAdd(self, item):
        if item in self.counterDict:
            return self.counterDict[item]
        else:
            self.counterDict[item] = self.counter
            self.counter += 1
            return self.counter

geneSet = CounterSet()

interactions = list()
references = list()
interxnCounter = 1
refCounter = 1

for network_file in args.network_files:
    print "Reading network file " + network_file
    with open(network_file) as f:
        arrs = [ l.rstrip('\n').split('\t') for l in f if not l.startswith('#') ]
        for idx, (source, target, weight, network, PMIDlist) in enumerate(arrs, interxnCounter):
            geneSet.lookupOrAdd(source),
            geneSet.lookupOrAdd(target),
            interxn = dict(model='annotations.interaction', pk = idx, fields = dict(
                source = source,
                target = target,
                input_source = network))
            interactions.append(interxn)

            if PMIDlist:
                for pmid in set(PMIDlist.split(',')):
                    ref = dict(model='annotations.interactionreference', pk=refCounter, fields = dict(
                        identifier = pmid,
                        interaction = idx
                    ))
                    refCounter += 1
                    references.append(ref)
        interxnCounter += len(arrs)

geneStructs = [ dict(model='annotations.gene',
                     fields = dict(name = gene))
                     for gene in geneSet.counterDict.keys()]
    
with open(args.output_prefix + '-genes.json', 'w') as out:
    json.dump( geneStructs, out, sort_keys=True, indent=4 )
with open(args.output_prefix + '-ppinetwork.json', 'w') as out:
    json.dump( interactions, out, sort_keys=True, indent=4 )
with open(args.output_prefix + '-ppirefs.json', 'w') as out:
    json.dump( references, out, sort_keys=True, indent=4 )
        
