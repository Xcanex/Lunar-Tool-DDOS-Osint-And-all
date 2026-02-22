import requests
from rich.console import Console

console = Console()


def run():
    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    headers = {"Authorization": token, "Content-Type": "application/json"}

    with console.status("[#818cf8]  DM kanallari aliniyor...[/]", spinner="moon"):
        r = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers, timeout=10)

    if r.status_code != 200:
        console.print("[red]  Gecersiz token.[/]")
        return

    channels = r.json()
    if not channels:
        console.print("[yellow]  Hicbir DM kanali bulunamadi.[/]")
        return

    console.print(f"[#818cf8]  {len(channels)} DM kanali bulundu. Kapatma basliyor...[/]")
    closed = 0

    for ch in channels:
        recipients = ch.get("recipients", [])
        name = recipients[0]["username"] if recipients else "Grup"
        try:
            resp = requests.delete(
                f"https://discord.com/api/v9/channels/{ch['id']}",
                headers={"Authorization": token}, timeout=10
            )
            if resp.status_code in (200, 204):
                closed += 1
                console.print(f"[#818cf8]  [+] Kapatildi: {name}[/]")
            else:
                console.print(f"[red]  [-] Basarisiz: {name} ({resp.status_code})[/]")
        except Exception:
            console.print(f"[red]  [-] Hata: {name}[/]")

    console.print(f"\n[#818cf8]  Tamamlandi. Kapatilan: {closed}/{len(channels)}[/]")
