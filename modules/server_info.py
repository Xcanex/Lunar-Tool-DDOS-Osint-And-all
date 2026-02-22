import requests
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    invite = console.input("[bold white]  Sunucu Daveti (link veya kod): [/]").strip()
    if not invite:
        console.print("[red]  Davet bos olamaz.[/]")
        return

    code = invite.split("/")[-1]

    with console.status("[#818cf8]  Sunucu bilgisi aliniyor...[/]", spinner="moon"):
        r = requests.get(f"https://discord.com/api/v9/invites/{code}?with_counts=true", timeout=10)

    if r.status_code != 200:
        console.print("[red]  Gecersiz davet.[/]")
        return

    data = r.json()
    guild = data.get("guild", {})
    inviter = data.get("inviter", {})
    channel = data.get("channel", {})

    table = Table(title="🌕 Sunucu Bilgisi", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Alan", style="bold white", min_width=22)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Sunucu Adi", guild.get("name", "N/A"))
    table.add_row("Sunucu ID", guild.get("id", "N/A"))
    table.add_row("Aciklama", guild.get("description", "Yok") or "Yok")
    table.add_row("Davet Kodu", data.get("code", "N/A"))
    table.add_row("Kanal", f"#{channel.get('name', '?')} ({channel.get('id', '?')})")
    table.add_row("Uye Sayisi", str(data.get("approximate_member_count", "?")))
    table.add_row("Cevrimici", str(data.get("approximate_presence_count", "?")))
    table.add_row("Boost Sayisi", str(guild.get("premium_subscription_count", 0)))

    features = guild.get("features", [])
    table.add_row("Ozellikler", ", ".join(features) if features else "Yok")

    verification = {0: "Yok", 1: "Dusuk", 2: "Orta", 3: "Yuksek", 4: "En Yuksek"}
    table.add_row("Dogrulama", verification.get(guild.get("verification_level", 0), "?"))
    table.add_row("NSFW Seviye", str(guild.get("nsfw_level", 0)))

    icon = guild.get("icon")
    if icon:
        ext = "gif" if icon.startswith("a_") else "png"
        table.add_row("Ikon", f"https://cdn.discordapp.com/icons/{guild['id']}/{icon}.{ext}")

    console.print()
    console.print(table)

    if inviter:
        table2 = Table(title="Davet Eden", border_style="#818cf8", header_style="bold #a5b4fc")
        table2.add_column("Alan", style="bold white", min_width=16)
        table2.add_column("Deger", style="#a78bfa")
        table2.add_row("Kullanici", inviter.get("username", "?"))
        table2.add_row("ID", inviter.get("id", "?"))
        table2.add_row("Global Ad", inviter.get("global_name", "N/A") or "N/A")
        console.print(table2)
