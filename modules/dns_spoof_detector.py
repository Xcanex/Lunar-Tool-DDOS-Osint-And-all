import socket
from rich.console import Console
from rich.table import Table

console = Console()

KNOWN_DNS = {
    "8.8.8.8": "Google",
    "8.8.4.4": "Google",
    "1.1.1.1": "Cloudflare",
    "1.0.0.1": "Cloudflare",
    "9.9.9.9": "Quad9",
    "208.67.222.222": "OpenDNS",
}

DOMAINS = ["google.com", "facebook.com", "twitter.com", "youtube.com", "github.com"]


def run():
    console.print("[#818cf8]  DNS Spoof Detector[/]")
    console.print("[dim]  Bilinen DNS sunuculari ile karsilastirir.[/]\n")

    table = Table(title="🔍 DNS Spoof Check", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Domain", style="bold white")
    table.add_column("Varsayilan DNS", style="#a78bfa")
    table.add_column("Google DNS", style="#a78bfa")
    table.add_column("Durum", style="bold")

    for domain in DOMAINS:
        try:
            default_ip = socket.gethostbyname(domain)
        except Exception:
            default_ip = "HATA"

        try:
            import subprocess
            result = subprocess.run(
                ["nslookup", domain, "8.8.8.8"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")
            google_ip = "?"
            for line in lines:
                if "Address" in line and "8.8.8.8" not in line:
                    google_ip = line.split(":")[-1].strip()
                    break
        except Exception:
            google_ip = "?"

        if default_ip == google_ip or google_ip == "?":
            status = "[green]Temiz[/]"
        else:
            status = "[red]FARKLI![/]"

        table.add_row(domain, default_ip, google_ip, status)

    console.print()
    console.print(table)
