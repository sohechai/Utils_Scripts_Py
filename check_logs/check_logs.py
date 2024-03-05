# Description: This script is used to check if the logs are complete. It compares the logs with the establishment list and prints the missing establishments.
# Usage: python check_establishments.py <log_file> <establishment_list_file>

import sys
from colorama import Fore, Style

def read_log_file(log_link, scheme):
    extracted_list = []
    with open(log_link, 'r') as f:
        sub_list = []
        for line in f:           
            if line.strip().startswith(scheme):
                if sub_list:
                    extracted_list.append(sub_list)
                    sub_list = []
                sub_list.append(line.strip())
            else:
                sub_list.append(line.strip())        
            for i, element in enumerate(sub_list):
                sub_list[i] = element.replace("---------------------", "")
        if sub_list:
            extracted_list.append(sub_list)     
    return extracted_list

def read_establishment_file(estab_link):
    with open(estab_link, 'r') as f:
        text = f.readlines() 
        file_content = [content.strip() for content in text]
        for i, element in enumerate(file_content):
            file_content[i] = element.replace("-", "")
        return file_content

def compare_lists(log_file, estab_file):
    global valid_file_elements 
    global establishment_file_elements
    global log_file_elements
    
    log_file_elements = read_log_file(log_file, "---------------------establishment")
    establishment_file_elements = read_establishment_file(estab_file)
    establishment_file_elements = [elem.strip() for elem in establishment_file_elements if elem.strip()]

    valid_file_elements = []
    
    for estab_element in establishment_file_elements:          
        for sub_list in log_file_elements:
            if estab_element.lower() in sub_list and estab_element.lower() != "":
                valid_file_elements.append(estab_element)

if len(sys.argv) != 3:
    print(Fore.RED + "Usage :\npython check_establishments.py <log_file> <establishment_list_file>" + Fore.RESET)
    sys.exit()

log_file_arg = sys.argv[1]
estab_file_arg = sys.argv[2]

scheme = "---------------------establishment"
compare_lists(log_file_arg, estab_file_arg)

err = False
error_list = []
for index, sub_list in enumerate(log_file_elements):
    for i, element in enumerate(sub_list):
        if element.startswith("E_"):
            err = True
            error_list.append(sub_list[0])

if error_list:
    print(Fore.RED + "[ERROR]" + Style.RESET_ALL)
    for err in error_list:
        print(err)

if establishment_file_elements == valid_file_elements and not err:
    print(Fore.GREEN + "[OK]\n" + Style.RESET_ALL + "Logs are complete.")
elif establishment_file_elements == valid_file_elements:
    print("")
    print(Fore.GREEN + "[OK]\n" + Style.RESET_ALL + "Logs are complete.")
    print("")
else:
    for item in establishment_file_elements:
        if item not in valid_file_elements:
            print(Fore.RED + "[KO]" + Style.RESET_ALL)
            print(f"{item}")
