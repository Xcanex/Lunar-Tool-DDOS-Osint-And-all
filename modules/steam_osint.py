import requests
from rich.console import Console
from rich.table import Table
console = Console()

def run():
    user = console.input("[bold white]  Steam vanity URL veya ID: [/]").strip()
    if not user:
        console.print("[red]  Bos olamaz.[/]")
        return
    console.print(f"[#818cf8]  Steam profili araniyor...[/]")
    profile_url = f"https://steamcommunity.com/id/{user}/"
    try:
        r = requests.get(profile_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if r.status_code == 200 and "profile_page" in r.text:
            console.print(f"[green]  Profil bulundu: {profile_url}[/]")
        else:
            profile_url = f"https://steamcommunity.com/profiles/{user}/"
            r = requests.get(profile_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if r.status_code == 200:
                console.print(f"[green]  Profil bulundu: {profile_url}[/]")
            else:
                console.print(f"[red]  Profil bulunamadi.[/]")
    except Exception as e:
        console.print(f"[red]  Hata: {e}[/]")
