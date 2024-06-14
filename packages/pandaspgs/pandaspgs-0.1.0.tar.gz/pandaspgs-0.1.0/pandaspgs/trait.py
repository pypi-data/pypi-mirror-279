from pandas import DataFrame, json_normalize, set_option

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class Trait:
    """
       An object that stores data of type Trait. To understand the significance of each column of the DataFrame. Please visit "EFOTrait_Ontology" in [PGS Catalog Documentation](https://www.pgscatalog.org/rest/) for details.

       Attributes:
            raw_data: list. Convert from obtained JSON data
            traits : DataFrame. It only exists if the parameter mode of constructor is Fat.
            trait_categories: DataFrame. It only exists if the parameter mode of constructor is Fat.
            trait_synonyms: DataFrame. It only exists if the parameter mode of constructor is Fat.
            trait_mapped_terms: DataFrame. It only exists if the parameter mode of constructor is Fat.
            associated_pgs_ids: DataFrame. It only exists if the parameter mode of constructor is Fat.
            child_associated_pgs_ids: DataFrame. It only exists if the parameter mode of constructor is Fat.
            mode: Fat or Thin. Specifies the mode of the returned object.

       ```python
       from pandaspgs.get_trait import get_traits

       ch = get_traits(trait_id='EFO_0004214')
       ch
       ch.raw_data
       ch.mode
       ch.traits
       ch.trait_categories
       ch.trait_synonyms
       ch.trait_mapped_terms
       ch.associated_pgs_ids
       ch.child_associated_pgs_ids
       ```
       Subset object s by either identifier or position
       ```python
       all_df = get_traits()
       all_df[0].traits
       all_df[0:3].traits
       all_df['EFO_0004214'].traits
       all_df[('EFO_0004214','HP_0002027','HP_0011458')].traits
       ```
       Objects can be manipulated like sets in the mathematical sense.
       ```python
       one = get_scores(trait_id='EFO_0004214')
       two = get_scores(trait_id='HP_0002027')
       three = get_scores(trait_id='HP_0011458')
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
            self.traits = DataFrame(
                columns=['id', 'label', 'description', 'url'])
            self.trait_categories = DataFrame(
                columns=['trait _id', 'trait_category'])
            self.trait_synonyms = DataFrame(columns=['trait_id', 'trait_synonym'])
            self.trait_mapped_terms = DataFrame(columns=['trait_id', 'trait_mapped_term'])
            self.associated_pgs_ids = DataFrame(columns=['trait_id', 'associated_pgs_id'])
            self.child_associated_pgs_ids = DataFrame(columns=['trait_id', 'child_associated_pgs_id'])
            return
        datas = json_normalize(data=data, max_level=1).drop(columns=['id', 'label', 'description', 'url'])
        datas['trait_categories'] = datas['trait_categories'].map(lambda x: x == [])
        datas['trait_synonyms'] = datas['trait_synonyms'].map(lambda x: x == [])
        datas['trait_mapped_terms'] = datas['trait_mapped_terms'].map(lambda x: x == [])
        datas['associated_pgs_ids'] = datas['associated_pgs_ids'].map(lambda x: x == [])
        datas['child_associated_pgs_ids'] = datas['child_associated_pgs_ids'].map(lambda x: x == [])
        self.traits = json_normalize(data=data, max_level=1).drop(
            columns=['trait_categories', 'trait_synonyms', 'trait_mapped_terms',
                     'associated_pgs_ids', 'child_associated_pgs_ids'])
        if not datas['trait_categories'].all():
            self.trait_categories = json_normalize(data=data, record_path=['trait_categories'], meta=['id'])
            self.trait_categories.columns = ['trait_category', 'trait_id']
        else:
            self.trait_categories = DataFrame(
                columns=['trait _id', 'trait_category'])
        if not datas['trait_synonyms'].all():
            self.trait_synonyms = json_normalize(data=data, record_path=['trait_synonyms'], meta=['id'])
            self.trait_synonyms.columns = ['trait_synonym', 'trait_id']
        else:
            self.trait_synonyms = DataFrame(columns=['trait_id', 'trait_synonym'])
        if not datas['trait_mapped_terms'].all():
            self.trait_mapped_terms = json_normalize(data=data, record_path=['trait_mapped_terms'], meta=['id'])
            self.trait_mapped_terms.columns = ['trait_mapped_term', 'trait_id']
        else:
            self.trait_mapped_terms = DataFrame(columns=['trait_id', 'trait_mapped_term'])
        if not datas['associated_pgs_ids'].all():
            self.associated_pgs_ids = json_normalize(data=data, record_path=['associated_pgs_ids'], meta=['id'])
            self.associated_pgs_ids.columns = ['associated_pgs_id', 'trait_id']
        else:
            self.associated_pgs_ids = DataFrame(columns=['trait_id', 'associated_pgs_id'])
        if not datas['child_associated_pgs_ids'].all():
            self.child_associated_pgs_ids = json_normalize(data=data, record_path=['child_associated_pgs_ids'],
                                                           meta=['id'])
            self.child_associated_pgs_ids.columns = ['child_associated_pgs_id', 'trait_id']
        else:
            self.child_associated_pgs_ids = DataFrame(columns=['trait_id', 'child_associated_pgs_id'])
        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("Trait is running in fat mode. It has 6 DataFrames with hierarchical dependencies.\ntraits: "
                    "%d rows\n|\n -associated_pgs_ids: %d rows\n|\n -child_associated_pgs_ids:"
                    "%d rows\n|\n -trait_categories: %d rows\n|\n -trait_mapped_terms: %d rows\n|\n -trait_synonyms:"
                    " %d rows" % (
                        len(self.traits), len(self.associated_pgs_ids), len(self.child_associated_pgs_ids),
                        len(self.trait_categories), len(self.trait_mapped_terms), len(self.trait_synonyms)))
        if self.mode == 'Thin':
            return ('Trait is running in thin mode. It has 1 list that contains the raw data.\nraw_data: a list of '
                    'size x.')

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
        return Trait(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return Trait(self.raw_data + other.raw_data, self.mode)
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
            return Trait(data, self.mode)
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
            return Trait(data, self.mode)
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
            return Trait(data, self.mode)
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
            return Trait(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)
