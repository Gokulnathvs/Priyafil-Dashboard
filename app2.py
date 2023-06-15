import pandas as pd  # pip install pandas openpyxl

from PIL import Image
import streamlit as st  # pip install streamlit
import plotly.express as px  # pip install plotly-express

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard 2", page_icon=":bar_chart:", layout="wide")

# sidebar logo
logo_image1 = Image.open('PriyafilLogo.png')
st.sidebar.image(logo_image1, use_column_width=True)

# main page logo
logo_image2 = Image.open('50years.png')
resized_image = logo_image2.resize((100,100))
st.image(resized_image)

st.title(":bar_chart: Dashboard")
st.sidebar.subheader("Visualization Settings")

# To set up a file
uploaded_file = st.sidebar.file_uploader(
    label="Upload your CSV file or Excel file", type=['csv', 'xlsx'])

global df
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        df = pd.read_excel(uploaded_file)

        # TOP KPI's
        totalFabricatedMtrs = int(df["FABRIC MTRS"].sum())
        totalFabricatedKgs = int(df["FABRIC KGS"].sum())
        totalSalesMtrs = int(df["SOLD MTRS"].sum())
        totalSalesKgs = int(df["SOLD KGS"].sum())
        totalSalesAmount = int(df["AMOUNT"].sum())

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.subheader("Total Fabricated in Mtrs:")
            st.subheader(f"{totalFabricatedMtrs:,}")
        with c2:
            st.subheader("Total Fabricated in Kgs:")
            st.subheader(f"{totalFabricatedKgs:,}")
        with c3:
            st.subheader("Total Sales in Mtrs:")
            st.subheader(f"{totalSalesMtrs:,}")
        with c4:
            st.subheader("Total Sales in Kgs:")
            st.subheader(f"{totalSalesKgs:,}")
        with c5:
            st.subheader("Total Sales in Amount:")
            st.subheader(f"{totalSalesAmount:,}")

        st.markdown("""---""")

    global numeric_columns
    try:
        st.write(df)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    except Exception as e:
        st.write('Please Upload file to the application')

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")

    year = st.sidebar.multiselect(
        "Select the Year ID:",
        options=df["TIME Y ID"].unique(),
        default=df["TIME Y ID"].unique(),
    )

    month = st.sidebar.multiselect(
        "Select the Month:",
        options=df["TIME M ID"].unique(),
        default=df["TIME M ID"].unique(),
    )

    df_selection = df[
        (df["TIME Y ID"].isin(year)) &
        (df["TIME M ID"].isin(month))
    ]
    
    
    
    # TOP KPI's based on selected filters
    totalFabricatedMtrs_filtered = int(df_selection["FABRIC MTRS"].sum())
    totalFabricatedKgs_filtered = int(df_selection["FABRIC KGS"].sum())
    totalSalesMtrs_filtered = int(df_selection["SOLD MTRS"].sum())
    totalSalesKgs_filtered = int(df_selection["SOLD KGS"].sum())
    totalSalesAmount_filtered = int(df_selection["AMOUNT"].sum())

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.subheader("Total Fabricated in Mtrs:")
        st.subheader(f"{totalFabricatedMtrs_filtered:,}")
    with c2:
        st.subheader("Total Fabricated in Kgs:")
        st.subheader(f"{totalFabricatedKgs_filtered:,}")
    with c3:
        st.subheader("Total Sales in Mtrs:")
        st.subheader(f"{totalSalesMtrs_filtered:,}")
    with c4:
        st.subheader("Total Sales in Kgs:")
        st.subheader(f"{totalSalesKgs_filtered:,}")
    with c5:
        st.subheader("Total Sales in Amount:")
        st.subheader(f"{totalSalesAmount_filtered:,}")
        
    st.markdown("""---""")
    

    # Add a select widget for the sidebar
    chart_select = st.sidebar.selectbox(
        label="Select the chart type",
        options=['Bar Chart', 'Pie Chart', 'Scatterplot', 'Lineplot', 'Histogram', 'Top 5']
    )

    if chart_select == 'Bar Chart':
        st.sidebar.subheader("Bar Plot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', numeric_columns)

            aggregated_data = df_selection.groupby(x_values)[y_values].sum().reset_index()
            plot = px.bar(data_frame=aggregated_data, x=x_values, y=y_values)

            # Format y-axis tick labels
            plot.update_layout(yaxis=dict(tickformat='.0f'))

            # Display charts
            st.plotly_chart(plot)
        except Exception as e:
            st.sidebar.error("Error: " + str(e))

    elif chart_select == 'Scatterplot':
        st.sidebar.subheader("Scatterplot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', numeric_columns)
            plot = px.scatter(data_frame=df_selection, x=x_values, y=y_values)
            # Display charts
            st.plotly_chart(plot)
        except Exception as e:
            st.sidebar.error("Error: " + str(e))

    elif chart_select == 'Lineplot':
        st.sidebar.subheader("Line Plot Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', numeric_columns)
            
            aggregated_data = df_selection.groupby(x_values)[y_values].sum().reset_index()
            plot = px.line(data_frame=aggregated_data, x=x_values, y=y_values)

            # Display charts
            st.plotly_chart(plot)
        except Exception as e:
            st.sidebar.error("Error: " + str(e))

    elif chart_select == 'Pie Chart':
        st.sidebar.subheader("Pie Chart Settings")
        try:
            x_values = st.sidebar.selectbox('Labels', numeric_columns)
            y_values = st.sidebar.selectbox('Values', numeric_columns)

            plot = px.pie(data_frame=df_selection, names=x_values, values=y_values)

            # Display charts
            st.plotly_chart(plot)
        except Exception as e:
            st.sidebar.error("Error: " + str(e))


    elif chart_select == 'Top 5':
        st.sidebar.subheader("Top 5 Settings")
        try:
            x_values = st.sidebar.selectbox('X axis', numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', numeric_columns)

            aggregated_data = df_selection.groupby(x_values)[y_values].sum().reset_index()
            aggregated_data = aggregated_data.nlargest(5, y_values)
            plot = px.bar(data_frame=aggregated_data, x=x_values, y=y_values)

            # Format y-axis tick labels
            plot.update_layout(yaxis=dict(tickformat='.0f'))

            # Display charts
            st.plotly_chart(plot)
        except Exception as e:
            st.sidebar.error("Error: " + str(e))

    
    
    
else:
    st.write('Please Upload file to the application')






# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
    
    
