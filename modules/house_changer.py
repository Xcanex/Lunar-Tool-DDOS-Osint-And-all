import requests
from rich.console import Console
console = Console()

HOUSES = {
    "1": ("Bravery",    1),
    "2": ("Brilliance", 2),
    "3": ("Balance",    3),
}


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    headers = {"Authorization": token, "Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    user = r.json()
    console.print(f"[#818cf8]  Giris: {user.get('username', '?')}#{user.get('discriminator', '0')}[/]\n")

    console.print("  [white]1.[/] Bravery    (yesil)")
    console.print("  [white]2.[/] Brilliance (mor)")
    console.print("  [white]3.[/] Balance    (turuncu)\n")

    choice = console.input("[bold white]  House secimi (1-3): [/]").strip()

    if choice not in HOUSES:
        console.print("[red]  Gecersiz secim.[/]")
        return

    name, house_id = HOUSES[choice]

    try:
        r = requests.post("https://discord.com/api/v10/hypesquad/online",
                          headers=headers, json={"house_id": house_id}, timeout=10)
        if r.status_code == 204:
            console.print(f"[bold green]  HypeSquad '{name}' olarak degistirildi![/]")
        else:
            console.print(f"[red]  Degistirilemedi (HTTP {r.status_code}).[/]")
    except Exception as e:
        console.print(f"[red]  Hata: {e}[/]")
