import requests
import webbrowser
from rich.console import Console
from rich.table import Table
console = Console()


def run():
    bot_id = console.input("[bold white]  Bot Client ID: [/]").strip()
    if not bot_id or not bot_id.isdigit():
        console.print("[red]  Gecerli bir Client ID girin.[/]")
        return

    perms = console.input("[bold white]  Yetki (varsayilan 8=Admin): [/]").strip() or "8"

    invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot&permissions={perms}"

    with console.status("[#818cf8]  Kontrol ediliyor...[/]"):
        try:
            r = requests.get(invite_url, timeout=10, allow_redirects=False)
            status = r.status_code
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    table = Table(title="Bot Invite", border_style="#818cf8")
    table.add_column("Alan", style="bold white", min_width=14)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Client ID", bot_id)
    table.add_row("Yetki", perms)
    table.add_row("HTTP Status", str(status))
    table.add_row("Gecerli", "[green]Evet[/]" if status in [200, 302, 303] else "[red]Hayir[/]")
    table.add_row("Invite URL", invite_url)

    console.print()
    console.print(table)

    ac = console.input("\n[bold white]  Tarayicide acilsin mi? (e/h): [/]").strip().lower()
    if ac == "e":
        try:
            webbrowser.open_new_tab(invite_url)
            console.print("[green]  Tarayici acildi.[/]")
        except Exception:
            console.print(f"[yellow]  Link: {invite_url}[/]")
