import requests
import random
import time
from rich.console import Console
console = Console()

def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return
    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    languages = ["ja", "zh-TW", "ko", "zh-CN", "th", "uk", "ru", "el", "cs",
                 "tr", "vi", "hi", "pl", "nl", "fr", "de", "es", "it", "pt-BR",
                 "sv-SE", "da", "fi", "no", "hu", "ro", "bg", "hr", "lt"]

    console.print("[#818cf8]  Dil dongusu baslatildi. Ctrl+C ile durdurun.[/]")
    console.print("[dim]  Desteklenen diller: " + ", ".join(languages[:10]) + "...[/]")

    try:
        while True:
            lang = random.choice(languages)
            try:
                requests.patch("https://discord.com/api/v9/users/@me/settings",
                               headers=headers, json={"locale": lang}, timeout=5)
                console.print(f"[#818cf8]  [+] Dil: {lang}[/]")
            except Exception:
                console.print(f"[red]  [-] Basarisiz: {lang}[/]")
            time.sleep(2)
    except KeyboardInterrupt:
        console.print("\n[dim]  Durduruldu.[/]")
