import random
import os
from rich.console import Console
console = Console()

def run():
    mode = console.input("[bold white]  Mod: 1=Rastgele, 2=Aralik, 3=Belirli subnet: [/]").strip() or "1"
    count_str = console.input("[bold white]  Kac IP (varsayilan 20): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 0 < int(count_str) <= 10000 else 20

    ips = []
    if mode == "2":
        prefix = console.input("[bold white]  Prefix (orn: 192.168.1): [/]").strip() or "192.168.1"
        for i in range(count):
            ips.append(f"{prefix}.{random.randint(1, 254)}")
    elif mode == "3":
        subnet = console.input("[bold white]  Subnet (orn: 10.0.0): [/]").strip() or "10.0.0"
        for i in range(count):
            ips.append(f"{subnet}.{random.randint(1, 254)}")
    else:
        for _ in range(count):
            ips.append(f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}")

    for ip in ips[:20]:
        console.print(f"  [#a78bfa]{ip}[/]")
    if count > 20:
        console.print(f"  [dim]... ve {count - 20} IP daha[/]")

    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "generated_ips.txt"), "w") as f:
        for ip in ips:
            f.write(ip + "\n")
    console.print(f"[#818cf8]  {count} IP output/generated_ips.txt dosyasina kaydedildi.[/]")
