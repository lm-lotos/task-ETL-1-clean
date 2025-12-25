# Завдання для дата-аналітика (навчальний проєкт)

# ## Загальний опис  
# Мета цього проєкту — опрацювати набір даних за допомогою бібліотеки Pandas: очистити його, виконати трансформації, створити нові колонки, відфільтрувати інформацію й зберегти фінальний результат у форматах, придатних для подальшого аналізу. Це навчальний проєкт, заснований на підходах, описаних у статті: *“Pandas: управління даними проєкту (2)”*. (Джерело: Medium)

# ---

# ## Мета проєкту  
# - Отримати практичний досвід застосування Pandas для обробки реальних табличних даних.  
# - Навчитись перетворювати сирі дані у структурований та аналітично готовий формат.  
# - Підготувати DataFrame, який можна буде аналізувати або візуалізувати.

# ---

# ## Основні цілі  
# 1. Завантажити та дослідити вхідні дані.  
# 2. Видалити зайві рядки та колонки.  
# 3. Додати нові колонки на основі існуючих даних.  
# 4. Вставити нові записи (рядки) у DataFrame.  
# 5. Виконати фільтрацію даних за різними критеріями.  
# 6. Створити підвибірки (сегменти) даних за логічними умовами.  
# 7. Зберегти підготовлений DataFrame у зовнішні формати для подальшого використання.


# Educational project

import pandas as pd
import numpy as np

pd.set_option("displau.max_columns", 50)   # перегляд файлу  (налаштування візуалізації)
pd.set_option("display.width", 90)

url = "https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv"
# url = "data/uk-500.csv"

df = pd.read_csv(url)

COLUMNS_TO_DROP = [] # список, якщо великими буквами - то це константа, яка не змінюється

# print("\n--- head ---")
# print(df.head())

# print("\n--- info ---")
# print(df.info())

# print("\n--- describe ---")
# print(df.describe())

print("\n--- describe for str ---")
print(df.describe(include=[object]).T)

print("--- null ---")
# print(df.isna().sum())
print(df.isna().sum().sort_values(ascending=False).head(20))

print("--- duplicated ---")
print(df.duplicated().sum())

# буває коли потрібно лише назви колонок, тобі буде:
print("--- List columns ---")
list_col = df.columns
print(list(list_col))
for i, col in enumerate(df.columns):

    print(f"{i:02d}. {col}")
# 2. наступний етап - очищення даних
df_raw = df.copy()

if COLUMNS_TO_DROP:
    print("\n--- delet columns in list ---")
    df_raw = df_raw.drop(columns=[col for col in COLUMNS_TO_DROP if col in df_raw.columns], errors='ignore')
   
    # columns = []
    # for col in COLUMNS_TO_DROP:
    #     if col in df_raw.columns:
    #         columns.append(col)
else:
    print("\nCOLUMNS_TO_DROP = []")
def standardize_text(s):
    if pd.isna(s):
        return np.nan

    if not isinstance(s, str):
        s = str(s)

    s = s.strip()
    s = s.split()
    s = " ".join(s.split())

    return s 

for col in df_raw.select_dtypes(include=['object']).columns:
    df_raw[col] = df_raw[col].apply
    (standardize_text)

# print(df_raw)

possible_email_cols = [c for c in df.columns if "email" in c.lower()]  # можна взагалі написати mail, це взагалі буде універсально
possible_web_cols = [c for c in df.columns if ("web" in c.lower() or "website" in c.lower() or "url" in c.lower())]

possible_phone_cols = [c for c in df.columns if ("phone" in c.lower() or "telephone" in c.lower() or "tel" in c.lower())]

possible_fax_cols = [c for c in df.columns if  "fax" in c.lower()]

# генерація списку
# [змінна_циклу in де проходимося (з приміненими операціями) 
# [0, 1, 2, 3]
# [n for n in range(4)]

print("\nPossible columns:")
print("Email cols:", possible_email_cols)
print("Web cols:", possible_web_cols)
print("Phone cols:", possible_phone_cols)
print("Fax cols:", possible_fax_cols)


# Приміняємо зміни

for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(standardize_text)

# email
for col in possible_email_cols:
    df[col] = df[col].str.lower()

# web
for col in possible_web_cols:
    df[col] = df[col].str.lower()

# clean phone/fax
def clean_phone(x):
    if pd.isna(x):
        return np.nan
    s = str(x)
    s = s.strip()

    # plus = ""
    # if s.startswith("+")
    #     plus = "+"

    plus = "+" if s.startswith("+") else ""
    # тут дописати коментар
    # залишаю плюс, якщо юзер сам його поставив; все інше чистимо до цифр, бо в реальних даних телефонують як попало

    digits = "".join(ch for ch in s if ch.isdigit())

    if digits == "":
        return np.nan
    
    return plus + digits
for col in possible_phone_cols + possible_fax_cols:
    df[col] = df[col].apply(clean_phone)


    def title_if_str(s):
        if pd.isna(s):
            return np.nan
        return str(s).title()
    
    city_cols = [c for c in df.columns if c.lower() in ("city", "city_name")]

    # 3.Створення нових колонок (Feature Engineering)

    df["full_name"] = df.first_name + " " + df.last_name

    df["city_length"] = df
    ["city"].arrly(len)

    # df["city2"] = df["city"].str.len()

    # df["is_gmail"] = 
    # print([bool(s) for s in df["email"] if "@gmail.com" in str(s).lower()])


    df["is_gmail"] = [True if "gmail.com" in str(s).lower() else False for s in df["email"]]



    #possible_email_cols = [c for c in df.columns if "email" in c lower()]

    # 4. фільтрація даних

    print("\n--- підвибірки ---")

    gmail_users = df.loc[df['is_gmail'] == True]#.copy()
    print(gmail_users)

    print("Gmail users:", len (gmail_users))

    # працівники кмпанії з "LLC" або "Ltd"

    # df["company_name"]

    # df["company_name"]

    df["company_name"] = df["company_name"].finnal("")
    # print(df["company_name"].finnal(""))
    
    mask_LLC_Ltd = df.company_name.str.contains(r"\b(LLC|Ltd|llc|LTD|ltd)\b", regex=True, na=False)
    # print(mask_LLC-Ltd)

    company_llc_ltd = df.loc[mask_LLC_Ltd].copy()
    # print(company_llc_ltd)

    print("Company LLC and Ltd:", len (company_llc_ltd))

# 5.Позиційна вибірка (ilos)

# Блочок для витягування конкретних позицій — тут прямо мануальна робота по цифрам
try:
    # Беремо перші 10 рядків і колонки 2-5 (із нульової індексації, звісно)
    first_10_cols_2_5 = df.iloc[:10, 2:6]
    print("\nПерші10 рядків + колонки 2-5")
    print(first_10_cols_2_5)

except Exception as e:
    # Якщо щось бахнулося — ловимо і не даємо коду здохнути
    print("Can't (Перші 10 рядків + колонки 2-5):", e)
    
    # Витягуємо кожний 10-й рядок — корисно дивитись загальний патерн
    every_10th = df.iloc[::10, :].copy()
    print("\nevery_10th")
    print(every_10th)

# random — це вже чистий форсаж, підглядання в дані без філософії
try:
    # 5 випадкових рядків для sanity-check, seed фіксований щоб не гуляло
    random_5 = df.sample(5, random_state=42)
    print("\nrandom 5 row")
    print(random_5)

except Exception as e:
    # Ну буває, що й рандом не радує
    print("Can't (random 5 row):", e)


# 6. Групування та статистика

print("\n--- Групування та статистика")

# дивлюсь, які домени найчастіше трапляються
print(df["email"].str.split("@").str[-1].value_counts().head(5))

# топ міст, просто щоб мати уявлення
print(df["city"].value_counts().head(5))

# скільки рядків на місто + якесь “середнє”, хай буде
agg_by_city = df.groupby("city").agg(
    people_count=("city", "size"),
    avg_people=("first_name", "mean")
)
# print(agg_by_city)

# додаю колонку з доменом, бо далі треба
df["domain"] = df["email"].str.split("@").str[-1]

# рахуємо по містах: скільки людей і скільки різних доменів
agg_by_city = (
    df.groupby("city")
      .agg(
          peopl_count=("first_name", "count"),
          uniq_dom=("domain", "nunique")
      )
      .sort_values("peopl_count", ascending=False)
      .head(10)
)

# просто рахую людей по містах і сортую
count_by_city = (
    df.groupby("city")
      .size()
      .reset_index(name="count")
      .sort_values("count", ascending=False)
)

print(count_by_city)



    # print(df.head())


   
        




