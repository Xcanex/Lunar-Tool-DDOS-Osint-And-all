import hashlib
from rich.console import Console
from rich.table import Table

console = Console()

HASH_LENGTHS = {
    32:  "MD5",
    40:  "SHA-1",
    56:  "SHA-224",
    64:  "SHA-256",
    96:  "SHA-384",
    128: "SHA-512",
    8:   "CRC32",
}


def run():
    hash_input = console.input("[bold white]  Hash degeri: [/]").strip()
    if not hash_input:
        console.print("[red]  Hash bos olamaz.[/]")
        return

    length = len(hash_input)
    detected = HASH_LENGTHS.get(length)

    table = Table(title="Hash Analyzer", border_style="#818cf8")
    table.add_column("Alan", style="bold white", min_width=16)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Hash", hash_input[:64] + ("..." if len(hash_input) > 64 else ""))
    table.add_row("Uzunluk", str(length))
    table.add_row("Hex", "Evet" if all(c in "0123456789abcdefABCDEF" for c in hash_input) else "Hayir")
    table.add_row("Tespit", detected or "Bilinmiyor")

    if detected:
        possible = [detected]
        if length == 32:
            possible.append("NTLM")
        if length == 40:
            possible.extend(["MySQL5", "RIPEMD-160"])
        if length == 64:
            possible.append("SHA3-256")
        if length == 128:
            possible.append("SHA3-512")
        table.add_row("Olasi Turler", ", ".join(possible))

    console.print()
    console.print(table)

    console.print("\n[#818cf8]  Yaygin stringlerle karsilastiriliyor...[/]")
    common = ["admin", "password", "123456", "root", "test", "1234", "qwerty", "abc123"]
    for word in common:
        for algo in ["md5", "sha1", "sha256", "sha512"]:
            try:
                h = hashlib.new(algo, word.encode()).hexdigest()
                if h == hash_input.lower():
                    console.print(f"  [bold green]ESLESTI: '{word}' ({algo})[/]")
                    return
            except Exception:
                pass
    console.print("[dim]  Yaygin stringlerde eslesme bulunamadi.[/]")
