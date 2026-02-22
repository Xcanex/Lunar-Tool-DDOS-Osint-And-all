import requests
from rich.console import Console
from rich.table import Table

console = Console()

VPN_DETECTION_APIS = [
    "https://ipinfo.io/{}/json",
    "https://ipapi.co/{}/json",
]


def run():
    ip = console.input("[bold white]  IP adresi (bos = kendi IP): [/]").strip()
    if not ip:
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
        except Exception:
            console.print("[red]  IP alinamadi.[/]")
            return

    console.print(f"[#818cf8]  {ip} kontrol ediliyor...[/]")

    table = Table(title=f"VPN Check: {ip}", border_style="#818cf8")
    table.add_column("Alan", style="bold white", min_width=16)
    table.add_column("Deger", style="#a78bfa")

    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        if r.status_code == 200:
            data = r.json()
            table.add_row("IP", data.get("ip", "?"))
            table.add_row("Hostname", data.get("hostname", "N/A"))
            table.add_row("Sehir", data.get("city", "?"))
            table.add_row("Bolge", data.get("region", "?"))
            table.add_row("Ulke", data.get("country", "?"))
            table.add_row("ISP", data.get("org", "?"))

            org = (data.get("org", "") or "").lower()
            hostname = (data.get("hostname", "") or "").lower()
            vpn_keywords = ["vpn", "proxy", "tor", "hosting", "cloud", "datacenter",
                           "digitalocean", "amazon", "google", "azure", "ovh", "vultr"]
            is_vpn = any(kw in org for kw in vpn_keywords) or any(kw in hostname for kw in vpn_keywords)
            table.add_row("VPN/Proxy", "[red]MUHTEMEL[/]" if is_vpn else "[green]Hayir[/]")
    except Exception as e:
        console.print(f"[red]  Hata: {e}[/]")

    console.print()
    console.print(table)
