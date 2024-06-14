# pandasPGS: a Python package for easy retrieval of PGS Catalog data

## Installation
`pip install pandaspgs`
## Documentation
See [pandasPGS Documentation](https://tianzelab.github.io/pandaspgs/)
## Licensing information
### Source code
MIT License
### Data from PGS Catalog
The PGS Catalog and all its contents are available under the general terms of use for EMBL-EBI services
## Example 1. Investigating trends in diabetes-related polygenic risk scores
### Step 1
```Python
from pandaspgs import *
from plotnine import*
```
### Step 2
```Python
traits = get_traits(term='diabetes')
traits
# Trait is running in fat mode. It has 6 DataFrames with hierarchical dependencies.
# traits: 6 rows
# |
#  -associated_pgs_ids: 186 rows
# |
#  -child_associated_pgs_ids:265 rows
# |
#  -trait_categories: 13 rows
# |
#  -trait_mapped_terms: 57 rows
# |
#  -trait_synonyms: 66 rows
```
### Step 3
```Python
traits.traits
#         id                  label                                description                                          url                     
# 0    EFO_0000400            diabetes mellitus  A metabolic disorder characterized by abnormal...          http://www.ebi.ac.uk/efo/EFO_0000400
# 1    EFO_0006842  diabetes mellitus biomarker                                                             http://www.ebi.ac.uk/efo/EFO_0006842
# 2    EFO_0003770         diabetic retinopathy  A chronic, pathological complication associate...          http://www.ebi.ac.uk/efo/EFO_0003770
# 3    EFO_0004593         gestational diabetes  Carbohydrate intolerance first diagnosed durin...          http://www.ebi.ac.uk/efo/EFO_0004593
# 4  MONDO_0005147     type 1 diabetes mellitus  A chronic condition characterized by minimal o...  http://purl.obolibrary.org/obo/MONDO_0005147
# 5  MONDO_0005148     type 2 diabetes mellitus  A type of diabetes mellitus that is characteri...  http://purl.obolibrary.org/obo/MONDO_0005148
```
### Step 4
```Python
score1 = get_scores(trait_id='EFO_0000400')
score2 = get_scores(trait_id='EFO_0006842')
score3 = get_scores(trait_id='EFO_0003770')
score4 = get_scores(trait_id='EFO_0004593')
score5 = get_scores(trait_id='MONDO_0005147')
score6 = get_scores(trait_id='MONDO_0005148')
diabetes_score = score1+score2+score3+score4+score5+score6
diabetes_score
# Score is running in fat mode. It has 7 DataFrames with hierarchical dependencies.
# scores:186 rows
# |
#  -samples_variants: 253 rows
#   |
#    -samples_variants_cohorts: 386 rows
# |
#  -samples_training: 107 rows
#   |
#    -samples_training_cohorts: 97 rows
# |
#  -trait_efo: 195 rows
# |
#  -ancestry_distribution: 447 rows
```
### Step 5
```Python
pic=ggplot(diabetes_score.trait_efo)+geom_bar(aes(x='label'))+coord_flip()
pic.save(filename='Additional file 1.png',dpi=300)
```
## Example 2: Investigating polygenic risk scores for gestational diabetes
### Step 1
```Python
from pandaspgs import *
```
### Step 2
```Python
traits = get_traits(term='gestational diabetes')
traits.traits
#        id              label                            description                                      url                 
# 0  EFO_0004593  gestational diabetes  Carbohydrate intolerance first diagnosed durin...  http://www.ebi.ac.uk/efo/EFO_0004593
traits.traits['id'][0]
# 'EFO_0004593'
traits.traits['description'][0]
# 'Carbohydrate intolerance first diagnosed during pregnancy. [NCIT: P378]'
```
### Step 3
```Python
gd_pgs = get_scores(trait_id='EFO_0004593')
gd_pgs.scores
#       id        name                    ftp_scoring_file                   matches_publication                   trait_reported                  trait_additional            method_name            method_params  variants_number  variants_interactions variants_genomebuild weight_type date_release                      license                       publication.id                 publication.title                        publication.doi        publication.PMID  publication.journal  publication.firstauthor publication.date_publication   ftp_harmonized_scoring_files.GRCh38.positions      ftp_harmonized_scoring_files.GRCh37.positions   
# 0  PGS002256  GRS4_GDM  https://ftp.ebi.ac.uk/pub/databases/spot/pgs/s...         True          Gestational diabetes mellitus in early pregnancy       None        Genome-wide significant variants    p < 0.05           4                   0                    NR             log(OR)   2022-02-16   PGS obtained from the Catalog should be cited ...    PGP000282    An early prediction model for gestational diab...  10.1186/s13098-022-00788-y      35073990      Diabetol Metab Syndr           Wu Q                   2022-01-24           https://ftp.ebi.ac.uk/pub/databases/spot/pgs/s...  https://ftp.ebi.ac.uk/pub/databases/spot/pgs/s...
gd_pgs.scores['id'][0]
# PGS002256
gd_pgs.scores['name'][0]
# 'GRS4_GDM'
gd_pgs.scores['matches_publication'][0]
# True
gd_pgs.scores['trait_reported'][0]
# 'Gestational diabetes mellitus in early pregnancy'
gd_pgs.scores['variants_number'][0]
# 4
```
### Step 4
```Python
gd_pgs.scores['publication.id'][0]
# PGP000282
gd_pgs.scores['publication.PMID'][0]
# 35073990
gd_pgs.scores['publication.date_publication'][0]
# '2022-01-24'
gd_pgs.scores['publication.journal'][0]
# 'Diabetol Metab Syndr'
gd_pgs.scores['publication.title'][0]
# 'An early prediction model for gestational diabetes mellitus based on genetic variants and clinical characteristics in China.'
open_in_pubmed(gd_pgs.scores['publication.PMID'][0])
```
### Step 5
```Python
gd_pgs.samples_variants
#    sample_number  sample_cases  sample_controls  sample_percent_male sample_age phenotyping_free followup_time ancestry_broad ancestry_free ancestry_country ancestry_additional source_GWAS_catalog source_PMID source_DOI cohorts_additional  id  score_id   followup_time.estimate_type  followup_time.estimate  followup_time.interval.type  followup_time.interval.lower  followup_time.interval.upper  followup_time.variability_type  followup_time.variability  followup_time.unit
# 0       671            332            339                0.0            None          None            None       East Asian       Chinese         China              None                None            None       None           None          0  PGS002256             NaN                        NaN                       NaN                           NaN                           NaN                            NaN                          NaN                     NaN              
gd_pgs.samples_variants['sample_number'][0]
# 671
gd_pgs.samples_variants['ancestry_broad'][0]
# 'East Asian'
```
### Step 6
```Python
gd_file = read_scoring_file('PGS002256')
gd_file
#       rsID    effect_allele other_allele  effect_weight hm_source   hm_rsID    hm_chr   hm_pos   hm_inferOtherAllele
# 0  rs10830963        G            C           1.327       ENSEMBL  rs10830963    11    92708710         NaN         
# 1   rs1436953        T            C           1.292       ENSEMBL   rs1436953    15    62414014         NaN         
# 2   rs7172432        G            A           1.283       ENSEMBL   rs7172432    15    62396389         NaN         
# 3  rs16955379        C            T           1.220       ENSEMBL  rs16955379    16    81489373         NaN 
```
### Step 7
```Python
snp1=gd_file[['rsID','effect_allele','other_allele','effect_weight']].loc[0]
snp1
# rsID             rs10830963
# effect_allele             G
# other_allele              C
# effect_weight         1.327
# Name: 0, dtype: object  
from pandaspgs.file_operation import genotype_weighted_score
genotype_weighted_score(snp1)
#   rs10830963_genotype  rs10830963_weighted_score
# 0          G/G                   2.654          
# 1          G/C                   1.327          
# 2          C/C                   0.000 
```
### Step 8
```Python
df_list = [] 
for x in range(len(gd_file)):
    snp_x = gd_file[['rsID','effect_allele','other_allele','effect_weight']].loc[x]
    df_x = genotype_weighted_score(snp_x)
    df_x['key'] = 1
    df_list.append(df_x)
from functools import reduce
combination_df = reduce(lambda x, y: x.merge(y,on='key'), df_list)
del combination_df['key']
combination_df
#    rs10830963_genotype  rs10830963_weighted_score rs1436953_genotype  rs1436953_weighted_score rs7172432_genotype  rs7172432_weighted_score rs16955379_genotype  rs16955379_weighted_score
# 0           G/G                   2.654                   T/T                   2.584                  G/G                   2.566                   C/C                   2.44           
# 1           G/G                   2.654                   T/T                   2.584                  G/G                   2.566                   C/T                   1.22           
# 2           G/G                   2.654                   T/T                   2.584                  G/G                   2.566                   T/T                   0.00           
# 3           G/G                   2.654                   T/T                   2.584                  G/A                   1.283                   C/C                   2.44           
# 4           G/G                   2.654                   T/T                   2.584                  G/A                   1.283                   C/T                   1.22           
# ..                 ...                        ...                ...                       ...                ...                       ...                 ...                        ...
# 76          C/C                   0.000                   C/C                   0.000                  G/A                   1.283                   C/T                   1.22           
# 77          C/C                   0.000                   C/C                   0.000                  G/A                   1.283                   T/T                   0.00           
# 78          C/C                   0.000                   C/C                   0.000                  A/A                   0.000                   C/C                   2.44           
# 79          C/C                   0.000                   C/C                   0.000                  A/A                   0.000                   C/T                   1.22           
# 80          C/C                   0.000                   C/C                   0.000                  A/A                   0.000                   T/T                   0.00           
# [81 rows x 8 columns]
```
### Step 9
```Python
combination_df['genotypes']=combination_df['rs10830963_genotype']+"-"+combination_df['rs1436953_genotype']+"-"+combination_df['rs7172432_genotype']+"-"+combination_df['rs16955379_genotype']
combination_df['scores']= combination_df['rs10830963_weighted_score']+combination_df['rs1436953_weighted_score']+combination_df['rs7172432_weighted_score']+combination_df['rs16955379_weighted_score']
combination_df[['genotypes','scores']].sort_values(by='scores', ascending=False)
#       genotypes      scores
# 0   G/G-T/T-G/G-C/C  10.244
# 1   G/G-T/T-G/G-C/T   9.024
# 3   G/G-T/T-G/A-C/C   8.961
# 9   G/G-T/C-G/G-C/C   8.952
# 27  G/C-T/T-G/G-C/C   8.917
# ..              ...     ...
# 53  G/C-C/C-A/A-T/T   1.327
# 71  C/C-T/C-A/A-T/T   1.292
# 77  C/C-C/C-G/A-T/T   1.283
# 79  C/C-C/C-A/A-C/T   1.220
# 80  C/C-C/C-A/A-T/T   0.000
# 
# [81 rows x 2 columns]
```
