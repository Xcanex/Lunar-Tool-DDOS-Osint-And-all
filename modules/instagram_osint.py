import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    username = console.input("[bold white]  Instagram kullanici adi: [/]").strip()
    if not username:
        console.print("[red]  Bos olamaz.[/]")
        return

    with console.status("[#818cf8]  Arastiriliyor...[/]", spinner="moon"):
        try:
            r = requests.get(f"https://www.instagram.com/{username}/?__a=1&__d=1",
                             headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    if r.status_code != 200:
        console.print(f"[red]  Kullanici bulunamadi veya erisim engellendi ({r.status_code}).[/]")
        console.print(f"[dim]  Profil linki: https://www.instagram.com/{username}/[/]")
        return

    try:
        data = r.json().get("graphql", {}).get("user", {})
    except Exception:
        console.print("[yellow]  Veri parse edilemedi. Profil mevcut olabilir.[/]")
        console.print(f"[dim]  https://www.instagram.com/{username}/[/]")
        return

    table = Table(title=f"📷 @{username}", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Alan", style="bold white", min_width=16)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Tam Ad", data.get("full_name", "N/A"))
    table.add_row("Bio", (data.get("biography", "") or "Yok")[:100])
    table.add_row("Takipci", str(data.get("edge_followed_by", {}).get("count", "?")))
    table.add_row("Takip", str(data.get("edge_follow", {}).get("count", "?")))
    table.add_row("Gonderi", str(data.get("edge_owner_to_timeline_media", {}).get("count", "?")))
    table.add_row("Gizli", "Evet" if data.get("is_private") else "Hayir")
    table.add_row("Dogrulanmis", "Evet" if data.get("is_verified") else "Hayir")
    table.add_row("ID", data.get("id", "?"))

    console.print()
    console.print(table)
