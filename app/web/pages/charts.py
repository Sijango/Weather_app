import streamlit as st
import pandas as pd
import datetime
import random

from app.data.draw import draw_line_chart, draw_histogram_chart, draw_heat_chart, draw_load_chart
from app.data.word import WordDocument


def app():
    st.markdown("## Графики")
    # TRY !!!!!!!!!!!!!!
    date_type = pd.read_csv("data/date_type_file.csv", encoding="utf-8")
    type_file = date_type["second"].tolist()[1]

    names = []
    st.markdown(f"### Доступна информация по приборам:")

    for i in range(2, len(date_type)):
        name = date_type['first'].tolist()[i]
        names.append(name)
        st.markdown(f"{i-1}. Прибор: {name}")

    name = st.selectbox('Выберете прибор для отображения информации:',
                        names)

    if type_file == "csv":
        data = pd.read_csv("data/csv/data.csv", encoding="utf-8")
        columns = pd.read_csv("data/csv/column_type_desc.csv", encoding="utf-8")
    else:
        data = pd.read_csv(f"data/json/data/{name}.csv", encoding="utf-8")
        columns = pd.read_csv(f"data/json/name_columns/{name}.csv", encoding="utf-8")

    create_chart(data, name, date_type, columns)


def create_chart(data, name_file, date_type, columns):
    if data is not None:
        date_in = date_type["first"].tolist()[0]
        date_out = date_type["second"].tolist()[0]

        st.markdown(f"## Информация по прибору: {name_file}")
        st.markdown(f"##### За промежуток времени с {date_in} по {date_out}")
        st.markdown(f"#### Данные в табличной форме:")
        st.dataframe(data)

        cols = columns["column_name"].tolist()
        col = [x for x in cols if 'temp' in x]

        st.markdown(f"### Построение графика")
        cols = st.multiselect(
            "Выберите параметры по которым будут строиться графики:",
            cols[1:],
            col
        )

        time = st.slider(
            "Выберете диапазон времени:",
            min_value=datetime.datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S"),
            max_value=datetime.datetime.strptime(date_out, "%Y-%m-%d %H:%M:%S"),
            value=(datetime.datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S"),
                   datetime.datetime.strptime(date_out, "%Y-%m-%d %H:%M:%S")),
            format="YY-MM-DD H:M"
        )

        date_in = time[0].strftime("%Y-%m-%d %H:%M:%S")
        date_out = time[1].strftime("%Y-%m-%d %H:%M:%S")

        type_chart = st.radio(
            "Тип графика:",
            ("Линейный", "Столбчатый"),
        )

        status_data = st.radio(
            "Как строить графики?",
            ("Данные, как есть",
             "Усреднять за час",
             "Усреднять за каждые 3 часа",
             "Усреднять за сутки",
             "Минимальные и максимальные параметры за сутки")
        )

        st.markdown("Построить дополнительные графики?")
        heat_chart = st.checkbox("График теплоотдачи")
        load_chart = st.checkbox("График нагрузки")

        # if st.button('Построить график'):
        if type_chart == "Линейный":
            fig = draw_line_chart(data, cols, name_file, date_in, date_out, status_data)
        elif type_chart == "Столбчатый":
            fig = draw_histogram_chart(data, cols, name_file, date_in, date_out, status_data)
        st.plotly_chart(fig, use_container_width=True)

        fig.write_image("data/images/main.png")

        if heat_chart:
            fig_heat = draw_heat_chart(data, cols, name_file, date_in, date_out, status_data)
            st.plotly_chart(fig_heat, use_container_width=True)

            fig_heat.write_image("data/images/heat.png")

        if load_chart:
            fig_load = draw_load_chart(data, cols, name_file, date_in, date_out, status_data)
            st.plotly_chart(fig_load, use_container_width=True)

            fig_load.write_image("data/images/load.png")

        if st.button("Создать отчёт"):
            cur_time = datetime.datetime.now()
            cur_time = cur_time.strftime("%Y-%m-%d %H:%M")

            doc = WordDocument(path_file=f"data/Report_{cur_time}.docx",
                               name_file=f"Report_{cur_time}.docx",
                               name=name_file,
                               date_in=date_in,
                               date_out=date_out,
                               type_chart=type_chart,
                               param_draw=status_data)
            doc.set_style()
            doc.set_title()

            doc.set_main_data(image=f"data/images/main.png")
            if heat_chart:
                doc.set_heat_data(image="data/images/heat.png")
            if load_chart:
                doc.set_load_data(image=f"data/images/load.png")

            doc.save()

            st.markdown("##### Отчёт создан!")
            with open(doc.path, "rb") as file:
                st.download_button(
                    label="Загрузить отчёт",
                    data=file,
                    file_name=doc.name_file
                )


if __name__ == '__main__':
    app()
