#!/bin/bash

# file stems and locations of network files
NETWORK_STEMS="hint-annotated hprd-annotated iref9-annotated multinet"
NETWORK_DIR="../../../magi/data/ppis"

NETWORK_FILES=""
for stem in $NETWORK_STEMS;
do
	 NETWORK_FILES="${NETWORK_FILES} ${NETWORK_DIR}/${stem}.tsv"
done

python networksToFixture.py -gf hg19-genome.json -o all-networks -nf ${NETWORK_FILES} 
