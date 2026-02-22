import requests
from rich.console import Console
console = Console()

def run():
    user = console.input("[bold white]  TikTok kullanici adi: [/]").strip()
    if not user:
        console.print("[red]  Bos olamaz.[/]")
        return
    console.print(f"[#818cf8]  TikTok profili araniyor: @{user}[/]")
    try:
        r = requests.get(f"https://www.tiktok.com/@{user}",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if r.status_code == 200:
            console.print(f"[green]  Profil bulundu: https://www.tiktok.com/@{user}[/]")
            if f'"uniqueId":"{user}"' in r.text:
                console.print(f"[#818cf8]  Profil dogrulanmis.[/]")
        else:
            console.print(f"[red]  Profil bulunamadi ({r.status_code}).[/]")
    except Exception as e:
        console.print(f"[red]  Hata: {e}[/]")
    console.print(f"[dim]  Google: https://www.google.com/search?q=site:tiktok.com+{user}[/]")
