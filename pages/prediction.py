import pandas as pd
import streamlit as st
import datetime
import plotly.express as px
import plotly.graph_objects as go
import calendar
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
#from seaborn import sns

def main():
    
    st.title("Forecasting using Time Series model")
    st.write("Here, we will forecast pollutant levels for selected number of days. Well refined data will be used for forecasting, where we have removed majority of potential outliers. ARIMA (Autoregressive Integrated Moving Average) will be used as time series model.")
    data = pd.read_csv(r"C:\Users\Pratik\Desktop\borivali_AQI.csv")
    today1 = datetime.date.today()
    drop = st.selectbox(label="choose pollutants",options=["PM2.5","PM10","NO2","SO2","CO","Ozone"])
    start_date = "2021-01-01"
    end_date = "2023-02-03"
    # Convert the 'Date' column to datetime objects if it's not already
    data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y %H:%M').dt.normalize()

    # Use boolean indexing to select rows within the date range
    data1 = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    data2 = data1.fillna(0) # removing missing values by converting NaN to 0.
    data3 = data2.groupby("Date")[drop].mean()
    #st.dataframe(data3)
    q1 = data3.quantile(0.25) # lower quartile
    q3 = data3.quantile(0.75) # upper quartile
    iqr = q3 - q1
    lb = q1 - 1*iqr #setting lower limit
    ub = q3 + 1*iqr #setting upper limit
    # I have used 1 instead of 1.5, so that every outliers are removed
    poll = data3[(data3 >= lb) & (data3 <= ub)]
    #st.dataframe(poll)
    fig5, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(poll)
    #st.pyplot(fig5)

    from statsmodels.tsa.stattools import adfuller
    adf = adfuller(poll)
    #st.write("ADF stats",round(adf[0],3))
    #st.write("p-value",round(adf[1],3))
    #for key,value in adf[4].items():
       #st.write(f"{key}:{round(value,3)}")

    from statsmodels.tsa.stattools import kpss
    kp = kpss(poll)
    #st.write("kpss stats",round(kp[0],3))
    #st.write("p-value",round(kp[1],3))
    #for key,value in kp[3].items():
       #st.write(f"{key}:{round(value,3)}")
    #st.write("ARIMA model rmse error",rms1)
    st.header("model performance")
    st.write("Before using the model for forecasting, we will calculate Root Mean Squared Error of the model of actual values and values predicted by the model. Less the RMSE, greater is the performance of the model.")
    if drop == "SO2" or drop == "Ozone":
        m1 = ARIMA(poll,order=(2,1,2))
        m1_fit = m1.fit()
        m1_pred = m1_fit.predict(dynamic=False)
        f3 = go.Figure()
        f3.add_trace(go.Scatter(x=poll.index, y=m1_pred, name='actual'))
        f3.add_trace(go.Scatter(x=poll.index, y=poll, name='predicted',line=dict(color="green")))
        f3.update_layout(yaxis=dict(title=dict(text=f"{drop} levels")))
        f3.update_layout(xaxis=dict(title=dict(text=f"Date")))
        st.plotly_chart(f3,use_container_width=True,height=200)
        rms1 = round(np.sqrt(mean_squared_error(poll,m1_pred)),3)
        st.write("RMSE: ",rms1)

        st.header("Forecasting pollutant levels")
        st.write("After evaluating model performance, we will use the model to forecast pollutant levels after Feb 3, 2023. You can also select the number of days, by which the model will forecast for.")
        drop2 = st.selectbox(label="choose days for prediction",options=[30,60,90,120,150,180])
        f_dates = pd.date_range(start="2023-02-03",periods=drop2)
        fr = m1_fit.forecast(steps=drop2)
        fr1 = pd.DataFrame({"Date":f_dates,"pred_value":fr})
        fr1 = fr1.set_index("Date")
        st.subheader("Forecasted values data")
        st.write("The data contains date after Feb 3, 2023 to the days selected by the user, along with values forecasted by the model.")
        st.dataframe(fr1)
        final = pd.concat([poll,fr1])
        #st.dataframe(final)
        st.subheader("Forecasted values graph")
        st.write("Here we plot actual values as well as pollutant levels forecasted.")
        f6 = go.Figure()
        f6.add_trace(go.Scatter(x=final.index, y=final[drop], name='actual',line=dict(color="green")))
        f6.add_trace(go.Scatter(x=final.index, y=final["pred_value"], name='forecast',line=dict(color="red")))
        f6.update_layout(yaxis=dict(title=dict(text=f"{drop} levels")))
        f6.update_layout(xaxis=dict(title=dict(text=f"Date")))
        st.plotly_chart(f6,use_container_width=True,height=200)
    else:
        m1 = ARIMA(poll,order=(2,0,2))
        m1_fit = m1.fit()
        m1_pred = m1_fit.predict(dynamic=False)
        f3 = go.Figure()
        f3.add_trace(go.Scatter(x=poll.index, y=m1_pred, name='actual'))
        f3.add_trace(go.Scatter(x=poll.index, y=poll, name='predicted',line=dict(color="green")))
        f3.update_layout(yaxis=dict(title=dict(text=f"{drop} levels")))
        f3.update_layout(xaxis=dict(title=dict(text=f"Date")))
        st.plotly_chart(f3,use_container_width=True,height=200)
        rms1 = round(np.sqrt(mean_squared_error(poll,m1_pred)),3)
        st.write("RMSE: ",rms1)

        st.header("Forecasting pollutant levels")
        st.write("After evaluating model performance, we will use the model to forecast pollutant levels after Feb 3, 2023. You can also select the number of days, by which the model will forecast for.")
        drop2 = st.selectbox(label="choose days for prediction",options=[30,60,90,120,150,180])
        f_dates = pd.date_range(start="2023-02-03",periods=drop2)
        fr = m1_fit.forecast(steps=drop2)
        fr1 = pd.DataFrame({"Date":f_dates,"pred_value":fr})
        fr1 = fr1.set_index("Date")
        st.subheader("Forecasted values data")
        st.write("The data contains date after Feb 3, 2023 to the days selected by the user, along with values forecasted by the model.")
        st.dataframe(fr1)
        final = pd.concat([poll,fr1])
        #st.dataframe(final)
        st.subheader("Forecasted values graph")
        st.write("Here we plot actual values as well as pollutant levels forecasted.")
        f6 = go.Figure()
        f6.add_trace(go.Scatter(x=final.index, y=final[drop], name='actual',line=dict(color="green")))
        f6.add_trace(go.Scatter(x=final.index, y=final["pred_value"], name='forecast',line=dict(color="red")))
        f6.update_layout(yaxis=dict(title=dict(text=f"{drop} levels")))
        f6.update_layout(xaxis=dict(title=dict(text=f"Date")))
        st.plotly_chart(f6,use_container_width=True,height=200)
if __name__ == "__main__":
    main()
