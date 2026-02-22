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
    reason = console.input("[bold white]  Ban sebebi (opsiyonel): [/]").strip() or "Nuked"

    console.print("[#818cf8]  Uyeler aliniyor...[/]")
    members = []
    after = "0"
    while True:
        r = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000&after={after}",
                         headers=headers, timeout=10)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        members.extend(batch)
        after = batch[-1]["user"]["id"]
        if len(batch) < 1000:
            break

    if not members:
        console.print("[yellow]  Uye bulunamadi.[/]")
        return

    console.print(f"[#818cf8]  {len(members)} uye banlaniyor...[/]")
    banned = 0
    for m in members:
        uid = m["user"]["id"]
        name = m["user"].get("username", "?")
        try:
            resp = requests.put(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{uid}",
                                headers=headers, json={"reason": reason}, timeout=10)
            if resp.status_code in (200, 204):
                banned += 1
                console.print(f"[#818cf8]  [+] Banlandi: {name}[/]")
            elif resp.status_code == 429:
                time.sleep(resp.json().get("retry_after", 1))
        except Exception:
            pass
        time.sleep(0.3)
    console.print(f"\n[#818cf8]  Banlanan: {banned}[/]")
