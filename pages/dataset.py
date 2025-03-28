import pandas as pd
import streamlit as st
import datetime
def main():
    st.title("Dataset View")
    st.write("This is an original data that will be used, but we will also feature the data due to presence of missing values. You can also download it for your referrence.")
    data = pd.read_csv(r"borivali_AQI.csv")
    st.dataframe(data,hide_index=True)
    st.header("About the data")
    st.write("Here we will describe the dataset. So this is a dataset of air pollutants containing from year 2021 to 2023. It also has columns such as date and pollutant levels such as PM2.5, PM10, NO2, SO2, CO and Ozone. Lets discuss those pollutants")
    st.header("Pollutants in glace")
    st.write("PM2.5 refers to fine inhalable particles, 2.5 micrometers or smaller in diameter, that can penetrate deep into the lungs and bloodstream, posing a significant health risk.")
    st.write("PM10 refers to inhalable particulate matter with a diameter of 10 micrometers or less, commonly found in dust, smoke, and other airborne particles, which can be inhaled and potentially cause health problems.")
    st.write("Nitrogen dioxide (NO2) is a reddish-brown, pungent gas, a major air pollutant formed by burning fuels, and can cause respiratory problems and contribute to smog and acid rain.")
    st.write("Sulfur dioxide (SO2) is a colorless gas with a pungent odor, a common air pollutant primarily from burning fossil fuels and industrial processes, and a precursor to acid rain.")
    st.write("Carbon monoxide (CO) is a colorless, odorless, and tasteless gas produced by the incomplete burning of fuels like gasoline, natural gas, and wood. It's dangerous because it displaces oxygen in the blood, leading to potentially fatal poisoning.")
    st.write("Ozone pollution, a key component of smog, is a harmful air pollutant formed when nitrogen oxides and volatile organic compounds react in sunlight, particularly on hot, sunny days, and can cause respiratory problems and damage to vegetation.")
    st.header("WHO limit of pollutants")
    st.write("We will discuss WHO limit of the pollutants, which could be useful for analysis")
    df1 = pd.DataFrame({"pollutants":["PM2.5","PM10","NO2","SO2","CO","Ozone"],"WHO limit":["15ug/mm3","45ug/mm3","25ug/mm3","40ug/mm3","4mg/mm3","100ug/mm3"]})
    df1 = df1.reset_index(drop=True)
    st.table(df1.set_index(pd.Index(range(len(df1)))))  # Resets index and displays cleanly

if __name__ == "__main__":
    main()
