import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    username = console.input("[bold white]  Roblox kullanici adi: [/]").strip()
    if not username:
        console.print("[red]  Bos olamaz.[/]")
        return

    with console.status("[#818cf8]  Profil analiz ediliyor...[/]", spinner="moon"):
        try:
            r = requests.post("https://users.roblox.com/v1/usernames/users",
                              json={"usernames": [username]}, timeout=10)
            if not r.json().get("data"):
                console.print("[red]  Kullanici bulunamadi.[/]")
                return
            uid = r.json()["data"][0]["id"]

            info = requests.get(f"https://users.roblox.com/v1/users/{uid}", timeout=10).json()
            friends = requests.get(f"https://friends.roblox.com/v1/users/{uid}/friends", timeout=10).json()
            groups = requests.get(f"https://groups.roblox.com/v2/users/{uid}/groups/roles", timeout=10).json()
            badges = requests.get(f"https://accountinformation.roblox.com/v1/users/{uid}/roblox-badges", timeout=10)
            inventory = requests.get(f"https://inventory.roblox.com/v2/users/{uid}/inventory?assetTypes=Hat&limit=10", timeout=10)
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    table = Table(title=f"Profile Analysis: {username}", border_style="#818cf8")
    table.add_column("Alan", style="bold white", min_width=18)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Kullanici", info.get("name", "?"))
    table.add_row("Display", info.get("displayName", "?"))
    table.add_row("ID", str(uid))
    created = info.get("created", "?")[:10]
    table.add_row("Kayit Tarihi", created)
    table.add_row("Banli", "Evet" if info.get("isBanned") else "Hayir")

    friend_list = friends.get("data", [])
    table.add_row("Arkadas Sayisi", str(len(friend_list)))
    if friend_list:
        top_friends = ", ".join([f.get("name", "?") for f in friend_list[:5]])
        table.add_row("Arkadaslar", top_friends)

    grup_data = groups.get("data", [])
    table.add_row("Grup Sayisi", str(len(grup_data)))
    for g in grup_data[:3]:
        grp = g.get("group", {})
        role = g.get("role", {})
        table.add_row(f"  {grp.get('name', '?')}", role.get("name", "?"))

    desc = info.get("description", "") or ""
    activity = "Aktif" if len(desc) > 10 else "Dusuk aktivite"
    table.add_row("Aktivite", activity)
    table.add_row("Bio Uzunluk", str(len(desc)))

    console.print()
    console.print(table)
