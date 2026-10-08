import pytesseract
from PIL import Image
import re
import csv
import os

def extract_data_rpa(image_path):
    img = Image.open(image_path)
    
    raw_text = pytesseract.image_to_string(img)
    
    print("\nOCR Output:\n")
    print(raw_text)

    print("--------------------------------------\n")
    
    
    name_match = re.search(r'Name/Phone.*?(?::|;)\s*[_]*\s*(.*?)(?=\s*Date|\n)', raw_text, re.IGNORECASE)
    extracted_name = name_match.group(1).replace('_', '').strip() if name_match else "Not Found"
    
    date_match = re.search(r'Date.*?(?::|;)\s*[_]*\s*([\d/]+)', raw_text, re.IGNORECASE)
    extracted_date = date_match.group(1).strip() if date_match else "Not Found"
    
    manager_match = re.search(r'Supervisor/Manager.*?(?::|;)\s*[_]*\s*(.*?)(?=\s*(?:R&D|RED)\s*Group|\n)', raw_text, re.IGNORECASE)
    extracted_manager = manager_match.group(1).replace('_', '').strip() if manager_match else "Not Found"
    
    group_match = re.search(r'(?:R&D|RED)\s*Group.*?(?::|;)\s*[_]*\s*(.*?)(?=\n|$)', raw_text, re.IGNORECASE)
    extracted_group = group_match.group(1).replace('_', '').strip() if group_match else "Not Found"
    
    suggestion_match = re.search(r'Suggestion.*?(?::|;)\s*[_]*\s*(.*?)(?=\s*Suggested Solution)', raw_text, re.IGNORECASE | re.DOTALL)
    if suggestion_match:
        extracted_suggestion = re.sub(r'\s+', ' ', suggestion_match.group(1)).strip()
    else:
        extracted_suggestion = "Not Found"
    
    return {
        "file_name": os.path.basename(image_path),
        "name_phone_ext": extracted_name,
        "date": extracted_date,
        "supervisor_manager": extracted_manager,
        "rd_group": extracted_group,
        "suggestion": extracted_suggestion
    }

def save_to_csv(data_dict, csv_path):
    field_names = [
        "file_name", 
        "name_phone_ext", 
        "date", 
        "supervisor_manager", 
        "rd_group", 
        "suggestion"
    ]
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerow(data_dict)
        

if __name__ == "__main__":
    test_image = "data/sample_funsd_form.png"
    csv_output = "data/rpa_extraction.csv"
    
    if os.path.exists(test_image):
        extracted_data = extract_data_rpa(test_image)
        print("\nRPA Result:\n")
        for key, value in extracted_data.items():
            print(f"{key.upper()}: {value}")
        save_to_csv(extracted_data, csv_output)
    else:
        print(f"Error: Image {test_image} not found.")