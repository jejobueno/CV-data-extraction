from extractSections import get_section_data
from convertListToString import listToString
from match_name_surname import extract_name
from match_email import extract_email
from match_phone_number import extract_mobile_number

sections = get_section_data('curriculum_vitae_data/word/3.docx')


# Check overall personal_info section
personal_info = sections['text'].iloc[0]
#print(type(personal_info))

# Convert to string
info_str = listToString(personal_info)

# Check person's name
person_name = extract_name(info_str)
print(person_name[0])

# Check e-mail
email = extract_email(info_str)
print(email)
#print(list(set(personal_info).intersection(person_name)))

# Check phone number
phone_num = extract_mobile_number(info_str)
print(phone_num)
