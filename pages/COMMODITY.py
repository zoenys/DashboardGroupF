import streamlit as st
import pandas as pd
import plotly.express as px
from mysql_con import get_data

def main():
    st.set_page_config(page_title="Detailed Commodity Analysis", page_icon="📈", layout="wide")
    st.header("Detailed Commodity Analysis")

    # Dropdown for selecting the commodity table
    commodity = st.sidebar.selectbox("Select Commodity Table:", ["minyak_bumi", "minyak", "gas_alam", "biji_tembaga", "batu_bara"])
    commodity_display = commodity.replace('_', ' ').upper()
    st.subheader(f"**{commodity_display}**")

    # Load data from the selected table
    df = pd.DataFrame(get_data(commodity), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])

    # Ensure all numeric columns are converted properly and handle NaN
    try:
        df['Data'] = pd.to_numeric(df['Data'], errors='coerce').fillna(0)
        for year in range(2012, 2024):
            df[str(year)] = pd.to_numeric(df[str(year)], errors='coerce').fillna(0)
    except Exception as e:
        st.error(f"Error converting data types: {e}")

    # Metrics and Visualizations
    st.markdown("## Metrics Cards")
    try:
        most_common_country = df['Negara Tujuan'].value_counts().idxmax()
        count_most_common_country = df['Negara Tujuan'].value_counts().max()

        year_columns = [str(year) for year in range(2012, 2024)]
        total_by_year = df[year_columns].sum()
        max_total_by_year = total_by_year.idxmax()
        value_max_total_by_year = total_by_year[max_total_by_year]

        total_ton = df[year_columns].sum().sum()  # Calculate total tons across all years
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Country with Most Entries", most_common_country, f"{count_most_common_country} times")
    with c2:
        st.metric("Year with Highest Total", max_total_by_year, f"{value_max_total_by_year:,} tons")
    with c3:
        st.metric("Total", f"{total_ton:,} Tons")  # Display total tons

    # Select column year for both bar plot and pie chart
    selected_column = st.selectbox("Choose a Column Year for Annual Distribution Charts:", [str(year) for year in range(2012, 2024)])

    # Create two columns for bar plot and pie chart side by side
    col1, col2 = st.columns(2)

    # Left column: Horizontal Bar Plot
    with col1:
        st.markdown("### Horizontal Bar Plot")
        fig_bar = px.bar(df, x=selected_column, y='Negara Tujuan', color='Negara Tujuan', 
                        title=f"Distribution in {selected_column}",
                        labels={selected_column: "Tons"},
                        orientation='h',  # Horizontal bar plot
                        color_discrete_sequence=px.colors.qualitative.Set3)  # Set different colors for each country
        st.plotly_chart(fig_bar, use_container_width=True)

    # Right column: Pie Chart
    with col2:
        st.markdown("### Pie Chart")
        fig_pie = px.pie(df, names='Negara Tujuan', values=selected_column, title=f"Country-wise Distribution in {selected_column}",
                        color_discrete_sequence=px.colors.qualitative.Set3)  # Set different colors for pie chart
        st.plotly_chart(fig_pie, use_container_width=True)

    st.sidebar.image("images/T_GROUP-removebg-preview.png")

if __name__ == "__main__":
    main()
