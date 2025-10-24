import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the dataset
data = pd.read_csv('data/SuperMarket Analysis.csv')
print("✅ Data loaded successfully!\n")
print(data.head())  # Show first 5 rows

# Step 2: Basic summary
print("\nNumber of rows and columns:", data.shape)
print("\nColumn names:", list(data.columns))

# Step 3: Average rating by Product Line
avg_rating = data.groupby('Product line')['Rating'].mean().sort_values(ascending=False)

# Step 4: Plot the visualization
plt.figure(figsize=(10,6))
avg_rating.plot(kind='bar', color='orchid')
plt.title('Average Rating by Product Line', fontsize=14, fontweight='bold')
plt.xlabel('Product Line')
plt.ylabel('Average Rating')
plt.xticks(rotation=30)
plt.tight_layout()

# Step 5: Show and save chart
plt.savefig("output_chart.png")
print("\n📸 Chart saved as 'output_chart.png'")
plt.show()
print("The chart has been displayed and saved as 'output_chaert.png'.")
import os
print("Current working directory:", os.getcwd())
print("Saving chart as:", os.path.abspath("output_chart.png"))