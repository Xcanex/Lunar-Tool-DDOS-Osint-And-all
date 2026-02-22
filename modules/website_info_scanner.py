import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    url = console.input("[bold white]  Hedef URL: [/]").strip()
    if not url:
        console.print("[red]  URL bos olamaz.[/]")
        return
    if not url.startswith("http"):
        url = "https://" + url

    with console.status("[#818cf8]  Website bilgisi aliniyor...[/]", spinner="moon"):
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    table = Table(title="🌐 Website Info", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Alan", style="bold white", min_width=22)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("URL", url)
    table.add_row("Status", str(r.status_code))
    table.add_row("Server", r.headers.get("Server", "Bilinmiyor"))
    table.add_row("Content-Type", r.headers.get("Content-Type", "?"))
    table.add_row("Boyut", f"{len(r.content)} bytes")

    for h in ["X-Powered-By", "X-Frame-Options", "X-Content-Type-Options",
              "Strict-Transport-Security", "Content-Security-Policy",
              "Set-Cookie", "Access-Control-Allow-Origin"]:
        val = r.headers.get(h)
        if val:
            table.add_row(h, val[:80])

    try:
        import socket
        from urllib.parse import urlparse
        host = urlparse(url).hostname
        ip = socket.gethostbyname(host)
        table.add_row("IP", ip)
    except Exception:
        pass

    console.print()
    console.print(table)
