# Description: This script is used to analyze a log file and make a report of usefull information
# Usage: python3 check_ETB.py <log_file>

import sys
from colorama import Fore, Style

def read_establishments_info(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    establishments_info = {}
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) >= 2:
            establishments_info[parts[1]] = line.strip()
    return establishments_info

establishments_info = read_establishments_info('./ETB_info.txt')

def generate_report_line(establishment, vfm_count, agents_count, rs, error):
    if establishment is None or vfm_count == 0:
        return None
    report_line = f"{Fore.GREEN}({vfm_count} VFM) - "
    report_line += f"{Fore.YELLOW}{establishments_info.get(establishment)} - "
    if agents_count is not None and agents_count.isdigit():
        report_line += f"{Fore.GREEN}({agents_count} agent(s)) "
    if error is not None:
        report_line += f"{Fore.RED}[{error}]"
    report_line += Style.RESET_ALL
    return report_line

def analyze_log(log_file):
    with open(log_file, 'r') as file:
        lines = file.readlines()

    establishment = None
    vfm_count = 0
    agents_count = None
    rs = None
    error = None
    report = []
    establishments_with_rs = []
    establishments_without_rs = []

    for i in range(len(lines)):
        line = lines[i]
        if "E_" in line:
            error = "ERREUR"
        if "--------------server" in line:
            report_line = generate_report_line(establishment, vfm_count, agents_count, rs, error)
            if report_line is not None:
                report.append(report_line)
                if rs == "RS":
                    establishments_with_rs.append(establishment)
                else:
                    establishments_without_rs.append(establishment)
            establishment = line.strip().split()[-1].replace('--------------', '')
            vfm_count = 0
            agents_count = None
            rs = None
            error = None
        elif "journee.travail" in line:
            for j in range(i, len(lines)):
                if "row" in lines[j]:
                    agents_count = ''.join(filter(str.isdigit, lines[j]))
                    break
        elif "Nom de fichier" in line:
            vfm_count += 1
        elif "insert" in line:
            for j in range(i, len(lines)):
                if "row" in lines[j]:
                    num_rows = int(''.join(filter(str.isdigit, lines[j])))
                    rs = "RS" if num_rows > 0 else "Pas de RS"
                    break

    report_line = generate_report_line(establishment, vfm_count, agents_count, rs, error)
    if report_line is not None:
        report.append(report_line)
        if rs == "RS":
            establishments_with_rs.append(establishment)
        else:
            establishments_without_rs.append(establishment)

    establishments_info = read_establishments_info('./ETB_info.txt')
    establishments_with_rs.sort()
    establishments_without_rs.sort()

    print(Fore.BLACK + "[Tous les établissements] (" + str(len(establishments_with_rs) + len(establishments_without_rs)) + " établissements)" + Fore.RESET)
    for establishment in establishments_with_rs:
        print(Fore.BLUE + establishments_info.get(establishment) + Fore.RESET)
    for establishment in establishments_without_rs:
        print(Fore.BLUE + establishments_info.get(establishment) + Fore.RESET)
    
    print('')

    print(Fore.BLACK + "[Établissements avec RS] (" + str(len(establishments_with_rs)) + " établissements)" + Fore.RESET)
    for establishment in establishments_with_rs:
        print(Fore.GREEN + establishments_info.get(establishment) + Fore.RESET)

    print(Fore.BLACK + "\n[Établissements sans RS] (" + str(len(establishments_without_rs)) + " établissements)" + Fore.RESET)
    for establishment in establishments_without_rs:
        print(Fore.YELLOW + establishments_info.get(establishment) + Fore.RESET)

    return report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        report = analyze_log(log_file)

        print(Fore.BLACK + Style.BRIGHT + "\n╔═════════════════════╗")
        print("║    COMPTE RENDU     ║")
        print("╚═════════════════════╝" + Style.RESET_ALL)

        if not report:
            print(Fore.GREEN + "Aucun établissement n'a produit de VFM" + Fore.RESET)
        else:
            for line in report:
                print(line)
    else:
        print(Fore.RED + "Usage :\npython3 check_ETB.py <log_file>" + Fore.RESET)