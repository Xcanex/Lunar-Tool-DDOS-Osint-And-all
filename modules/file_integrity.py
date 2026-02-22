import os
import hashlib
from rich.console import Console
from rich.table import Table

console = Console()

def run():
    path = console.input("[bold white]  Dosya/Klasor yolu: [/]").strip()
    if not path or not os.path.exists(path):
        console.print("[red]  Yol bulunamadi.[/]")
        return

    files = []
    if os.path.isfile(path):
        files = [path]
    else:
        for root, _, fnames in os.walk(path):
            for f in fnames:
                files.append(os.path.join(root, f))

    table = Table(title="🔒 File Integrity", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Dosya", style="bold white")
    table.add_column("Boyut", style="#a78bfa")
    table.add_column("MD5", style="dim")
    table.add_column("SHA256", style="dim")

    for fp in files[:30]:
        try:
            size = os.path.getsize(fp)
            with open(fp, "rb") as f:
                data = f.read()
            md5 = hashlib.md5(data).hexdigest()[:16] + "..."
            sha = hashlib.sha256(data).hexdigest()[:16] + "..."
            table.add_row(os.path.basename(fp)[:25], f"{size}B", md5, sha)
        except Exception:
            table.add_row(os.path.basename(fp)[:25], "?", "Hata", "Hata")

    console.print()
    console.print(table)
    console.print(f"[#818cf8]  {len(files)} dosya kontrol edildi.[/]")
