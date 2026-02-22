import requests
import threading
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    with console.status("[#818cf8]  Arkadaslar aliniyor...[/]", spinner="moon"):
        fr = requests.get("https://discord.com/api/v9/users/@me/relationships",
                          headers=headers, timeout=10)

    friends = fr.json() if fr.status_code == 200 else []
    if not friends:
        console.print("[yellow]  Hicbir arkadas bulunamadi.[/]")
        return

    console.print(f"[#818cf8]  {len(friends)} arkadas bulundu. Engelleme basliyor...[/]")
    blocked = 0

    for friend in friends:
        user = friend.get("user", {})
        name = user.get("username", "?")
        uid = friend.get("id", "")
        try:
            payload = {"type": 2}
            resp = requests.put(
                f"https://discord.com/api/v9/users/@me/relationships/{uid}",
                headers=headers, json=payload, timeout=10
            )
            if resp.status_code in (200, 204):
                blocked += 1
                console.print(f"[#818cf8]  [+] Engellendi: {name}[/]")
            else:
                console.print(f"[red]  [-] Basarisiz: {name} ({resp.status_code})[/]")
        except Exception:
            console.print(f"[red]  [-] Hata: {name}[/]")

    console.print(f"\n[#818cf8]  Tamamlandi. Engellenen: {blocked}/{len(friends)}[/]")
