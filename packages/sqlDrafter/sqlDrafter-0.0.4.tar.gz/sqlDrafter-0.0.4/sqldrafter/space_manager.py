import requests
from sqldrafter.util import identify_categorical_columns
from io import StringIO
import pandas as pd
import json







def create_space(
    self,
    title: str,
    desc: str,
    dbQueryType:str
) -> int:
    try:
        headers = {"api_key":self.api_key}
        res = requests.post(f"{self.base_url}/api/space/manage/add",
                        json={
                            "name": title,
                            "busiDesc" : desc,
                            "engineType": self.engineType,
                            "dbQueryType":dbQueryType,
                            "sqlStr":"1"
                        },
                        headers=headers
                        )
        resp = res.json()
        if(resp["success"]):
            return resp["data"]["id"]
    except:
        return 0
