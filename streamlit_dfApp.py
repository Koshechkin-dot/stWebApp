import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import mannwhitneyu, chi2_contingency

def run():
    columns = []
    selectableTests = ["Mann Whitney test", "Chi2 contingency test"]
    st.title("DataFrame App")
    file = st.file_uploader("Choose a dataset (ends with .csv)")
    if file is not None:
        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            st.error("No data in dataset")        
        except pd.errors.ParserError:
            st.error("Can not parse") 
        if df.dropna().empty:
            st.error("Dataset is empty")
        else:
            columns = df.columns.to_list()   

        fst = st.selectbox(
            "Choose first column", 
            columns
        )
        sec = st.selectbox(
            "Choose second column",
            columns
        )
        st.header("Plotting")
        if df[fst].dtype == "object":
            st.write(f"{fst} is none numeric type, please select other column")  
        elif df[sec].dtype == "object":
            st.write(f"{sec} is none numeric type, please select other column")    
        else:
            fig = px.histogram(df, x = fst, y = sec)
            st.plotly_chart(fig)


        st.header("Hypothesis testing")
        test = st.selectbox("Select test", selectableTests)
        if test == "Mann Whitney test":
            _, pvalue = mannwhitneyu(df[fst], df[sec])
            st.write(f"Mann Whitney test result: {pvalue:.3f}")
        if test == "Chi2 contingency test":
            contingency_table = pd.crosstab(df[fst], df[sec])
            _, pvalue, _, _ = chi2_contingency(contingency_table)
            st.write(f"Chi2 contingency test result: {pvalue:.3f}")

if __name__=='__main__':
    run()