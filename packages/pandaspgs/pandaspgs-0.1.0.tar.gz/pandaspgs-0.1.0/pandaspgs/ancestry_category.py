from pandas import DataFrame, json_normalize, set_option

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class AncestryCategory:
    """
       An object that stores data of type AncestryCategory. To understand the significance of each column of the DataFrame. Please visit "Other endpoints" in [PGS Catalog Documentation](https://www.pgscatalog.org/rest/) for details.

       Attributes:
            raw_data: list. Convert from obtained JSON data
            ancestry_categories : DataFrame. It only exists if the parameter mode of constructor is Fat.
            categories: DataFrame. It only exists if the parameter mode of constructor is Fat.
            mode: Fat or Thin. Specifies the mode of the returned object.

       ```python
       from pandaspgs.get_ancestry_category import get_ancestry_categories

       ch = get_ancestry_categories()
       ch
       ch.raw_data
       ch.mode
       ch.ancestry_categories
       ch.categories
       ```
       Subset object s by either identifier or position
       ```python
       all_df = get_ancestry_categories()
       all_df[0].ancestry_categories
       all_df[0:3].ancestry_categories
       all_df['AFR'].ancestry_categories
       all_df[('AFR','ASN','EAS')].ancestry_categories
       ```
       Objects can be manipulated like sets in the mathematical sense.
       ```python
       all_df = get_ancestry_categories()
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
            self.ancestry_categories = DataFrame(
                columns=['symbols', 'display_category'])
            self.categories = DataFrame(
                columns=['symbols', 'category'])
            return
        datas = json_normalize(data=data, max_level=1).drop(columns=['symbols', 'display_category'])
        datas['categories'] = datas['categories'].map(lambda x: x == [])
        self.ancestry_categories = json_normalize(data=data, max_level=1).drop(
            columns=['categories'])
        if not datas['categories'].all():
            self.categories = json_normalize(data=data, record_path=['categories'], meta=['symbols'])
            self.categories.columns = ['category', 'symbols']

        else:
            self.categories = DataFrame(
                columns=['symbols', 'category'])

    def __str__(self):
        if self.mode == 'Fat':
            return ("AncestryCategory is running in fat mode. It has 2 DataFrames with hierarchical "
                    "dependencies.\nancestry_categories: %d rows\n|\n -categories: %d rows" % (
                        len(self.ancestry_categories), len(self.categories)))
        if self.mode == 'Thin':
            return (
                'AncestryCategory is running in thin mode. It has 1 list that contains the raw data.\nraw_data: a list of '
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
            raw_data_dict[j['symbols']] = j
        sub_set = []
        for i in arr:
            if isinstance(i, str):
                sub_set.append(raw_data_dict[i])
            elif isinstance(i, int):
                sub_set.append(raw_data[i])
            else:
                raise TypeError('Invalid item type: {}'.format(type(i)))
        return AncestryCategory(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return AncestryCategory(self.raw_data + other.raw_data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __sub__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['symbols'])
                self_dict[i['symbols']] = i
            for j in other.raw_data:
                other_key_set.add(j['symbols'])
            sub_key = self_key_set - other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return AncestryCategory(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __and__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['symbols'])
                self_dict[i['symbols']] = i
            for j in other.raw_data:
                other_key_set.add(j['symbols'])
            sub_key = self_key_set & other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return AncestryCategory(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __or__(self, other):
        if self.mode == other.mode:
            and_dict = {}
            for i in self.raw_data:
                and_dict[i['symbols']] = i
            for j in other.raw_data:
                and_dict[j['symbols']] = j
            data = list(and_dict.values())
            return AncestryCategory(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __xor__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            and_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['symbols'])
                and_dict[i['symbols']] = i
            for j in other.raw_data:
                other_key_set.add(j['symbols'])
                and_dict[j['symbols']] = j
            sub_key = self_key_set ^ other_key_set
            data = []
            for k in sub_key:
                data.append(and_dict[k])
            return AncestryCategory(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)
