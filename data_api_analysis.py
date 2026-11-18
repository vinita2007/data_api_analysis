import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Fetch Data from a REST API (JSON Payload)
API_URL = "https://jsonplaceholder.typicode.com/users"
response = requests.get(API_URL)

if response.status_code == 200:
    raw_data = response.json()
    print(f"Successfully fetched {len(raw_data)} records from API.")
else:
    raise Exception(f"API Request Failed with status code: {response.status_code}")

# 2. Data Loading & Manipulation using Pandas and NumPy
df = pd.json_normalize(raw_data)

# Select relevant columns and simulate analytical metrics (e.g., Sales & Rating)
np.random.seed(42)
clean_df = pd.DataFrame({
    "User_ID": df["id"],
    "Name": df["name"],
    "City": df["address.city"],
    "Company": df["company.name"],
    "Projects_Completed": np.random.randint(5, 30, size=len(df)),
    "Revenue_Generated": np.round(np.random.uniform(15000, 95000, size=len(df)), 2)
})

# Data Cleaning: Check for missing values & duplicates
clean_df.drop_duplicates(inplace=True)
clean_df.fillna({"Revenue_Generated": clean_df["Revenue_Generated"].mean()}, inplace=True)

# 3. Statistical Analysis & Report Generation
print("\n--- Summary Statistics ---")
print(clean_df[["Projects_Completed", "Revenue_Generated"]].describe())

avg_revenue = np.mean(clean_df["Revenue_Generated"])
top_performer = clean_df.loc[clean_df["Revenue_Generated"].idxmax()]

print(f"\nAverage Revenue Generated: ₹{avg_revenue:.2f}")
print(f"Top Performer: {top_performer['Name']} (₹{top_performer['Revenue_Generated']:.2f})")

# Save cleaned report to CSV
clean_df.to_csv("api_analysis_report.csv", index=False)
print("\nReport saved successfully as 'api_analysis_report.csv'.")

# 4. Data Visualization using Matplotlib & Seaborn
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.barplot(
    data=clean_df.sort_values(by="Revenue_Generated", ascending=False),
    x="Revenue_Generated",
    y="Name",
    palette="viridis"
)

plt.title("Revenue Generated per User (API Dataset Analysis)", fontsize=14, fontweight="bold")
plt.xlabel("Revenue Generated (₹)")
plt.ylabel("User Name")
plt.tight_layout()
plt.savefig("revenue_chart.png")
plt.show()
