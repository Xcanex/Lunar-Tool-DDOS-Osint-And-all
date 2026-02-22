import requests
from rich.console import Console

console = Console()


def run():
    url = console.input("[bold white]  Webhook URL: [/]").strip()
    if not url or "discord" not in url.lower():
        console.print("[red]  Gecersiz webhook URL.[/]")
        return

    console.print("[yellow]  Bu webhook silinecek. Emin misin? (e/h): [/]", end="")
    ans = input().strip().lower()
    if ans != "e":
        console.print("[dim]  Iptal edildi.[/]")
        return

    try:
        r = requests.delete(url, timeout=10)
        if r.status_code == 204:
            console.print("[#818cf8]  [+] Webhook basariyla silindi![/]")
        else:
            console.print(f"[red]  [-] Silme basarisiz: {r.status_code}[/]")
    except Exception as e:
        console.print(f"[red]  Hata: {e}[/]")
