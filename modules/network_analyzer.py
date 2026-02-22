import subprocess
import socket
import time
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    interface = console.input("[bold white]  Ag arayuzu (bos = varsayilan): [/]").strip()
    duration_str = console.input("[bold white]  Dinleme suresi (saniye, varsayilan 10): [/]").strip()
    duration = int(duration_str) if duration_str.isdigit() else 10

    console.print(f"[#818cf8]  Ag trafigi {duration} saniye dinleniyor...[/]")

    connections = {}
    try:
        import psutil
        start = time.time()
        while time.time() - start < duration:
            for conn in psutil.net_connections(kind="inet"):
                if conn.status == "ESTABLISHED" and conn.raddr:
                    key = f"{conn.raddr.ip}:{conn.raddr.port}"
                    if key not in connections:
                        connections[key] = {
                            "local": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "?",
                            "remote": key,
                            "pid": conn.pid or 0,
                            "status": conn.status
                        }
            time.sleep(1)
    except ImportError:
        console.print("[yellow]  psutil gerekli: pip install psutil[/]")
        return

    if connections:
        table = Table(title="Network Traffic", border_style="#818cf8")
        table.add_column("Yerel", style="bold white")
        table.add_column("Uzak", style="#a78bfa")
        table.add_column("PID", style="dim")
        table.add_column("Durum", style="bold")
        for conn in list(connections.values())[:30]:
            table.add_row(conn["local"], conn["remote"], str(conn["pid"]), conn["status"])
        console.print(table)
    else:
        console.print("[yellow]  Aktif baglanti bulunamadi.[/]")
    console.print(f"[#818cf8]  Toplam: {len(connections)} baglanti[/]")
