#!/usr/env python

# Load required modules
import sys, os, argparse, json, re, datetime
now = datetime.date.today().strftime("%Y-%m-%d")

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-cff', '--cancer_file', type=str, required=True)
parser.add_argument('-o', '--output_file', type=str, required=True)
args = parser.parse_args( sys.argv[1:] )

# Load the cancers, add the requisite info, and write to file
with open(args.cancer_file) as f:
    arrs = [ l.rstrip().split('\t') for l in f if not l.startswith('#') ]
    cancers = [ ]
    for i, arr in enumerate(arrs):
        fields = dict(created_on=now, last_edited=now)
        fields.update(zip(['name', 'abbr', 'color'], arr))
        cancers.append(dict(model='annotations.cancer', pk=i+1, fields=fields))

with open(args.output_file, 'w') as out:
    json.dump(cancers, out, sort_keys=True, indent=4)
