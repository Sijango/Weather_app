import datetime

import pandas as pd
import numpy as np
import plotly.express as px

from app.config import HEAT, LOAD
from app.data.data import cut_data_with_date, get_min_in_day, get_max_in_day, convert_to_one_day, convert_to_one_hour, \
    convert_to_three_hours, convert_data


def draw_heat_chart(data, columns, name, date_in, date_out, status):
    labels = {
        "Date": "Дата",
        "value": "Теплоощущение"
    }

    data_cuts = cut_data_with_date(data, date_in, date_out)
    cols = [col for col in columns if 'temp' in col or "Date" in col]
    data_cuts = convert_data(data_cuts, cols, HEAT)

    fig = draw_line(data_cuts, cols, name+" (Теплоощущение) ", labels, date_in, date_out, status)
    return fig


def draw_load_chart(data, columns, name, date_in, date_out, status):
    labels = {
        "Date": "Дата",
        "value": "Нагрузка"
    }

    data_cuts = cut_data_with_date(data, date_in, date_out)
    cols = [col for col in columns if 'temp' in col or "Date" in col]
    data_cuts = convert_data(data_cuts, cols, LOAD)

    fig = draw_line(data_cuts, cols, name+" (Нагрузка) ", labels, date_in, date_out, status)
    return fig


def draw_histogram_chart(data, columns, name, date_in, date_out, status):
    labels = {
        "Date": "Дата",
        "value": "Параметры"
    }

    data_cuts = cut_data_with_date(data, date_in, date_out)
    fig = draw_histogram(data_cuts, columns, name, labels, date_in, date_out, status)

    return fig


def draw_line_chart(data, columns, name, date_in, date_out, status):
    labels = {
        "Date": "Дата",
        "value": "Параметры"
    }

    data_cuts = cut_data_with_date(data, date_in, date_out)
    fig = draw_line(data_cuts, columns, name, labels, date_in, date_out, status)

    return fig


def draw_histogram(data_cuts, columns, name, labels, date_in, date_out, status):
    if status == "Данные, как есть":
        fig = px.bar(data_cuts,
                     x="Date",
                     y=columns,
                     labels=labels,
                     title="Прибор: "+name+" c "+date_in+" по "+date_out)

    elif status == "Усреднять за час":
        data_cuts = convert_to_one_hour(data_cuts, columns)

        fig = px.bar(data_cuts,
                     x="Date",
                     y=columns,
                     labels=labels,
                     title="Прибор: " + name + " c " + date_in + " по " + date_out)

    elif status == "Усреднять за сутки":
        data_cuts = convert_to_one_day(data_cuts, columns)

        fig = px.bar(data_cuts,
                     x="Date",
                     y=columns,
                     labels=labels,
                     title="Прибор: " + name + " c " + date_in + " по " + date_out)

    elif status == "Усреднять за каждые 3 часа":
        data_cuts = convert_to_three_hours(data_cuts, columns)

        fig = px.bar(data_cuts,
                     x="Date",
                     y=columns,
                     labels=labels,
                     title="Прибор: " + name + " c " + date_in + " по " + date_out)

    elif status == "Минимальные и максимальные параметры за сутки":
        data_min = get_min_in_day(data_cuts)
        data_max = get_max_in_day(data_cuts)

        columns_new = []
        for i, _ in enumerate(columns):
            columns_new.append(columns[i] + "_max")
            columns_new.append(columns[i] + "_min")

        all_data = pd.concat([data_min, data_max.drop(columns="Date")], axis=1)

        fig = px.bar(all_data,
                     x="Date",
                     y=columns_new,
                     labels=labels,
                     title="Прибор: " + name + " c " + date_in + " по " + date_out)

    return fig


def draw_line(data_cuts, columns, name, labels, date_in, date_out, status):
    if status == "Данные, как есть":
        fig = px.line(data_cuts,
                      x="Date",
                      y=columns,
                      labels=labels,
                      title="Прибор: " + name + " c " + date_in + " по " + date_out,
                      markers=True)

    elif status == "Усреднять за час":
        data_cuts = convert_to_one_hour(data_cuts, columns)

        fig = px.line(data_cuts,
                      x="Date",
                      y=columns,
                      labels=labels,
                      title="Прибор: " + name + " c " + date_in + " по " + date_out,
                      markers=True)

    elif status == "Усреднять за сутки":
        data_cuts = convert_to_one_day(data_cuts, columns)

        fig = px.line(data_cuts,
                      x="Date",
                      y=columns,
                      labels=labels,
                      title="Прибор: " + name + " c " + date_in + " по " + date_out,
                      markers=True)

    elif status == "Усреднять за каждые 3 часа":
        data_cuts = convert_to_three_hours(data_cuts, columns)

        fig = px.line(data_cuts,
                      x="Date",
                      y=columns,
                      labels=labels,
                      title="Прибор: " + name + " c " + date_in + " по " + date_out,
                      markers=True)

    elif status == "Минимальные и максимальные параметры за сутки":
        data_min = get_min_in_day(data_cuts)
        data_max = get_max_in_day(data_cuts)

        columns_new = []
        for i, _ in enumerate(columns):
            columns_new.append(columns[i]+"_max")
            columns_new.append(columns[i]+"_min")

        all_data = pd.concat([data_min, data_max.drop(columns="Date")], axis=1)

        fig = px.line(all_data,
                      x="Date",
                      y=columns_new,
                      labels=labels,
                      title="Прибор: "+name+" c "+date_in+" по "+date_out,
                      markers=True)

    return fig


if __name__ == '__main__':
    data = pd.read_csv("../../data/csv/data.csv")
    columns = pd.read_csv("../../data/csv/column_type_desc.csv")
    name = columns["column_name"].tolist()[-1]

    columns = [col for col in columns["column_name"].tolist() if "temp" in col.lower()]

    fig = draw_histogram_chart(data, columns, name, "2022-08-15 23:04:37", "2022-08-16 1:04:37")
    fig.show()
