import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🛒 Supermarket Data Dashboard")

# Upload section
uploaded_file = st.file_uploader("📂 Upload your Supermarket Sales CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    st.write("### Sample Data")
    st.dataframe(df.head())

    # 👉 Your existing dashboard charts and logic go here
    # Example:
    st.write("### Sales by Product Line")
    chart_data = df['Product line'].value_counts()
    st.bar_chart(chart_data)

else:
    st.warning("Please upload a CSV file to start the analysis.")
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'step' not in st.session_state:
    st.session_state.step = 1

st.set_page_config(page_title="SmartCart Analytics", layout="wide")


# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
        .login-card-hack {
            background: linear-gradient(130deg, #e6f2ff 0%, #f7e5ff 110%);
            padding: 2.6em 2.5em 2.1em 2.5em;
            border-radius: 18px;
            min-width: 350px;
            max-width: 400px;
            margin: 60px auto 40px auto;
            box-shadow: 0 10px 60px #b389f822;
            animation: bounceIn 880ms cubic-bezier(.42,0,.15,1.2);
        }
        @keyframes bounceIn {
            0% { transform: scale(0.82) translateY(-60px); opacity: .3;}
            62%{ transform:scale(1.05);}
            93%{ transform:scale(.95);}
            100%{ transform:scale(1) translateY(0); opacity: 1;}
        }
        .welcome-glow {
            background: linear-gradient(90deg, #5badfc 40%, #b078fa 90%);
            color: #fff;
            font-size: 1.6em;
            font-weight: bold;
            border-radius: 11px;
            padding: 0.75em 0 0.58em 0;
            margin-bottom: 22px;
            letter-spacing: 1.1px;
            text-align: center;
            text-shadow: 0px 2px 18px #a0c7fd99;
            box-shadow: 0 0 22px #a073f812;
            animation: glowcycle 1.9s infinite alternate;
        }
        @keyframes glowcycle {
            0%   {text-shadow: 0 2px 19px #a073f880;}
            80%  {text-shadow: 0 3px 13px #bdd8ff;}
            100% {text-shadow: 0 2px 20px #a073f844;}
        }
        .demo-creds {
            color: #313850;
            font-size: .99em;
            margin-top: 1.09em;
            border-radius: 7px;
            background:#eef7f8;
            border: 1px solid #ececf6;
            padding: 0.8em .7em .4em .7em;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class='login-card-hack'>
            <div class='welcome-glow'>Welcome to SmartCart 🛒</div>
        """, unsafe_allow_html=True
    )
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if username.strip().lower() == "smartcart" and password.strip().lower() == "smartcart":
            st.session_state.logged_in = True
        else:
            st.error("⛔ Invalid credentials! Use the demo values below.")
    st.markdown(
        """
        <div class='demo-creds'>
        <b>DEMO login:</b><br>
        Username: <code>smartcart</code><br>
        Password: <code>smartcart</code>
        </div>
        </div>
        """, unsafe_allow_html=True
    )
    st.stop()

# --- DASHBOARD INTRO PAGE ---
if st.session_state.step == 1:
    st.markdown("<h1 style='text-align:center; margin-bottom:10px;'>🛒 SmartCart Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; margin-top:-10px; color:#3c68c4'>Market Basket Analysis for Retailers</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='margin:2.1em auto; max-width:690px; background:#fcfdfe; border-radius:12px; border: 1px solid #ecf1f7; padding:1.55em 1.48em 1.1em 1.48em; font-size:1.18em; text-align:left;'>
        <b style="color:#0d3965;">What does this dashboard do?</b>
        <ul>
          <li>Discovers product combinations that are most often bought together.</li>
          <li>Shows <b>"If Buy A → Recommend B"</b> rules for smarter cross-selling.</li>
        </ul>
        <b style="color:#145589;">Key Terms:</b>
        <ul>
          <li><b>Lift</b>: How much more likely items are bought together vs by chance.</li>
          <li><b>Support</b>: How often the combo occurs in all transactions.</li>
          <li><b>Confidence</b>: How likely B is bought if A is bought.</li>
        </ul>
        <b style="color:#1a866c;">Real Business Use:</b>
        <ul>
          <li>Create combo offers for top rule pairs</li>
          <li>Place frequently bought-together items next to each other</li>
          <li>Target bundles to specific customer groups</li>
        </ul>
        <i style="color:#575959;">Click <b>Next</b> to view your dashboard.</i>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Next"):
        st.session_state.step = 2
    st.stop()

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='text-align:center;'>🛒 SmartCart Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Market Basket Analysis for Retailers</h4>", unsafe_allow_html=True)
st.success("Analysis ready — explore your product combos below!")

try:
    DATA_PATH = "data/SuperMarket Analysis.csv"
    data = pd.read_csv(DATA_PATH)
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error(f"Data file not found at {DATA_PATH}. Please place it inside the 'data' folder.")
    st.stop()

@st.cache_data
def run_mba(df):
    try:
        basket_input = df[['Invoice ID', 'Product line']].dropna()
        basket = (basket_input
                  .groupby(['Invoice ID', 'Product line'])['Product line']
                  .count()
                  .unstack()
                  .reset_index()
                  .fillna(0)
                  .set_index('Invoice ID'))
        basket = basket.applymap(lambda x: 1 if x > 0 else 0)
    except KeyError as e:
        st.warning(f"MBA Warning: Missing column {e}. Cannot perform MBA.")
        return pd.DataFrame()
    frequent_itemsets = apriori(basket, min_support=0.001, use_colnames=True)
    if frequent_itemsets.empty:
        return pd.DataFrame()
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
    if rules.empty:
        return pd.DataFrame()
    rules["antecedents"] = rules["antecedents"].apply(lambda x: ', '.join(list(x)))
    rules["consequents"] = rules["consequents"].apply(lambda x: ', '.join(list(x)))
    rules_display = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
    rules_display.columns = ['If Buy (Antecedent)', 'Then Buy (Consequent)', 'Support', 'Confidence', 'Lift']
    return rules_display.sort_values(by='Lift', ascending=False)

st.sidebar.header("Filter Options")
selected_city = st.sidebar.selectbox("Select City", options=["All"] + list(data["City"].unique()))
selected_gender = st.sidebar.selectbox("Select Gender", options=["All"] + list(data["Gender"].unique()))

filtered_data = data.copy()
if selected_city != "All":
    filtered_data = filtered_data[filtered_data["City"] == selected_city]
if selected_gender != "All":
    filtered_data = filtered_data[filtered_data["Gender"] == selected_gender]

col1, col2 = st.columns([1, 1])

with col1:
    st.write("#### Dataset Preview")
    st.dataframe(filtered_data.head(10))
    st.write("#### Top Product Lines by Quantity Sold")
    product_sales = filtered_data.groupby("Product line")["Quantity"].sum().sort_values(ascending=False)
    st.bar_chart(product_sales)

with col2:
    st.write("#### Product Recommendation Rules")
    st.write("Actionable Insights — (If you buy A, recommend B)")
    mba_rules_df = run_mba(data)
    if not mba_rules_df.empty:
        st.dataframe(mba_rules_df.head(10), height=300)
        st.write("Rule Strength Visualization (Lift)")
        fig2, ax = plt.subplots(figsize=(7, 3.5))
        sns.barplot(
            x='Lift',
            y='If Buy (Antecedent)',
            data=mba_rules_df.head(5).reset_index(),
            ax=ax
        )
        st.pyplot(fig2)
    else:
        st.warning("No association rules found. Try adding more transaction data or lowering min_support.")

st.write("---")
st.markdown(
    "<div style='text-align:center; color:#313342;'>© 2025 SmartCart Analytics | Created by Mahathi Tarugu | Hackathon Final</div>",
    unsafe_allow_html=True
)