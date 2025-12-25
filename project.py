import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 120)

# 1. Extract
url = "https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv"
df = pd.read_csv(url)

print("HEAD:")
print(df.head())

print("\nINFO:")
df.info()

print("\nDESCRIBE:")
print(df.describe())

print("\nMISSING VALUES:")
print(df.isna().sum())

print("\nDUPLICATES:")
print(df.duplicated().sum())


# 2. Cleaning
df_clean = df.copy()
df_clean = df_clean.dropna(how="all")
df_clean = df_clean.drop_duplicates()

text_cols = df_clean.select_dtypes(include="object").columns
for col in text_cols:
    df_clean[col] = df_clean[col].fillna("").astype(str).str.strip()

print("\nCLEANED INFO:")
df_clean.info()


# 3. Feature Engineering
df_clean["email_domain"] = df_clean["email"].str.split("@").str[-1].str.lower()
df_clean["full_name"] = (df_clean["first_name"].fillna("") + " " + df_clean["last_name"].fillna("")).str.strip()
df_clean["city_length"] = df_clean["city"].str.len()
df_clean["is_gmail"] = df_clean["email_domain"] == "gmail.com"

print("\nFEATURE SAMPLE:")
print(df_clean[["full_name", "email_domain", "city_length", "is_gmail"]].head())


# 4. Filtering
gmail_users = df_clean[df_clean["is_gmail"]]
llc_ltd_companies = df_clean[df_clean["company_name"].str.contains(r"\b(LLC|Ltd)\b", case=False, na=False)]
london_users = df_clean[df_clean["city"].str.lower() == "london"]

df_clean["company_word_count"] = df_clean["company_name"].str.split().str.len()
long_company_names = df_clean[df_clean["company_word_count"] >= 4]

first_10_rows = df_clean.iloc[:10, 2:6]
every_10th_row = df_clean.iloc[::10]
random_5_rows = df_clean.sample(5, random_state=42)

print("\nFILTER RESULTS:")
print("Gmail users:", len(gmail_users))
print("LLC/Ltd companies:", len(llc_ltd_companies))
print("London users:", len(london_users))
print("Company names 4+ words:", len(long_company_names))


# 5. Statistics
people_by_city = (
    df_clean.groupby("city")
    .size()
    .reset_index(name="people_count")
    .sort_values("people_count", ascending=False)
)

top_5_cities = people_by_city.head(5)
top_5_domains = df_clean["email_domain"].value_counts().head(5)
unique_domains_count = df_clean["email_domain"].nunique()

print("\nTOP 5 CITIES:")
print(top_5_cities)

print("\nTOP 5 DOMAINS:")
print(top_5_domains)

print("\nUNIQUE DOMAIN COUNT:")
print(unique_domains_count)


# 6. Export
df_clean.to_csv("uk500_clean.csv", index=False, encoding="utf-8")
gmail_users.to_csv("gmail_users.csv", index=False, encoding="utf-8")

with pd.ExcelWriter("stats.xlsx", engine="xlsxwriter") as writer:
    top_5_cities.to_excel(writer, sheet_name="Top_5_Cities", index=False)
    top_5_domains.to_frame(name="count").to_excel(writer, sheet_name="Top_5_Email_Domains")

print("\nEXPORT DONE")
print("Saved: uk500_clean.csv, gmail_users.csv, stats.xlsx")