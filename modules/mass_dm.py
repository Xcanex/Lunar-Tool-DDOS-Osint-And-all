import requests
import threading
import time
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    message = console.input("[bold white]  Mesaj: [/]").strip()
    if not message:
        console.print("[red]  Mesaj bos olamaz.[/]")
        return

    rep_str = console.input("[bold white]  Tekrar sayisi (varsayilan 1): [/]").strip()
    repetition = int(rep_str) if rep_str.isdigit() and int(rep_str) > 0 else 1

    headers = {"Authorization": token, "Content-Type": "application/json"}

    with console.status("[#818cf8]  DM kanallari aliniyor...[/]", spinner="moon"):
        r = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers, timeout=10)

    if r.status_code != 200:
        console.print("[red]  Gecersiz token veya erisim yok.[/]")
        return

    channels = r.json()
    if not channels:
        console.print("[yellow]  Hicbir DM kanali bulunamadi.[/]")
        return

    console.print(f"[#818cf8]  {len(channels)} DM kanali bulundu. Mass DM basliyor...[/]")
    sent = 0
    failed = 0

    def send_batch(batch):
        nonlocal sent, failed
        for ch in batch:
            recipients = ch.get("recipients", [])
            user_name = recipients[0]["username"] if recipients else "?"
            try:
                resp = requests.post(
                    f"https://discord.com/api/v9/channels/{ch['id']}/messages",
                    headers={"Authorization": token},
                    data={"content": message}, timeout=10
                )
                if resp.status_code == 200:
                    sent += 1
                    console.print(f"[#818cf8]  [+] Gonderildi: {user_name}[/]")
                else:
                    failed += 1
                    console.print(f"[red]  [-] Basarisiz ({resp.status_code}): {user_name}[/]")
            except Exception:
                failed += 1

    for rep in range(repetition):
        if repetition > 1:
            console.print(f"[dim]  --- Tur {rep+1}/{repetition} ---[/]")
        threads = []
        for i in range(0, len(channels), 3):
            batch = channels[i:i+3]
            t = threading.Thread(target=send_batch, args=(batch,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        if rep < repetition - 1:
            time.sleep(0.5)

    console.print(f"\n[#818cf8]  Tamamlandi. Gonderildi: {sent} | Basarisiz: {failed}[/]")
