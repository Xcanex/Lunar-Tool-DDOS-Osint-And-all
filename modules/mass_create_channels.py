import requests
import time
from rich.console import Console

console = Console()


def _get_bot_headers():
    token = console.input("[bold white]  Bot Token: [/]").strip()
    if not token:
        return None, None
    return token, {"Authorization": f"Bot {token}", "Content-Type": "application/json"}


def run():
    token, headers = _get_bot_headers()
    if not headers:
        console.print("[red]  Token bos olamaz.[/]")
        return

    guild_id = console.input("[bold white]  Sunucu ID: [/]").strip()
    if not guild_id:
        console.print("[red]  Sunucu ID bos olamaz.[/]")
        return

    count_str = console.input("[bold white]  Kac kanal olusturulsun (varsayilan 50): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 0 < int(count_str) <= 500 else 50

    name = console.input("[bold white]  Kanal adi (varsayilan 'nuked'): [/]").strip() or "nuked"

    console.print(f"[#818cf8]  {count} kanal olusturuluyor...[/]")
    created = 0

    for i in range(count):
        try:
            r = requests.post(
                f"https://discord.com/api/v9/guilds/{guild_id}/channels",
                headers=headers, json={"name": f"{name}-{i+1}", "type": 0}, timeout=10
            )
            if r.status_code in (200, 201):
                created += 1
                console.print(f"[#818cf8]  [+] Kanal olusturuldu: {name}-{i+1}[/]")
            elif r.status_code == 429:
                retry = r.json().get("retry_after", 1)
                time.sleep(retry)
            else:
                console.print(f"[red]  [-] Hata: {r.status_code}[/]")
        except Exception:
            pass
        time.sleep(0.3)

    console.print(f"\n[#818cf8]  Tamamlandi. Olusturulan: {created}[/]")
