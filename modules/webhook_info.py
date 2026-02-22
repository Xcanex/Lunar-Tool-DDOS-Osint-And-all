import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    url = console.input("[bold white]  Webhook URL: [/]").strip()
    if not url or "discord" not in url.lower():
        console.print("[red]  Gecersiz webhook URL.[/]")
        return

    with console.status("[#818cf8]  Webhook bilgisi aliniyor...[/]", spinner="moon"):
        r = requests.get(url, timeout=10)

    if r.status_code != 200:
        console.print("[red]  Webhook bulunamadi veya gecersiz.[/]")
        return

    data = r.json()

    table = Table(title="🌕 Webhook Bilgisi", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Alan", style="bold white", min_width=16)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("ID", data.get("id", "N/A"))
    table.add_row("Token", data.get("token", "N/A")[:30] + "...")
    table.add_row("Isim", data.get("name", "N/A"))
    table.add_row("Avatar", str(data.get("avatar", "Yok")))
    table.add_row("Tip", "Bot" if data.get("type") == 1 else "Webhook")
    table.add_row("Kanal ID", data.get("channel_id", "N/A"))
    table.add_row("Sunucu ID", data.get("guild_id", "N/A"))

    console.print()
    console.print(table)

    user = data.get("user")
    if user:
        table2 = Table(title="Webhook Sahibi", border_style="#818cf8", header_style="bold #a5b4fc")
        table2.add_column("Alan", style="bold white", min_width=16)
        table2.add_column("Deger", style="#a78bfa")
        table2.add_row("Kullanici", user.get("username", "?"))
        table2.add_row("ID", user.get("id", "?"))
        table2.add_row("Display", user.get("global_name", "N/A") or "N/A")
        console.print(table2)
