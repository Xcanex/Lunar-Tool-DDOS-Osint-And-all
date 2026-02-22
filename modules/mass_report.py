import requests
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


def run():
    console.print("[#818cf8]  Mass Report Tool[/]")
    console.print("[dim]  Rapor turleri: 1=Spam, 2=Taciz, 3=NSFW, 4=Tehdit, 5=Diger[/]")

    msg_link = console.input("[bold white]  Mesaj Linki (veya User ID): [/]").strip()
    if not msg_link:
        console.print("[red]  Link/ID bos olamaz.[/]")
        return


    guild_id = channel_id = message_id = ""
    if "/" in msg_link:
        parts = msg_link.split("/")
        if len(parts) >= 3:
            guild_id = parts[-3] if len(parts) >= 3 else ""
            channel_id = parts[-2] if len(parts) >= 2 else ""
            message_id = parts[-1] if len(parts) >= 1 else ""

    reason_str = console.input("[bold white]  Rapor turu (1-5, varsayilan 1): [/]").strip()
    reason_map = {
        "1": 0, "2": 1, "3": 2, "4": 3, "5": 4
    }
    reason = reason_map.get(reason_str, 0)

    count_str = console.input("[bold white]  Kac kere rapor? (varsayilan 5): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 0 < int(count_str) <= 100 else 5

    token = console.input("[bold white]  Discord Token: [/]").strip()
    if not token:
        console.print("[red]  Token bos olamaz.[/]")
        return

    headers = {"Authorization": token, "Content-Type": "application/json"}
    sent = 0
    failed = 0

    with Progress(
        SpinnerColumn(spinner_name="moon"),
        TextColumn("[#818cf8]{task.description}[/]"),
        BarColumn(bar_width=30, style="#312e81", complete_style="#818cf8"),
        TextColumn("[bold white]{task.completed}/{task.total}[/]"),
        console=console,
    ) as progress:
        task = progress.add_task("Raporlaniyor...", total=count)

        for i in range(count):
            try:
                payload = {
                    "channel_id": channel_id,
                    "message_id": message_id,
                    "guild_id": guild_id,
                    "reason": reason
                }
                r = requests.post(
                    "https://discord.com/api/v9/report",
                    headers=headers, json=payload, timeout=10
                )
                if r.status_code in (200, 201, 204):
                    sent += 1
                elif r.status_code == 429:
                    retry = r.json().get("retry_after", 2)
                    time.sleep(retry)
                    r2 = requests.post(
                        "https://discord.com/api/v9/report",
                        headers=headers, json=payload, timeout=10
                    )
                    if r2.status_code in (200, 201, 204):
                        sent += 1
                    else:
                        failed += 1
                else:
                    failed += 1
            except Exception:
                failed += 1

            progress.advance(task)
            time.sleep(0.5)

    console.print(f"\n[#818cf8]  Tamamlandi. Gonderildi: {sent} | Basarisiz: {failed}[/]")
