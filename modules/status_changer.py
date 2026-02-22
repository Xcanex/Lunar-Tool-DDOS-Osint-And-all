import requests
import time
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    count_str = console.input("[bold white]  Kac status dongusu? (maks 4, varsayilan 2): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 1 <= int(count_str) <= 4 else 2

    statuses = []
    for i in range(count):
        s = console.input(f"[bold white]  Status {i+1}: [/]").strip()
        if s:
            statuses.append(s)

    if not statuses:
        console.print("[red]  En az 1 status girilmeli.[/]")
        return

    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    console.print("[#818cf8]  Status dongusu baslatildi. Ctrl+C ile durdurun.[/]")

    try:
        while True:
            for status in statuses:
                payload = {"custom_status": {"text": status}}
                try:
                    requests.patch("https://discord.com/api/v9/users/@me/settings",
                                   headers=headers, json=payload, timeout=5)
                    console.print(f"[#818cf8]  [+] Status: {status}[/]")
                except Exception:
                    console.print(f"[red]  [-] Basarisiz: {status}[/]")
                time.sleep(5)
    except KeyboardInterrupt:
        console.print("\n[dim]  Status changer durduruldu.[/]")
