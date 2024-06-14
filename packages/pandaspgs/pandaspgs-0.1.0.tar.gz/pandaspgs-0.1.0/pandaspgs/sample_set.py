from pandas import DataFrame, json_normalize, set_option, Series

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)
import numpy


class SampleSet:
    """
       An object that stores data of type SampleSet. To understand the significance of each column of the DataFrame. Please visit "SampleSet" in [PGS Catalog Documentation](https://www.pgscatalog.org/rest/) for details.

       Attributes:
            raw_data: list. Convert from obtained JSON data
            sample_sets: DataFrame. It only exists if the parameter mode of constructor is Fat.
            samples: DataFrame. It only exists if the parameter mode of constructor is Fat.
            cohorts: DataFrame. It only exists if the parameter mode of constructor is Fat.
            mode: Fat or Thin. Specifies the mode of the returned object.

       ```python
       from pandaspgs.get_sample_set import get_sample_sets

       ch = get_sample_sets(pss_id='PSS000001')
       ch
       ch.raw_data
       ch.mode
       ch.sample_sets
       ch.samples
       ch.cohorts
       ```
       Subset object s by either identifier or position
       ```python
       all_df = get_sample_sets()
       all_df[0].sample_sets
       all_df[0:3].sample_sets
       all_df['PSS000001'].sample_sets
       all_df[('PSS000001','PSS000002','PSS000003')].sample_sets
       ```
       Objects can be manipulated like sets in the mathematical sense.
       ```python
       one = get_sample_sets(pss_id='PSS000001')
       two = get_sample_sets(pss_id='PSS000002')
       three = get_sample_sets(pss_id='PSS000003')
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
            self.sample_sets = DataFrame(
                columns=['id'])
            self.samples = DataFrame(
                columns=['id', 'sample_set_id', 'sample_number', 'sample_cases', 'sample_controls',
                         'sample_percent_male', 'sample_age.estimate_type', 'sample_age.estimate',
                         'sample_age.interval.type', 'sample_age.interval.lower', 'sample_age.interval.upper',
                         'sample_age.variability_type', 'sample_age.variability', 'sample_age.unit',
                         'phenotyping_free', 'followup_time.estimate_type', 'followup_time.estimate',
                         'followup_time.interval.type', 'followup_time.interval.lower', 'followup_time.interval.upper',
                         'followup_time.variability_type', 'followup_time.variability', 'followup_time.unit',
                         'ancestry_broad', 'ancestry_free', 'ancestry_country', 'ancestry_additional',
                         'source_GWAS_catalog', 'source_PMID', 'source_DOI', 'cohorts_additional'])
            self.cohorts = DataFrame(columns=['sample_set_id', 'sample_id', 'name_short', 'name_full', 'name_others'])
            return
        datas = json_normalize(data=data, max_level=1)
        datas['samples'] = datas['samples'].map(lambda x: x == [])
        self.sample_sets = json_normalize(data=data, max_level=1).drop(
            columns=['samples'])
        if not datas['samples'].all():
            self.samples = json_normalize(data=data, record_path=['samples'], meta=['id'])
            self.samples['sample_set_id'] = self.samples['id']
            self.samples['id'] = Series(data=range(0, len(self.samples)))
            cohort = self.samples[['id', 'sample_set_id', 'cohorts']].copy()
            self.samples = self.samples.drop(columns=['cohorts'])
            cohort['sample_id'] = cohort['id']
            cohort['cohorts'] = cohort['cohorts'].apply(lambda x: x if len(x) > 0 else numpy.nan)
            cohort = cohort.dropna()
            cohort = cohort.explode('cohorts')
            cohort[['name_short', 'name_full', 'name_others']] = cohort['cohorts'].apply(
                lambda x: Series(data=[x['name_short'], x['name_full'], x['name_others']]))
            cohort = cohort.drop(columns=['id', 'cohorts'])
            self.cohorts = cohort

        else:
            self.samples = DataFrame(
                columns=['id', 'sample_set_id', 'sample_number', 'sample_cases', 'sample_controls',
                         'sample_percent_male', 'sample_age.estimate_type', 'sample_age.estimate',
                         'sample_age.interval.type', 'sample_age.interval.lower', 'sample_age.interval.upper',
                         'sample_age.variability_type', 'sample_age.variability', 'sample_age.unit',
                         'phenotyping_free', 'followup_time.estimate_type', 'followup_time.estimate',
                         'followup_time.interval.type', 'followup_time.interval.lower', 'followup_time.interval.upper',
                         'followup_time.variability_type', 'followup_time.variability', 'followup_time.unit',
                         'ancestry_broad', 'ancestry_free', 'ancestry_country', 'ancestry_additional',
                         'source_GWAS_catalog', 'source_PMID', 'source_DOI', 'cohorts_additional'])
            self.cohorts = DataFrame(columns=['sample_set_id', 'sample_id', 'name_short', 'name_full', 'name_others'])
        if 'publication' in self.sample_sets.columns:
            self.sample_sets = self.sample_sets.drop(columns=['pubication'])
            self.sample_sets = self.sample_sets.reindex(
                columns=self.sample_sets.columns.tolist() + ['publication.title',
                                                             'publication.doi', 'publication.PMID',
                                                             'publication.journal',
                                                             'publication.firstauthor',
                                                             'publication.date_publication'])
        if 'sample_age' in self.samples.columns:
            self.samples = self.samples.drop(columns=['sample_age'])
            if 'sample_age.estimate_type' not in self.samples.columns:
                self.samples = self.samples.reindex(
                    columns=self.samples.columns.tolist() + ['sample_age.estimate_type', 'sample_age.estimate',
                                                             'sample_age.interval.type', 'sample_age.interval.lower',
                                                             'sample_age.interval.upper',
                                                             'sample_age.variability_type', 'sample_age.variability',
                                                             'sample_age.unit']
            )
        if 'followup_time' in self.samples.columns:
            self.samples = self.samples.drop(columns=['followup_time'])
            if 'followup_time.estimate_type' not in self.samples.columns:
                self.samples = self.samples.reindex(
                    columns=self.samples.columns.tolist() + ['followup_time.estimate_type', 'followup_time.estimate',
                                                             'followup_time.interval.type',
                                                             'followup_time.interval.lower',
                                                             'followup_time.interval.upper',
                                                             'followup_time.variability_type',
                                                             'followup_time.variability',
                                                             'followup_time.unit'])
        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("SampleSet is running in fat mode. It has 3 DataFrames with hierarchical dependencies.\n"
                    "sample_sets:"
                    "%d rows\n|\n -samples: %d rows\n  |\n   -cohorts: %d rows" % (
                        len(self.sample_sets), len(self.samples), len(self.cohorts)))
        if self.mode == 'Thin':
            return ('SampleSet is running in thin mode. It has 1 list that contains the raw data.\nraw_data: a list of '
                    'size %d.' % len(self.raw_data))

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
        return SampleSet(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return SampleSet(self.raw_data + other.raw_data, self.mode)
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
            return SampleSet(data, self.mode)
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
            return SampleSet(data, self.mode)
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
            return SampleSet(data, self.mode)
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
            return SampleSet(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)
