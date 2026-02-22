import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    cookie = console.input("[bold white]  Roblox .ROBLOSECURITY cookie: [/]").strip()
    if not cookie:
        console.print("[red]  Cookie bos olamaz.[/]")
        return

    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie

    with console.status("[#818cf8]  Trade gecmisi aliniyor...[/]", spinner="moon"):
        try:
            auth = session.get("https://users.roblox.com/v1/users/authenticated", timeout=10)
            if auth.status_code != 200:
                console.print("[red]  Gecersiz cookie.[/]")
                return
            uid = auth.json().get("id")
            name = auth.json().get("name", "?")

            inbound = session.get(
                f"https://trades.roblox.com/v1/trades/Completed?sortOrder=Desc&limit=10",
                timeout=10
            )
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    console.print(f"[#818cf8]  Kullanici: {name} (ID: {uid})[/]")

    if inbound.status_code == 200:
        trades = inbound.json().get("data", [])
        if not trades:
            console.print("[yellow]  Trade gecmisi bos.[/]")
            return

        table = Table(title="Trade History", border_style="#818cf8")
        table.add_column("Trade ID", style="bold white")
        table.add_column("Partner", style="#a78bfa")
        table.add_column("Durum", style="bold")
        table.add_column("Tarih", style="dim")

        for t in trades:
            partner = t.get("user", {}).get("name", "?")
            status = t.get("status", "?")
            created = (t.get("created", "") or "?")[:10]
            color = "[green]" if status == "Completed" else "[red]"
            table.add_row(str(t.get("id", "?")), partner, f"{color}{status}[/]", created)

        console.print()
        console.print(table)
    else:
        console.print(f"[red]  Trade verisi alinamadi ({inbound.status_code}).[/]")
