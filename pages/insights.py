import pandas as pd
import streamlit as st
import datetime
import plotly.express as px
import plotly.graph_objects as go
import calendar
import numpy as np

def main():
    
    st.title("Analytics and Insights")
    st.write("In this page we will perform analysis to gain insights from the filtered data. One thing is also to be noted that for analysis in same year, both start date and end date should have same year to be selected. ")
    data = pd.read_csv(r"C:\Users\Pratik\Desktop\borivali_AQI.csv")
    col1, col2 = st.columns(2)
    today1 = datetime.date.today()
    drop = st.selectbox(label="choose pollutants",options=["PM2.5","PM10","NO2","SO2","CO","Ozone"])
    with col1:
        start = st.date_input("start date",datetime.date(today1.year-2,today1.month,today1.day))
    with col2:
        end = st.date_input("end date",datetime.date(today1.year-2,today1.month,today1.day))
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    # Convert the 'Date' column to datetime objects if it's not already
    data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y %H:%M').dt.normalize()

    # Use boolean indexing to select rows within the date range
    data1 = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    data2 = data1.fillna(0) # removing missing values by converting NaN to 0.
    data3 = data2.groupby("Date")[drop].mean()
    st.header("Daily data")
    st.write("After applying filters we will get the desired data, as well as perform analysis on them to gain insights.")
    st.dataframe(data3)

    st.header("Plots")
    st.write("For analysis, we will select variety of plots from drop down to understand and visualize data.")
    drop1 = st.selectbox(label="choose plots",options=["line","trendlines","scatter"])
    if drop1 == "line":
      f = go.Figure()
      f.add_trace(go.Scatter(x=data3.index, y=data3, name=drop))
      f.update_layout(yaxis=dict(title=dict(text=f"{drop} levels")))
      f.update_layout(xaxis=dict(title=dict(text=f"Date")))
      #f.add_trace(go.Scatter(x=data3.index, y=[15]*365, name='WHO limit for PM2.5',line=dict(color="green")))
      st.plotly_chart(f,use_container_width=True,height=200)
    if drop1 == "trendlines":
      fig = px.scatter(data3, x=data3.index, y=data3, trendline="ewm",trendline_options=dict(halflife=2),trendline_color_override="red")
      #f.add_trace(go.Scatter(x=data3.index, y=[15]*365, name='WHO limit for PM2.5',line=dict(color="green")))
      st.plotly_chart(fig,use_container_width=True,height=200)
    if drop1 == "scatter":
      fig = px.scatter(data3, x=data3.index, y=data3)
      st.plotly_chart(fig,use_container_width=True,height=200)

    st.header("Monthly data")
    st.write("We have obtained monthly data by grouping the previous data into months. In this data numbers from 1 to 12 represents months from January to December.")  
    dx = {"date":data3.index,"levels":data3}
    dis = pd.DataFrame(dx)
    dis = dis.drop("date",axis=1)
    data_anim = dis.groupby(dis.index.month).mean().reset_index()
    data_anim.rename(columns={'Date': 'month'}, inplace=True)
    data_anim

    st.header("Plots for monthly data")
    st.write("For analysis, we will select variety of plots from drop down to understand and visualize data.")
    drop2 = st.selectbox(label="choose plots",options=["line","bar plots","pie charts"])
    data_anim["month"] = data_anim["month"].map(lambda x: calendar.month_abbr[x])
    if drop2 == "line":
      f2 = go.Figure()
      f2.add_trace(go.Scatter(x=data_anim["month"],y=data_anim["levels"]))
      f2.update_layout(yaxis=dict(title=dict(text=f"monthly {drop} levels")))
      f2.update_layout(xaxis=dict(title=dict(text=f"Date")))
      st.plotly_chart(f2,use_container_width=True,height=200)
    if drop2 == "bar plots":
      fig3 = px.histogram(data_anim,x=data_anim["month"],y=data_anim["levels"],nbins=4)
      fig3.update_layout(yaxis=dict(title=dict(text=f"monthly {drop} levels")))
      st.plotly_chart(fig3,use_container_width=True,height=200)
    if drop2 == "pie charts":
      fig3 = px.pie(data_anim,names=data_anim["month"],values=data_anim["levels"],title=f"{drop} level distribution over the months")
      st.plotly_chart(fig3,use_container_width=True,height=200)
    h = data_anim.groupby("month")["levels"].mean()
    xx = pd.DataFrame({"year":h.index,"average":h})
    xyz = np.mean(xx["average"])
    st.header("Average levels from start date to end date")
    if drop == "CO":
      st.write(f"After monthly analysis, average levels of the pollutants will be displayed. Therefore, average {drop} level in mg/mm3")
      st.write(xyz)
    else:
      st.write(f"After monthly analysis, average levels of the pollutants will be displayed. Therefore, average {drop} level in ug/mm3")
      st.write(xyz)
if __name__ == "__main__":
    main()
