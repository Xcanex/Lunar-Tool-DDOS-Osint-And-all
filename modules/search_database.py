import os
from rich.console import Console
console = Console()

def run():
    console.print("[#818cf8]  Search Database[/]")
    console.print("[dim]  Yerel veritabani dosyalarinda arama yapar.[/]\n")
    search = console.input("[bold white]  Aranacak terim: [/]").strip()
    if not search:
        console.print("[red]  Terim bos olamaz.[/]")
        return
    db_dir = console.input("[bold white]  Veritabani klasoru (varsayilan ./database): [/]").strip()
    if not db_dir:
        db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
    if not os.path.isdir(db_dir):
        console.print(f"[yellow]  Klasor bulunamadi: {db_dir}[/]")
        console.print("[dim]  'database' klasoru olusturup .txt dosyalari ekleyin.[/]")
        return
    found = 0
    for fname in os.listdir(db_dir):
        fpath = os.path.join(db_dir, fname)
        if os.path.isfile(fpath):
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if search.lower() in line.lower():
                            found += 1
                            console.print(f"[#a78bfa]  {fname}:{i} -> {line.strip()[:80]}[/]")
                            if found >= 50:
                                console.print("[dim]  50 sonuc limiti.[/]")
                                return
            except Exception:
                pass
    console.print(f"\n[#818cf8]  Toplam {found} sonuc bulundu.[/]")
