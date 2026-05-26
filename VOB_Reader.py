import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# PAGE CONFIG


st.set_page_config(
    page_title="Vendor Order Book Dashboard",
    layout="wide"
)


# TITLE


st.title("Vendor Order Book Dashboard")


# FILE UPLOAD


file = st.file_uploader(
    "Upload VOB File",
    type=["csv", "xlsx"]
)


# MAIN LOGIC


if file:

    
    # READ FILE
    

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    
    # OVERALL TEAM PERFORMANCE
    

    st.header("Overall Team Performance")

    # Overall KPI Calculations

    total_po = df["Purchase Document"].nunique()

    total_buyers = df["Buyer Name*"].nunique()

    total_vendors = df["Vendor Name"].nunique()

    # Overall Unconfirmed
    overall_unconfirmed = df[
        df["Vendor Confirmation – Detailed*"] == "NOT Confirmed by Vendor"
    ]

    overall_unconfirmed_po = overall_unconfirmed[
        "Purchase Document"
    ].nunique()

    # Overall Overdue
    overall_overdue = df[
        df["Overdue Status – Detailed*"] == "OVERDUE"
    ]

    overall_overdue_po = overall_overdue[
        "Purchase Document"
    ].nunique()

    # Overall Scrap
    overall_scrap = df[
        df["Scrap Line*"] == "Y"
    ]

    overall_scrap_po = overall_scrap[
        "Purchase Document"
    ].nunique()

    
    # OVERALL KPI DISPLAY
    

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total POs",
            total_po
        )

    with col2:
        st.metric(
            "Total Buyers",
            total_buyers
        )

    with col3:
        st.metric(
            "Total Vendors",
            total_vendors
        )

    st.divider()

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Overall Unconfirmed POs",
            overall_unconfirmed_po
        )

    with col5:
        st.metric(
            "Overall Overdue POs",
            overall_overdue_po
        )

    with col6:
        st.metric(
            "Overall Scrap POs",
            overall_scrap_po
        )

    
    # OVERALL CHARTS
    

    st.subheader("Overall PO Health Analysis")

    overall_summary_df = pd.DataFrame({
        "Category": [
            "Unconfirmed",
            "Overdue",
            "Scrap"
        ],
        "Count": [
            overall_unconfirmed_po,
            overall_overdue_po,
            overall_scrap_po
        ]
    })

    overall_chart1, overall_chart2 = st.columns(2)

    # Overall Pie Chart
    with overall_chart1:

        overall_pie = px.pie(
            overall_summary_df,
            names="Category",
            values="Count",
            title="Overall PO Status Distribution"
        )

        st.plotly_chart(
            overall_pie,
            use_container_width=True
        )

    # Overall Bar Chart
    with overall_chart2:

        overall_bar = px.bar(
            overall_summary_df,
            x="Category",
            y="Count",
            title="Overall PO Status Comparison"
        )

        st.plotly_chart(
            overall_bar,
            use_container_width=True
        )

    st.divider()

    
    # FILTER SECTION
    

    st.header("Buyer / Vendor Analysis")

    st.sidebar.header("Filters")

    filter_type = st.sidebar.radio(
        "Filter By",
        ["Buyer", "Vendor"]
    )

    
    # BUYER FILTER
    

    if filter_type == "Buyer":

        buyer_list = sorted(
            df["Buyer Name*"].dropna().unique().tolist()
        )

        selected_buyer = st.sidebar.selectbox(
            "Select Buyer",
            buyer_list
        )

        filtered_df = df[
            df["Buyer Name*"] == selected_buyer
        ]

        st.subheader(
            f"Buyer Analysis : {selected_buyer}"
        )

    
    # VENDOR FILTER
    

    else:

        vendor_list = sorted(
            df["Vendor Name"].dropna().unique().tolist()
        )

        selected_vendor = st.sidebar.selectbox(
            "Select Vendor",
            vendor_list
        )

        filtered_df = df[
            df["Vendor Name"] == selected_vendor
        ]

        st.subheader(
            f"Vendor Analysis : {selected_vendor}"
        )

    
    # FILTERED KPI CALCULATIONS
    

    # Unconfirmed
    unconfirmed = filtered_df[
        filtered_df["Vendor Confirmation – Detailed*"] == "NOT Confirmed by Vendor"
    ]

    unconfirmed_po = unconfirmed[
        "Purchase Document"
    ].nunique()

    # Overdue
    overdue = filtered_df[
        filtered_df["Overdue Status – Detailed*"] == "OVERDUE"
    ]

    overdue_po = overdue[
        "Purchase Document"
    ].nunique()

    # Scrap
    scrap = filtered_df[
        filtered_df["Scrap Line*"] == "Y"
    ]

    scrap_po = scrap[
        "Purchase Document"
    ].nunique()

    
    # FILTERED KPI DISPLAY
    

    col7, col8, col9 = st.columns(3)

    with col7:
        st.metric(
            "Unconfirmed POs",
            unconfirmed_po
        )

    with col8:
        st.metric(
            "Overdue POs",
            overdue_po
        )

    with col9:
        st.metric(
            "Scrap POs",
            scrap_po
        )

    
    # FILTERED CHARTS
    

    st.subheader(f"{filter_type} PO Health Analysis")

    filtered_summary_df = pd.DataFrame({
        "Category": [
            "Unconfirmed",
            "Overdue",
            "Scrap"
        ],
        "Count": [
            unconfirmed_po,
            overdue_po,
            scrap_po
        ]
    })

    filtered_chart1, filtered_chart2 = st.columns(2)

    # Filtered Pie Chart
    with filtered_chart1:

        filtered_pie = px.pie(
            filtered_summary_df,
            names="Category",
            values="Count",
            title=f"{filter_type} PO Status Distribution"
        )

        st.plotly_chart(
            filtered_pie,
            use_container_width=True
        )

    # Filtered Bar Chart
    with filtered_chart2:

        filtered_bar = px.bar(
            filtered_summary_df,
            x="Category",
            y="Count",
            title=f"{filter_type} PO Status Comparison"
        )

        st.plotly_chart(
            filtered_bar,
            use_container_width=True
        )

    
    # FILTERED DATA
    

    st.subheader("Filtered Data")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    
    # DETAIL TABS
    

    tab1, tab2, tab3 = st.tabs([
        "Unconfirmed Details",
        "Overdue Details",
        "Scrap Details"
    ])

    
    # UNCONFIRMED TAB
    

    with tab1:

        st.subheader("Unconfirmed PO Details")

        st.write(
            "Total Lines:",
            unconfirmed.shape[0]
        )

        st.dataframe(
            unconfirmed,
            use_container_width=True
        )

    
    # OVERDUE TAB
    

    with tab2:

        st.subheader("Overdue PO Details")

        st.write(
            "Total Lines:",
            overdue.shape[0]
        )

        st.dataframe(
            overdue,
            use_container_width=True
        )

    
    # SCRAP TAB
    

    with tab3:

        st.subheader("Scrap PO Details")

        st.write(
            "Total Lines:",
            scrap.shape[0]
        )

        st.dataframe(
            scrap,
            use_container_width=True
        )


# NO FILE UPLOADED


else:

    st.info(
        "Please upload a CSV or Excel file to get started."
    )
