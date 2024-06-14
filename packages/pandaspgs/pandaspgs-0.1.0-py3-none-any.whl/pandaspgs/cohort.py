from pandas import DataFrame, json_normalize, set_option
from pandas import concat

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class Cohort:
    """
     An object that stores data of type Cohort. To understand the significance of each column of the DataFrame. Please visit "Cohort_extended" in [PGS Catalog Documentation](https://www.pgscatalog.org/rest/) for details.

    Attributes:
        raw_data: list. Convert from obtained JSON data
        cohorts: DataFrame. It only exists if the parameter mode of constructor is Fat.
        associated_pgs_ids: DataFrame. It only exists if the parameter mode of constructor is Fat.
        mode: Fat or Thin. Specifies the mode of the returned object.

    ```Python
    from pandaspgs.get_cohort import get_cohorts

    ch = get_cohorts(cohort_symbol='ABCFS')
    ch
    ch.raw_data
    ch.mode
    ch.cohorts
    ch.associated_pgs_ids
    ```
    Subset object s by either identifier or position
    ```Python
    all_df = get_cohorts()
    all_df[0].cohorts
    all_df[0:3].cohorts
    all_df['100-plus'].cohorts
    all_df[('100-plus','23andMe','2SISTER')].cohorts
    ```
    Objects can be manipulated like sets in the mathematical sense.
    ```Python
    one = get_cohorts(cohort_symbol='100-plus')
    two = get_cohorts(cohort_symbol='23andMe')
    three = get_cohorts(cohort_symbol='2SISTER')
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
            self.cohorts = DataFrame(
                columns=['name_short', 'name_full', 'name_others'])
            self.associated_pgs_ids = DataFrame(
                columns=['name_short', 'associated_pgs_id', 'stage'])
            return
        datas = json_normalize(data=data, max_level=1).drop(columns=['name_short', 'name_full', 'name_others'])
        datas['associated_pgs_ids.development'] = datas['associated_pgs_ids.development'].map(lambda x: x == [])
        datas['associated_pgs_ids.evaluation'] = datas['associated_pgs_ids.evaluation'].map(lambda x: x == [])
        self.cohorts = json_normalize(data=data, max_level=1).drop(
            columns=['associated_pgs_ids.development', 'associated_pgs_ids.evaluation'])
        if not datas['associated_pgs_ids.development'].all() or not datas['associated_pgs_ids.evaluation'].all():
            dva = json_normalize(data=data, record_path=['associated_pgs_ids', 'development'], meta=['name_short'])
            eva = json_normalize(data=data, record_path=['associated_pgs_ids', 'evaluation'], meta=['name_short'])
            dva['stage'] = 'development'
            eva['stage'] = 'evaluation'
            self.associated_pgs_ids = concat([dva, eva])
            self.associated_pgs_ids.columns = ['associated_pgs_id', 'name_short', 'stage']
        else:
            self.associated_pgs_ids = DataFrame(
                 columns=['associated_pgs_id', 'name_short', 'stage'])

        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("Cohort is running in fat mode. It has 2 DataFrames with hierarchical dependencies.\n"
                    "cohorts: %d rows\n|\n -associated_pgs_ids: %d rows" % (len(self.cohorts),
                                                                                 len(self.associated_pgs_ids)))
        if self.mode == 'Thin':
            return ('Cohort is running in thin mode. It has 1 list that contains the raw data.\nraw_data: a list '
                    'of size %d.') % len(self.raw_data)

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
            raw_data_dict[j['name_short']] = j
        sub_set = []
        for i in arr:
            if isinstance(i, str):
                sub_set.append(raw_data_dict[i])
            elif isinstance(i, int):
                sub_set.append(raw_data[i])
            else:
                raise TypeError('Invalid item type: {}'.format(type(i)))
        return Cohort(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return Cohort(self.raw_data + other.raw_data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __sub__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['name_short'])
                self_dict[i['name_short']] = i
            for j in other.raw_data:
                other_key_set.add(j['name_short'])
            sub_key = self_key_set - other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return Cohort(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __and__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['name_short'])
                self_dict[i['name_short']] = i
            for j in other.raw_data:
                other_key_set.add(j['name_short'])
            sub_key = self_key_set & other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return Cohort(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __or__(self, other):
        if self.mode == other.mode:
            and_dict = {}
            for i in self.raw_data:
                and_dict[i['name_short']] = i
            for j in other.raw_data:
                and_dict[j['name_short']] = j
            data = list(and_dict.values())
            return Cohort(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __xor__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            and_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['name_short'])
                and_dict[i['name_short']] = i
            for j in other.raw_data:
                other_key_set.add(j['name_short'])
                and_dict[j['name_short']] = j
            sub_key = self_key_set ^ other_key_set
            data = []
            for k in sub_key:
                data.append(and_dict[k])
            return Cohort(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)
