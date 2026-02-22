import requests
import webbrowser
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    headers = {"Authorization": token, "Content-Type": "application/json"}

    with console.status("[#818cf8]  Token kontrol ediliyor...[/]", spinner="moon"):
        r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)

    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    data = r.json()

    table = Table(title="🌕 Token Login", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Alan", style="bold white", min_width=18)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Kullanici", f"{data.get('username', '?')}#{data.get('discriminator', '0')}")
    table.add_row("Display Name", data.get("global_name", "N/A") or "N/A")
    table.add_row("ID", data.get("id", "N/A"))
    table.add_row("Email", data.get("email", "N/A") or "N/A")
    table.add_row("Telefon", data.get("phone", "N/A") or "N/A")
    table.add_row("MFA", "Acik" if data.get("mfa_enabled") else "Kapali")
    table.add_row("Nitro", "Var" if data.get("premium_type", 0) > 0 else "Yok")

    console.print()
    console.print(table)

    console.print("\n[#818cf8]  Tarayicide acmak ister misin? (e/h): [/]", end="")
    ans = input().strip().lower()
    if ans == "e":
        login_url = f"https://discord.com/login"
        console.print(f"[dim]  Token ile giris icin tarayici uzantisi gereklidir.[/]")
        console.print(f"[dim]  Token: {token[:20]}...[/]")
        webbrowser.open(login_url)
