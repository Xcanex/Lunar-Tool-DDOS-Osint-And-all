import requests
import random
import string
import threading
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


def run():
    count_str = console.input("[bold white]  Kac kod uretilsin (varsayilan 100): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 0 < int(count_str) <= 10000 else 100

    thread_str = console.input("[bold white]  Thread sayisi (varsayilan 3): [/]").strip()
    threads_num = int(thread_str) if thread_str.isdigit() and 0 < int(thread_str) <= 10 else 3

    valid_codes = []
    checked = [0]
    lock = threading.Lock()

    def check_codes(start, end):
        for _ in range(start, end):
            code = "".join(random.choices(string.ascii_letters + string.digits, k=16))
            try:
                r = requests.get(
                    f"https://discord.com/api/v10/entitlements/gift-codes/{code}",
                    timeout=5
                )
                with lock:
                    checked[0] += 1
                if r.status_code == 200:
                    with lock:
                        valid_codes.append(code)
                    console.print(f"[bold green]  [!!!] GECERLI KOD: https://discord.gift/{code}[/]")
            except Exception:
                with lock:
                    checked[0] += 1

    per_thread = count // threads_num
    threads = []

    console.print(f"[#818cf8]  {count} kod kontrol ediliyor ({threads_num} thread)...[/]")

    for i in range(threads_num):
        s = i * per_thread
        e = s + per_thread if i < threads_num - 1 else count
        t = threading.Thread(target=check_codes, args=(s, e), daemon=True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    console.print(f"\n[#818cf8]  Tamamlandi. Kontrol: {checked[0]} | Gecerli: {len(valid_codes)}[/]")
    if valid_codes:
        os_path = __import__("os").path
        out_dir = os_path.join(os_path.dirname(os_path.dirname(__file__)), "output")
        __import__("os").makedirs(out_dir, exist_ok=True)
        with open(os_path.join(out_dir, "valid_nitro.txt"), "a") as f:
            for c in valid_codes:
                f.write(f"https://discord.gift/{c}\n")
        console.print(f"[#818cf8]  Gecerli kodlar output/valid_nitro.txt dosyasina kaydedildi.[/]")
