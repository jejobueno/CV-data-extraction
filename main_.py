from extractSections import get_section_data
from match_name_email import certificate_name
from match_email import extract_email
from match_phone_number import extract_mobile_number


# Check person's name
person_name = certificate_name(pdf)
print(person_name[0])

# Check e-mail
email = extract_email(pdf)
print(email)
#print(list(set(personal_info).intersection(person_name)))

# Check phone number
phone_num = extract_mobile_number(pdf)
print(phone_num)
