# README #

### DESCRIPTION ###

This directory contains scripts for creating JSON fixture files for loading data
into Django that was originally in MAGI TSV format. It also contains the data
files themselves.

You should ensure 
The current workflow for creating the fixture files is:

(from this directory)
> python cancersToFixtures.py -cff ../../../magi/data/icgc-tcga-cancers.tsv -o icgc-tcga-cancers.json
> python genomeToFixture.py -gf ../../../magi/data/genome/hg19_genes_list.tsv -o hg19
> python annotationsToFixture.py -af ../../../magi/data/variant-annotations/pmc-search/tcga-pancancer-stad-pmc-search-magi-format.tsv ../../../magi/data/variant-annotations/docm/docm-variants-magi-format.tsv -cff icgc-tcga-cancers.json -o pmc-search-docm -s "PMC Search" DoCM --heritable "" Somatic -gf hg19-genome.json
> bash networkToFixture.sh

> cd ../.. # go to the base project directory
> python manage.py loaddata annotations/fixtures/hg19-genome.json annotations/fixtures/icgc-tcga-cancers.json annotations/fixtures/*genes.json
> python manage.py loaddata annotations/fixtures/*.json

### LOGS ###

#### 2015/09/22 ####

I generated the cancer fixture file:

    python cancersToFixtures.py -cff ../../../magi/data/icgc-tcga-cancers.tsv -o icgc-tcga-cancers.json

And then generate the merged DoCM and PMC Search annotation files:

    python annotationsToFixture.py -af ../../../magi/data/variant-annotations/pmc-search/tcga-pancancer-stad-pmc-search-magi-format.tsv ../../../magi/data/variant-annotations/docm/docm-variants-magi-format.tsv -cff icgc-tcga-cancers.json -o pmc-search-docm -s "PMC Search" DoCM --heritable "" Somatic

I then loaded the data into Django:

    >>> cd ../../
    >>> python manage.py loaddata annotations/fixtures/icgc-tcga-cancers.json annotations/fixtures/pmc-search-docm-mutations.json annotations/fixtures/pmc-search-docm-references.json annotations/fixtures/pmc-search-docm-annotations.json

#### 2015/11/? ####

For loading ppi networks:

I generated the networks fixture file:

> source annotations/fixtures/networksToFixture.sh

Then I loaded the data in django.

> python manage.py annotations/fixtures/all-networks*

#### 2015/12/8 ####

We now provide a conversion script to create a genome fixture, which must be loaded into the database before annotations or networks.

The script can be run as

> python genomeToFixture.py -gf ../../../magi/data/genome/hg19_genes_list.tsv -o hg19

The fixtures should then be loaded in specific order, genome and cancers first:

> python manage.py loaddata annotations/fixtures/hg19-genome.json annotations/fixtures/icgc-tcga-cancers.json
> python manage.py loaddata annotations/fixtures/*.json

