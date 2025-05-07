import urllib.request
import http.cookiejar as cookielib
import re
import sys
import random
import threading
import socket
import subprocess

# Renkler
W  = "\033[0m"
R  = "\033[31m"
G  = "\033[32m"
O  = "\033[33m"
B  = "\033[34m"

def logo():
    print(G + "\n                                                                   ")

# Clear ekran ve logo göster
if sys.platform.startswith('linux'):
    subprocess.call("clear", shell=True)
else:
    subprocess.call("cls", shell=True)
logo()

# Örnek search fonksiyonu (düzenlenmiş)
def search(inurl, maxc):
    urls = []
    for site in sitearray:
        site = site.strip()
        page = 0
        try:
            while page < int(maxc):
                jar = cookielib.CookieJar()
                query = inurl + "+site:" + site
                results_web = 'http://www.search-results.com/web?q=' + query + '&hl=en&page=' + str(page) + '&src=hmp'
                request_web = urllib.request.Request(results_web)
                agent = random.choice(header)
                request_web.add_header('User-Agent', agent)
                opener_web = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
                text = opener_web.open(request_web).read().decode('utf-8')
                stringreg = re.compile('(?<=href=")(.*?)(?=")')
                names = stringreg.findall(text)
                page += 1
                for name in names:
                    if name not in urls:
                        # Filtreleme işlemleri
                        if re.search(r'\(', name) or re.search("<", name) or re.search(r"^/", name) or re.search(r"^(http://)\d", name):
                            pass
                        elif any(x in name for x in ["google", "duckduckgo", "ixquick", "webcrawler", "dogpile", "yippy", "Bing", "youtube", "phpbuddy", "iranhack", "phpbuilder", "codingforums", "phpfreaks", "br.search.yahoo", "ajax.googleapis", "search.lycos", "gigablast", "web.search.naver", "dmoz", "%"]):
                            pass
                        else:
                            urls.append(name)
                percent = int((page / int(maxc)) * 100)
                sys.stdout.write("\rSite: %s | Nycto Collected urls: %s | Percent Done: %s | Current page no.: %s <> " % (site, str(len(urls)), str(percent), str(page)))
                sys.stdout.flush()
        except KeyboardInterrupt:
            pass
    tmplist = []
    print("\n\n[+] URLS (unsorted): ", len(urls))
    for url in urls:
        try:
            host = url.split("/", 3)
            domain = host[2]
            if domain not in tmplist and "=" in url:
                finallist.append(url)
                tmplist.append(domain)
        except:
            pass
    print("[+] URLS (sorted)  : ", len(finallist))
    return finallist

# Geri kalan fonksiyonlar ve sınıflar için de benzer düzenlemeleri yapmalısınız.
