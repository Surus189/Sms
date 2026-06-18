import xml.etree.ElementTree as ET
import pandas as pd
import re
import os

# File paths
input_path = r'D:\suru\Sms\sms (1).xml'
output_path = r'D:\suru\Sms\cleaned_sms.csv'

# 1. Masking Function (Private details-a mask pannum)
def mask_text(text):
    if not isinstance(text, str): return text
    # 5 digits-kku mela irukura numbers-a 'XXXX' nu maathum (Account/Phone numbers)
    return re.sub(r'\d{5,}', 'XXXX', text)

print("Processing files... Wait for a moment!")

# 2. Parsing the XML
try:
    tree = ET.parse(input_path)
    root = tree.getroot()

    data = []
    # SMS Backup & Restore XML structure iterates through <sms> tags
    for sms in root.findall('sms'):
        body = sms.get('body')
        readable_date = sms.get('readable_date')
        
        # Apply mask
        masked_body = mask_text(body)
        
        data.append({'date': readable_date, 'message': masked_body})

    # 3. Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Success! Cleaned data saved at: {output_path}")

except Exception as e:
    print(f"Error: {e}")