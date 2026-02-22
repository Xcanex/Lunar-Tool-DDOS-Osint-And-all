import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    item_id = console.input("[bold white]  Roblox Item ID: [/]").strip()
    if not item_id or not item_id.isdigit():
        console.print("[red]  Gecerli ID girin.[/]")
        return

    with console.status("[#818cf8]  Item arastiriliyor...[/]", spinner="moon"):
        try:
            r = requests.get(f"https://economy.roblox.com/v2/assets/{item_id}/details", timeout=10)
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            return

    if r.status_code != 200:
        console.print("[red]  Item bulunamadi.[/]")
        return

    data = r.json()
    table = Table(title=f"Item: {data.get('Name', '?')}", border_style="#818cf8")
    table.add_column("Alan", style="bold white", min_width=18)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Isim", data.get("Name", "?"))
    table.add_row("ID", str(item_id))
    table.add_row("Aciklama", (data.get("Description", "") or "Yok")[:60])
    table.add_row("Tur", data.get("AssetTypeName", "?"))
    table.add_row("Olusturucu", data.get("Creator", {}).get("Name", "?"))
    table.add_row("Fiyat", str(data.get("PriceInRobux", "Satilmiyor")))
    table.add_row("Satis", str(data.get("Sales", "?")))
    table.add_row("Favoriler", str(data.get("FavoriteCount", "?")))
    table.add_row("Limited", "Evet" if data.get("IsLimited") or data.get("IsLimitedUnique") else "Hayir")
    table.add_row("Satilik Mi", "Evet" if data.get("IsForSale") else "Hayir")
    table.add_row("Olusturulma", (data.get("Created", "") or "?")[:10])
    table.add_row("Guncelleme", (data.get("Updated", "") or "?")[:10])

    console.print()
    console.print(table)
