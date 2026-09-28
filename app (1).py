import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="ShopperSense - Purchase Intent Predictor",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load the model
try:
    model = joblib.load('shopper_revenue_model.pkl')
except FileNotFoundError:
    model = None

# Custom CSS Styling (same theme as before)
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 38px;
            color: #4C6E91;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #6F6875;
            font-size: 18px;
            margin-bottom: 20px;
        }

        .stButton>button {
            width: 100%;
            background-color: #A9C6DE;
            color: #2F3E4D;
            font-size: 18px;
            font-weight: 600;
            padding: 10px;
            border-radius: 15px;
            border: 1px solid #C9DCC5;
        }

        .stButton>button:hover {
            background-color: #8FB3D1;
            color: white;
        }

        .card {
            background-color: #FFFDF7;
            box-shadow: 1px 1px 10px #E6DDE0;
            padding: 14px;
            border-radius: 15px;
            border: 1px solid #EADCC8;
            color: #2F3E4D;
        }

        .card h4 {
            color: #4C6E91;
            margin-top: 0;
        }

        .footer{
            text-align : center;
            color: #6F6875;
            font-size: 14px;
            margin-top: 25px;
        }
    </style>
""", unsafe_allow_html=True)


def header(subtitle):
    st.markdown('<div class="title">🛒 ShopperSense</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)


def footer():
    st.write("---")
    st.markdown('<div class="footer">© 2025 ShopperSense. All rights reserved.</div>', unsafe_allow_html=True)


def go_to_predict():
    st.session_state.page = "Predict"


# ---------------------------------------------------------------
# Page 1: Home (landing page)
# ---------------------------------------------------------------
def home_page():
    header("Know which visitors are ready to buy")

    st.markdown("""
        <div class="card">
            <h4>Welcome!</h4>
            ShopperSense looks at how a visitor behaves on an online store,
            such as the pages they view, the time they spend and the pages they
            leave from, and predicts whether they are likely to make a purchase.
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="card">
                <h4>1. Enter</h4>
                Add details about a visitor's browsing session.
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="card">
                <h4>2. Predict</h4>
                Our trained model checks the buying signals.
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="card">
                <h4>3. Act</h4>
                See the purchase probability and plan your next step.
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.button("Try the Predictor", on_click=go_to_predict)
    footer()


# ---------------------------------------------------------------
# Page 2: About Us
# ---------------------------------------------------------------
def about_page():
    header("About Us")

    st.markdown("""
        <div class="card">
            <h4>Accuracy</h4>
            Accuracy: 0.85
            Precision: 0.511
            Recall: 0.749
            F1 Score: 0.607
            ROC-AUC: 0.896
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("""
        <div class="card">
            <h4>What we do</h4>
            Our model is trained on the Online Shoppers Purchasing Intention
            dataset. It learns from past sessions to estimate whether a new
            session will end in a purchase.
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("""
        <div class="card">
            <h4>Why it matters</h4>
            Knowing who is likely to buy helps stores decide where to focus
            offers, discounts and support, so fewer sales are missed.
        </div>
    """, unsafe_allow_html=True)
    footer()


# ---------------------------------------------------------------
# Page 3: Predict
# ---------------------------------------------------------------
def predict_page():
    header("Online Shopper Purchase Intent Predictor")

    if model is None:
        st.error("Error: 'shopper_revenue_model.pkl' not found. Please ensure it is in the same directory as this script.")
        return

    # Input section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        administrative = st.number_input("Administrative Pages Viewed", 0, 30, step=1, value=2)
        administrative_duration = st.number_input("Administrative Duration (secs)", 0.0, 5000.0, step=10.0, value=80.0)
        informational = st.number_input("Informational Pages Viewed", 0, 30, step=1, value=0)
        informational_duration = st.number_input("Informational Duration (secs)", 0.0, 5000.0, step=10.0, value=0.0)
        product_related = st.number_input("Product-Related Pages Viewed", 0, 700, step=1, value=30)
        product_related_duration = st.number_input("Product-Related Duration (secs)", 0.0, 20000.0, step=10.0, value=600.0)
        bounce_rates = st.number_input("Bounce Rate", 0.0, 1.0, step=0.01, value=0.01)
        exit_rates = st.number_input("Exit Rate", 0.0, 1.0, step=0.01, value=0.02)
        page_values = st.number_input("Page Values", 0.0, 400.0, step=1.0, value=15.0)
    with col2:
        special_day = st.slider("Special Day Closeness", 0.0, 1.0, step=0.1, value=0.0)
        month = st.selectbox(
            "Month",
            ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        )
        operating_systems = st.selectbox("Operating System", [1, 2, 3, 4, 5, 6, 7, 8])
        browser = st.selectbox("Browser", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        region = st.selectbox("Region", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        traffic_type = st.selectbox("Traffic Type", list(range(1, 21)))
        visitor_type = st.selectbox("Visitor Type", ["New_Visitor", "Returning_Visitor", "Other"])
        weekend = st.selectbox("Weekend Session?", ["No", "Yes"])
    st.markdown('</div>', unsafe_allow_html=True)

    # Prediction button
    st.write("")
    predict_btn = st.button("Predict Purchase Intent")
    if predict_btn:
        input_data = pd.DataFrame({
            'Administrative(Account settings etc.)': [administrative],
            'Administrative_Duration': [administrative_duration],
            'Informational(FAQ,shipment tracking etc.)': [informational],
            'Informational_Duration': [informational_duration],
            'ProductRelatedPages': [product_related],
            'ProductRelated_Duration': [product_related_duration],
            'BounceRates(wxiting after viewing one page)': [bounce_rates],
            'ExitRates': [exit_rates],
            'PageValues': [page_values],
            'SpecialDay': [special_day],
            'Month': [month],
            'OperatingSystems': [operating_systems],
            'Browser': [browser],
            'Region': [region],
            'TrafficType': [traffic_type],
            'VisitorType': [visitor_type],
            'Weekend': [weekend == "Yes"]
        })
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        if prediction:
            st.success(f"✅ **Likely to Purchase!** Estimated probability: {probability:.1%}")
        else:
            st.warning(f"🚫 **Unlikely to Purchase.** Estimated probability: {probability:.1%}")
    footer()


# ---------------------------------------------------------------
# Navigation (sidebar)
# ---------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.title("🛒 ShopperSense")
st.sidebar.radio("Go to", ["Home", "About Us", "Predict"], key="page")

if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "About Us":
    about_page()
else:
    predict_page()
