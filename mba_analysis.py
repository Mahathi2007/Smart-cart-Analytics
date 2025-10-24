import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
data = pd.read_csv('data/SuperMarket Analysis.csv')
print("Detected columns:",list(data.columns))
print("First 5 rows of your dataset:")
print(data.head())
basket = pd.get_dummies(data[['Product line', 'Invoice ID']]
    .set_index('Invoice ID')['Product line']).groupby('Invoice ID').sum()
print("Basket format preview:")
print(basket.head())
frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)
print("Top frequent itemsets:")
print(frequent_itemsets.sort_values(by='support', ascending=False).head(10))
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.2)
print("Top 10 association rules:")
print(rules.sort_values(by='lift', ascending=False).head(10))
basket = basket.astype(bool)
frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)
print("Top frequent itemsets:")
print(frequent_itemsets.sort_values(by='support', ascending=False).head(10))
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.2)
if not rules.empty:
    print("Top association rules (by confidence):")
    print(rules.sort_values(by='confidence', ascending=False).head(10))
else:
    print("No association rules found with the current parameters.")

import matplotlib.pyplot as plt
frequent_itemsets.sort_values(by='support', ascending=False).head(10).plot.bar(x='itemsets', y='support')
plt.title("Top Frequent Itemsets")
plt.ylabel("Support")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()