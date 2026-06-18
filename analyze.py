import pandas as pd
import re
import matplotlib.pyplot as plt

# 1. Load the data
df = pd.read_csv(r'D:\suru\Sms\cleaned_sms.csv')

# 2. Filter & Extract Amount
pattern = r'(?i)(debited|credited|spent|received|rs\.|transaction)'
df_filtered = df[df['message'].str.contains(pattern, na=False)].copy()

def extract_amount(text):
    match = re.search(r'(?:rs\.?|inr)\s?(\d+(?:,\d+)*(?:\.\d+)?)', text, re.IGNORECASE)
    if match:
        amount_str = match.group(1).replace(',', '')
        return float(amount_str)
    return None

df_filtered['amount'] = df_filtered['message'].apply(extract_amount)
df_final = df_filtered.dropna(subset=['amount']).copy()

# 3. Categorize
def categorize(text):
    text = text.lower()
    if any(word in text for word in ['credited', 'received', 'deposited']):
        return 'Credit'
    else:
        return 'Debit'

df_final['type'] = df_final['message'].apply(categorize)

# 4. Summary Output
summary = df_final.groupby('type')['amount'].sum()
print(summary)

# 5. Visualization
summary.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title('Expense vs Income Distribution')
plt.ylabel('')
plt.show()
# Check Top 5 Credits and Debits
print("\n--- Top 5 Credits (Income) ---")
print(df_final[df_final['type'] == 'Credit'].sort_values('amount', ascending=False).head(5))

print("\n--- Top 5 Debits (Expenses) ---")
print(df_final[df_final['type'] == 'Debit'].sort_values('amount', ascending=False).head(5))