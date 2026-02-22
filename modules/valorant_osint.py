import requests
from rich.console import Console
console = Console()

def run():
    user = console.input("[bold white]  Valorant kullanici adi#tag: [/]").strip()
    if not user:
        console.print("[red]  Bos olamaz.[/]")
        return
    console.print(f"[#818cf8]  Valorant profili araniyor: {user}[/]")
    parts = user.split("#")
    name = parts[0]
    tag = parts[1] if len(parts) > 1 else ""
    try:
        r = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}", timeout=10)
        if r.status_code == 200:
            data = r.json().get("data", {})
            console.print(f"[green]  Hesap bulundu![/]")
            console.print(f"  [#a78bfa]Isim: {data.get('name', '?')}#{data.get('tag', '?')}[/]")
            console.print(f"  [#a78bfa]Seviye: {data.get('account_level', '?')}[/]")
            console.print(f"  [#a78bfa]Bolge: {data.get('region', '?')}[/]")
            card = data.get("card", {})
            if card.get("large"):
                console.print(f"  [#a78bfa]Kart: {card['large']}[/]")
        else:
            console.print(f"[red]  Hesap bulunamadi ({r.status_code}).[/]")
    except Exception as e:
        console.print(f"[red]  Hata: {e}[/]")
    console.print(f"[dim]  Tracker: https://tracker.gg/valorant/profile/riot/{user.replace('#', '%23')}[/]")
