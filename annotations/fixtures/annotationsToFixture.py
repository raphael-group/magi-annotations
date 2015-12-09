#!/usr/env python

# what to run?

# Load required modules
import sys, os, argparse, json, re, datetime, glob
###############
def readExisting(fileGlob, keyfields):
    existing = set()
    fixture_files = []
    for pattern in fileGlob:
        fixture_files.extend(glob.glob(pattern))

    for fil in fixture_files:
        print 'Reading file ' + fil + '...'
        with open(fil) as f:
            content = json.load(f)
            for item in content:
                field_dict = item['fields']
                key_item = tuple(field_dict[field] for field in keyfields)
                existing.add(key_item)

    return existing

###############
now = datetime.date.today().strftime("%Y-%m-%d")

# CONSTANTS
mutTypeToAbbr = dict(missense='MS', nonsense='NS', frame_shift_del='FSL', in_frame_del='IFD', frame_shift_ins='FSI', in_frame_ins='ISI')
heritableToAbbr = dict(Germline='G', Somatic='S')

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-af', '--annotation_files', type=str, required=True, nargs='*')
parser.add_argument('-cff', '--cancer_fixture_file', type=str, required=True)
parser.add_argument('-o', '--output_prefix', type=str, required=True)
parser.add_argument('-s', '--sources', type=str, required=True, nargs='*')
parser.add_argument('--heritable', type=str, required=False, default=None, nargs='*', choices=['', 'Germline', 'Somatic'])
args = parser.parse_args( sys.argv[1:] )

# Load the cancers file
with open(args.cancer_fixture_file) as f:
    cancers = json.load(f)
    cancerToPk = dict( (c['fields']['abbr'], c['pk']) for c in cancers )

# Read any previous sample files

# Load the annotations file to create a list of mutations
mutations, mutationPk, mutationToPk = [], 1, dict()
parsedRows = [ ]

# note: this depends on the locations given in networksToFixture.py
seen = set()

for annotation_file, source, heritable in zip(args.annotation_files, args.sources, args.heritable):
    with open(annotation_file) as f:
        arrs = [ l.rstrip('\n').split('\t') for l in f if not l.startswith('#') ]
        for gene, transcript, cancer, mutClass, mutType, locus, change, pmid in arrs:
            # Ignore duplicate rows
            if (gene, transcript, cancer, mutClass, mutType, locus, change, pmid) in seen:
                continue
            else:
                seen.add((gene, transcript, cancer, mutClass, mutType, locus, change, pmid))

            # Try to parse the amino acid change
            try:
                oaa, parsedLocus, naa = re.match(r"([A-Za-z]+)([0-9]+)([A-za-z*]+)", change, re.I).groups()
                parsedLocus = int(parsedLocus)
            except (ValueError, AttributeError):
                print 'Skipping [{}:{}]...'.format(gene, change)
                continue

            # Record a unique mutation key per row
            mutationKey = (gene, parsedLocus, oaa, naa, mutClass, mutType)
            if not mutationKey in mutationToPk:
                mutationToPk[mutationKey] = mutationPk
                m = dict(model='annotations.mutation', pk=mutationPk, fields=dict(
                    gene=gene,
                    locus=parsedLocus,
                    original_amino_acid=oaa,
                    new_amino_acid=naa,
                    mutation_type=mutTypeToAbbr[mutType],
                    mutation_class=mutClass.upper(),
                    created_on=now,
                    last_edited=now
                ))
                mutations.append( m )
                mutationPk += 1

            # Append the parsed, de-duplicated rows
            parsedRows.append( (gene, cancer, mutClass, mutType, parsedLocus, oaa, naa, pmid, source, heritable ) )


# Create a list of references
refs, refPk, referenceToMutationToPk = [], 1, dict()
for i, (gene, cancer, mutClass, mutType, locus, oaa, naa, pmid, source, heritable) in enumerate(parsedRows):
    mutationKey = (gene, locus, oaa, naa, mutClass, mutType)
    if pmid in referenceToMutationToPk:
        if not mutationKey in referenceToMutationToPk[pmid]:
            referenceToMutationToPk[pmid][mutationKey] = refPk
        else:
            continue
    else:
        referenceToMutationToPk[pmid] = { mutationKey: refPk }

    mutationPk = mutationToPk[mutationKey]
    if pmid.lower().startswith('pmc'):
        db, identifier = 'PMC', pmid.lower().split('pmc')[1]
    else:
        db, identifier = 'PMID', pmid

    fields = dict(mutation=mutationPk, identifier=identifier, source=source,
                  db=db, created_on=now, last_edited=now)
    refs.append(dict(model='annotations.reference', pk=refPk, fields=fields) )
    refPk += 1

# Create a list of annotations
annotations = []
for i, (gene, cancer, mutClass, mutType, locus, oaa, naa, pmid, source, heritable) in enumerate(parsedRows):
    mutationKey = (gene, locus, oaa, naa, mutClass, mutType)
    fields = dict(created_on=now, last_edited=now)
    if heritable is not None and heritable != '':
        fields['heritable'] = heritableToAbbr[heritable]
    if cancer:
        if cancer == 'aml': cancer = 'laml'
        fields['cancer'] = cancer

    fields['reference'] = referenceToMutationToPk[pmid][mutationKey]
    annotation = dict(model='annotations.annotation', pk=i+1, fields=fields)
    annotations.append(annotation)

# Output to JSON
with open(args.output_prefix + '-annotations.json', 'w') as out:
    json.dump( annotations, out, sort_keys=True, indent=4 )
with open(args.output_prefix + '-mutations.json', 'w') as out:
    json.dump( mutations, out, sort_keys=True, indent=4 )
with open(args.output_prefix + '-references.json', 'w') as out:
    json.dump( refs, out, sort_keys=True, indent=4 )
