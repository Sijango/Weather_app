import pandas as pd
import streamlit as st

from app.data.get_weather import yandex_weather


def app():
    st.markdown("## Данные с Яндекса")

    try:
        weather = yandex_weather(55.755864, 37.617698)

        link = weather["link"]
        city = weather["city"]
        temp = str(weather['fact']['temp']) + "°С"
        wind_speed = str(weather['fact']['wind_speed']) + "м/с"
        humidity = str(weather['fact']['humidity']) + "%"
        pressure_mm = weather['fact']['pressure_mm']

        st.markdown(f"##### Погода в городе: {city}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Температура", temp)
        col2.metric("Скорость ветра", wind_speed)
        col3.metric("Влажность", humidity)
        col4.metric("Атм. давление (в мм рт.ст.)", pressure_mm)

        st.markdown(f"##### Данные погоды взяты с [Яндекса]({link})")
    except:
        st.markdown("##### Ошибка в подключении. Проверьте соединение с интернетом")


if __name__ == '__main__':
    app()
