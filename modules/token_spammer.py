import requests
import threading
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    channel_id = console.input("[bold white]  Kanal ID: [/]").strip()
    if not channel_id:
        console.print("[red]  Kanal ID bos olamaz.[/]")
        return

    message = console.input("[bold white]  Mesaj: [/]").strip()
    if not message:
        console.print("[red]  Mesaj bos olamaz.[/]")
        return

    threads_str = console.input("[bold white]  Thread sayisi (varsayilan 2): [/]").strip()
    thread_count = int(threads_str) if threads_str.isdigit() and 0 < int(threads_str) <= 10 else 2

    console.print(f"[#818cf8]  Spam baslatiliyor ({thread_count} thread)...[/]")
    console.print("[yellow]  Durdurmak icin Ctrl+C basin.[/]")

    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    def spam():
        while True:
            try:
                r = requests.post(
                    f"https://discord.com/api/channels/{channel_id}/messages",
                    data={"content": message}, headers=headers, timeout=10
                )
                if r.status_code == 200:
                    short_msg = message[:20] + "..." if len(message) > 20 else message
                    console.print(f"[#818cf8]  [+] Gonderildi: {short_msg}[/]")
                elif r.status_code == 429:
                    retry = r.json().get("retry_after", 1)
                    import time
                    time.sleep(retry)
                else:
                    console.print(f"[red]  [-] Hata: {r.status_code}[/]")
            except Exception:
                pass

    try:
        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=spam, daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        console.print("\n[dim]  Spam durduruldu.[/]")
