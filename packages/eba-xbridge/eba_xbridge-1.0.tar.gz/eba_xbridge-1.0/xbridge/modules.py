"""
Module with the classes related to modules, containing the "instructions" for the conversion.
"""

import copy
import json
from pathlib import Path
from zipfile import ZipFile

import pandas as pd


class Module:
    """Class representing an XBRL Module.

    It has attributes like code, url, taxonomy_code, date, tables
    and input_path, whose main function is to operate with the module and return properties like a specific table from
    the JSON file used as input, an object, a dictionary using the attributes as keys, a module object from a part of
    preprocessed JSON file and the variables that are present in it.

    It is used when taxonomies are loaded to collect the information associated to the tables belonging to the module.

    :param code: The code of the XBRL module.

    :param url: The module reference within the taxonomy.

    :param taxonomy_code: The code of the module within to the taxonomy.

    :param date: Dates contained in the module.

    :param tables: The tables that form the module.

    """

    def __init__(self, code=None, url=None, taxonomy_code=None, date=None, tables=None):
        self.code = code
        self.url = url
        self.taxonomy_code = taxonomy_code
        self.date = date
        self._tables = tables if tables is not None else []
        self.taxonomy_module_path = None

    @property
    def tables(self):
        """Returns the :obj:`tables <xbridge.taxonomy.Table>` defined in the JSON file for the :obj:`module <xbridge.taxonomy.Module>`"""
        return self._tables

    def extract_tables(self, zip_file: ZipFile):
        """Extracts the :obj:`tables <xbridge.taxonomy.Table>` in the JSON files for the :obj:`modules <xbridge.taxonomy.Module>` in the taxonomy"""

        self._tables = []
        bin_read = zip_file.read(self.taxonomy_module_path)

        info = json.loads(bin_read.decode("utf-8"))

        for table_code, table in info["tables"].items():
            if table_code[1:] in ("FI", "FootNotes"):
                continue

            table_url = table["url"]
            table_folder_name = table_code[1:].lower()
            table_folder_name = table_folder_name.replace("-", ".")

            path = self.taxonomy_module_path.split("/mod/")[0]

            table_path = (
                path + "/tab/" + table_folder_name + "/" + table_folder_name + ".json"
            )
            table = Table.from_taxonomy(
                zip_file, table_path, code=table_code[1:], url=table_url
            )

            self.tables.append(table)

    def get_table(self, table_code: str):
        """Returns a :obj:`table <xbridge.taxonomy.Table>` object with the given code"""
        for table in self.tables:
            if table.code_name == table_code:
                return table
        raise ValueError(f"Table {table_code} not found in module {self.code}")

    def to_dict(self):
        """Returns a dictionary"""
        return {
            "code": self.code,
            "url": self.url,
            "taxonomy_code": self.taxonomy_code,
            "date": self.date,
            "tables": [tab.to_dict() for tab in self.tables],
        }

    @classmethod
    def from_taxonomy(cls, zip_file: ZipFile, json_file_path: str):
        """Returns a :obj:`module <xbridge.taxonomy.Module>` object from a part of the JSON file"""

        url_split = json_file_path.split("/")
        taxonomy_code = url_split[7]
        date = url_split[8]

        code = Path(json_file_path).stem

        obj = cls(code=code, url=json_file_path, taxonomy_code=taxonomy_code, date=date)

        obj.taxonomy_module_path = json_file_path

        obj.extract_tables(zip_file)

        return obj

    @classmethod
    def from_serialized(cls, input_path: str | Path):
        """Returns a :obj:`module <xbridge.taxonomy.Module>` object from a JSON file"""
        input_path = input_path if isinstance(input_path, Path) else Path(input_path)
        with open(input_path, "r", encoding="UTF-8") as fl:
            module_dict = json.load(fl)

        tables = module_dict.pop("tables")
        tables = [Table.from_dict(table) for table in tables]

        obj = cls(**module_dict, tables=tables)

        return obj

    @property
    def variables_location(self):
        """Returns a dictionary with the :obj:`variables <xbridge.taxonomy.Variable>`
        and the :obj:`tables <xbridge.taxonomy.Table>` where they are present"""
        variables = {}
        for table in self.tables:
            for variable in table.variables:
                if variable.code not in variables:
                    variables[variable.code] = [table.code]
                else:
                    variables[variable.code].append(table.code)
        return variables

    @property
    def repeated_variables(self):
        """Returns a dictionary with the :obj:`variables <xbridge.taxonomy.Variable>` and the :obj:`tables <xbridge.taxonomy.Table>`
        where they are present, if they are repeated"""
        result = {}
        for k, v in self.variables_location.items():
            if len(v) > 1:
                result[k] = v
        return result

    def __repr__(self) -> str:
        return f"<Module - {self.code}>"


class Table:
    """Class representing an XBRL :obj:`table <xbridge.taxonomy.Table>` as defined in the JSON file.

    Its properties allow to return open keys, variables and attributes from the :obj:`table <xbridge.taxonomy.Table>`. It can also generate a
    variable dataframe or work with one already created.
    Finally, it can return a dictionary using its attributes or a :obj:`Table <xbridge.taxonomy.Table>` object from the preprocessed JSON file.

    It is used when module is loaded to collect the information associated to the variables and open keys
    belonging to the table.

    :param code: The code of the table.

    :param url: The table reference within the module.

    :param open_keys: Open key contained in the table.

    :param variables: the variables that belongs to the table.

    :param attributes: attributes related to the variables that can be extracted from the table.

    :param input_zip_path: Path to the file used as table.
    """

    def __init__(
        self,
        code=None,
        url=None,
        open_keys=None,
        variables=None,
        attributes=None,
        input_zip_path=None,
    ):

        self.table_zip_path = input_zip_path
        self.code = code
        self.url = url
        self._open_keys = open_keys if open_keys is not None else []
        self._variables = variables if variables is not None else []
        self._attributes = attributes if attributes is not None else []
        self._datapoint_df = None

    @property
    def open_keys(self):
        """Returns the open keys for the :obj:`table <xbridge.taxonomy.Table>`"""
        return self._open_keys

    @property
    def variables(self):
        """Returns the :obj:`variable <xbridge.taxonomy.Variable>` for the :obj:`table <xbridge.taxonomy.Table>`"""
        return self._variables

    @property
    def attributes(self):
        """Returns the attributes for the :obj:`table <xbridge.taxonomy.Table>`"""
        return self._attributes

    @property
    def variable_columns(self):
        """
        Returns the columns for the :obj:`variable <xbridge.taxonomy.Variable>` dataframe
        """
        cols = set(self.variable_df.columns)
        cols.remove("datapoint")
        return cols

    @property
    def variable_df(self):
        """
        Returns a dataframe with the :obj:`variable <xbridge.taxonomy.Variable>` and extensional context

        """
        return self._datapoint_df

    def generate_variable_df(self):
        """Returns a dataframe with the :obj:`variable <xbridge.taxonomy.Variable>` and extensional context"""
        variables = []
        for variable in self.variables:
            variable_info = {}
            for dim_k, dim_v in variable.dimensions.items():
                if dim_k not in ("unit", "decimals"):
                    variable_info[dim_k] = dim_v.split(":")[1]
            if "concept" in variable.dimensions:
                variable_info["metric"] = variable.dimensions["concept"].split(":")[1]
                del variable_info["concept"]

            variable_info["datapoint"] = variable.code
            variables.append(copy.copy(variable_info))
        self._datapoint_df = pd.DataFrame(variables)

    def extract_open_keys(self, zip_file: ZipFile):
        """Extracts the open keys for the :obj:`table <xbridge.taxonomy.Table>`"""
        self._open_keys = []
        self._attributes = []

        bin_read = zip_file.read(self.table_zip_path)

        table_json = json.loads(bin_read.decode("utf-8"))
        table_template = table_json["tableTemplates"][self.code]
        for column_name in table_template.get("columns", []):
            if column_name == "unit":
                self._attributes.append(column_name)
            elif column_name not in ("datapoint", "factValue"):
                self._open_keys.append(column_name)

    def extract_variables(self, zip_file: ZipFile):
        """Extract the :obj:`variable <xbridge.taxonomy.Variable>` for the :obj:`table <xbridge.taxonomy.Table>`"""
        self._variables = []
        bin_read = zip_file.read(self.table_zip_path)

        table_json = json.loads(bin_read.decode("utf-8"))
        if self.code in table_json["tableTemplates"]:
            variables_dict = table_json["tableTemplates"][self.code]["columns"][
                "datapoint"
            ]["propertyGroups"]
            for elto_k, elto_v in variables_dict.items():
                datapoint = Variable.from_taxonomy(elto_k, elto_v)
                self._variables.append(datapoint)

    def to_dict(self):
        """Returns a dictionary for the :obj:`table <xbridge.taxonomy.Table>`"""
        return {
            "code": self.code,
            "url": self.url,
            "open_keys": self.open_keys,
            "variables": [var.to_dict() for var in self.variables],
            "attributes": self.attributes,
        }

    @classmethod
    def from_taxonomy(cls, zip_file: ZipFile, table_path: str, code: str, url: str):
        """Returns a :obj:`table <xbridge.taxonomy.Table>` object from a part of the preprocessed JSON file"""
        obj = cls(code=code, url=url)
        obj.table_zip_path = table_path

        obj.extract_open_keys(zip_file)
        obj.extract_variables(zip_file)

        # obj.generate_datapoint_df()

        return obj

    @classmethod
    def from_dict(cls, table_dict):
        """Returns a :obj:`table <xbridge.taxonomy.Table>` object from a dictionary"""
        variables = table_dict.pop("variables")
        variables = [Variable.from_dict(variable) for variable in variables]

        obj = cls(**table_dict, variables=variables)
        obj.generate_variable_df()

        return obj

    def __repr__(self) -> str:
        return f"<Table - {self.code}>"


class Variable:
    """Class representing a variable as represented in the JSON files. Can return or extract the `dimension <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=a%20taxonomy.-,Dimension,-A%20qualifying%20characteristic>`_
    of the :obj:`variable <xbridge.taxonomy.Variable>`, create a dictionary using its attributes as keys or return a variable object from the
    preprocessed JSON file.


    :param code: The code of the variable.

    :param dimensions: the `dimensions <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=a%20taxonomy.-,Dimension,-A%20qualifying%20characteristic>`_ of the variable.

    :param attributes: The attributes related to the variable.

    """

    def __init__(self, code=None, dimensions=None, attributes=None):
        self.code = code
        self._dimensions = dimensions
        self._attributes = attributes

    @property
    def dimensions(self):
        """Returns the `dimensions <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=a%20taxonomy.-,Dimension,-A%20qualifying%20characteristic>`_ of a variable"""
        return self._dimensions

    def extract_dimensions(self, datapoint_dict):
        """Extracts the `dimensions <https://www.xbrl.org/guidance/xbrl-glossary/#:~:text=a%20taxonomy.-,Dimension,-A%20qualifying%20characteristic>`_ for the variable"""
        self._dimensions = datapoint_dict["dimensions"]
        if "decimals" in datapoint_dict:
            self._attributes = datapoint_dict["decimals"]

    def to_dict(self):
        """Returns a dictionary with the attributes"""
        return {
            "code": self.code,
            "dimensions": self.dimensions,
            "attributes": self._attributes,
        }

    @classmethod
    def from_taxonomy(cls, variable_id, variable_dict):
        """Returns a :obj:`variable <xbridge.taxonomy.Variable>` object from a part of the preprocessed JSON file"""
        obj = cls(code=variable_id)
        obj.extract_dimensions(variable_dict)

        return obj

    @classmethod
    def from_dict(cls, variable_dict):
        """Returns a :obj:`variable <xbridge.taxonomy.Variable>` object from a dictionary"""
        modified_dimensions = {}
        for k, v in variable_dict["dimensions"].items():
            if ":" in k:
                k = k.split(":")[1]
                modified_dimensions[k] = v
            else:
                modified_dimensions[k] = v
        modified_dict = variable_dict.copy()
        modified_dict["dimensions"] = modified_dimensions
        obj = cls(**modified_dict)
        # print(modified_dict)
        return obj

    def __repr__(self) -> str:
        return f"<Variable - {self.code}>"
