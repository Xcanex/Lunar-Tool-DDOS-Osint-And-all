import os
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS
    except ImportError:
        console.print("[red]  Pillow kutuphanesi gerekli: pip install Pillow[/]")
        return

    path = console.input("[bold white]  Resim dosya yolu: [/]").strip()
    if not path or not os.path.isfile(path):
        console.print("[red]  Dosya bulunamadi.[/]")
        return

    try:
        img = Image.open(path)
        exif_data = img._getexif()
    except Exception as e:
        console.print(f"[red]  Resim acilamadi: {e}[/]")
        return

    if not exif_data:
        console.print("[yellow]  Bu resimde EXIF verisi bulunamadi.[/]")
        return

    table = Table(title="📷 EXIF Verisi", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Tag", style="bold white", min_width=22)
    table.add_column("Deger", style="#a78bfa")

    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if isinstance(value, bytes):
            value = value[:50]
        table.add_row(str(tag), str(value)[:80])

    console.print()
    console.print(table)
