import streamlit as st
import pandas as pd
import os

from app.config import HEADER_TEXT
from app.data.data import init_folders
from app.web import multipage
from app.web.pages import charts,\
                          load_another_data,\
                          uploads_files


def main():
    init_folders()

    st.title("Информационный центр")
    st.markdown(HEADER_TEXT)

    app = multipage.MultiPage()

    app.add_page("Загрузка данных", uploads_files.app)
    app.add_page("Графики", charts.app)
    app.add_page("Альтернативные источники", load_another_data.app)

    app.run()


if __name__ == '__main__':
    main()
