import unittest
from typing import List, Dict, Any
from pydantic import BaseModel
from crimson.data_class import DataClassList
import pandas as pd


class UnitData(BaseModel):
    arg1: int
    arg2: str


class ManyData(DataClassList):
    data: List[UnitData]


unit_data_list = [UnitData(arg1=i, arg2=f"number {i}") for i in range(10)]


class TestDataClassList(unittest.TestCase):

    def setup1(self) -> ManyData:
        unitdatas = ManyData(data=unit_data_list)
        return unitdatas

    def test_call(self):
        unitdatas: ManyData = self.setup1()

        unitdata_list: List[UnitData] = unitdatas()
        self.assertIsInstance(unitdata_list, list)

        for unitdata in unitdata_list:
            self.assertIsInstance(unitdata, UnitData)

    def test_get_list_dict(self):
        unitdatas: ManyData = self.setup1()

        list_dict: List[Dict[str, Any]] = unitdatas.get_list_dict()

        self.assertIsInstance(list_dict, list)

        for unitdata in list_dict:
            self.assertIsInstance(unitdata, dict)

    def test_get_dataframe(self):
        unitdatas: ManyData = self.setup1()

        df: pd.DataFrame = unitdatas.get_dataframe()

        expected_columns = ['arg1', 'arg2']
        self.assertListEqual(list(df.columns), expected_columns)

        self.assertEqual(len(df), len(unit_data_list))


if __name__ == "__main__":
    unittest.main()
