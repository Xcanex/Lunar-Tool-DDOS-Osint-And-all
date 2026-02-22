import os
from rich.console import Console
console = Console()

def run():
    console.print("[#818cf8]  Dox Creator[/]")
    console.print("[dim]  Bilgi topla ve dosyaya kaydet.[/]\n")
    fields = ["Tam Ad", "Yas", "Dogum Tarihi", "Adres", "Sehir", "Ulke",
              "Email", "Telefon", "IP Adresi", "Discord", "Instagram",
              "Twitter", "Facebook", "Okul/Is", "Notlar"]
    data = {}
    for f in fields:
        val = console.input(f"[bold white]  {f}: [/]").strip()
        data[f] = val if val else "Bilinmiyor"

    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, f"dox_{data['Tam Ad'].replace(' ', '_')}.txt")
    with open(fname, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("  LUNAR TOOL - DOX CREATOR\n")
        f.write("=" * 50 + "\n\n")
        for k, v in data.items():
            f.write(f"  {k}: {v}\n")
        f.write("\n" + "=" * 50 + "\n")
    console.print(f"\n[#818cf8]  Dox kaydedildi: output/{os.path.basename(fname)}[/]")
