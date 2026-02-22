import zipfile
import string
import random
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
console = Console()


def run():
    console.print("[bold #818cf8]  ZIP/RAR Sifre Kirici[/]")
    console.print("[dim]  Sifreli arsiv dosyalarini kirar.[/]\n")

    file_path = console.input("[bold white]  ZIP dosya yolu: [/]").strip()
    if not file_path or not os.path.exists(file_path):
        console.print("[red]  Dosya bulunamadi.[/]")
        return

    if not file_path.lower().endswith(".zip"):
        console.print("[red]  Sadece .zip dosyalari desteklenir.[/]")
        return

    try:
        zf = zipfile.ZipFile(file_path)
    except Exception as e:
        console.print(f"[red]  Dosya acilamadi: {e}[/]")
        return

    try:
        zf.extractall(pwd=None)
        console.print("[yellow]  Bu dosya sifre ile korunmuyor.[/]")
        return
    except RuntimeError:
        pass
    except Exception:
        pass

    console.print(f"[#818cf8]  Dosya: {file_path}[/]")
    console.print(f"[#818cf8]  Arsivdeki dosya sayisi: {len(zf.namelist())}[/]\n")

    console.print("  [white]1.[/] Wordlist ile kirma")
    console.print("  [white]2.[/] Brute force (rastgele)\n")

    method = console.input("[bold white]  Metod (1/2): [/]").strip() or "1"

    found_pw = {"value": None}

    def try_password(pw):
        if found_pw["value"]:
            return
        try:
            zf.extractall(pwd=pw.encode())
            found_pw["value"] = pw
            return True
        except (RuntimeError, zipfile.BadZipFile, Exception):
            return False

    if method == "1":
        wl_path = console.input("[bold white]  Wordlist yolu (veya bos=varsayilan): [/]").strip()

        if not wl_path:
            wl_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wordlists")
            if os.path.exists(wl_dir):
                files = [f for f in os.listdir(wl_dir) if f.endswith(".txt")]
                if files:
                    wl_path = os.path.join(wl_dir, files[0])
                    console.print(f"[dim]  Varsayilan: {wl_path}[/]")

        if not wl_path or not os.path.exists(wl_path):
            console.print("[yellow]  Wordlist bulunamadi, yaygin sifreleri deniyorum...[/]")
            common = ["123456", "password", "1234", "12345", "123456789", "admin",
                      "qwerty", "abc123", "111111", "letmein", "welcome", "monkey",
                      "dragon", "master", "1234567", "12345678", "test", "pass",
                      "iloveyou", "trustno1", "000000", "1q2w3e", "654321"]
            for pw in common:
                if try_password(pw):
                    break
        else:
            console.print(f"[#818cf8]  Wordlist yukluyor: {wl_path}[/]")
            count = 0
            try:
                with open(wl_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        pw = line.strip()
                        if not pw:
                            continue
                        count += 1
                        if count % 1000 == 0:
                            console.print(f"[dim]  Denenen: {count}[/]")
                        if try_password(pw):
                            break
                        if found_pw["value"]:
                            break
            except Exception as e:
                console.print(f"[red]  Hata: {e}[/]")

    elif method == "2":
        min_len = console.input("[bold white]  Min uzunluk (varsayilan 4): [/]").strip()
        max_len = console.input("[bold white]  Max uzunluk (varsayilan 8): [/]").strip()
        min_l = int(min_len) if min_len.isdigit() else 4
        max_l = int(max_len) if max_len.isdigit() else 8
        thread_str = console.input("[bold white]  Thread (varsayilan 4): [/]").strip()
        threads = int(thread_str) if thread_str.isdigit() else 4

        console.print(f"[#818cf8]  Brute force: {min_l}-{max_l} karakter, {threads} thread[/]")

        all_chars = string.ascii_letters + string.digits + string.punctuation
        count = {"val": 0}

        def brute():
            while not found_pw["value"]:
                pw = "".join(random.choice(all_chars) for _ in range(random.randint(min_l, max_l)))
                count["val"] += 1
                if count["val"] % 500 == 0:
                    console.print(f"[dim]  Denenen: {count['val']}[/]")
                try_password(pw)

        try:
            ts = []
            for _ in range(threads):
                t = threading.Thread(target=brute, daemon=True)
                t.start()
                ts.append(t)
            for t in ts:
                t.join(timeout=120)
        except KeyboardInterrupt:
            pass

    if found_pw["value"]:
        console.print(f"\n[bold green]  SIFRE BULUNDU: {found_pw['value']}[/]")
    else:
        console.print("\n[yellow]  Sifre bulunamadi.[/]")
