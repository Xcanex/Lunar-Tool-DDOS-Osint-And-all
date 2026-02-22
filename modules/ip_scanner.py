import socket
import threading
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    target = console.input("[bold white]  Hedef IP veya domain: [/]").strip()
    if not target:
        console.print("[red]  Hedef bos olamaz.[/]")
        return

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        console.print("[red]  Gecersiz hedef.[/]")
        return

    port_range = console.input("[bold white]  Port araligi (varsayilan 1-1024): [/]").strip() or "1-1024"
    parts = port_range.split("-")
    start_port = int(parts[0]) if len(parts) >= 1 and parts[0].isdigit() else 1
    end_port = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1024

    console.print(f"[#818cf8]  Taraniyor: {ip} ({start_port}-{end_port})...[/]")

    open_ports = []
    lock = threading.Lock()

    def scan_port(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                with lock:
                    open_ports.append(port)
            s.close()
        except Exception:
            pass

    threads = []
    for port in range(start_port, min(end_port + 1, start_port + 5000)):
        t = threading.Thread(target=scan_port, args=(port,), daemon=True)
        t.start()
        threads.append(t)
        if len(threads) >= 200:
            for th in threads:
                th.join(timeout=2)
            threads = []

    for th in threads:
        th.join(timeout=2)

    if open_ports:
        table = Table(title=f"IP Scanner: {ip}", border_style="#818cf8")
        table.add_column("Port", style="bold white")
        table.add_column("Durum", style="#a78bfa")
        for p in sorted(open_ports):
            table.add_row(str(p), "[green]ACIK[/]")
        console.print(table)
    else:
        console.print("[yellow]  Acik port bulunamadi.[/]")
    console.print(f"[#818cf8]  Toplam acik: {len(open_ports)}[/]")
