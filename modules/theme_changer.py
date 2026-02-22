import requests
import time
from itertools import cycle
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

    themes = cycle(["dark", "light"])
    console.print("[#818cf8]  Tema dongusu baslatildi. Ctrl+C ile durdurun.[/]")

    try:
        while True:
            theme = next(themes)
            try:
                payload = {"theme": theme}
                requests.patch("https://discord.com/api/v9/users/@me/settings",
                               headers=headers, json=payload, timeout=5)
                console.print(f"[#818cf8]  [+] Tema: {theme}[/]")
            except Exception:
                console.print(f"[red]  [-] Basarisiz: {theme}[/]")
            time.sleep(3)
    except KeyboardInterrupt:
        console.print("\n[dim]  Theme changer durduruldu.[/]")
