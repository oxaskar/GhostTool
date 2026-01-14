#!/usr/bin/env python3
import os
import sys
import time
import requests
import socket
import subprocess
import random
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

# Renkleri başlat
init()

# Tool Bilgileri
TOOL_ADI = "PhantomStrike"
VERSIYON = "3.0"
GELISTIRICI = "0xaskar "
GITHUB = "https://github.com/0xaskar"
MOTTO = " Pentest Aracı"

# Özel ASCII Başlık
BANNER = f"""
{Fore.RED}
▓█████▄  ██▀███   ▄▄▄       ███▄ ▄███▓ ██▓███   ██▓    ▄▄▄     ▄▄▄█████▓
▒██▀ ██▌▓██ ▒ ██▒▒████▄    ▓██▒▀█▀ ██▒▓██░  ██▒▓██▒   ▒████▄   ▓  ██▒ ▓▒
░██   █▌▓██ ░▄█ ▒▒██  ▀█▄  ▓██    ▓██░▓██░ ██▓▒▒██░   ▒██  ▀█▄ ▒ ▓██░ ▒░
░▓█▄   ▌▒██▀▀█▄  ░██▄▄▄▄██ ▒██    ▒██ ▒██▄█▓▒ ▒▒██░   ░██▄▄▄▄██░ ▓██▓ ░ 
░▒████▓ ░██▓ ▒██▒ ▓█   ▓██▒▒██▒   ░██▒▒██▒ ░  ░░██████▒▓█   ▓██▒ ▒██▒ ░ 
 ▒▒▓  ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ░  ░▒▓▒░ ░  ░░ ▒░▓  ░▒▒   ▓▒█░ ▒ ░░   
 ░ ▒  ▒   ░▒ ░ ▒░  ▒   ▒▒ ░░  ░      ░░▒ ░     ░ ░ ▒  ░ ▒   ▒▒ ░   ░    
 ░ ░  ░   ░░   ░   ░   ▒   ░      ░   ░░         ░ ░    ░   ▒    ░      
   ░       ░           ░  ░       ░                ░  ░     ░  ░        
 ░                                                                      
{Fore.BLUE}─────────────────────────────────────────────────────────────
{Fore.MAGENTA}╔══════════════════════════════════════════════════════╗
{Fore.MAGENTA}║ {Fore.CYAN}Sürüm: {VERSIYON}{' '*(48-len(VERSIYON)-7)}{Fore.MAGENTA}║
{Fore.MAGENTA}║ {Fore.CYAN}Geliştirici: {GELISTIRICI}{' '*(48-len(GELISTIRICI)-14)}{Fore.MAGENTA}║
{Fore.MAGENTA}║ {Fore.CYAN}GitHub: {GITHUB}{' '*(48-len(GITHUB)-9)}{Fore.MAGENTA}║
{Fore.MAGENTA}║ {Fore.RED}{MOTTO}{' '*(48-len(MOTTO))}{Fore.MAGENTA}║
{Fore.MAGENTA}╚══════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

# Renk Şeması
R = Fore.RED
G = Fore.GREEN
B = Fore.BLUE
Y = Fore.YELLOW
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE

def ekrani_temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def yukleniyor(baslik, sure=2):
    print(f"\n{Y}[+] {baslik}...{W}")
    for i in range(sure*5):
        print(f"{C}[{'>'*(i+1)}{' '*(sure*5-i-1)}]{W}", end='\r')
        time.sleep(0.2)
    print()

def menu_goster():
    ekrani_temizle()
    print(BANNER)
    print(f"{C}1.{W} XSS Açık Tarayıcı")
    print(f"{C}2.{W} SQL Enjeksiyon Tarayıcı")
    print(f"{C}3.{W} Admin Panel Bulucu")
    print(f"{C}4.{W} Port Tarayıcı")
    print(f"{C}5.{W} Subdomain Bulucu")
    print(f"{C}6.{W} Web Zafiyet Analiz")
    print(f"{C}0.{W} Çıkış")
    print(f"\n{M}Seçim yapın: {W}", end="")

# 1. XSS Açık Tarayıcı
def xss_tarayici():
    ekrani_temizle()
    print(f"{R}=== XSS Açık Tarayıcı ==={W}\n")
    
    url = input(f"{B}Hedef URL (örn: http://site.com): {W}")
    
    yukleniyor("XSS açıkları taranıyor", 3)
    
    payloads = ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>', 
                "'\"><script>alert(1)</script>", '<svg/onload=alert(1)>']
    
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        forms = soup.find_all('form')
        
        if not forms:
            print(f"\n{R}[!] Form bulunamadı!{W}")
        else:
            print(f"\n{G}[+] {len(forms)} form bulundu{W}")
            for i, form in enumerate(forms, 1):
                print(f"\n{Y}[*] Form {i}:{W}")
                action = form.get('action', '')
                method = form.get('method', 'get').upper()
                print(f"{C}Action:{W} {action}")
                print(f"{C}Method:{W} {method}")
                
                for payload in payloads:
                    print(f"\n{M}Payload test ediliyor:{W} {payload}")
                    time.sleep(0.5)
                    if method == 'POST':
                        data = {}
                        for input_tag in form.find_all('input'):
                            name = input_tag.get('name', '')
                            if name:
                                data[name] = payload
                        try:
                            post_url = url + action if action.startswith('/') else url + '/' + action
                            r = requests.post(post_url, data=data)
                            if payload in r.text:
                                print(f"{G}[+] XSS Açığı Bulundu!{W}")
                            else:
                                print(f"{R}[-] XSS Açığı Bulunamadı{W}")
                        except:
                            print(f"{R}[-] Hata oluştu!{W}")
    
    except Exception as e:
        print(f"\n{R}[!] Hata: {str(e)}{W}")
    
    input(f"\n{B}Devam etmek için Enter'a basın...{W}")

# 2. SQL Enjeksiyon Tarayıcı
def sql_tarayici():
    ekrani_temizle()
    print(f"{R}=== SQL Enjeksiyon Tarayıcı ==={W}\n")
    
    url = input(f"{B}Hedef URL (örn: http://site.com/page?id=1): {W}")
    
    yukleniyor("SQL açıkları taranıyor", 3)
    
    payloads = ["'", "' OR '1'='1", "' OR 1=1--", "' OR 1=1#", "' OR 1=1/*"]
    
    try:
        for payload in payloads:
            test_url = url + payload if '?' in url else url + '?' + payload
            print(f"\n{M}Test ediliyor:{W} {test_url}")
            r = requests.get(test_url)
            
            error_messages = [
                "SQL syntax", "MySQL", "ORA-", "syntax error",
                "unclosed quotation mark", "SELECT", "UNION"
            ]
            
            vulnerable = False
            for error in error_messages:
                if error.lower() in r.text.lower():
                    vulnerable = True
                    break
            
            if vulnerable:
                print(f"{G}[+] SQL Enjeksiyon Açığı Bulundu!{W}")
                break
            else:
                print(f"{R}[-] SQL Açığı Bulunamadı{W}")
    
    except Exception as e:
        print(f"\n{R}[!] Hata: {str(e)}{W}")
    
    input(f"\n{B}Devam etmek için Enter'a basın...{W}")

# 3. Admin Panel Bulucu
def admin_bulucu():
    ekrani_temizle()
    print(f"{R}=== Admin Panel Bulucu ==={W}\n")
    
    url = input(f"{B}Hedef URL (örn: http://site.com): {W}")
    
    yukleniyor("Admin panelleri aranıyor", 3)
    
    admin_paths = [
        "admin", "admin.php", "admin/login", "adminpanel", 
        "wp-admin", "administrator", "login", "yonetim",
        "panel", "controlpanel", "cms", "backend"
    ]
    
    found = False
    for path in admin_paths:
        test_url = url + '/' + path
        print(f"\n{M}Test ediliyor:{W} {test_url}")
        try:
            r = requests.get(test_url, timeout=5)
            if r.status_code == 200:
                print(f"{G}[+] Olası Admin Paneli: {test_url}{W}")
                found = True
            else:
                print(f"{R}[-] Bulunamadı{W}")
        except:
            print(f"{R}[-] Hata oluştu!{W}")
    
    if not found:
        print(f"\n{R}[!] Admin paneli bulunamadı{W}")
    
    input(f"\n{B}Devam etmek için Enter'a basın...{W}")

# 4. Port Tarayıcı
def port_tarayici():
    ekrani_temizle()
    print(f"{R}=== Port Tarayıcı ==={W}\n")
    
    hedef = input(f"{B}Hedef IP veya Domain: {W}")
    portlar = input(f"{B}Port aralığı (örn: 80-443): {W}") or "80-443"
    
    try:
        baslangic, bitis = map(int, portlar.split('-'))
    except:
        baslangic, bitis = 80, 443
    
    yukleniyor(f"{baslangic}-{bitis} portları taranıyor", 3)
    
    print(f"\n{Y}[*] {hedef} için port taraması başladı{W}")
    
    acik_portlar = []
    for port in range(baslangic, bitis+1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((hedef, port))
            if result == 0:
                print(f"{G}[+] Port {port} açık{W}")
                acik_portlar.append(port)
            else:
                print(f"{R}[-] Port {port} kapalı{W}")
            sock.close()
        except:
            print(f"{R}[!] Port {port} hatası{W}")
    
    print(f"\n{Y}[*] Tarama tamamlandı!{W}")
    if acik_portlar:
        print(f"{G}[+] Açık portlar: {', '.join(map(str, acik_portlar))}{W}")
    else:
        print(f"{R}[-] Açık port bulunamadı{W}")
    
    input(f"\n{B}Devam etmek için Enter'a basın...{W}")

# 5. Subdomain Bulucu
def subdomain_bulucu():
    ekrani_temizle()
    print(f"{R}=== Subdomain Bulucu ==={W}\n")
    
    domain = input(f"{B}Hedef Domain (örn: site.com): {W}")
    
    yukleniyor("Subdomain'ler aranıyor", 3)
    
    subdomains = [
        "www", "mail", "ftp", "webmail", "admin", "blog",
        "dev", "test", "api", "secure", "portal", "cpanel"
    ]
    
    found = []
    for sub in subdomains:
        test_domain = f"{sub}.{domain}"
        print(f"\n{M}Test ediliyor:{W} {test_domain}")
        try:
            ip = socket.gethostbyname(test_domain)
            print(f"{G}[+] Bulundu: {test_domain} -> {ip}{W}")
            found.append(test_domain)
        except:
            print(f"{R}[-] Bulunamadı{W}")
    
    print(f"\n{Y}[*] Tarama tamamlandı!{W}")
    if found:
        print(f"{G}[+] Bulunan subdomain'ler: {', '.join(found)}{W}")
    else:
        print(f"{R}[-] Subdomain bulunamadı{W}")
    
    input(f"\n{B}Devam etmek için Enter'a basın...{W}")

# 6. Web Zafiyet Analiz
def web_zafiyet_analiz():
    ekrani_temizle()
    print(f"{R}=== Web Zafiyet Analiz ==={W}\n")
    
    url = input(f"{B}Hedef URL (örn: http://site.com): {W}")
    
    yukleniyor("Kapsamlı web zafiyet analizi yapılıyor", 5)
    
    print(f"\n{Y}[*] Temel Bilgiler:{W}")
    try:
        r = requests.get(url)
        print(f"{C}Sunucu:{W} {r.headers.get('Server', 'Bilinmiyor')}")
        print(f"{C}X-Powered-By:{W} {r.headers.get('X-Powered-By', 'Bilinmiyor')}")
    except:
        print(f"{R}[!] Bilgi alınamadı{W}")
    
    print(f"\n{Y}[*] Güvenlik Başlıkları Kontrolü:{W}")
    security_headers = [
        'X-Frame-Options', 'X-XSS-Protection',
        'X-Content-Type-Options', 'Content-Security-Policy',
        'Strict-Transport-Security'
    ]
    
    missing = []
    for header in security_headers:
        if header in r.headers:
            print(f"{G}[+] {header}: {r.headers[header]}{W}")
        else:
            print(f"{R}[-] {header} eksik{W}")
            missing.append(header)
    
    if missing:
        print(f"\n{R}[!] Eksik güvenlik başlıkları: {', '.join(missing)}{W}")
    else:
        print(f"\n{G}[+] Tüm kritik güvenlik başlıkları mevcut{W}")
    
    input(f"\n{B}Devam etmek için Enter'a basın...{W}")

def main():
    while True:
        menu_goster()
        secim = input().strip()
        
        if secim == "1":
            xss_tarayici()
        elif secim == "2":
            sql_tarayici()
        elif secim == "3":
            admin_bulucu()
        elif secim == "4":
            port_tarayici()
        elif secim == "5":
            subdomain_bulucu()
        elif secim == "6":
            web_zafiyet_analiz()
        elif secim == "0":
            print(f"\n{G}PhantomStrike kapatılıyor. Gölgelerde kalın!{W}")
            sys.exit(0)
        else:
            print(f"\n{R}Geçersiz seçim!{W}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{G}PhantomStrike kapatılıyor. Gölgelerde kalın!{W}")
        sys.exit(0)
