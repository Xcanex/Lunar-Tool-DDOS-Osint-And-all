import hashlib
import itertools
import string
import threading
from rich.console import Console

console = Console()

HASH_TYPES = {32: "md5", 40: "sha1", 64: "sha256", 128: "sha512"}

def run():
    target = console.input("[bold white]  Hash: [/]").strip()
    if not target:
        console.print("[red]  Hash bos olamaz.[/]")
        return

    hash_type = HASH_TYPES.get(len(target))
    if not hash_type:
        console.print("[yellow]  Hash turu taninamadi. MD5/SHA1/SHA256/SHA512 desteklenir.[/]")
        hash_type = console.input("[bold white]  Hash turu (md5/sha1/sha256): [/]").strip() or "md5"

    console.print(f"[#818cf8]  Hash turu: {hash_type}[/]")
    mode = console.input("[bold white]  Mod: 1=Wordlist, 2=Brute (max 4 char): [/]").strip()

    if mode == "1":
        wl = console.input("[bold white]  Wordlist dosya yolu: [/]").strip()
        try:
            with open(wl, "r", errors="ignore") as f:
                for line in f:
                    word = line.strip()
                    h = hashlib.new(hash_type, word.encode()).hexdigest()
                    if h == target.lower():
                        console.print(f"\n[bold green]  BULUNDU: {word}[/]")
                        return
            console.print("[red]  Bulunamadi.[/]")
        except FileNotFoundError:
            console.print("[red]  Dosya bulunamadi.[/]")
    else:
        console.print("[#818cf8]  Brute force baslatiliyor (max 4 karakter)...[/]")
        charset = string.ascii_lowercase + string.digits
        for length in range(1, 5):
            for combo in itertools.product(charset, repeat=length):
                word = "".join(combo)
                h = hashlib.new(hash_type, word.encode()).hexdigest()
                if h == target.lower():
                    console.print(f"\n[bold green]  BULUNDU: {word}[/]")
                    return
        console.print("[red]  Bulunamadi (4 karakter limitinde).[/]")
