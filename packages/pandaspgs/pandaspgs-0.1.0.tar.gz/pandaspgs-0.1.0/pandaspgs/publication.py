from pandas import DataFrame, json_normalize, set_option
from pandas import concat

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class Publication:
    """
       An object that stores data of type Publication. To understand the significance of each column of the DataFrame. Please visit "Publication" in [PGS Catalog Documentation](https://www.pgscatalog.org/rest/) for details.

       Attributes:
            raw_data: list. Convert from obtained JSON data
            publications: DataFrame. It only exists if the parameter mode of constructor is Fat.
            associated_pgs_ids: DataFrame. It only exists if the parameter mode of constructor is Fat.
            mode: Fat or Thin. Specifies the mode of the returned object.

       ```python
       from pandaspgs.get_publication import get_publications

       ch = get_publications(pgs_id='PGS000001')
       ch
       ch.raw_data
       ch.mode
       ch.publications
       ch.associated_pgs_ids
       ```
       Subset object s by either identifier or position
       ```python
       all_df = get_publications()
       all_df[0].publications
       all_df[0:3].publications
       all_df['PGP000001'].publications
       all_df[('PGP000001','PGP000002','PGP000003')].publications
       ```
       Objects can be manipulated like sets in the mathematical sense.
       ```python
       one = get_cohorts(ppm_id='PPM000001')
       two = get_cohorts(ppm_id='PPM000002')
       three = get_cohorts(ppm_id='PPM000003')
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
            self.publications = DataFrame(
                columns=['id', 'title', 'doi', 'PMID', 'journal', 'firstauthor', 'date_publication', 'date_release'
                    , 'authors'])
            self.associated_pgs_ids = DataFrame(
                columns=['publication_id', 'associated_pgs_id', 'stage'])
            return
        datas = json_normalize(data=data, max_level=1).drop(columns=['id', 'title', 'doi', 'PMID', 'journal'
            , 'firstauthor', 'date_publication', 'date_release', 'authors'])
        datas['associated_pgs_ids.development'] = datas['associated_pgs_ids.development'].map(lambda x: x == [])
        datas['associated_pgs_ids.evaluation'] = datas['associated_pgs_ids.evaluation'].map(lambda x: x == [])
        self.publications = json_normalize(data=data, max_level=1).drop(
            columns=['associated_pgs_ids.development', 'associated_pgs_ids.evaluation'])
        if not datas['associated_pgs_ids.development'].all() or not datas['associated_pgs_ids.evaluation'].all():
            dva = json_normalize(data=data, record_path=['associated_pgs_ids', 'development'], meta=['id'])
            eva = json_normalize(data=data, record_path=['associated_pgs_ids', 'evaluation'], meta=['id'])
            dva['stage'] = 'development'
            eva['stage'] = 'evaluation'
            self.associated_pgs_ids = concat([dva, eva])
            self.associated_pgs_ids.columns = ['associated_pgs_id', 'publication_id', 'stage']
        else:
            self.associated_pgs_ids = DataFrame(
                columns=['associated_pgs_id', 'publication_id', 'stage'])

        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("Publication is running in fat mode. It has 2 DataFrames with hierarchical dependencies.\n"
                    "publications: %d rows\n|\n -associated_pgs_ids: %d rows" % (len(self.publications),
                                                                                 len(self.associated_pgs_ids)))
        if self.mode == 'Thin':
            return ('Publication is running in thin mode. It has 1 list that contains the raw data.\nraw_data: a list '
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
            raw_data_dict[j['id']] = j
        sub_set = []
        for i in arr:
            if isinstance(i, str):
                sub_set.append(raw_data_dict[i])
            elif isinstance(i, int):
                sub_set.append(raw_data[i])
            else:
                raise TypeError('Invalid item type: {}'.format(type(i)))
        return Publication(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return Publication(self.raw_data + other.raw_data, self.mode)
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
            return Publication(data, self.mode)
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
            return Publication(data, self.mode)
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
            return Publication(data, self.mode)
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
            return Publication(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)
