# import streamlit as st
# from db_helper import predict
#
# st.title("CodeX Beverage : Price Prediction")
#
# row1 = st.columns(4)
# row2 = st.columns(4)
# row3 = st.columns(4)
# row4 = st.columns(4)
#
# with row1[0]:
#     age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28)
# with row1[1]:
#     gender = st.selectbox('Gender',['Male','Female'])
# with row1[2]:
#     zone = st.selectbox('Zone', ['Urban', 'Semi-Urban', 'Metro', 'Rural'])
# with row1[3]:
#     occupation = st.selectbox('Occupation', ['Working Professional', 'Student', 'Entrepreneur', 'Retired'])
#
# with row2[0]:
#     income_level = st.selectbox('Income Level', ['<10L', '> 35L', '16L - 25L', 'Not Reported', '10L - 15L',
#        '26L - 35L'])
# with row2[1]:
#     consumer_frequency = st.selectbox('Consumer frequency(weekly)',['3-4 times', '5-7 times', '0-2 times'])
# with row2[2]:
#     current_brand = st.selectbox('Current Brand',['Newcomer','Established'])
# with row2[3]:
#     consumption_size = st.selectbox('Preferable Consumption Size', ['Medium (500 ml)', 'Large (1 L)', 'Small (250 ml)'])
#
# with row3[0]:
#     awareness_of_other_brands = st.selectbox('Awareness of other brands', ['0 to 1', '2 to 4', 'above 4'])
# with row3[1]:
#     reasons_for_choosing_brands = st.selectbox('Reasons for choosing brands',['Price', 'Quality', 'Availability', 'Brand Reputation'])
# with row3[2]:
#     flavor_preference = st.selectbox('Flavour Preferences',['Traditional', 'Exotic'])
# with row3[3]:
#     purchase_channel = st.selectbox('Purchase Channel', ['Online', 'Retail Store'])
#
# with row4[0]:
#     packaging_preference = st.selectbox('Packaging preferences', ['0 to 1', '2 to 4', 'above 4'])
# with row4[1]:
#     health_concerns = st.selectbox('Health Concerns',['Price', 'Quality', 'Availability', 'Brand Reputation'])
# with row4[2]:
#     typical_consumption_situations = st.selectbox('Typical Consumption Situations',['Traditional', 'Exotic'])
#
# if st.button('Predict'):
#     predicted = predict()
#     st.write(predicted)


import streamlit as st
from db_helper import predict

# Page configuration
st.set_page_config(page_title="CodeX Beverage - Price Prediction", page_icon="🥤", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem !important;
        color: #2e86ab;
        border-bottom: 2px solid #2e86ab;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .prediction-box {
        background-color: #f0f8ff;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-top: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.2rem;
        padding: 0.7rem;
        border-radius: 8px;
        border: none;
    }
    .stButton button:hover {
        background-color: #1565a3;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🥤 CodeX Beverage</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; color: #666;">Price Prediction Tool</h2>', unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2 = st.tabs(["📊 Input Parameters", "ℹ️ About"])

with tab1:
    # Create columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)

        # Personal info in two columns
        pers_col1, pers_col2 = st.columns(2)

        with pers_col1:
            age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28,
                                  help="Enter your current age")
            gender = st.selectbox('Gender', ['Male', 'Female'])
            zone = st.selectbox('Zone', ['Urban', 'Semi-Urban', 'Metro', 'Rural'])

        with pers_col2:
            occupation = st.selectbox('Occupation', ['Working Professional', 'Student', 'Entrepreneur', 'Retired'])
            income_levels = st.selectbox('Income Level',
                                        ['<10L', '> 35L', '16L - 25L', 'Not Reported', '10L - 15L', '26L - 35L'])

        st.markdown('<div class="section-header">Consumption Habits</div>', unsafe_allow_html=True)

        # Consumption habits in two columns
        cons_col1, cons_col2 = st.columns(2)

        with cons_col1:
            consume_frequency = st.selectbox('Consumer frequency (weekly)', ['3-4 times', '5-7 times', '0-2 times'])
            current_brand = st.selectbox('Current Brand', ['Newcomer', 'Established'])
            preferable_consumption_size = st.selectbox('Preferable Consumption Size',
                                            ['Medium (500 ml)', 'Large (1 L)', 'Small (250 ml)'])

        with cons_col2:
            awareness_of_other_brands = st.selectbox('Awareness of other brands', ['0 to 1', '2 to 4', 'above 4'])
            reasons_for_choosing_brands = st.selectbox('Reasons for choosing brands',
                                                       ['Price', 'Quality', 'Availability', 'Brand Reputation'])

        st.markdown('<div class="section-header">Preferences</div>', unsafe_allow_html=True)

        # Preferences in two columns
        pref_col1, pref_col2 = st.columns(2)

        with pref_col1:
            flavor_preference = st.selectbox('Flavour Preferences', ['Traditional', 'Exotic'])
            purchase_channel = st.selectbox('Purchase Channel', ['Online', 'Retail Store'])

        with pref_col2:
            packaging_preference = st.selectbox('Packaging preferences', ['0 to 1', '2 to 4', 'above 4'])
            health_concerns = st.selectbox('Health Concerns', ['Low', 'Medium', 'High'])
            typical_consumption_situations = st.selectbox('Typical Consumption Situations',['Active (eg. Sports, gym)', 'Social (eg. Parties)',
       'Casual (eg. At home)'])

    with col2:
        st.markdown('<div class="section-header">Prediction</div>', unsafe_allow_html=True)

        # Info box
        st.info("""
        **How to use:**
        1. Fill in all the parameters on the left
        2. Click the Predict button below
        3. View your personalized price prediction
        """)

        # Prediction button and result
        if st.button('🔮 Predict Price', use_container_width=True):
            with st.spinner('Calculating your personalized price prediction...'):
                predicted = predict(
    age,
    income_levels,
    health_concerns,
    consume_frequency,
    preferable_consumption_size,
    gender,
    zone,
    occupation,
    current_brand,
    awareness_of_other_brands,
    reasons_for_choosing_brands,
    flavor_preference,
    purchase_channel,
    packaging_preference,
    typical_consumption_situations
)

            st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
            st.markdown(f"### 💰 Predicted Price")
            st.markdown(f"# **{predicted}**")
            st.markdown('</div>', unsafe_allow_html=True)

            # Additional insights
            st.success("""
            **Insight:** This price is calculated based on your demographic profile, 
            consumption habits, and market preferences.
            """)

with tab2:
    st.markdown("""
    ## About CodeX Beverage Price Prediction

    This tool uses machine learning to predict optimal pricing for beverages based on:

    - **Demographic factors** (age, gender, location, occupation, income)
    - **Consumption patterns** (frequency, brand loyalty, package size)
    - **Market preferences** (flavors, purchasing channels, health concerns)

    ### How it works:
    1. Our algorithm analyzes historical market data
    2. Correlates consumer profiles with pricing sensitivity
    3. Generates personalized price predictions

    ### Use cases:
    - Market research and analysis
    - Pricing strategy development
    - Consumer behavior insights
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>CodeX Beverage Analytics • Powered by AI • 2024</p>",
            unsafe_allow_html=True)