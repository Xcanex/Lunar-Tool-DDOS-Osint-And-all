import requests
import threading
import time
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    channel_id = console.input("[bold white]  Kanal ID (spam icin): [/]").strip()
    message = console.input("[bold white]  Spam mesaji: [/]").strip() or "@everyone Raided by Lunar"

    if not token or not channel_id:
        console.print("[red]  Token ve Kanal ID zorunlu.[/]")
        return

    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    console.print("[#818cf8]  Raid baslatiliyor...[/]")
    console.print("[yellow]  Ctrl+C ile durdurun.[/]")

    def spam():
        while True:
            try:
                requests.post(
                    f"https://discord.com/api/channels/{channel_id}/messages",
                    data={"content": message},
                    headers={"Authorization": token}, timeout=10
                )
            except Exception:
                pass
            time.sleep(0.3)

    try:
        threads = []
        for _ in range(3):
            t = threading.Thread(target=spam, daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        console.print("\n[dim]  Raid durduruldu.[/]")
