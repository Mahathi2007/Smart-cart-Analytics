import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def generate_rules(df):
    # Diagnostics: Show incoming DataFrame
    print("Data Sample ----")
    print(df.head(10))
    print("Columns:", df.columns.tolist())
    if 'Invoice ID' not in df.columns or 'Product line' not in df.columns:
        print("ERROR: Required columns missing.")
        return "<p>Data missing required columns (Invoice ID, Product line).</p>", ["Data error."]

    print(f"Unique invoices: {df['Invoice ID'].nunique()}")
    print(f"Unique products: {df['Product line'].nunique()}")

    try:
        # Basket conversion
        basket = pd.crosstab(df['Invoice ID'], df['Product line'])
        print(" Basket Matrix ----")
        print(basket.head(10))
        print(f"Basket shape: {basket.shape}")
    except Exception as e:
        print("Basket error:", str(e))
        return "<p>Error preparing basket for analysis.</p>", ["Basket conversion error."]

    # Handle empty basket
    if basket.shape[0] == 0 or basket.shape[1] == 0:
        print("Basket is empty: no transactions or products.")
        return "<p>No transactions with more than one product.</p>", ["No data for rule mining."]

    # Apriori: lower thresholds for better results in small/sparse data
    frequent_itemsets = apriori(basket, min_support=0.0001, use_colnames=True)
    print(f"Frequent itemsets found: {len(frequent_itemsets)}")
    print(frequent_itemsets.head())

    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    print(f"Rules found: {len(rules)}")
    print(rules[['antecedents', 'consequents', 'confidence']].head())

    # Format for rendering
    if not rules.empty:
        rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        rules_display = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    else:
        rules_display = pd.DataFrame([{'antecedents':'-', 'consequents':'-', 'support':0, 'confidence':0, 'lift':0}])

    recommendations = []
    if not rules.empty:
        for _, row in rules.sort_values('confidence', ascending=False).head(3).iterrows():
            recommendations.append(
                f"If buy: {row['antecedents']} → Recommend: {row['consequents']} (confidence: {row['confidence']:.2f})"
            )
    else:
        recommendations.append("No strong combos found in the data.")

    return rules_display.to_html(classes='data'), recommendations