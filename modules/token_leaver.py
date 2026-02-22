import requests
import threading
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Gecersiz token veya erisim yok.[/]")
        return

    guilds = r.json()
    if not guilds:
        console.print("[yellow]  Hicbir sunucu bulunamadi.[/]")
        return

    console.print(f"[#818cf8]  {len(guilds)} sunucu bulundu. Ayrilma basliyor...[/]")

    left = 0
    failed = 0

    def leave_batch(batch):
        nonlocal left, failed
        for guild in batch:
            try:
                resp = requests.delete(
                    f"https://discord.com/api/v8/users/@me/guilds/{guild['id']}",
                    headers={"Authorization": token}, timeout=10
                )
                if resp.status_code in (200, 204):
                    left += 1
                    console.print(f"[#818cf8]  [+] Ayrildi: {guild.get('name', '?')}[/]")
                elif resp.status_code == 400:
                    resp2 = requests.delete(
                        f"https://discord.com/api/v8/guilds/{guild['id']}",
                        headers={"Authorization": token}, timeout=10
                    )
                    if resp2.status_code in (200, 204):
                        left += 1
                        console.print(f"[#818cf8]  [+] Silindi (sahip): {guild.get('name', '?')}[/]")
                    else:
                        failed += 1
                        console.print(f"[red]  [-] Basarisiz: {guild.get('name', '?')}[/]")
                else:
                    failed += 1
                    console.print(f"[red]  [-] Hata {resp.status_code}: {guild.get('name', '?')}[/]")
            except Exception as e:
                failed += 1
                console.print(f"[red]  [-] Hata: {e}[/]")

    threads = []
    for i in range(0, len(guilds), 3):
        batch = guilds[i:i+3]
        t = threading.Thread(target=leave_batch, args=(batch,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    console.print(f"\n[#818cf8]  Tamamlandi. Ayrildi: {left} | Basarisiz: {failed}[/]")
