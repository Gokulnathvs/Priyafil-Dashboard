import pandas as pd  # pip install pandas openpyxl

from PIL import Image
import streamlit as st  # pip install streamlit
import plotly.express as px  # pip install plotly-express

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title = "Priyafil | Dashboard", page_icon = ":peacock:", layout = "wide")

def page1():
       
       
    # ---- READ EXCEL ----
    df = pd.read_excel(
        io = "MONTH YEAR WISE AGGREGATED.xlsx",
        engine = "openpyxl",
        sheet_name = "MONTH YEAR WISE AGGREGATED",
        skiprows = 0,
        usecols = "A:L",
        nrows = 10000,
    )


    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")

    year = st.sidebar.multiselect(
        "Select the Year ID:",
        options = df["TIME Y ID"].unique(),
        default = df["TIME Y ID"].unique(),
    )

    month = st.sidebar.multiselect(
        "Select the Month:",
        options = df["TIME M ID"].unique(),
        default = df["TIME M ID"].unique(),
    )

    df_selection = df[
        (df["TIME Y ID"].isin(year)) & 
        (df["TIME M ID"].isin(month))
    ]


    # ---- MAINPAGE ----
    st.title("📊 Dashboard")
    st.markdown("##")


    # TOP KPI's
    totalFabricatedMtrs = int(df_selection["FABRIC MTRS"].sum())
    totalFabricatedKgs = int(df_selection["FABRIC KGS"].sum())
    totalSalesMtrs = int(df_selection["SOLD MTRS"].sum())
    totalSalesKgs = int(df_selection["SOLD KGS"].sum())
    totalSalesAmount = int(df_selection["AMOUNT"].sum())

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

    # Display the filtered DataFrame
    st.dataframe(df_selection)

    # SALES FOR EACH YEAR [PIE CHART]
    sales_by_Year = df_selection.groupby(by = ["TIME Y ID"]).sum()["AMOUNT"]

    fig_product_salesYear = px.pie(
        names = sales_by_Year.index,
        values = sales_by_Year,
        title = "<b> Sales in Amount for each Year </b>",
        color_discrete_sequence=px.colors.qualitative.Set3,
        template = "plotly_white"
    )

    fig_product_salesYear.update_traces(textposition = 'inside', textinfo = 'label')

    st.plotly_chart(fig_product_salesYear)

    # LINE PLOT FOR TIME
    salesYear_by_Amt = df_selection.groupby(by = ["TIME ID"]).sum()[["AMOUNT"]]

    fig_product_salesYAmt = px.line(
        salesYear_by_Amt,
        x = salesYear_by_Amt.index,
        y = ["AMOUNT"],
        title = "<b> Sales in Amount for each Year and Month </b>",
        color_discrete_sequence = ["#E71111"],
        template = "plotly_white",
    )

    fig_product_salesYAmt.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid = False),
        yaxis = dict(title = "Sum of Amount",
                tickformat = ',d')
    )

    st.plotly_chart(fig_product_salesYAmt)

    # BAR CHART FOR COUNT OF ITEM ID FOR EACH YEAR
    salesCount_by_Year = (
        df_selection.groupby(by=["TIME Y ID"])["ITEM ID"].nunique()
    )

    fig_product_salesYCount = px.bar(
        salesCount_by_Year,
        x=salesCount_by_Year.index,
        y=["ITEM ID"],
        orientation="v",
        title="<b>Count of Item ID for each Year</b>",
        color_discrete_sequence=["#C70039"],
        template="plotly_white"
    )

    fig_product_salesYCount.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_salesYCount.update_layout(
        yaxis=dict(
            title="Count",
            tickformat=',d'
        )
    )

    st.plotly_chart(fig_product_salesYCount)


    # SALES FOR EACH YEAR [BAR CHART]
    salesKgs_by_Year = (
        df_selection.groupby(by=["TIME Y ID"]).sum()[["SOLD KGS"]]
    )

    fig_product_salesYKgs = px.bar(
        salesKgs_by_Year,
        x=salesKgs_by_Year.index,
        y=["SOLD KGS"],
        orientation="v",
        title="<b> Sales in Kilograms for each Year </b>",
        color_discrete_sequence=["#FFC300"],
        template="plotly_white"
    )

    fig_product_salesYKgs.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_salesYKgs.update_layout(
        yaxis=dict(
            title="Sum of Kgs",
            tickformat=',d'
        )
    )

    salesAmt_by_Year = (
        df_selection.groupby(by=["TIME Y ID"]).sum()[["AMOUNT"]]
    )

    fig_product_salesYAmt = px.bar(
        salesAmt_by_Year,
        x=salesAmt_by_Year.index,
        y=["AMOUNT"],
        orientation="v",
        title="<b> Sales in Amount for each Year </b>",
        color_discrete_sequence=["#FFC300"],
        template="plotly_white"
    )

    fig_product_salesYAmt.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_salesYAmt.update_layout(
        yaxis=dict(
            title="Sum of Amount",
            tickformat=',d'
        )
    )

    c1, c2 = st.columns(2)
    c1.plotly_chart(fig_product_salesYKgs, use_container_width=True)
    c2.plotly_chart(fig_product_salesYAmt, use_container_width=True)

    # SALES FOR EACH MONTH [BAR CHART]
    salesKgs_by_Month = (
        df_selection.groupby(by=["TIME M ID"]).sum()[["SOLD KGS"]]
    )

    fig_product_salesMKgs = px.bar(
        salesKgs_by_Month,
        x=salesKgs_by_Month.index,
        y=["SOLD KGS"],
        orientation="v",
        title="<b> Sales in Kilograms for each Month </b>",
        color_discrete_sequence=["#3FD771"],
        template="plotly_white"
    )

    fig_product_salesMKgs.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_salesMKgs.update_layout(
        yaxis=dict(
            title="Sum of Kgs",
            tickformat=',d'
        )
    )

    salesAmt_by_Month = (
        df_selection.groupby(by=["TIME M ID"]).sum()[["AMOUNT"]]
    )

    fig_product_salesMAmt = px.bar(
        salesAmt_by_Month,
        x=salesAmt_by_Month.index,
        y=["AMOUNT"],
        orientation="v",
        title="<b> Sales in Amount for each Month </b>",
        color_discrete_sequence=["#3FD771"],
        template="plotly_white"
    )

    fig_product_salesMAmt.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_salesMAmt.update_layout(
        yaxis=dict(
            title="Sum of Amount",
            tickformat=',d'
        )
    )

    c1, c2 = st.columns(2)
    c1.plotly_chart(fig_product_salesMKgs, use_container_width=True)
    c2.plotly_chart(fig_product_salesMAmt, use_container_width=True)


    # SALES BY STATE ID [BAR CHART]
    salesKgs_by_stateID = (
        df_selection.groupby(by=["STATE ID"]).sum()[["SOLD KGS"]]
    )

    fig_product_salesKgs = px.bar(
        salesKgs_by_stateID,
        x=salesKgs_by_stateID.index,
        y=["SOLD KGS"],
        orientation="v",
        title="<b> Sales in Kilograms for each State </b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )

    fig_product_salesKgs.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_salesKgs.update_layout(
        yaxis=dict(
            title="Sum of Kgs",
            tickformat=',d'  # Display numbers with commas as thousands separator
        )
    )

    salesAmt_by_stateID = (
        df_selection.groupby(by=["STATE ID"]).sum()[["AMOUNT"]]
    )

    fig_product_salesAmt = px.bar(
        salesAmt_by_stateID,
        x=salesAmt_by_stateID.index,
        y=["AMOUNT"],
        orientation="v",
        title="<b> Sales in Amount for each State </b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )

    fig_product_salesAmt.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_salesAmt.update_layout(
        yaxis=dict(
            title="Sum of Amount",
            tickformat=',d'
        )
    )

    c1, c2 = st.columns(2)
    c1.plotly_chart(fig_product_salesKgs, use_container_width=True)
    c2.plotly_chart(fig_product_salesAmt, use_container_width=True)


    # TOP 5 MONTHS
    top_5_Months = (
        df_selection.groupby(by = ["TIME M ID"]).sum()[["AMOUNT"]].nlargest(5, "AMOUNT")
    )

    fig_product_top_5_Months = px.bar(
        top_5_Months,
        x=top_5_Months.index,
        y=["AMOUNT"],
        orientation="v",
        title="<b> TOP 5 Months  </b>",
        color_discrete_sequence=["#3FD771"],
        template="plotly_white"
    )

    fig_product_top_5_Months.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_top_5_Months.update_layout(
        yaxis=dict(
            title="Sum of Amount",
            tickformat=',d'
        )
    )

    st.plotly_chart(fig_product_top_5_Months)


    # TOP 5 PARTY
    top_5_PartyID = (
        df_selection.groupby(by=["PARTY ID"]).sum()[["AMOUNT"]].nlargest(5, "AMOUNT")
    )

    fig_product_top_5_PartyID = px.bar(
        top_5_PartyID,
        x=top_5_PartyID.index,
        y=["AMOUNT"],
        orientation="v",
        title="<b> TOP 5 Party </b>",
        color_discrete_sequence=["#C70039"],
        template="plotly_white"
    )

    fig_product_top_5_PartyID.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_top_5_PartyID.update_layout(
        yaxis=dict(
            title="Sum of Amount",
            tickformat=",d"
        )
    )

    st.plotly_chart(fig_product_top_5_PartyID)


    # TOP 5 STATE
    top_5_StateID = (
        df_selection.groupby(by=["STATE ID"]).sum()[["AMOUNT"]].nlargest(5, "AMOUNT")
    )

    fig_product_top_5_StateID = px.bar(
        top_5_StateID,
        x=top_5_StateID.index,
        y=["AMOUNT"],
        orientation="v",
        title="<b> TOP 5 State </b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )

    fig_product_top_5_StateID.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    fig_product_top_5_StateID.update_layout(
        yaxis=dict(
            title="Sum of Amount",
            tickformat=",d"
        )
    )

    st.plotly_chart(fig_product_top_5_StateID)







    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    
def page2():
       
    # Your content for Page 2 goes here

    st.title("📈 Plotting Area")
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
            options=['Bar Chart', 'Pie Chart', 'Scatterplot', 'Lineplot', 'Top 5', 'Bottom 5']
        )

        if chart_select == 'Bar Chart':
            st.sidebar.subheader("Bar Plot Settings")
            try:
                x_values = st.sidebar.selectbox('X axis', numeric_columns)
                y_values = st.sidebar.selectbox('Y axis', numeric_columns)

                aggregated_data = df_selection.groupby(x_values)[y_values].sum().reset_index()
                plot = px.bar(data_frame=aggregated_data, x=x_values, y=y_values,
                              color_discrete_sequence=["#2E86C1"], 
                              template="plotly_white")

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
                plot = px.scatter(data_frame=df_selection, x=x_values, y=y_values,
                                  color_discrete_sequence=["#424949"], 
                                  template="plotly_white",
                                  trendline='ols')
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
                plot = px.line(data_frame=aggregated_data, x=x_values, y=y_values,
                               color_discrete_sequence=["#E71111"],
                                template="plotly_white")

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
                plot = px.bar(data_frame=aggregated_data, x=x_values, y=y_values,
                              color_discrete_sequence=["#C70039"],
                              template="plotly_white")

                # Format y-axis tick labels
                plot.update_layout(yaxis=dict(tickformat='.0f'))

                # Display charts
                st.plotly_chart(plot)
            except Exception as e:
                st.sidebar.error("Error: " + str(e))
                
        elif chart_select == 'Bottom 5':
            st.sidebar.subheader("Bottom 5 Settings")
            try:
                x_values = st.sidebar.selectbox('X axis', numeric_columns)
                y_values = st.sidebar.selectbox('Y axis', numeric_columns)

                aggregated_data = df_selection.groupby(x_values)[y_values].sum().reset_index()
                aggregated_data = aggregated_data.nsmallest(5, y_values)  # Use nsmallest() to get the bottom 5 values
                plot = px.bar(data_frame=aggregated_data, x=x_values, y=y_values,
                            color_discrete_sequence=["#F16E0D "],
                            template="plotly_white")

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
    
 
def page3():
    # main page logo
    logo_image2 = Image.open('50years.png')
    resized_image = logo_image2.resize((100,100))
    st.image(resized_image)
    
    # Title
    st.title(":peacock: Welcome to Priyafil")
    
    # sidebar logo
    logo_image1 = Image.open('PriyafilLogo.png')
    st.sidebar.image(logo_image1, use_column_width=True)
    
 
    
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Home", "Dashboard", "Plotting Area"))

    # Conditionally display the selected page
    if page == "Home":
        page3()
    elif page == "Dashboard":
        page1()
    elif page == "Plotting Area":
        page2()


# ... Define other pages if needed

if __name__ == "__main__":
    main()
