from typing import List, Dict, Any, TypeVar
from pydantic import BaseModel
import pandas as pd

T = TypeVar("T", bound=BaseModel)


class DataClassList(BaseModel):
    data: List[BaseModel]

    def __call__(self) -> List[BaseModel]:
        return self.data

    def get_list_dict(self) -> List[Dict[str, Any]]:
        return [item.model_dump() for item in self.data]

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.get_list_dict())
