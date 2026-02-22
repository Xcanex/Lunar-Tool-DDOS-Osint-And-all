import requests
import webbrowser
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

    with console.status("[#818cf8]  Giris yapiliyor...[/]", spinner="moon"):
        try:
            r = session.get("https://users.roblox.com/v1/users/authenticated", timeout=10)
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    if r.status_code != 200:
        console.print("[red]  Gecersiz cookie.[/]")
        return

    data = r.json()
    uid = data.get("id", "?")
    name = data.get("name", "?")
    display = data.get("displayName", "?")

    table = Table(title="Roblox Cookie Login", border_style="#818cf8")
    table.add_column("Alan", style="bold white", min_width=14)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Kullanici", name)
    table.add_row("Display", display)
    table.add_row("ID", str(uid))
    table.add_row("Durum", "[green]Giris basarili![/]")
    table.add_row("Profil", f"https://www.roblox.com/users/{uid}/profile")

    try:
        rb = session.get(f"https://economy.roblox.com/v1/users/{uid}/currency", timeout=10)
        if rb.status_code == 200:
            robux = rb.json().get("robux", "?")
            table.add_row("Robux", str(robux))
    except Exception:
        pass

    try:
        fr = session.get(f"https://friends.roblox.com/v1/users/{uid}/friends/count", timeout=10)
        if fr.status_code == 200:
            table.add_row("Arkadas", str(fr.json().get("count", "?")))
    except Exception:
        pass

    console.print()
    console.print(table)

    ac = console.input("\n[bold white]  Tarayicide profili ac? (e/h): [/]").strip().lower()
    if ac == "e":
        try:
            webbrowser.open(f"https://www.roblox.com/users/{uid}/profile")
            console.print("[green]  Tarayici acildi.[/]")
        except Exception:
            pass
