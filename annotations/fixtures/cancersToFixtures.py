#!/usr/env python

# Load required modules
import sys, os, argparse, json, re, datetime
import fixture_utils as django_fixtures
now = datetime.date.today().strftime("%Y-%m-%d")

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-cff', '--cancer_file', type=str, required=True)
parser.add_argument('-o', '--output_file', type=str, required=True)
args = parser.parse_args( sys.argv[1:] )

# Load the cancers, add the requisite info, and write to file
with open(args.cancer_file) as f:
    # raw_data already has format name, abbr, color
    raw_data = [ l.rstrip().split('\t') for l in f if not l.startswith('#') ]

cancers = django_fixtures.add_field_and_model_names(raw_data,
                                                    ('name','abbr','color'), 'annotations.cancer',
                                                    pk=True, timestamp=True)

django_fixtures.export_as_fixture(args.output_file, cancers)
