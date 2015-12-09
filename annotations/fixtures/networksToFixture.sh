#!/bin/bash

NETWORK_STEMS="hint-annotated hprd-annotated iref9-annotated multinet"
NETWORK_DIR="../../../magi/data/ppis"

NETWORK_FILES=""
for stem in $NETWORK_STEMS;
do
	 NETWORK_FILES="${NETWORK_FILES} ${NETWORK_DIR}/${stem}.tsv"
done

python networksToFixture.py -o all-networks -nf ${NETWORK_FILES} 
