import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    user_id = console.input("[bold white]  Roblox User ID: [/]").strip()
    if not user_id or not user_id.isdigit():
        console.print("[red]  Gecerli bir ID girin.[/]")
        return

    with console.status("[#818cf8]  Arastiriliyor...[/]", spinner="moon"):
        try:
            info = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10).json()
            if "errors" in info:
                console.print("[red]  Kullanici bulunamadi.[/]")
                return
            friends = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count", timeout=10).json()
            followers = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count", timeout=10).json()
            following = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count", timeout=10).json()
            groups = requests.get(f"https://groups.roblox.com/v2/users/{user_id}/groups/roles", timeout=10).json()
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    table = Table(title=f"Roblox ID: {user_id}", border_style="#818cf8")
    table.add_column("Alan", style="bold white", min_width=16)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Kullanici Adi", info.get("name", "?"))
    table.add_row("Display", info.get("displayName", "?"))
    table.add_row("ID", str(user_id))
    table.add_row("Aciklama", (info.get("description", "") or "Yok")[:60])
    table.add_row("Olusturulma", info.get("created", "?")[:10])
    table.add_row("Banli", "Evet" if info.get("isBanned") else "Hayir")
    table.add_row("Arkadas", str(friends.get("count", "?")))
    table.add_row("Takipci", str(followers.get("count", "?")))
    table.add_row("Takip", str(following.get("count", "?")))

    grup_list = groups.get("data", [])
    table.add_row("Grup Sayisi", str(len(grup_list)))
    for g in grup_list[:5]:
        table.add_row(f"  Grup", f"{g.get('group', {}).get('name', '?')} ({g.get('role', {}).get('name', '?')})")

    table.add_row("Profil", f"https://www.roblox.com/users/{user_id}/profile")
    table.add_row("Avatar", f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=420&height=420")

    console.print()
    console.print(table)
