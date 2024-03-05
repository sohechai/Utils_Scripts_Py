# Description: This script reads a file and returns the batch number and signal if there is late batch >= 18:00
# Usage: python script_name.py file_name.txt

from colorama import Fore, Back, Style
import sys

if len(sys.argv) != 2:
    print("Usage: python script_name.py file_name.txt")
    sys.exit(1)

file_name = sys.argv[1]

try:
    with open(file_name, 'r') as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"The file {file_name} was not found.")
    sys.exit(1)

order_numbers = []
request_times = []

for line in lines:
    if '|' in line:
        columns = line.split('|')
        if len(columns) >= 3:
            try:
                num = int(columns[1].strip())
                time = int(columns[2].strip())
                order_numbers.append(num)
                if time >= 180000:
                    print(Fore.RED + "[DELAY] batch number: " + str(num) + " at: " + str(time) + Fore.RESET)
            except ValueError:
                continue

print(Fore.CYAN + "[BATCH]")
print("(" + ','.join(map(str, order_numbers)) + ")" + Fore.RESET)
