# README #

### DESCRIPTION ###

This directory contains scripts for creating JSON fixture files for loading data
into Django that was originally in MAGI TSV format. It also contains the data
files themselves.

### LOGS ###

#### 2015/09/22 ####

I generated the cancer fixture file:

    python cancersToFixtures.py -cff ../../../magi/data/icgc-tcga-cancers.tsv -o icgc-tcga-cancers.json

And then generate the merged DoCM and PMC Search annotation files:

    python annotationsToFixture.py -af ../../../magi/data/variant-annotations/pmc-search/tcga-pancancer-stad-pmc-search-magi-format.tsv ../../../magi/data/variant-annotations/docm/docm-variants-magi-format.tsv -cff icgc-tcga-cancers.json -o pmc-search-docm -s "PMC Search" DoCM --heritable "" Somatic

I then loaded the data into Django:

    >>> cd ../../
    >>> python manage.py loaddata annotations/fixtures/icgc-tcga-cancers.json annotations/fixtures/pmc-search-docm-mutations.json annotations/fixtures/pmc-search-docm-references.json annotations/fixtures/pmc-search-docm-annotations.json