import datetime
import decimal
import json
import os
import re
import sys
import pwinput
from prompt_toolkit import prompt

import sqldrafter

USAGE_STRING = """
使用: sqldrafter <command>
可使用命令如下:
    init\t\t\t初始化数据源
    createSpace\t\t\t初始化空间信息返回空间ID
    gen <spaceID> <table1> <table2>\t 为使用的表生成execle
    update <file>\t\t 更新必要的表信息给sqldrater
    query\t\t\t 进行一个查询
"""

home_dir = os.path.expanduser("~")


def main():
    if len(sys.argv) < 2:
        print(USAGE_STRING)
        sys.exit(1)
    if sys.argv[1] == "init":
        init()
    if sys.argv[1] == "createSpace":
        createSpace()

    else:
        print(f"Unknown command: {sys.argv[1]}")
        print(USAGE_STRING)
        sys.exit(1)


def init():
    """
    初始化数据源配置在 ~/.sqldrafter/connection.json
    """

    print("Welcome to \033[94msqldrafter\033[0m!\n")
    filepath = os.path.join(home_dir, ".sqldrafter", "connection.json")
    if os.path.exists(filepath):
        print(
            "目前已有数据源配置，请问是否覆盖? (y/n)"
        )
        overwrite = prompt().strip()
        if overwrite.lower() != "y":
            print("目前不覆盖，配置无变化！")
            sys.exit(0)
        else:
            print("我们将创建新的数据源配置在 ~/.sqldrafter/connection.json")
    else:
        print("我们将创建新的数据源配置在 ~/.sqldrafter/connection.json")
        if not os.path.exists(os.path.join(home_dir, ".sqldrafter")):
            os.mkdir(os.path.join(home_dir, ".sqldrafter"))

    if os.environ.get("SQLDRAFTER_API_KEY"):
        print(
            "我们发现您的 SQLDRAFTER_API_KEY 存在您的环境中. 我们将使用它。"
        )
        api_key = os.environ.get("SQLDRAFTER_API_KEY")
    else:
        print(
            "请输入SQLDRAFTER_API_KEY. You can get it from https://www.sqldrafter.com/accounts/dashboard/ and creating an account:"
        )
        api_key = prompt().strip()

    # prompt user for db_type
    print(
        "请选择一个数据库类型 "
        + ", ".join(sqldrafter.SUPPORTED_DB_TYPES)
    )
    db_type = prompt().strip()
    db_type = db_type.lower()
    while db_type not in sqldrafter.SUPPORTED_DB_TYPES:
        print(
            "您输入的数据库，我们并不支持，目前只支持如下数据库： "
            + ", ".join(sqldrafter.SUPPORTED_DB_TYPES)
        )
        db_type = prompt().strip()
        db_type = db_type.lower()
    print("请输入数据库地址:")
    host = prompt().strip()
    print("请输入数据库端口:")
    port = prompt().strip()
    print("请输入数据库用户名:")
    user = prompt().strip()
    print("请输入数据库密码:")
    password = pwinput.pwinput(prompt="Please enter your database password:")
    db_creds = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
        }

    sqldrafter.sqlDrafter(api_key=api_key, db_type=db_type, db_creds=db_creds)
    # write to filepath and print confirmation
    with open(filepath, "w") as f:
        data = {"api_key": api_key, "db_type": db_type, "db_creds": db_creds}
        json.dump(data, f, indent=4)
    print(f"数据源配置将保存在  {filepath}.")
    sys.exit(0)
def createSpace():
    """
    初始化数据源配置在 ~/.sqldrafter/connection.json
    """
    sq = sqldrafter.sqlDrafter();
    # print welcome message
    print("请输入空间标题：")
    title = prompt().strip()
    print("请输入空间描述：")
    desc = prompt().strip()
    print( "该空间是否是单库查询(y/n)")
    isSingle=prompt().strip();
    dbQueryType =1
    if(isSingle.lower()=="y"):
        dbQueryType=2
    spaceID= sq.create_space(title,desc,dbQueryType)
    if( spaceID>0):
        print("该空间ID为："+spaceID+"请妥善保存。")
    sys.exit(0)









def to_str(field) -> str:
    if isinstance(field, str):
        return field
    elif isinstance(field, int):
        return str(field)
    elif isinstance(field, float):
        return str(field)
    elif isinstance(field, datetime.datetime):
        return field.strftime("%Y-%m-%d")
    elif isinstance(field, datetime.date):
        return field.strftime("%Y-%m-%d")
    elif isinstance(field, datetime.timedelta):
        return str(field)
    elif isinstance(field, datetime.time):
        return field.strftime("%H:%M:%S")
    elif isinstance(field, list):
        return str(field)
    elif isinstance(field, dict):
        return str(field)
    elif isinstance(field, bool):
        return str(field)
    elif isinstance(field, decimal.Decimal):
        return str(field)
    elif field is None:
        return "NULL"
    else:
        raise ValueError(f"Unknown type: {type(field)}")


def print_table(columns, data):
    data_header = data + [tuple(columns)]
    column_widths = [
        max(len(to_str(row[i])) for row in data_header) for i in range(len(columns))
    ]
    for i, column in enumerate(columns):
        print(column.ljust(column_widths[i]), end=" | ")
    print()
    for i, column_width in enumerate(column_widths):
        print("-" * column_width, end="-+-" if i < len(column_widths) - 1 else "-|\n")

    for row in data:
        for i, value in enumerate(row):
            print(to_str(value).ljust(column_widths[i]), end=" | ")
        print()








if __name__ == "__main__":
    main()
