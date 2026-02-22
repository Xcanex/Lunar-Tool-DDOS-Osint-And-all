import requests
from rich.console import Console
from rich.table import Table

console = Console()

CHECKS = [
    ("SQL Injection", ["'", "\"", "1' OR '1'='1", "1 UNION SELECT NULL--"]),
    ("XSS", ["<script>alert(1)</script>", "<img onerror=alert(1)>"]),
    ("Directory Traversal", ["../../../etc/passwd", "..\\..\\..\\windows\\system32"]),
    ("Open Redirect", ["//evil.com", "https://evil.com"]),
]


def run():
    url = console.input("[bold white]  Hedef URL (https://...): [/]").strip()
    if not url:
        console.print("[red]  URL bos olamaz.[/]")
        return
    if not url.startswith("http"):
        url = "https://" + url

    console.print(f"[#818cf8]  {url} taraniyor...[/]")

    table = Table(title="🛡️ Vulnerability Scan", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Test", style="bold white", min_width=20)
    table.add_column("Payload", style="dim")
    table.add_column("Durum", style="#a78bfa")

    for test_name, payloads in CHECKS:
        for payload in payloads[:2]:
            try:
                test_url = f"{url}?q={payload}" if "?" not in url else f"{url}&q={payload}"
                r = requests.get(test_url, timeout=5,
                                 headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=False)
                if payload in r.text:
                    table.add_row(test_name, payload[:30], "[red]Potansiyel Risk[/]")
                else:
                    table.add_row(test_name, payload[:30], "[green]Temiz[/]")
            except Exception:
                table.add_row(test_name, payload[:30], "[dim]Hata[/]")

    
    try:
        r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        security_headers = ["X-Frame-Options", "X-Content-Type-Options",
                           "Strict-Transport-Security", "Content-Security-Policy"]
        for h in security_headers:
            status = "[green]Var[/]" if h in r.headers else "[yellow]Eksik[/]"
            table.add_row("Header", h, status)
    except Exception:
        pass

    console.print()
    console.print(table)
