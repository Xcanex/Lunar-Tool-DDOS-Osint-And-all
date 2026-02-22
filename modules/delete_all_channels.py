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

    with console.status("[#818cf8]  Kanallar aliniyor...[/]", spinner="moon"):
        r = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Kanallar alinamadi.[/]")
        return

    channels = r.json()
    console.print(f"[#818cf8]  {len(channels)} kanal siliniyor...[/]")
    deleted = 0
    for ch in channels:
        try:
            resp = requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}", headers=headers, timeout=10)
            if resp.status_code in (200, 204):
                deleted += 1
                console.print(f"[#818cf8]  [+] Silindi: {ch.get('name', '?')}[/]")
            elif resp.status_code == 429:
                time.sleep(resp.json().get("retry_after", 1))
        except Exception:
            pass
        time.sleep(0.3)
    console.print(f"\n[#818cf8]  Silinen: {deleted}[/]")
