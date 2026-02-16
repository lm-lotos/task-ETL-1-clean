## Результати проєкту
Python ETL pipeline for cleaning and transforming a real-world contact dataset.

The project demonstrates a full data processing workflow:
• data extraction from CSV
• data cleaning and normalization
• feature engineering
• export of analytical dataset
## How to run

```bash
pip install -r requirements.txt
python project.py
```

У межах даного навчального проєкту було реалізовано повний цикл обробки даних за підходом **ETL (Extract, Transform, Load)** на прикладі реального табличного датасету **UK-500**, що містить персональні та контактні дані користувачів.

На етапі **Extract** виконано завантаження вхідного CSV-файлу та первинний дослідницький аналіз структури даних (EDA), зокрема перевірку типів даних, наявності пропущених значень і дублікатів.

На етапі **Transform** здійснено очищення та стандартизацію даних: усунено зайві пробіли, приведено текстові поля до єдиного формату, очищено телефонні та факсові номери від неструктурованих символів, нормалізовано email-адреси та вебпосилання. У межах feature engineering створено нові аналітичні ознаки, зокрема:
- `full_name` — об’єднане ім’я та прізвище;
- `email_domain` — домен електронної пошти;
- `is_gmail` — логічний індикатор використання Gmail;
- `city_length` — довжина назви міста.

Додатково виконано фільтрацію та сегментацію даних за доменом електронної пошти та типом компанії, а також побудовано агреговані показники для аналізу розподілу користувачів за містами та email-доменами.

На етапі **Load** фінальні результати збережено у зовнішні формати:
- очищений датасет — у форматі CSV;
- вибірки та агреговані статистики — у форматі Excel з окремими аркушами.

Отриманий у результаті DataFrame є структурованим, аналітично готовим та придатним для подальшого аналізу, візуалізації або використання у бізнес-завданнях.

## Output

After running the script, a cleaned dataset will be generated:

uk500_clean.csv — ready-to-use analytical table
stats.xlsx — aggregated statistics
gmail_users.csv — filtered Gmail users
