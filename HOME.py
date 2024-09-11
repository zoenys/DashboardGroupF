import streamlit as st
import pandas as pd
import plotly.express as px
from mysql_con import get_data
from login import login, logout

# Check login status
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()  # Show login page if not logged in
else:
    def main():
        st.set_page_config(page_title="Home Mining Dashboard", page_icon="⛏", layout="wide")
        st.title(f"Welcome, {st.session_state['username']}!")
        st.sidebar.image("images/T_GROUP-removebg-preview.png")

        # Logout button
        logout()

        # Prepare data for each commodity
        df_minyak_bumi = pd.DataFrame(get_data("minyak_bumi"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])
        df_minyak = pd.DataFrame(get_data("minyak"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])
        df_gas_alam = pd.DataFrame(get_data("gas_alam"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])
        df_biji_tembaga = pd.DataFrame(get_data("biji_tembaga"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])
        df_batu_bara = pd.DataFrame(get_data("batu_bara"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])

        # Show metrics for each commodity separately
        cols = st.columns(5)  # 5 columns for 5 commodities
        try:
            # Sum for the years 2012-2023 for each commodity
            total_minyak_bumi = df_minyak_bumi[[str(year) for year in range(2012, 2024)]].sum().sum()
            total_minyak = df_minyak[[str(year) for year in range(2012, 2024)]].sum().sum()
            total_gas_alam = df_gas_alam[[str(year) for year in range(2012, 2024)]].sum().sum()
            total_biji_tembaga = df_biji_tembaga[[str(year) for year in range(2012, 2024)]].sum().sum()
            total_batu_bara = df_batu_bara[[str(year) for year in range(2012, 2024)]].sum().sum()

            # Display the metric cards for each commodity
            cols[0].metric(label="Total Ton for Minyak Bumi (2012-2023)", value=f"{total_minyak_bumi:,.0f} tons")
            cols[1].metric(label="Total Ton for Minyak (2012-2023)", value=f"{total_minyak:,.0f} tons")
            cols[2].metric(label="Total Ton for Gas Alam (2012-2023)", value=f"{total_gas_alam:,.0f} tons")
            cols[3].metric(label="Total Ton for Biji Tembaga (2012-2023)", value=f"{total_biji_tembaga:,.0f} tons")
            cols[4].metric(label="Total Ton for Batu Bara (2012-2023)", value=f"{total_batu_bara:,.0f} tons")
        except Exception as e:
            st.error(f"Failed to load data: {str(e)}")

        # Sidebar for multiselect options
        st.sidebar.header("Filter by Commodity and Country")

        # Commodity selection in sidebar with default only "minyak_bumi" selected
        selected_commodities = st.sidebar.multiselect("Select Commodity Tables:", 
                                                    ["minyak_bumi", "minyak", "gas_alam", "biji_tembaga", "batu_bara"], 
                                                    default=["minyak_bumi"])

        combined_data = []

        # Process data for the selected commodities
        for commodity in selected_commodities:
            try:
                # Load data for each commodity separately based on selection
                if commodity == "minyak_bumi":
                    df = pd.DataFrame(get_data("minyak_bumi"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])
                elif commodity == "minyak":
                    df = pd.DataFrame(get_data("minyak"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])
                elif commodity == "gas_alam":
                    df = pd.DataFrame(get_data("gas_alam"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])
                elif commodity == "biji_tembaga":
                    df = pd.DataFrame(get_data("biji_tembaga"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])
                elif commodity == "batu_bara":
                    df = pd.DataFrame(get_data("batu_bara"), columns=['Negara Tujuan', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Data'])

                # Country selection in sidebar
                country_key = f"{commodity}_countries"
                if country_key not in st.session_state or not st.session_state[country_key]:
                    st.session_state[country_key] = df['Negara Tujuan'].unique().tolist()  # Default to all countries

                # Multiselect for selecting multiple countries
                selected_countries = st.sidebar.multiselect(f"Select Countries for {commodity.replace('_', ' ').title()}:",
                                                            df['Negara Tujuan'].unique(), key=country_key)

                # Filter data by selected countries
                df_filtered = df[df['Negara Tujuan'].isin(selected_countries)]

                # Pivot data to get years as columns
                if not df_filtered.empty:
                    df_pivot = df_filtered.melt(id_vars=['Negara Tujuan'],
                                                value_vars=[str(year) for year in range(2012, 2024)],
                                                var_name='Year', value_name='Value')
                    df_pivot['Commodity'] = commodity.replace('_', ' ').title()  # Add commodity name for legend
                    df_pivot['Identifier'] = df_pivot['Commodity'] + " - " + df_pivot['Negara Tujuan']  # Unique identifier for color
                    combined_data.append(df_pivot)

            except Exception as e:
                st.error(f"Failed to process data for {commodity}: {str(e)}")

        # Check if there is any data to plot
        if combined_data:
            # Concatenate all commodity data into a single DataFrame
            final_data = pd.concat(combined_data)

            # Convert Year to integer for plotting
            final_data['Year'] = final_data['Year'].astype(int)

            # Line chart visualization for multiple commodities and countries
            fig = px.line(final_data, x='Year', y='Value', color='Identifier',
                        title="Comparative Trends by Commodity and Country",
                        labels={'Value': 'Volume'}, line_dash='Identifier')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected countries and commodities. Please adjust your selections.")

    if __name__ == "__main__":
        main()
