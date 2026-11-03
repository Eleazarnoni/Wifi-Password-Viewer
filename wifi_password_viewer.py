"""
WiFi Password Viewer
By HexSecTeam | Built by Eleazar Ofutet
View saved WiFi profiles & passwords stored on your system

VirusTotal Note:
This script may be flagged as HackTool/PUP by antivirus.
This is a FALSE POSITIVE - Expected for password viewer tools.
It uses: netsh wlan show profile "NAME" key=clear
AV detects it as HackTool.Win32.PassView / Riskware
But it's NOT malware - Just displays YOUR saved passwords locally.
No network upload, open source, ethical use only.
"""

import subprocess
import sys

def banner():
    print(r"""
    ╔════════════════════════════════════════╗
    ║  WiFi Password Viewer                ║
    ║  By HexSecTeam                       ║
    ║  Built by Eleazar Ofutet             ║
    ╚════════════════════════════════════════╝
    """)

def get_profiles():
    try:
        output = subprocess.check_output(
            "netsh wlan show profiles", shell=True, text=True
        )
        names = [line.split(":")[1].strip() for line in output.split("\n") if "All User Profile" in line]
        return names
    except Exception as e:
        print(f"Error: {e} - Run as Administrator")
        return []

def main():
    banner()
    print("[*] Scanning saved WiFi profiles...\n")
    names = get_profiles()
    if not names:
        print("No saved WiFi profiles found!")
        return
    for i, name in enumerate(names, 1):
        print(f"[{i}] {name}")
    try:
        choice = input("\nChoose WiFi number (or 'all'): ").strip().lower()
        if choice == "all":
            for name in names:
                result = subprocess.check_output(
                    f'netsh wlan show profile "{name}" key=clear',
                    shell=True, text=True
                )
                print(f"\nProfile: {name}\n{result}")
        else:
            wifi = names[int(choice)-1]
            result = subprocess.check_output(
                f'netsh wlan show profile "{wifi}" key=clear',
                shell=True, text=True
            )
            print(result)
            for line in result.split("\n"):
                if "Key Content" in line:
                    print(f"\nPassword: {line.split(':')[1].strip()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if sys.platform != "win32":
        print("Works only on Windows")
        sys.exit(1)
    main()