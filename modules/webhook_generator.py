import string
import random
import threading
import requests
from rich.console import Console
console = Console()


def run():
    thread_str = console.input("[bold white]  Thread sayisi (varsayilan 10): [/]").strip()
    threads_num = int(thread_str) if thread_str.isdigit() and 0 < int(thread_str) <= 100 else 10

    console.print(f"[#818cf8]  {threads_num} thread ile webhook taranıyor... Ctrl+C ile durdurun.[/]")

    found = {"count": 0, "valid": []}
    lock = threading.Lock()
    chars = string.ascii_letters + string.digits + "-_"

    def check():
        while True:
            p1 = "".join(str(random.randint(0, 9)) for _ in range(19))
            p2 = "".join(random.choice(chars) for _ in range(68))
            url = f"https://discord.com/api/webhooks/{p1}/{p2}"
            try:
                r = requests.head(url, timeout=5)
                with lock:
                    found["count"] += 1
                    if found["count"] % 50 == 0:
                        console.print(f"[dim]  Taranan: {found['count']}[/]")
                    if r.status_code == 200:
                        found["valid"].append(url)
                        console.print(f"[bold green]  GECERLI WEBHOOK: {url}[/]")
            except Exception:
                pass

    threads = []
    try:
        for _ in range(threads_num):
            t = threading.Thread(target=check, daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        console.print(f"\n[dim]  Durduruldu. Toplam: {found['count']}[/]")
        if found["valid"]:
            console.print(f"[green]  {len(found['valid'])} gecerli webhook bulundu:[/]")
            for v in found["valid"]:
                console.print(f"  {v}")
        else:
            console.print("[yellow]  Gecerli webhook bulunamadi.[/]")
