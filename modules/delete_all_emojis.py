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

    with console.status("[#818cf8]  Emojiler aliniyor...[/]", spinner="moon"):
        r = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/emojis", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Emojiler alinamadi.[/]")
        return

    emojis = r.json()
    if not emojis:
        console.print("[yellow]  Hicbir emoji bulunamadi.[/]")
        return

    console.print(f"[#818cf8]  {len(emojis)} emoji siliniyor...[/]")
    deleted = 0
    for emoji in emojis:
        try:
            resp = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/emojis/{emoji['id']}",
                                   headers=headers, timeout=10)
            if resp.status_code in (200, 204):
                deleted += 1
                console.print(f"[#818cf8]  [+] Silindi: {emoji.get('name', '?')}[/]")
            elif resp.status_code == 429:
                time.sleep(resp.json().get("retry_after", 1))
        except Exception:
            pass
        time.sleep(0.3)
    console.print(f"\n[#818cf8]  Silinen: {deleted}[/]")
