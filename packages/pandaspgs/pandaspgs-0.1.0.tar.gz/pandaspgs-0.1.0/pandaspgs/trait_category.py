from pandas import DataFrame, json_normalize, set_option

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class TraitCategory:
    """
       An object that stores data of type TraitCategory. To understand the significance of each column of the DataFrame. Please visit "TraitCategory" in [PGS Catalog Documentation](https://www.pgscatalog.org/rest/) for details.

       Attributes:
            raw_data: list. Convert from obtained JSON data
            efotraits : DataFrame. It only exists if the parameter mode of constructor is Fat.
            trait_categories: DataFrame. It only exists if the parameter mode of constructor is Fat.

       ```python
       from pandaspgs.get_trait import get_trait_categories

       ch = get_trait_categories()
       ch
       ch.raw_data
       ch.mode
       ch.efotraits
       ch.trait_categories
       ```
       Subset object s by either identifier or position
       ```python
       all_df = get_trait_categories()
       all_df[0].efotraits
       all_df[0:3].efotraits
       all_df['Biological process'].efotraits
       all_df[('Biological process','Body measurement','Cancer')].efotraits
       ```
       Objects can be manipulated like sets in the mathematical sense.
       ```python
       all_df = get_trait_categories()
       one = all_df[0]
       two = all_df[1]
       three = all_df[2]
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
            self.efotraits = DataFrame(
                columns=['id', 'label', 'description', 'url', 'category_id'])
            self.trait_categories = DataFrame(
                columns=['id', 'label'])
            return
        for i in range(len(data)):
            data[i]['id1'] = i

        self.trait_categories = json_normalize(data=data, max_level=1).drop(columns=['efotraits'])
        self.trait_categories.columns = ['label', 'id']
        self.efotraits = json_normalize(data=data, record_path=['efotraits'], meta=['id1'])
        self.efotraits.columns = ['id', 'label', 'description', 'url', 'category_id']

    def __str__(self):
        if self.mode == 'Fat':
            return ("TraitCategory is running in fat mode. It has 2 DataFrames with hierarchical "
                    "dependencies.\ntrait_categories: %d rows\n|\n -efotraits: %d rows" % (
                        len(self.trait_categories), len(self.efotraits)))
        if self.mode == 'Thin':
            return (
                'TraitCategory is running in thin mode. It has 1 list that contains the raw data.\nraw_data: a list of '
                'size %d.') % len(self.raw_data)

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
            raw_data_dict[j['label']] = j
        sub_set = []
        for i in arr:
            if isinstance(i, str):
                sub_set.append(raw_data_dict[i])
            elif isinstance(i, int):
                sub_set.append(raw_data[i])
            else:
                raise TypeError('Invalid item type: {}'.format(type(i)))
        return TraitCategory(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return TraitCategory(self.raw_data + other.raw_data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __sub__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['label'])
                self_dict[i['label']] = i
            for j in other.raw_data:
                other_key_set.add(j['label'])
            sub_key = self_key_set - other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return TraitCategory(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __and__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['label'])
                self_dict[i['label']] = i
            for j in other.raw_data:
                other_key_set.add(j['label'])
            sub_key = self_key_set & other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return TraitCategory(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __or__(self, other):
        if self.mode == other.mode:
            and_dict = {}
            for i in self.raw_data:
                and_dict[i['label']] = i
            for j in other.raw_data:
                and_dict[j['label']] = j
            data = list(and_dict.values())
            return TraitCategory(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __xor__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            and_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['label'])
                and_dict[i['label']] = i
            for j in other.raw_data:
                other_key_set.add(j['label'])
                and_dict[j['label']] = j
            sub_key = self_key_set ^ other_key_set
            data = []
            for k in sub_key:
                data.append(and_dict[k])
            return TraitCategory(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)
