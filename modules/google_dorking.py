import urllib.parse
import webbrowser
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


DORK_DB = {
    "1": {
        "name": "Hassas Dosyalar",
        "desc": "SQL dump, env, log, yedek dosyalar",
        "dorks": [
            ("SQL Dump",          'site:{t} filetype:sql'),
            ("ENV Dosyasi",       'site:{t} filetype:env'),
            ("Log Dosyasi",       'site:{t} filetype:log'),
            ("Config Dosyasi",    'site:{t} filetype:conf'),
            ("Yedek Dosya",       'site:{t} filetype:bak'),
            ("Eski Dosya",        'site:{t} filetype:old'),
            ("XML Data",          'site:{t} filetype:xml'),
            ("JSON Data",         'site:{t} filetype:json'),
            ("CSV Data",          'site:{t} filetype:csv'),
            ("Excel",             'site:{t} filetype:xlsx'),
            ("PDF Dokuman",       'site:{t} filetype:pdf'),
            ("Word Dokuman",      'site:{t} filetype:docx'),
            ("Bash Script",       'site:{t} filetype:sh'),
            ("PHP Config",        'site:{t} filetype:php.bak'),
        ],
    },
    "2": {
        "name": "Admin Panelleri",
        "desc": "Login, admin, dashboard panelleri",
        "dorks": [
            ("Admin Panel",       'site:{t} inurl:admin'),
            ("Login Sayfasi",     'site:{t} inurl:login'),
            ("Control Panel",     'site:{t} inurl:panel'),
            ("Dashboard",         'site:{t} inurl:dashboard'),
            ("WordPress Admin",   'site:{t} inurl:wp-admin'),
            ("cPanel",            'site:{t} inurl:cpanel'),
            ("phpMyAdmin",        'site:{t} inurl:phpmyadmin'),
            ("Webmail",           'site:{t} inurl:webmail'),
            ("Admin Login Title", 'site:{t} intitle:"admin login"'),
            ("Manager",           'site:{t} inurl:manager'),
        ],
    },
    "3": {
        "name": "Dizin Listeleme",
        "desc": "Acik dizinler, index of",
        "dorks": [
            ("Index Of",          'site:{t} intitle:"index of"'),
            ("Directory Listing", 'site:{t} intitle:"directory listing"'),
            ("Parent Directory",  'site:{t} intitle:"parent directory"'),
            ("Apache Status",     'site:{t} intitle:"Apache Status"'),
            ("Server Info",       'site:{t} intitle:"server info"'),
        ],
    },
    "4": {
        "name": "Veritabani",
        "desc": "DB dump, SQL injection izleri",
        "dorks": [
            ("phpMyAdmin",        'site:{t} inurl:phpmyadmin'),
            ("SQL INSERT",        'site:{t} filetype:sql "INSERT INTO"'),
            ("SQL CREATE",        'site:{t} filetype:sql "CREATE TABLE"'),
            ("DB Backup",         'site:{t} inurl:backup filetype:sql'),
            ("Adminer",           'site:{t} inurl:adminer'),
            ("DB Manager",        'site:{t} inurl:db inurl:manager'),
        ],
    },
    "5": {
        "name": "Sifre & Kimlik",
        "desc": "Sifre dosyalari, credential leak",
        "dorks": [
            ("Password TXT",      'site:{t} filetype:txt "password"'),
            ("Password LOG",      'site:{t} filetype:log "password"'),
            ("Username+Password", 'site:{t} "username" "password" filetype:txt'),
            ("Credentials",       'site:{t} inurl:credentials'),
            (".htpasswd",         'site:{t} filetype:htpasswd'),
            ("Shadow File",       'site:{t} intitle:"index of" "shadow"'),
            ("Private Key",       'site:{t} filetype:pem "PRIVATE KEY"'),
            ("SSH Key",           'site:{t} filetype:ppk'),
        ],
    },
    "6": {
        "name": "Konfigürasyon",
        "desc": "INI, YML, TOML, config dosyalari",
        "dorks": [
            ("INI Config",        'site:{t} filetype:ini'),
            ("YAML Config",       'site:{t} filetype:yml'),
            ("TOML Config",       'site:{t} filetype:toml'),
            ("CFG Config",        'site:{t} filetype:cfg'),
            ("Config URL",        'site:{t} inurl:config'),
            ("Setup URL",         'site:{t} inurl:setup'),
            (".env File",         'site:{t} "DB_PASSWORD" filetype:env'),
            ("wp-config",         'site:{t} "wp-config" filetype:txt'),
        ],
    },
    "7": {
        "name": "Subdomain",
        "desc": "Alt domain kesfetme",
        "dorks": [
            ("Subdomain 1",      'site:*.{t}'),
            ("Subdomain 2",      'site:*.*.{t}'),
            ("Related Sites",    'related:{t}'),
            ("Cache",            'cache:{t}'),
        ],
    },
    "8": {
        "name": "Hata Mesajlari",
        "desc": "SQL error, debug, stack trace",
        "dorks": [
            ("MySQL Error",       'site:{t} "SQL syntax" "mysql"'),
            ("PHP Warning",       'site:{t} "Warning:" "mysql"'),
            ("Fatal Error",       'site:{t} "Fatal error"'),
            ("Stack Trace",       'site:{t} "Stack trace"'),
            ("Debug Mode",        'site:{t} inurl:debug'),
            ("Laravel Debug",     'site:{t} "Whoops!" "Laravel"'),
            ("Django Debug",      'site:{t} "Traceback" "Django"'),
            ("ASP.NET Error",     'site:{t} "Server Error in"'),
        ],
    },
    "9": {
        "name": "API & Endpoint",
        "desc": "API endpoint, swagger, graphql",
        "dorks": [
            ("API Endpoint",      'site:{t} inurl:api'),
            ("Swagger",           'site:{t} inurl:swagger'),
            ("GraphQL",           'site:{t} inurl:graphql'),
            ("REST API",          'site:{t} inurl:rest'),
            ("API Docs",          'site:{t} intitle:"API documentation"'),
            ("JSON API",          'site:{t} inurl:api filetype:json'),
            (".git Exposed",      'site:{t} inurl:.git'),
        ],
    },
    "10": {
        "name": "Guvenlik Aciklari",
        "desc": "Upload, install, test sayfalar",
        "dorks": [
            ("Upload Sayfasi",    'site:{t} inurl:upload'),
            ("Install Sayfasi",   'site:{t} inurl:install'),
            ("Test Sayfasi",      'site:{t} inurl:test'),
            ("Backup File",       'site:{t} inurl:backup'),
            ("Staging",           'site:{t} inurl:staging'),
            ("Dev/Debug",         'site:{t} inurl:dev'),
            ("Robots.txt",        'site:{t} inurl:robots.txt'),
            ("Sitemap",           'site:{t} inurl:sitemap.xml'),
        ],
    },
}


def make_url(dork):
    return f"https://www.google.com/search?q={urllib.parse.quote(dork)}"


def run():
    while True:
        console.print()
        console.print("[bold #818cf8]  ╔══════════════════════════════════════════╗[/]")
        console.print("[bold #818cf8]  ║        GOOGLE DORKING ENGINE v2          ║[/]")
        console.print("[bold #818cf8]  ╚══════════════════════════════════════════╝[/]")
        console.print()

        console.print("  [bold white]1.[/] Hedef site - tum kategoriler")
        console.print("  [bold white]2.[/] Hedef site - kategori sec")
        console.print("  [bold white]3.[/] Ozel dork sorgusu")
        console.print("  [bold white]4.[/] Hazir dork sablonlari (hedefsiz)")
        console.print("  [bold white]5.[/] Toplu tarama + dosyaya kaydet")
        console.print("  [bold white]0.[/] Geri don\n")

        choice = console.input("[bold #818cf8]  >> dork > [/]").strip()

        if choice == "0":
            return


        elif choice == "1":
            target = console.input("[bold white]  Hedef domain: [/]").strip()
            if not target:
                console.print("[red]  Domain bos olamaz.[/]")
                continue

            results = []
            for cat_data in DORK_DB.values():
                cat_name = cat_data["name"]
                for dork_name, dork_tmpl in cat_data["dorks"]:
                    d = dork_tmpl.format(t=target)
                    url = make_url(d)
                    results.append((cat_name, dork_name, d, url))

            console.print(f"\n[bold #818cf8]  {target} icin {len(results)} dork olusturuldu[/]\n")

            current_cat = ""
            for cat, name, dork, url in results:
                if cat != current_cat:
                    current_cat = cat
                    console.print(f"\n  [bold #a78bfa]--- {cat} ---[/]")
                console.print(f"  [white]{name:<20}[/] {dork}")
                console.print(f"  [dim]{url}[/]")

            console.print(f"\n[#818cf8]  Toplam: {len(results)} dork[/]")

            save = console.input("\n[bold white]  Dosyaya kaydet? (e/h): [/]").strip().lower()
            if save == "e":
                _save_to_file(target, results)


        elif choice == "2":
            console.print()
            for k, v in DORK_DB.items():
                console.print(f"  [white]{k.rjust(2)}.[/] {v['name']:<22} [dim]{v['desc']}[/]")

            cat_choice = console.input("\n[bold white]  Kategori: [/]").strip()
            if cat_choice not in DORK_DB:
                console.print("[red]  Gecersiz kategori.[/]")
                continue

            target = console.input("[bold white]  Hedef domain: [/]").strip()
            if not target:
                console.print("[red]  Domain bos olamaz.[/]")
                continue

            cat_data = DORK_DB[cat_choice]
            console.print(f"\n[bold #a78bfa]  {cat_data['name']} - {target}[/]\n")

            results = []
            for i, (dork_name, dork_tmpl) in enumerate(cat_data["dorks"], 1):
                d = dork_tmpl.format(t=target)
                url = make_url(d)
                results.append((cat_data["name"], dork_name, d, url))
                console.print(f"  [white]{i:2}. {dork_name:<20}[/] {d}")
                console.print(f"     [dim]{url}[/]")

            console.print(f"\n  [dim]Numara girin = tarayicida ac | a = tumunu ac | 0 = geri[/]")

            while True:
                sub = console.input("[bold #818cf8]  >> ac > [/]").strip()
                if sub == "0":
                    break
                elif sub.lower() == "a":
                    for _, _, _, url in results:
                        try:
                            webbrowser.open_new_tab(url)
                        except Exception:
                            pass
                    console.print("[green]  Tum linkler acildi.[/]")
                    break
                elif sub.isdigit() and 1 <= int(sub) <= len(results):
                    idx = int(sub) - 1
                    try:
                        webbrowser.open_new_tab(results[idx][3])
                        console.print(f"  [green]+[/] {results[idx][1]} acildi")
                    except Exception:
                        console.print(f"  [yellow]{results[idx][3]}[/]")

        elif choice == "3":
            dork = console.input("[bold white]  Dork sorgusu: [/]").strip()
            if dork:
                url = make_url(dork)
                console.print(f"\n  [white]Dork:[/] {dork}")
                console.print(f"  [white]Link:[/] {url}")
                ac = console.input("\n[bold white]  Tarayicide ac? (e/h): [/]").strip().lower()
                if ac == "e":
                    try:
                        webbrowser.open_new_tab(url)
                        console.print("[green]  Acildi.[/]")
                    except Exception:
                        pass

        elif choice == "4":
            templates = [
                ("Tum Passwordlar",    '"password" filetype:txt'),
                ("Tum SQL Dumplari",   '"INSERT INTO" filetype:sql'),
                ("Acik Kameralar",     'inurl:"/view.shtml" intitle:"Network Camera"'),
                ("Acik Printerlar",    'inurl:":631" "printers"'),
                ("FTP Serverler",      'intitle:"index of" inurl:ftp'),
                ("Private Key",        '"PRIVATE KEY" filetype:pem'),
                ("SSH Config",         'filetype:conf "sshd_config"'),
                ("VPN Config",         'filetype:ovpn "remote"'),
                ("Env Dosyalari",      '"DB_PASSWORD" filetype:env'),
                ("WordPress Config",   '"wp-config.php" filetype:txt'),
                ("Exposed .git",       'intitle:"index of" ".git"'),
                ("Server Status",      'intitle:"Apache Status" "Server Version"'),
                ("phpinfo()",          'intitle:"phpinfo()" "Configuration"'),
                ("Admin Panelleri",    'intitle:"admin" inurl:login'),
                ("Pastebin Leak",      'site:pastebin.com "password"'),
            ]

            console.print("\n[bold #a78bfa]  Hazir Dork Sablonlari[/]\n")
            for i, (name, dork) in enumerate(templates, 1):
                console.print(f"  [white]{i:2}.[/] {name:<22} [dim]{dork}[/]")

            console.print(f"\n  [dim]Numara girin = tarayicida ac | 0 = geri[/]")
            sub = console.input("[bold #818cf8]  >> sablon > [/]").strip()
            if sub.isdigit() and 1 <= int(sub) <= len(templates):
                idx = int(sub) - 1
                url = make_url(templates[idx][1])
                console.print(f"\n  [white]{templates[idx][0]}[/]")
                console.print(f"  {url}")
                try:
                    webbrowser.open_new_tab(url)
                    console.print("[green]  Acildi.[/]")
                except Exception:
                    pass

        elif choice == "5":
            target = console.input("[bold white]  Hedef domain: [/]").strip()
            if not target:
                console.print("[red]  Domain bos olamaz.[/]")
                continue

            results = []
            for cat_data in DORK_DB.values():
                for dork_name, dork_tmpl in cat_data["dorks"]:
                    d = dork_tmpl.format(t=target)
                    url = make_url(d)
                    results.append((cat_data["name"], dork_name, d, url))

            _save_to_file(target, results)

        else:
            console.print("[red]  Gecersiz secim.[/]")


def _save_to_file(target, results):
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "dorks")
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, f"dorks_{target.replace('.', '_')}.txt")

    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"Google Dorks - {target}\n")
        f.write(f"{'=' * 60}\n\n")
        current_cat = ""
        for cat, name, dork, url in results:
            if cat != current_cat:
                current_cat = cat
                f.write(f"\n--- {cat} ---\n")
            f.write(f"{name}: {dork}\n")
            f.write(f"  {url}\n\n")

    console.print(f"[bold green]  {len(results)} dork kaydedildi: output/dorks/{os.path.basename(fname)}[/]")
