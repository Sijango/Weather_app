from io import StringIO

import numpy as np
import pandas as pd
import streamlit as st

from app.config import UPLOAD_TEXT
from app.data.data import convert_json_to_csv


def app():
    st.markdown("## Загрузка данных")
    st.markdown(UPLOAD_TEXT)

    st.write("\n")

    uploaded_file = st.file_uploader("Выберете файл:", type=['csv', 'txt', 'json'], accept_multiple_files=False)
    # uploaded_file = st.file_uploader("Выберете файл:", type=['csv'], accept_multiple_files=False)
    status_button = False

    if uploaded_file is not None:
        type_file = uploaded_file.name.split('.')[1]

        try:
            if type_file == 'csv':
                uploaded_file = StringIO(uploaded_file.getvalue().decode("cp1251"))

                name_device = uploaded_file.readline().split(';')[1]

                data = pd.read_csv(uploaded_file, sep=';')
                status_button = True

            elif type_file == 'txt':
                json_file = pd.read_json(uploaded_file.read(), lines=True)
                data = convert_json_to_csv(json_file)

                type_file = "json"
                status_button = True

            elif type_file == 'json':
                json_file = pd.read_json(uploaded_file.read(), lines=True)
                data = convert_json_to_csv(json_file)

                status_button = True

        except Exception as ex:
            print(ex)
            st.markdown("#### Ошибка! Некорректно введён файл, повторите попытку! ####")
            status_button = False

    if status_button:
        if type_file == "csv":
            save_csv(data, name_device, type_file)
        elif type_file == "json":
            save_json(data, type_file)


def save_csv(data, name_device, type_file):
    st.markdown(f"#### Прибор: {name_device}")

    if st.button('Подтвердить'):
        try:
            cols = data.columns.tolist()
            for col in cols:
                if "Unnamed:" in col:
                    data = data.drop(columns=col)

        except Exception as ex:
            print(ex)

        st.write(data)

        data.to_csv("data/csv/data.csv", index=False)

        date_in = data["Date"].tolist()[0]
        date_out = data["Date"].tolist()[-1]

        columns = []
        for col in data.keys():
            columns.append((col, "Column"))

        columns_df = pd.DataFrame(columns, columns=['column_name', 'type'])
        columns_df.to_csv('data/csv/column_type_desc.csv', index=False)

        date_type_file = [(date_in, date_out), (name_device, type_file), (name_device, "Прибор")]
        date_type_file_df = pd.DataFrame(date_type_file, columns=['first', 'second'])
        date_type_file_df.to_csv("data/date_type_file.csv", index=False)

        st.markdown("**Имя колонки**-**Тип**")
        for i in range(columns_df.shape[0]):
            st.write(f"{i + 1}. **{columns_df.iloc[i]['column_name']}** - {columns_df.iloc[i]['type']}")


def save_json(data, type_file):
    names = []
    st.markdown(f"#### Загружена информация по приборам:")
    for i, name in enumerate(data.keys()):
        st.markdown(f"{i+1}. Прибор: {name}")
        names.append(name)

    if st.button('Подтвердить'):
        for name in data.keys():
            st.markdown(f"#### Прибор: {name}")

            data[name] = pd.DataFrame(data[name])
            try:
                cols = data[name].columns.tolist()
                for col in cols:
                    if "Unnamed:" in col:
                        data = data[name].drop(columns=col)

            except Exception as ex:
                print(ex)

            st.write(data[name])

            data[name].to_csv(f"data/json/data/{name}.csv", index=False)

            date_in = data[name]["Date"].tolist()[0]
            date_out = data[name]["Date"].tolist()[-1]

            columns = []
            for col in data[name].keys():
                columns.append((col, "Column"))

            columns_df = pd.DataFrame(columns, columns=['column_name', 'type'])
            columns_df.to_csv(f'data/json/name_columns/{name}.csv', index=False)

            st.markdown("**Имя колонки**-**Тип**")
            for i in range(columns_df.shape[0]):
                st.write(f"{i + 1}. **{columns_df.iloc[i]['column_name']}** - {columns_df.iloc[i]['type']}")

        date_type_file = [(date_in, date_out), ("ALL", type_file)]
        for name in names:
            date_type_file.append((name, "Прибор"))
        date_type_file_df = pd.DataFrame(date_type_file, columns=['first', 'second'])
        date_type_file_df.to_csv("data/date_type_file.csv", index=False)


if __name__ == '__main__':
    app()
