# import streamlit as st
# import pandas as pd
# import datetime
# import random
#
# from app.data.draw import draw_line_chart, draw_histogram_chart
# from app.config import settings
#
#
# def app():
#     st.markdown("## Графики")
#     # TRY !!!!!!!!!!!!!!
#     date_type = pd.read_csv("data/date_type_file.csv", encoding="utf-8")
#     type_file = date_type["second"].tolist()[1]
#
#     check_on_data = {}
#
#     st.markdown(f"### Доступна информация по приборам:")
#     for i in range(2, len(date_type)):
#         name = date_type['first'].tolist()[i]
#         check_on_data[name] = st.checkbox(f"{i-1}. Прибор: {name}")
#
#     date_in = date_type["first"].tolist()[0]
#     date_out = date_type["second"].tolist()[0]
#
#     for i, name in enumerate(check_on_data.keys()):
#         if type_file == "csv":
#             if check_on_data[name]:
#                 data = pd.read_csv("data/csv/data.csv", encoding="utf-8")
#                 columns = pd.read_csv("data/csv/column_type_desc.csv", encoding="utf-8")
#
#                 try:
#                     settings = pd.read_csv(f"data/json/{name}_settings.csv", encoding="utf-8")
#                 except:
#                     settings = {
#                         "multiselect": columns["column_name"].tolist()[-1],
#                         "radio": "Линейный",
#                         "slider": (datetime.datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S"),
#                                    datetime.datetime.strptime(date_out, "%Y-%m-%d %H:%M:%S"))
#                     }
#
#                     setting = pd.DataFrame(settings)
#                     setting.to_csv(f"data/csv/settings.csv", index=False)
#
#                 settings = create_chart(data, name, date_type, columns, i, settings)
#
#         else:
#             if check_on_data[name]:
#                 data = pd.read_csv(f"data/json/data/{name}.csv", encoding="utf-8")
#                 columns = pd.read_csv(f"data/json/name_columns/{name}.csv", encoding="utf-8")
#
#                 try:
#                     settings = pd.read_csv(f"data/json/{name}_settings.csv", encoding="utf-8")
#                 except:
#                     settings = {
#                         "multiselect": columns["column_name"].tolist()[-1],
#                         "radio": "Линейный",
#                         "slider": (datetime.datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S"),
#                                    datetime.datetime.strptime(date_out, "%Y-%m-%d %H:%M:%S"))
#                     }
#
#                     setting = pd.DataFrame(settings)
#                     setting.to_csv(f"data/json/{name}_settings.csv", index=False)
#
#                 settings = create_chart(data, name, date_type, columns, i, settings)
#
#
# def create_chart(data, name_file, date_type, columns, index, settings):
#     if data is not None:
#         date_in = date_type["first"].tolist()[0]
#         date_out = date_type["second"].tolist()[0]
#
#         st.markdown(f"## Информация по прибору: {name_file}")
#         st.markdown(f"##### За промежуток времени с {date_in} по {date_out}")
#         st.markdown(f"#### Данные в табличной форме:")
#         st.dataframe(data)
#
#         cols = columns["column_name"].tolist()
#         key = index + random.randint(1, 10123002)
#
#         st.markdown(f"### Построение графика")
#         settings['multiselect'] = st.multiselect(
#             "Выберите параметры по которым будут строиться графики:",
#             cols[1:],
#             default=settings['multiselect'],
#             # key=key
#         )
#         key = index + random.randint(1, 10123002)
#
#         settings["slider"] = st.slider(
#             "Выберете диапазон времени:",
#             min_value=datetime.datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S"),
#             max_value=datetime.datetime.strptime(date_out, "%Y-%m-%d %H:%M:%S"),
#             value=settings["slider"],
#             format="YY-MM-DD H:M",
#             # key=key
#         )
#
#         date_in = settings["slider"][0].strftime("%Y-%m-%d %H:%M:%S")
#         date_out = settings["slider"][1].strftime("%Y-%m-%d %H:%M:%S")
#         key = index + random.randint(1, 10123002)
#
#         radio_dict = {
#             "Линейный": 0,
#             "Столбчатый": 1
#         }
#
#         settings['radio'] = st.radio(
#             "Тип графика:",
#             ("Линейный", "Столбчатый"),
#             index=radio_dict[settings['radio']],
#             # key=key
#         )
#
#         key = index + random.randint(1, 10123002)
#         # if st.button('Построить график'):
#         if settings['radio'] == "Линейный":
#             fig = draw_line_chart(data, settings['multiselect'], name_file, date_in, date_out)
#         elif settings['radio'] == "Столбчатый":
#             fig = draw_histogram_chart(data, settings['multiselect'], name_file, date_in, date_out)
#         st.plotly_chart(fig, use_container_width=True)
#
#         return settings
#
#
# if __name__ == '__main__':
#     app()
