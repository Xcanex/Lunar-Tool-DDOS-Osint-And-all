import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    cookie = console.input("[bold white]  Roblox .ROBLOSECURITY cookie: [/]").strip()
    if not cookie:
        console.print("[red]  Cookie bos olamaz.[/]")
        return

    with console.status("[#818cf8]  Cookie kontrol ediliyor...[/]", spinner="moon"):
        try:
            session = requests.Session()
            session.cookies[".ROBLOSECURITY"] = cookie
            r = session.get("https://users.roblox.com/v1/users/authenticated", timeout=10)
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    if r.status_code != 200:
        console.print("[red]  Gecersiz cookie.[/]")
        return

    data = r.json()
    table = Table(title="🍪 Roblox Cookie Info", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Alan", style="bold white", min_width=16)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Kullanici", data.get("name", "?"))
    table.add_row("Display Name", data.get("displayName", "?"))
    table.add_row("ID", str(data.get("id", "?")))

    try:
        robux = session.get(f"https://economy.roblox.com/v1/users/{data['id']}/currency", timeout=10)
        if robux.status_code == 200:
            table.add_row("Robux", str(robux.json().get("robux", "?")))
    except Exception:
        pass

    console.print()
    console.print(table)
