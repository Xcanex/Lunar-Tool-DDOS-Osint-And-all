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
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    with console.status("[#818cf8]  Arkadaslar aliniyor...[/]", spinner="moon"):
        fr = requests.get("https://discord.com/api/v9/users/@me/relationships",
                          headers=headers, timeout=10)

    if fr.status_code != 200:
        console.print("[red]  Arkadas listesi alinamadi.[/]")
        return

    friends = fr.json()
    if not friends:
        console.print("[yellow]  Hicbir arkadas bulunamadi.[/]")
        return

    console.print(f"[#818cf8]  {len(friends)} arkadas bulundu. Silme basliyor...[/]")
    deleted = 0
    failed = 0

    def delete_batch(batch):
        nonlocal deleted, failed
        for friend in batch:
            user = friend.get("user", {})
            name = user.get("username", "?")
            try:
                resp = requests.delete(
                    f"https://discord.com/api/v9/users/@me/relationships/{friend['id']}",
                    headers={"Authorization": token}, timeout=10
                )
                if resp.status_code in (200, 204):
                    deleted += 1
                    console.print(f"[#818cf8]  [+] Silindi: {name}[/]")
                else:
                    failed += 1
                    console.print(f"[red]  [-] Basarisiz: {name}[/]")
            except Exception:
                failed += 1

    threads = []
    for i in range(0, len(friends), 3):
        batch = friends[i:i+3]
        t = threading.Thread(target=delete_batch, args=(batch,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    console.print(f"\n[#818cf8]  Tamamlandi. Silindi: {deleted} | Basarisiz: {failed}[/]")
