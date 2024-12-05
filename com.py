import streamlit as st
import mysql.connector
import pandas as pd

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Keer3009@",  # Replace with your password
            database="keerthana"   # Replace with your database name
        )
        return connection
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Function to fetch data from the database
def fetch_data(query):
    try:
        connection = create_connection()
        if not connection:
            return pd.DataFrame()  # Return empty DataFrame if connection fails
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Function to execute write queries (INSERT, UPDATE, DELETE)
def execute_query(query, params=None):
    try:
        connection = create_connection()
        if not connection:
            return
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()
    except Exception as e:
        st.error(f"Error executing query: {e}")

# Fetch unique values dynamically for dropdowns
def get_unique_values(column_name, table_name="DIC"):
    query = f"SELECT DISTINCT {column_name} FROM {table_name}"
    data = fetch_data(query)
    if column_name in data.columns:
        return data[column_name].dropna().sort_values().tolist()
    return []

# Sidebar content for Table tab only
def render_table_sidebar():
    st.sidebar.header("Filters")
    # Dynamically populate the Year filter
    year_options = ["All"] + get_unique_values("Year_num")
    year_filter = st.sidebar.selectbox("📅 Select Year", options=year_options)

    # Dynamically populate the Region filter
    region_options = ["All"] + get_unique_values("Region_Name")
    region_filter = st.sidebar.selectbox("🌎 Select Region", options=region_options)

    st.sidebar.header("Filter by Category")
    category_filter = st.sidebar.selectbox(
        "📂 Select Data Category", 
        options=["All", "Health Resources", "Maternal Data", "Infant Health"]
    )

    st.sidebar.header("Database Operations")
    operation = st.sidebar.selectbox("⚙️ Select Operation", options=["Lookup", "Add Entry", "Modify Entry", "Remove Entry"])
    return year_filter, region_filter, category_filter, operation

# Set Streamlit page configuration
st.set_page_config(
    page_title="🌟 Insights on Infant Health and Well-Being 🌟",
    layout="wide",
)

# Initialize session state for tab selection
if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = "Home"

# Navigation bar with tabs
def horizontal_menu():
    st.markdown(
        """
        <style>
        .nav-container {
            display: flex;
            justify-content: center;
            background-color: #2C3E50;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .nav-button {
            background-color: #ADD8E6;  /* Light blue background */
            border: none;
            color: white;
            font-weight: bold;
            font-size: 18px;
            margin-right: 2px;  /* Reduced spacing between buttons */
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .nav-button.active {
            background-color: #4682B4; /* Darker blue for active state */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1, 1])  # Maintain equal spacing for alignment
    with col1:
        if st.button("🏠 Home", key="home_button"):
            st.session_state["selected_tab"] = "Home"
    with col2:
        if st.button("📋 Table", key="table_button"):
            st.session_state["selected_tab"] = "Table"
    with col3:
        if st.button("🤖 Model", key="model_button"):
            st.session_state["selected_tab"] = "Model"

# Render the navigation bar
horizontal_menu()

# Update the selected tab based on session state
selected_tab = st.session_state["selected_tab"]

# Home Tab Content
if selected_tab == "Home":
    st.title("🌟 Empowering Health Insights: Understanding Maternal and Infant Well-being 🌟")
    
    st.markdown("""
    ### Subtitle
    *Our platform explores the intricate connections between maternal health, education, healthcare resources, and their effects on infant mortality and maternal outcomes.*
    """)
    
    st.markdown("""
    ## What We Achieve
    Our goal is to provide actionable insights that drive meaningful discussions and policies for maternal and infant health improvements. Here's what we offer:
    - **📊 Data-Driven Insights:** Analyze trends and correlations in global health metrics.
    - **🤝 User Engagement:** Empower users to add, update, and explore data for continuous learning.
    - **🤖 Predictive Modeling:** Utilize our machine learning models to predict health outcomes based on user-provided data.
    - **🎯 Customizable Filters:** Visualize and study health data by region, year, and demographic categories.
    """)

    st.markdown("""
    ## What You Can Do Here
    - **🔍 Explore Existing Data:** Use interactive filters to view trends and patterns.
    - **📈 Run Predictions:** Input data and get model-generated health predictions.
    - **📝 Contribute Data:** Add or modify entries to expand and refine the dataset.
    - **📊 Analyze Trends:** Discover how factors like healthcare resources, literacy, and immunization impact outcomes.
    """)

    st.markdown("""
    ## Impact of Our Work
    - **🌍 Policy Influence:** Equip policymakers with insights to make informed decisions.
    - **💪 Health Advocacy:** Support organizations and communities in addressing maternal and infant health challenges.
    - **📢 Global Awareness:** Highlight disparities and promote equitable healthcare access.
    """)

    st.markdown("""
    ---
    ### About the Project
    **Leveraging Health Data to Predict Infant Survival and Wellbeing from Pregnancy to Early Childhood**

    This project is designed to bridge the gap between available data and actionable insights, ensuring better healthcare outcomes for mothers and infants. Key aspects include:

    - **Analyzing Health Data:** By leveraging global datasets, we aim to identify patterns and correlations in maternal and infant health.
    - **Predicting Health Outcomes:** Our predictive models use machine learning to forecast infant survival rates and maternal well-being metrics.
    - **Interactive Platform:** Users can explore data by regions, years, and specific health categories, making the platform user-friendly and adaptable.
    - **Advocating for Change:** The insights generated empower healthcare organizations and policymakers to take data-driven decisions, improving resource allocation and accessibility.
    
    Together, we aim to create a platform that not only informs but also inspires meaningful change in global health outcomes.
    """)

# Table Tab Content
elif selected_tab == "Table":
    st.title("📋 Insights on Infant Health and Well-Being")
    st.markdown("This page allows you to filter and explore the health data from your database.")
    
    # Sidebar filters and operations
    year_filter, region_filter, category_filter, operation = render_table_sidebar()

    # Fetch all data from the database
    query = "SELECT * FROM DIC"
    data = fetch_data(query)

    if not data.empty:
        if year_filter != "All":
            data = data[data["Year_num"] == int(year_filter)]
        if region_filter != "All":
            data = data[data["Region_Name"] == region_filter]

        # Apply category filter
        if category_filter == "Health Resources":
            columns_to_display = [
                "Hospital_beds_per_1000_people", "Immunization_BCG_percent_of_one_year_old_children",
                "Immunization_HepB3_percent_of_one_year_old_children", "Immunization_measles_second_dose",
                "Immunization_Pol3_percent_of_one_year_old_children", "Physicians_per_1000_people",
                "Births_attended_by_skilled_health_staff_percent_of_total"
            ]
            data = data[columns_to_display]

        elif category_filter == "Maternal Data":
            columns_to_display = [
                "Pregnant_women_receiving_prenatal_care_percent", "Prevalence_of_anemia_among_pregnant_women_percent",
                "Prevalence_of_current_tobacco_use_pregnant_women", "Prevalence_of_hypertension_pregnant_women"
            ]
            data = data[columns_to_display]

        elif category_filter == "Infant Health":
            columns_to_display = [
                "Low_birthweight_babies_percent_of_births", "Mortality_rate_infant_per_1000_live_births",
                "Mortality_rate_infant_female_per_1000_live_births", "Mortality_rate_infant_male_per_1000_live_births",
                "Mortality_rate_neonatal_per_1000_live_births", "Newborns_protected_against_tetanus",
                "Number_of_infant_deaths", "Number_of_infant_deaths_female", "Number_of_infant_deaths_male",
                "Number_of_maternal_deaths", "Number_of_neonatal_deaths", "Number_of_stillbirths",
                "Stillbirth_rate_per_1000_total_births", "Infant_Mortality_Rate_to_Birth_Rate_Ratio"
            ]
            data = data[columns_to_display]

        if operation == "Lookup":
            st.subheader("Lookup Data")
            st.dataframe(data)
        elif operation == "Add Entry":
            st.subheader("🆕 Add New Data Entry")
            new_data = {}
            for column in data.columns:
                new_data[column] = st.text_input(f"Enter value for {column}")
            if st.button("✨ Add Entry"):
                query = f"INSERT INTO DIC ({', '.join(new_data.keys())}) VALUES ({', '.join(['%s'] * len(new_data))})"
                execute_query(query, tuple(new_data.values()))
                st.success("🎉 Entry added successfully!")
        elif operation == "Modify Entry":
            st.subheader("✏️ Modify Existing Entry")
            row_id = st.text_input("Enter the ID of the row to modify")
            if row_id:
                row_data = fetch_data(f"SELECT * FROM DIC WHERE id = {row_id}")
                if not row_data.empty:
                    updated_data = {}
                    for column in data.columns:
                        updated_data[column] = st.text_input(f"Update {column}", row_data[column].iloc[0])
                    if st.button("🔄 Modify Entry"):
                        set_clause = ", ".join([f"{col} = %s" for col in updated_data.keys()])
                        query = f"UPDATE DIC SET {set_clause} WHERE id = {row_id}"
                        execute_query(query, tuple(updated_data.values()))
                        st.success("✅ Entry updated successfully!")
                else:
                    st.warning("⚠️ Row not found.")
        elif operation == "Remove Entry":
            st.subheader("🗑️ Remove Data Entry")
            row_id = st.text_input("Enter the ID of the row to delete")
            if st.button("🗑️ Remove Entry"):
                query = "DELETE FROM DIC WHERE id = %s"
                execute_query(query, (row_id,))
                st.success("🗑️ Entry removed successfully!")

# Model Tab Content
elif selected_tab == "Model":
    st.title("🤖 Predictive Models")
    st.markdown("### 🚧 This page is under construction 🚧")
    st.info("🤖 Here you'll find predictions using machine learning models.")
