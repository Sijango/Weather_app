import datetime
import json
import os

import numpy as np
import pandas as pd

from app.config import HEAT, LOAD


def init_folders():
    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists("data/csv"):
        os.mkdir("data/csv")

    if not os.path.exists("data/images"):
        os.mkdir("data/images")

    if not os.path.exists("data/json"):
        os.mkdir("data/json")

    if not os.path.exists("data/json/data"):
        os.mkdir("data/json/data")

    if not os.path.exists("data/json/name_columns"):
        os.mkdir("data/json/name_columns")


def get_key(item, dict):
    for key, value in dict.items():
        if item in value:
            return key


def convert_data(data, cols, const):
    result = {"Date": data["Date"]}

    for col in cols:
        result[col] = [get_key(x, const) for x in data[col]]

    return pd.DataFrame(result)


def cut_data_with_date(data, date_in, date_out):
    tmp_date_in = datetime.datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S")
    tmp_date_out = datetime.datetime.strptime(date_out, "%Y-%m-%d %H:%M:%S")

    result_data = []

    for i, item in enumerate(data["Date"]):
        tmp = datetime.datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
        if tmp_date_in <= tmp <= tmp_date_out:
            result_data.append(data.loc[i])

    return pd.DataFrame(result_data)


def convert_to_one_hour(data, columns):
    tmp_data = {}
    result_data = {}

    for i in data.index.tolist():
        hour = data.loc[i]["Date"]
        hour = datetime.datetime.strptime(hour, "%Y-%m-%d %H:%M:%S")
        hour = hour.strftime("%Y-%m-%d %H")

        if hour not in tmp_data.keys():
            tmp_data[hour] = {}

        for col in columns:
            if col not in tmp_data[hour].keys():
                tmp_data[hour][col] = []

            tmp_data[hour][col].append(data.loc[i][col])

    for key, value in tmp_data.items():
        result_data[key] = {}

        for col, item in value.items():
            result_data[key][col] = count_average(item)

    result_data = convert_dict_to_df(result_data)
    return result_data


def convert_to_three_hours(data, columns):
    tmp_data = {}
    result_data = {}

    check_date = None

    for i in data.index.tolist():
        hour = data.loc[i]["Date"]
        hour = datetime.datetime.strptime(hour, "%Y-%m-%d %H:%M:%S")

        if check_date is None:
            check_date = hour

        if check_date < hour:
            check_date = hour
            check_date += datetime.timedelta(hours=3)

        hour = check_date.strftime("%Y-%m-%d %H")

        if hour not in tmp_data.keys():
            tmp_data[hour] = {}

        for col in columns:
            if col not in tmp_data[hour].keys():
                tmp_data[hour][col] = []

            tmp_data[hour][col].append(data.loc[i][col])

    for key, value in tmp_data.items():
        result_data[key] = {}

        for col, item in value.items():
            result_data[key][col] = count_average(item)

    result_data = convert_dict_to_df(result_data)
    return result_data


def convert_to_one_day(data, columns):
    tmp_data = {}
    result_data = {}

    for i in data.index.tolist():
        day = data.loc[i]["Date"].split()[0]
        if day not in tmp_data.keys():
            tmp_data[day] = {}

        for col in columns:
            if col not in tmp_data[day].keys():
                tmp_data[day][col] = []

            tmp_data[day][col].append(data.loc[i][col])

    for key, value in tmp_data.items():
        result_data[key] = {}

        for col, item in value.items():
            result_data[key][col] = count_average(item)

    result_data = convert_dict_to_df(result_data)
    return result_data


def get_min_in_day(data):
    result_data = {}
    last_day = 0

    for i in data.index.tolist():
        day = data.loc[i]["Date"].split()[0]

        if last_day != day:
            result_data[day] = {}

        for column in data.keys()[1:]:
            value = data.loc[i][column]

            if last_day != day:
                result_data[day][column + "_min"] = value

            result_data[day][column + "_min"] = search_min(value, result_data[day][column + "_min"])

        if last_day != day:
            last_day = day

    result_data = convert_dict_to_df(result_data)
    return result_data


def get_max_in_day(data):
    result_data = {}
    last_day = ''

    for i in data.index.tolist():
        day = data.loc[i]["Date"].split()[0]

        if last_day != day:
            result_data[day] = {}

        for column in data.keys()[1:]:
            value = data.loc[i][column]

            if last_day != day:
                result_data[day][column + "_max"] = value

            result_data[day][column + "_max"] = search_max(value, result_data[day][column + "_max"])

        if last_day != day:
            last_day = day

    result_data = convert_dict_to_df(result_data)
    return result_data


def convert_dict_to_df(data):
    result_data = []

    for col in data.keys():
        element = {"Date": col}

        for item in data[col].keys():
            element[item] = data[col][item]

        result_data.append(element)

    result_data = pd.DataFrame(result_data)
    return result_data


def count_average(data):
    average = 0
    try:
        for value in data:
            average += float(value)
        return average/len(data)
    except:
        return data[0]


def search_min(value, last_min_value):
    try:
        if float(last_min_value) > float(value):
            return value
        return last_min_value
    except:
        return value


def search_max(value, last_max_value):
    try:
        if float(last_max_value) < float(value):
            return value
        return last_max_value
    except:
        return value


def convert_json_to_csv(json_file):
    data = {}
    names = []

    for col in json_file.keys():
        name = json_file[col].tolist()[0]["uName"]
        serial = json_file[col].tolist()[0]["serial"]
        columns_in_item = json_file[col].tolist()[0]["data"].keys()
        data_in_item = json_file[col].tolist()[0]["data"]

        name_append = name + " " + serial
        tmp = {'Date': json_file[col].tolist()[0]["Date"]}

        for name_data_item in columns_in_item:
            tmp[name_data_item] = data_in_item[name_data_item]

        if name_append not in data.keys():
            data[name_append] = [tmp]
        else:
            data[name_append].append(tmp)

    return data
    # for name in names:
    #     tmp = pd.DataFrame(data[name])
    #     tmp.to_csv(f"data/json/data/{name}.csv", index=False)


if __name__ == '__main__':
    json_file = json.loads("data/json/log.json")
    convert_json_to_csv(json_file=json_file)
