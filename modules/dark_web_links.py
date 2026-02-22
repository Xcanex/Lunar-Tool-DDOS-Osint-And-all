import webbrowser
from rich.console import Console
from rich.table import Table

console = Console()

DARK_WEB_LINKS = {
    "1":  ("Mail2Tor", "https://mail2tor.com"),
    "2":  ("The Hidden Wiki", "https://thehiddenwiki.org"),
    "3":  ("Sci-Hub", "https://sci-hub.se"),
    "4":  ("SecureDrop", "https://securedrop.org"),
    "5":  ("DuckDuckGo Onion", "https://duckduckgo.com"),
    "6":  ("The CIA", "https://www.cia.gov"),
    "7":  ("Hidden Answers", "https://hiddenanswers.i2p"),
    "8":  ("DDoSNow", "https://ddosnow.com"),
    "9":  ("IPLogger", "https://iplogger.org"),
    "10": ("Grabify", "https://grabify.link"),
    "11": ("Whatstheirip", "https://whatstheirip.com"),
    "12": ("DoxBin", "https://doxbin.com"),
    "13": ("OSINT Industries", "https://osint.industries"),
    "14": ("Epieos", "https://epieos.com"),
    "15": ("Nuwber", "https://nuwber.com"),
    "16": ("OSINT Framework", "https://osintframework.com"),
    "17": ("Whatsmyname", "https://whatsmyname.app"),
    "18": ("SpyLink", "https://spylink.org"),
    "19": ("Stresser.zone", "https://stresser.zone"),
    "20": ("DDoS.services", "https://ddos.services"),
    "21": ("EasyCoin", "https://easycoin.cc"),
    "22": ("Deep Market", "https://deepmarket.org"),
    "23": ("OnionWallet", "https://onionwallet.com"),
    "24": ("Torch Search", "https://torch.ch"),
    "25": ("IPInfo", "https://ipinfo.io"),
    "26": ("Danex", "https://danex.io"),
    "27": ("Sentor", "https://sentor.org"),
    "28": ("Dark Mixer", "https://darkmixer.io"),
    "29": ("Mixabit", "https://mixabit.com"),
    "30": ("DrChronic", "https://drchronic.is"),
    "31": ("ccPal", "https://ccpal.cc"),
}


def run():
    while True:
        console.print()
        console.print("[bold #818cf8]  🕸️  DARK WEB LINKS[/]")
        console.print("[dim #312e81]  " + "─" * 48 + "[/]")


        keys = sorted(DARK_WEB_LINKS.keys(), key=lambda x: int(x))
        for i in range(0, len(keys), 3):
            row = ""
            for j in range(3):
                idx = i + j
                if idx < len(keys):
                    k = keys[idx]
                    name = DARK_WEB_LINKS[k][0]
                    row += f"[#818cf8][[/][white]{k.zfill(2)}[/][#818cf8]][/] {name:<16}"
            console.print(f"  {row}")

        console.print("[dim #312e81]  " + "─" * 48 + "[/]")
        console.print("  [dim]0 = Geri don[/]")
        console.print()

        choice = console.input("[bold #818cf8]  🕸️ sec > [/]").strip()

        if choice == "0" or choice.lower() == "back":
            break

        if choice in DARK_WEB_LINKS:
            name, url = DARK_WEB_LINKS[choice]
            console.print(f"[#818cf8]  Aciliyor: {name} -> {url}[/]")
            try:
                webbrowser.open(url)
            except Exception:
                console.print(f"[dim]  URL: {url}[/]")
        else:
            console.print("[red]  Gecersiz secim.[/]")
