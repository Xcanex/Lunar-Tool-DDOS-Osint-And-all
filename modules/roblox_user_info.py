import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    username = console.input("[bold white]  Roblox kullanici adi: [/]").strip()
    if not username:
        console.print("[red]  Bos olamaz.[/]")
        return

    with console.status("[#818cf8]  Arastiriliyor...[/]", spinner="moon"):
        try:
            r = requests.post("https://users.roblox.com/v1/usernames/users",
                              json={"usernames": [username]}, timeout=10)
            if r.status_code != 200 or not r.json().get("data"):
                console.print("[red]  Kullanici bulunamadi.[/]")
                return
            user_data = r.json()["data"][0]
            user_id = user_data["id"]

            info = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10).json()
            friends = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count", timeout=10).json()
            followers = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count", timeout=10).json()
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    table = Table(title=f"🎮 Roblox: {username}", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Alan", style="bold white", min_width=16)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Kullanici Adi", info.get("name", "?"))
    table.add_row("Display Name", info.get("displayName", "?"))
    table.add_row("ID", str(user_id))
    table.add_row("Aciklama", (info.get("description", "") or "Yok")[:80])
    table.add_row("Olusturulma", info.get("created", "?")[:10])
    table.add_row("Banlı", "Evet" if info.get("isBanned") else "Hayir")
    table.add_row("Arkadas", str(friends.get("count", "?")))
    table.add_row("Takipci", str(followers.get("count", "?")))
    table.add_row("Profil", f"https://www.roblox.com/users/{user_id}/profile")

    console.print()
    console.print(table)
