import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules

st.title("🛒 SmartCart Analytics Dashboard")

# Load data
data = pd.read_csv('data/SuperMarket Analysis.csv')

st.subheader("Dataset Preview")
st.dataframe(data.head())

# Convert into basket format
basket = pd.get_dummies(data[['Invoice ID', 'Product line']]
                        .set_index('Invoice ID')['Product line']).groupby('Invoice ID').sum()

# Apply Apriori
frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

st.subheader("Top Association Rules")
st.dataframe(rules.sort_values(by='lift', ascending=False).head(20))

# Simple chart
st.subheader("Top 10 Frequent Itemsets")
fig, ax = plt.subplots()
top_items = frequent_itemsets.sort_values(by='support', ascending=False).head(20)
ax.bar(top_items['itemsets'].astype(str), top_items['support'])
plt.xticks(rotation=45,fontsize=15)
st.pyplot(fig)