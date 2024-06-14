from pandas import DataFrame, json_normalize, set_option, Series

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)
import numpy


class Score:
    """
       An object that stores data of type Score. To understand the significance of each column of the DataFrame. Please visit "Score" in [PGS Catalog Documentation](https://www.pgscatalog.org/rest/) for details.

       Attributes:
            raw_data: list. Convert from obtained JSON data
            scores: DataFrame. It only exists if the parameter mode of constructor is Fat.
            samples_variants: DataFrame. It only exists if the parameter mode of constructor is Fat.
            samples_variants_cohorts: DataFrame. It only exists if the parameter mode of constructor is Fat.
            trait_efo: DataFrame. It only exists if the parameter mode of constructor is Fat.
            samples_training: DataFrame. It only exists if the parameter mode of constructor is Fat.
            samples_training_cohorts: DataFrame. It only exists if the parameter mode of constructor is Fat.
            ancestry_distribution: DataFrame. It only exists if the parameter mode of constructor is Fat.
            mode: Fat or Thin. Specifies the mode of the returned object.

       ```python
       from pandaspgs.get_score import get_scores

       ch = get_scores(pgs_id='PGS000001')
       ch
       ch.raw_data
       ch.mode
       ch.scores
       ch.samples_variants
       ch.samples_variants_cohorts
       ch.trait_efo
       ch.samples_training
       ch.samples_training_cohorts
       ch.ancestry_distribution
       ```
       Subset object s by either identifier or position
       ```python
       all_df = get_scores()
       all_df[0].scores
       all_df[0:3].scores
       all_df['PGS000001'].scores
       all_df[('PGS000001','PGS000002','PGS000003')].scores
       ```
       Objects can be manipulated like sets in the mathematical sense.
       ```python
       one = get_scores(pgs_id='PGS000001')
       two = get_scores(pgs_id='PGS000002')
       three = get_scores(pgs_id='PGS000003')
       one_and_two = one+two
       two_and_three = two+three
       only_one = one_and_two - two_and_three
       only_two = one_and_two & two_and_three
       one_and_two_and_three = one_and_two | two_and_three
       one_and_three = one_and_two ^ two_and_three
       ```
       """

    def __init__(self, data: list = [], mode: str = "Fat"):
        """
        Args:
            data: Raw JSON data.
            mode: Fat or Thin. Specifies the mode of the object.
        """
        if data is None:
            data = []
        if mode not in ['Thin', "Fat"]:
            raise Exception("Mode must be Fat or Thin")
        self.raw_data = data
        self.mode = mode
        if mode == "Thin":
            return
        if data is None or len(data) == 0:
            self.scores = DataFrame(
                columns=['id'
                    , 'name'
                    , 'ftp_scoring_file'
                    , 'ftp_harmonized_scoring_files.GRCh37.positions'
                    , 'ftp_harmonized_scoring_files.GRCh38.positions'
                    , 'publication.id'
                    , 'publication.title'
                    , 'publication.doi'
                    , 'publication.PMID'
                    , 'publication.journal'
                    , 'publication.firstauthor'
                    , 'publication.date_publication'
                    , 'matches_publication'
                    , 'trait_reported'
                    , 'trait_additional'
                    , 'method_name'
                    , 'method_params'
                    , 'variants_number'
                    , 'variants_interactions'
                    , 'variants_genomebuild'
                    , 'weight_type'
                    , 'date_release'
                    , 'license'
                         ])
            self.samples_variants = DataFrame(
                columns=['id'
                    , 'score_id'
                    , 'sample_number'
                    , 'sample_cases'
                    , 'sample_controls'
                    , 'sample_percent_male'
                    , 'sample_age.estimate_type'
                    , 'sample_age.estimate'
                    , 'sample_age.interval.type'
                    , 'sample_age.interval.lower'
                    , 'sample_age.interval.upper'
                    , 'sample_age.variability_type'
                    , 'sample_age.variability'
                    , 'sample_age.unit'
                    , 'phenotyping_free'
                    , 'followup_time.estimate_type'
                    , 'followup_time.estimate'
                    , 'followup_time.interval.type'
                    , 'followup_time.interval.lower'
                    , 'followup_time.interval.upper'
                    , 'followup_time.variability_type'
                    , 'followup_time.variability'
                    , 'followup_time.unit'
                    , 'ancestry_broad'
                    , 'ancestry_free'
                    , 'ancestry_country'
                    , 'ancestry_additional'
                    , 'source_GWAS_catalog'
                    , 'source_PMID'
                    , 'source_DOI'
                    , 'cohorts_additional'
                         ])
            self.samples_variants_cohorts = DataFrame(
                columns=['score_id'
                    , 'sample_id'
                    , 'name_short'
                    , 'name_full'
                    , 'name_others'])
            self.trait_efo = DataFrame(
                columns=['score_id'
                    , 'id'
                    , 'label'
                    , 'description'
                    , 'url'
                         ])
            self.samples_training = DataFrame(
                columns=['id'
                    , 'score_id'
                    , 'sample_number'
                    , 'sample_cases'
                    , 'sample_controls'
                    , 'sample_percent_male'
                    , 'sample_age.estimate_type'
                    , 'sample_age.estimate'
                    , 'sample_age.interval.type'
                    , 'sample_age.interval.lower'
                    , 'sample_age.interval.upper'
                    , 'sample_age.variability_type'
                    , 'sample_age.variability'
                    , 'sample_age.unit'
                    , 'phenotyping_free'
                    , 'followup_time.estimate_type'
                    , 'followup_time.estimate'
                    , 'followup_time.interval.type'
                    , 'followup_time.interval.lower'
                    , 'followup_time.interval.upper'
                    , 'followup_time.variability_type'
                    , 'followup_time.variability'
                    , 'followup_time.unit'
                    , 'ancestry_broad'
                    , 'ancestry_free'
                    , 'ancestry_country'
                    , 'ancestry_additional'
                    , 'source_GWAS_catalog'
                    , 'source_PMID'
                    , 'source_DOI'
                    , 'cohorts_additional'
                         ])
            self.samples_training_cohorts = DataFrame(
                columns=['score_id'
                    , 'sample_id'
                    , 'name_short'
                    , 'name_full'
                    , 'name_others'
                         ])
            self.ancestry_distribution = DataFrame(
                columns=['score_id'
                    , 'stage'
                    , 'dist'
                    , 'count'
                    , 'multi'])
            return
        datas = json_normalize(data=data, max_level=1)
        datas['samples_variants'] = datas['samples_variants'].map(lambda x: x == [])
        datas['samples_training'] = datas['samples_training'].map(lambda x: x == [])
        datas['trait_efo'] = datas['trait_efo'].map(lambda x: x == [])

        self.scores = json_normalize(data=data, max_level=1).drop(
            columns=['samples_variants', 'samples_training',
                     'trait_efo'])
        ancestry_distribution_to_drop = ['ancestry_distribution.eval', 'ancestry_distribution.gwas',
                                         'ancestry_distribution.dev']
        for to_drop in ancestry_distribution_to_drop:
            if to_drop in self.scores.columns:
                self.scores = self.scores.drop(columns=[to_drop])
        self.scores['ftp_harmonized_scoring_files.GRCh38.positions'] = self.scores[
            'ftp_harmonized_scoring_files.GRCh38'].map(
            lambda x: x['positions'])
        self.scores['ftp_harmonized_scoring_files.GRCh37.positions'] = self.scores[
            'ftp_harmonized_scoring_files.GRCh37'].map(
            lambda x: x['positions'])
        self.scores = self.scores.drop(
            columns=['ftp_harmonized_scoring_files.GRCh38', 'ftp_harmonized_scoring_files.GRCh37'])
        if not datas['samples_variants'].all():
            self.samples_variants = json_normalize(data=data, record_path=['samples_variants'], meta=['id'])
            self.samples_variants['score_id'] = self.samples_variants['id']
            self.samples_variants['id'] = Series(data=range(0, len(self.samples_variants)))
            cohort = self.samples_variants[['id', 'score_id', 'cohorts']].copy()
            self.samples_variants = self.samples_variants.drop(columns=['cohorts'])
            cohort['sample_id'] = cohort['id']
            cohort['cohorts'] = cohort['cohorts'].apply(lambda x: x if len(x) > 0 else numpy.nan)
            cohort = cohort.dropna()
            cohort = cohort.explode('cohorts')
            if len(cohort) == 0:
                self.samples_variants_cohorts = DataFrame(
                    columns=['score_id'
                        , 'sample_id'
                        , 'name_short'
                        , 'name_full'
                        , 'name_others'])
            else:
                cohort[['name_short', 'name_full', 'name_others']] = cohort['cohorts'].apply(
                    lambda x: Series(data=[x['name_short'], x['name_full'], x['name_others']]))
                cohort = cohort.drop(columns=['id', 'cohorts'])
                self.samples_variants_cohorts = cohort

        else:
            self.samples_variants = DataFrame(
                columns=['id'
                    , 'score_id'
                    , 'sample_number'
                    , 'sample_cases'
                    , 'sample_controls'
                    , 'sample_percent_male'
                    , 'sample_age.estimate_type'
                    , 'sample_age.estimate'
                    , 'sample_age.interval.type'
                    , 'sample_age.interval.lower'
                    , 'sample_age.interval.upper'
                    , 'sample_age.variability_type'
                    , 'sample_age.variability'
                    , 'sample_age.unit'
                    , 'phenotyping_free'
                    , 'followup_time.estimate_type'
                    , 'followup_time.estimate'
                    , 'followup_time.interval.type'
                    , 'followup_time.interval.lower'
                    , 'followup_time.interval.upper'
                    , 'followup_time.variability_type'
                    , 'followup_time.variability'
                    , 'followup_time.unit'
                    , 'ancestry_broad'
                    , 'ancestry_free'
                    , 'ancestry_country'
                    , 'ancestry_additional'
                    , 'source_GWAS_catalog'
                    , 'source_PMID'
                    , 'source_DOI'
                    , 'cohorts_additional'
                         ])
            self.samples_variants_cohorts = DataFrame(
                columns=['score_id'
                    , 'sample_id'
                    , 'name_short'
                    , 'name_full'
                    , 'name_others'])
        if not datas['samples_training'].all():
            self.samples_training = json_normalize(data=data, record_path=['samples_training'], meta=['id'])
            self.samples_training['score_id'] = self.samples_training['id']
            self.samples_training['id'] = Series(data=range(0, len(self.samples_training)))
            cohort = self.samples_training[['id', 'score_id', 'cohorts']].copy()
            self.samples_training = self.samples_training.drop(columns=['cohorts'])
            cohort['sample_id'] = cohort['id']
            cohort['cohorts'] = cohort['cohorts'].apply(lambda x: x if len(x) > 0 else numpy.nan)
            cohort = cohort.dropna()
            cohort = cohort.explode('cohorts')
            if len(cohort) == 0:
                self.samples_training_cohorts = DataFrame(
                    columns=['score_id'
                        , 'sample_id'
                        , 'name_short'
                        , 'name_full'
                        , 'name_others'])
            else:
                cohort[['name_short', 'name_full', 'name_others']] = cohort['cohorts'].apply(
                    lambda x: Series(data=[x['name_short'], x['name_full'], x['name_others']]))
                cohort = cohort.drop(columns=['id', 'cohorts'])
                self.samples_training_cohorts = cohort

        else:
            self.samples_training = DataFrame(
                columns=['id'
                    , 'score_id'
                    , 'sample_number'
                    , 'sample_cases'
                    , 'sample_controls'
                    , 'sample_percent_male'
                    , 'sample_age.estimate_type'
                    , 'sample_age.estimate'
                    , 'sample_age.interval.type'
                    , 'sample_age.interval.lower'
                    , 'sample_age.interval.upper'
                    , 'sample_age.variability_type'
                    , 'sample_age.variability'
                    , 'sample_age.unit'
                    , 'phenotyping_free'
                    , 'followup_time.estimate_type'
                    , 'followup_time.estimate'
                    , 'followup_time.interval.type'
                    , 'followup_time.interval.lower'
                    , 'followup_time.interval.upper'
                    , 'followup_time.variability_type'
                    , 'followup_time.variability'
                    , 'followup_time.unit'
                    , 'ancestry_broad'
                    , 'ancestry_free'
                    , 'ancestry_country'
                    , 'ancestry_additional'
                    , 'source_GWAS_catalog'
                    , 'source_PMID'
                    , 'source_DOI'
                    , 'cohorts_additional'
                         ])
            self.samples_training_cohorts = DataFrame(
                columns=['score_id'
                    , 'sample_id'
                    , 'name_short'
                    , 'name_full'
                    , 'name_others'
                         ])
        if not datas['trait_efo'].all():
            self.trait_efo = json_normalize(data=data, record_path=['trait_efo'], meta='id', meta_prefix='score_')

        else:
            self.trait_efo = DataFrame(
                columns=['score_id'
                    , 'id'
                    , 'label'
                    , 'description'
                    , 'url'])
        raw_ancestry_distribution = json_normalize(data=data, max_level=0)
        raw_ancestry_distribution['ancestry_distribution'] = raw_ancestry_distribution['ancestry_distribution'].map(
            lambda x: [{y: x[y]} for y in x])
        raw_ancestry_distribution = raw_ancestry_distribution.explode('ancestry_distribution')
        raw_ancestry_distribution['stage'] = raw_ancestry_distribution['ancestry_distribution'].map(
            lambda x: list(x.keys())[0])
        raw_ancestry_distribution['ancestry_distribution'] = raw_ancestry_distribution['ancestry_distribution'].map(
            lambda x: list(x.values())[0])
        raw_ancestry_distribution['dist'] = raw_ancestry_distribution['ancestry_distribution'].map(
            lambda x: x['dist'])
        raw_ancestry_distribution['count'] = raw_ancestry_distribution['ancestry_distribution'].map(
            lambda x: x['count'])
        raw_ancestry_distribution['multi'] = raw_ancestry_distribution['ancestry_distribution'].map(
            lambda x: x['multi'] if 'multi' in x else None)
        raw_ancestry_distribution['score_id'] = raw_ancestry_distribution['id']
        self.ancestry_distribution = raw_ancestry_distribution[
            ['score_id', 'stage', 'dist', 'count', 'multi']].copy().reset_index(drop=True)

        if 'publication' in self.scores.columns:
            self.scores = self.scores.drop(columns=['pubication'])
            self.scores = self.scores.reindex(
                columns=self.scores.columns.tolist() + ['publication.id'
                    , 'publication.title'
                    , 'publication.doi'
                    , 'publication.PMID'
                    , 'publication.journal'
                    , 'publication.firstauthor'
                    , 'publication.date_publication'])
        if 'sample_age' in self.samples_variants.columns:
            self.samples_variants = self.samples_variants.drop(columns=['sample_age'])
        if 'sample_age.interval' in self.samples_variants.columns:
            self.samples_variants = self.samples_variants.drop(columns=['sample_age.interval'])
        if 'followup_time' in self.samples_variants.columns:
            self.samples_variants = self.samples_variants.drop(columns=['followup_time'])
        if 'followup_time.interval' in self.samples_variants.columns:
            self.samples_variants = self.samples_variants.drop(columns=['followup_time.interval'])
        if 'sample_age' in self.samples_training.columns:
            self.samples_training = self.samples_training.drop(columns=['sample_age'])
        if 'sample_age.interval' in self.samples_training.columns:
            self.samples_training = self.samples_training.drop(columns=['sample_age.interval'])
        if 'followup_time' in self.samples_training.columns:
            self.samples_training = self.samples_training.drop(columns=['followup_time'])
        if 'followup_time.interval' in self.samples_training.columns:
            self.samples_training = self.samples_training.drop(columns=['followup_time.interval'])
        for miss_column in ['sample_age.estimate_type', 'sample_age.estimate', 'sample_age.interval.type',
                            'sample_age.interval.lower', 'sample_age.interval.upper', 'sample_age.variability_type',
                            'sample_age.variability', 'sample_age.unit', 'followup_time.estimate_type',
                            'followup_time.estimate', 'followup_time.interval.type', 'followup_time.interval.lower',
                            'followup_time.interval.upper', 'followup_time.variability_type',
                            'followup_time.variability', 'followup_time.unit']:
            if miss_column not in self.samples_training.columns:
                self.samples_training[miss_column] = None
            if miss_column not in self.samples_variants.columns:
                self.samples_variants[miss_column] = None
        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("Score is running in fat mode. It has 7 DataFrames with hierarchical dependencies.\n"
                    "scores:%d rows\n|\n -samples_variants: %d rows\n  |\n   -samples_variants_cohorts: %d rows\n|\n "
                    "-samples_training: %d rows"
                    "\n  |\n   -samples_training_cohorts: %d rows"
                    "\n|\n -trait_efo: %d rows"
                    "\n|\n -ancestry_distribution: %d rows" % (
                        len(self.scores), len(self.samples_variants), len(self.samples_variants_cohorts),
                        len(self.samples_training), len(self.samples_training_cohorts), len(self.trait_efo),
                        len(self.ancestry_distribution)))
        if self.mode == 'Thin':
            return ('Score is running in thin mode. It has 1 list that contains the raw data.\n raw_data: '
                    'a list of size %d.' % len(self.raw_data))

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        if isinstance(item, str) or isinstance(item, int):
            arr = [item]
        elif isinstance(item, list) or isinstance(item, tuple) or isinstance(item, range):
            arr = item
        elif isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            arr = list(range(start, stop, step))
        else:
            raise TypeError('Invalid argument type：{}'.format(type(item)))
        raw_data = self.raw_data
        raw_data_dict = {}
        for j in raw_data:
            raw_data_dict[j['id']] = j
        sub_set = []
        for i in arr:
            if isinstance(i, str):
                sub_set.append(raw_data_dict[i])
            elif isinstance(i, int):
                sub_set.append(raw_data[i])
            else:
                raise TypeError('Invalid item type: {}'.format(type(i)))
        return Score(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return Score(self.raw_data + other.raw_data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __sub__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['id'])
                self_dict[i['id']] = i
            for j in other.raw_data:
                other_key_set.add(j['id'])
            sub_key = self_key_set - other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return Score(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __and__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['id'])
                self_dict[i['id']] = i
            for j in other.raw_data:
                other_key_set.add(j['id'])
            sub_key = self_key_set & other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return Score(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __or__(self, other):
        if self.mode == other.mode:
            and_dict = {}
            for i in self.raw_data:
                and_dict[i['id']] = i
            for j in other.raw_data:
                and_dict[j['id']] = j
            data = list(and_dict.values())
            return Score(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __xor__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            and_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['id'])
                and_dict[i['id']] = i
            for j in other.raw_data:
                other_key_set.add(j['id'])
                and_dict[j['id']] = j
            sub_key = self_key_set ^ other_key_set
            data = []
            for k in sub_key:
                data.append(and_dict[k])
            return Score(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)
