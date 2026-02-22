import requests
import time
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Bot Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    guild_id = console.input("[bold white]  Sunucu ID: [/]").strip()
    count_str = console.input("[bold white]  Kac rol (varsayilan 50): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 0 < int(count_str) <= 250 else 50
    name = console.input("[bold white]  Rol adi (varsayilan 'nuked'): [/]").strip() or "nuked"

    console.print(f"[#818cf8]  {count} rol olusturuluyor...[/]")
    created = 0
    for i in range(count):
        try:
            r = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/roles",
                              headers=headers, json={"name": f"{name}-{i+1}"}, timeout=10)
            if r.status_code in (200, 201):
                created += 1
                console.print(f"[#818cf8]  [+] Rol: {name}-{i+1}[/]")
            elif r.status_code == 429:
                time.sleep(r.json().get("retry_after", 1))
            else:
                console.print(f"[red]  [-] Hata: {r.status_code}[/]")
        except Exception:
            pass
        time.sleep(0.3)
    console.print(f"\n[#818cf8]  Olusturulan: {created}[/]")
