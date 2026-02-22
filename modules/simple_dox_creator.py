import os
from rich.console import Console
console = Console()

def run():
    console.print("[#818cf8]  Simple Dox Creator[/]\n")
    fields = ["Ad", "Soyad", "Email", "Telefon", "Adres", "Notlar"]
    data = {}
    for f in fields:
        val = console.input(f"[bold white]  {f}: [/]").strip()
        data[f] = val if val else "N/A"

    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, f"simple_dox_{data['Ad']}.txt")
    with open(fname, "w", encoding="utf-8") as f:
        for k, v in data.items():
            f.write(f"{k}: {v}\n")
    console.print(f"\n[#818cf8]  Kaydedildi: output/{os.path.basename(fname)}[/]")
