import socket
from rich.console import Console
from rich.table import Table

console = Console()

GAME_PORTS = {
    25565: "Minecraft",
    27015: "Source (CS:GO/TF2)",
    27016: "Source Alt",
    7777: "Terraria/Unreal",
    19132: "Minecraft Bedrock",
    2302: "Arma/DayZ",
    5761: "FiveM (GTA V)",
    30120: "FiveM Alt",
    9987: "TeamSpeak",
    64738: "Mumble",
}

def run():
    ip = console.input("[bold white]  Sunucu IP: [/]").strip()
    if not ip:
        console.print("[red]  IP bos olamaz.[/]")
        return

    console.print(f"[#818cf8]  {ip} uzerinde oyun portlari taraniyor...[/]")

    table = Table(title="🎮 Game Server Scan", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Port", style="bold white")
    table.add_column("Oyun", style="#a78bfa")
    table.add_column("Durum", style="bold")

    found = 0
    for port, game in GAME_PORTS.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            result = s.connect_ex((ip, port))
            s.close()
            if result == 0:
                table.add_row(str(port), game, "[green]ACIK[/]")
                found += 1
            else:
                table.add_row(str(port), game, "[dim]Kapali[/]")
        except Exception:
            table.add_row(str(port), game, "[dim]Hata[/]")

    console.print()
    console.print(table)
    console.print(f"\n[#818cf8]  {found} acik oyun portu bulundu.[/]")
