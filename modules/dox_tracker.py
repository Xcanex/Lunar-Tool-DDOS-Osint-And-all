import webbrowser
import urllib.parse
from rich.console import Console
console = Console()

SEARCH_SITES = {
    "1":  ("Facebook",     "https://www.facebook.com/search/top/?q={}"),
    "2":  ("YouTube",      "https://www.youtube.com/results?search_query={}"),
    "3":  ("Twitter/X",    "https://twitter.com/search?f=users&q={}"),
    "4":  ("TikTok",       "https://www.tiktok.com/search?q={}"),
    "5":  ("Instagram",    "https://www.instagram.com/{}"),
    "6":  ("LinkedIn",     "https://www.linkedin.com/search/results/all/?keywords={}"),
    "7":  ("Reddit",       "https://www.reddit.com/search/?q={}"),
    "8":  ("GitHub",       "https://github.com/search?q={}"),
    "9":  ("Pinterest",    "https://www.pinterest.com/search/pins/?q={}"),
    "10": ("Google",       "https://www.google.com/search?q={}"),
    "11": ("Bing",         "https://www.bing.com/search?q={}"),
    "12": ("Yandex",       "https://yandex.com/search/?text={}"),
}


def run():
    console.print("[bold #818cf8]  DOX TRACKER[/]")
    console.print("[dim]  Sosyal medyada kisi arama[/]\n")
    console.print("  [white]1.[/] Kullanici adi ile ara")
    console.print("  [white]2.[/] Ad-soyad ile ara")
    console.print("  [white]3.[/] Serbest arama")
    console.print("  [white]0.[/] Geri don\n")

    mode = console.input("[bold white]  Secim: [/]").strip()
    if mode == "0":
        return

    if mode == "1":
        query = console.input("[bold white]  Kullanici adi: [/]").strip()
    elif mode == "2":
        ad = console.input("[bold white]  Ad: [/]").strip()
        soyad = console.input("[bold white]  Soyad: [/]").strip()
        query = f"{ad} {soyad}"
    elif mode == "3":
        query = console.input("[bold white]  Arama sorgusu: [/]").strip()
    else:
        console.print("[red]  Gecersiz secim.[/]")
        return

    if not query:
        console.print("[red]  Sorgu bos olamaz.[/]")
        return

    encoded = urllib.parse.quote(query)

    console.print(f"\n[#818cf8]  Aranacak: '{query}'[/]")
    console.print("[dim]  " + "-" * 50 + "[/]")
    for k, (name, url) in SEARCH_SITES.items():
        link = url.format(encoded)
        console.print(f"  [white]{k.rjust(2)}.[/] {name:<12} {link}")
    console.print("[dim]  " + "-" * 50 + "[/]")
    console.print("  [dim]a=Tum siteleri ac | numara=tek site ac | 0=geri[/]")

    while True:
        choice = console.input("[bold #818cf8]  >> tracker > [/]").strip()
        if choice == "0":
            break
        elif choice.lower() == "a":
            for k, (name, url) in SEARCH_SITES.items():
                link = url.format(encoded)
                try:
                    webbrowser.open_new_tab(link)
                except Exception:
                    pass
                console.print(f"  [green]+[/] {name} acildi")
            console.print("[#818cf8]  Tum siteler acildi.[/]")
        elif choice in SEARCH_SITES:
            name, url = SEARCH_SITES[choice]
            link = url.format(encoded)
            try:
                webbrowser.open_new_tab(link)
                console.print(f"  [green]+[/] {name} acildi")
            except Exception:
                console.print(f"  [yellow]Link: {link}[/]")
        else:
            console.print("[red]  Gecersiz secim.[/]")
