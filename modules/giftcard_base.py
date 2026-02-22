import random
import string
import os
from rich.console import Console

console = Console()

GIFT_CARDS = {
    "amazon":  {"prefix": "", "length": 14, "charset": string.ascii_uppercase + string.digits, "format": "XXXX-XXXXXX-XXXX"},
    "netflix": {"prefix": "", "length": 16, "charset": string.digits, "format": "XXXX-XXXX-XXXX-XXXX"},
    "apple":   {"prefix": "", "length": 16, "charset": string.ascii_uppercase + string.digits, "format": "XXXX-XXXX-XXXX-XXXX"},
    "steam":   {"prefix": "", "length": 15, "charset": string.ascii_uppercase + string.digits, "format": "XXXXX-XXXXX-XXXXX"},
    "google":  {"prefix": "", "length": 20, "charset": string.ascii_uppercase + string.digits, "format": "XXXX-XXXX-XXXX-XXXX-XXXX"},
    "spotify": {"prefix": "", "length": 16, "charset": string.ascii_uppercase + string.digits, "format": "XXXX-XXXX-XXXX-XXXX"},
}


def generate_code(card_type):
    cfg = GIFT_CARDS.get(card_type, GIFT_CARDS["amazon"])
    code = "".join(random.choices(cfg["charset"], k=cfg["length"]))
    fmt = cfg["format"]
    result = []
    idx = 0
    for ch in fmt:
        if ch == "X" and idx < len(code):
            result.append(code[idx])
            idx += 1
        else:
            result.append(ch)
    return "".join(result)


def run_generator(card_type, display_name):
    count_str = console.input(f"[bold white]  Kac {display_name} kodu uretilsin (varsayilan 20): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 0 < int(count_str) <= 5000 else 20

    console.print(f"[#818cf8]  {count} adet {display_name} kodu uretiliyor...[/]")

    codes = [generate_code(card_type) for _ in range(count)]

    for c in codes[:10]:
        console.print(f"[#a78bfa]  {c}[/]")
    if count > 10:
        console.print(f"[dim]  ... ve {count - 10} kod daha[/]")

    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"{card_type}_codes.txt")
    with open(filename, "a") as f:
        for c in codes:
            f.write(c + "\n")

    console.print(f"[#818cf8]  {count} kod output/{card_type}_codes.txt dosyasina kaydedildi.[/]")
