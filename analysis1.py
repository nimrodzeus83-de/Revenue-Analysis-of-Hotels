import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv(
    r"C:\Users\MySQLAdmin\Documents\Transactions.csv",
    encoding="cp1252"
    )

df.columns = (
    df.columns 
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace("(", "")
    .str.replace(")","")
)

for cols in df.select_dtypes(include="object"):
    df[cols] = df[cols].astype(str).str.strip()
    
df = df.replace(["", "-", " - "],pd.NA)

money_cols = [
    "price", "package_", "gross",
    "disc_amt", "sales", "dep"
]

for cols in money_cols:
    df[cols] = (
       df[cols]
       .astype(str)
       .str.replace(",", "",regex=False) 
    )
    df[cols] = pd.to_numeric(df[cols], errors="coerce")

df["customer_rating"] = pd.to_numeric(
    df["customer_rating"], 
    errors="coerce"
)

date_cols = ["arrival_date", "depature_date"]

for cols in date_cols:
    df[cols] = pd.to_datetime(
        df[cols],
        errors = "coerce",
        dayfirst=True
    )
    
for cols in date_cols:
    df[cols] = df[cols].dt.strftime("%Y-%m-%d")
    
df["membership"] = df["membership"].fillna("Unknown")

df = df.drop_duplicates()

df.to_csv("new_data.csv", index=False)

print("Data cleaned successfully")
print("")
#print(df.columns.tolist()) nakikita mo lahat ng exist data cols

pd.set_option("display.max_columns", None) #make all columns vissible
print(df.head(),end=" ") #view all the data cloumns 


#hotel_name 
#gross 
#disc_amt 
#sales 

#generates highest revenue

df1 = pd.read_csv("new_data.csv")
revenue = df1.groupby("hotel_name")[["sales", "disc_amt", "gross"]].sum()

ax = revenue.plot(kind="barh", figsize=(12, 7)) #horiontal bar

# Loop through each bar group
for container in ax.containers:
    # Use bar_label to place text inside the bars vertically
    ax.bar_label(
        container,
        fmt=lambda x: f"{x:,.0f}" if x > 0 else "",
        label_type="center",  # Places the text INSIDE the bar
        color="white",  # Makes the text white so it's readable against blue/green
        fontweight="bold",
        fontsize=10,
    )

plt.title("Revenue Analysis of Hotels", fontsize=15, fontweight="bold")
plt.xlabel("Amount (USD)")
plt.ylabel("Hotel Name")

plt.ticklabel_format(
    style="plain", axis="x"
)
plt.grid(
    axis="x", linestyle="--", alpha=0.7
)
plt.tight_layout()
plt.show()
