#!/bin/bash

################################################################################
# SETTINGS, FILES, AND DIRECTORIES
################################################################################

# Directories
PROJECT_DIR=`pwd`
FIXTURES_DIR=$PROJECT_DIR/annotations/fixtures
DATA_DIR=$PROJECT_DIR/data
PPI_DIR=$DATA_DIR/ppis
VARIANT_ANNOTATIONS=$DATA_DIR/variant-annotations

################################################################################
# DOWNLOAD AND UNPACK DATA
################################################################################

wget http://compbio-research.cs.brown.edu/software/magi/data/archives/latest.tar.gz
tar -xvzf latest.tar.gz
rm latest.tar.gz

################################################################################
# PROCESS THE GENOME AND CANCER TYPES
################################################################################
cd $FIXTURES_DIR

CANCERS_FIXTURE=$FIXTURES_DIR/icgc-tcga-cancers.json
python cancersToFixtures.py \
	-cff $DATA_DIR/icgc-tcga-cancers.tsv \
	-o $CANCERS_FIXTURE

GENOME_FIXTURE=$FIXTURES_DIR/hg19-genome.json
python genomeToFixture.py \
	-gf $DATA_DIR/genome/hg19_genes_list.tsv \
	-o $GENOME_FIXTURE

################################################################################
# PROCESS PROTEIN-PROTEIN INTERACTIONS WITH ANNOTATIONS
################################################################################
python networksToFixture.py \
	-gf $GENOME_FIXTURE \
	-o all-networks \
	-nf $PPI_DIR/iref9-annotated.tsv \
	    $PPI_DIR/hprd-annotated.tsv \
		$PPI_DIR/hint-annotated.tsv \
		$PPI_DIR/multinet.tsv

################################################################################
# PROCESS VARIANT ANNOTATIONS
################################################################################
python annotationsToFixture.py \
	-af $VARIANT_ANNOTATIONS/pmc-search/tcga-pancancer-stad-pmc-search-magi-format.tsv \
	    $VARIANT_ANNOTATIONS/docm/docm-variants-magi-format.tsv \
	-s "PMC Search" DoCM \
	-cff $CANCERS_FIXTURE -o pmc-search-docm \
	--heritable "" Somatic \
	-gf $GENOME_FIXTURE

################################################################################
# LOAD THE DATA INTO POSTGRES
################################################################################
cd $PROJECT_DIR

# Load the genes and cancers
python manage.py loaddata $GENOME_FIXTURE $CANCERS_FIXTURE $FIXTURES_DIR/*genes.json

# Load the variant annotations
python manage.py loaddata $FIXTURES_DIR/pmc-search-docm*.json

# Load the protein-protein interactions
python manage.py loaddata $FIXTURES_DIR/all-networks*
