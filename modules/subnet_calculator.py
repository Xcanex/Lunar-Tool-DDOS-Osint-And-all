import ipaddress
from rich.console import Console
from rich.table import Table

console = Console()


def run():
    cidr = console.input("[bold white]  CIDR (orn: 192.168.1.0/24): [/]").strip()
    if not cidr:
        console.print("[red]  CIDR bos olamaz.[/]")
        return

    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as e:
        console.print(f"[red]  Gecersiz CIDR: {e}[/]")
        return

    table = Table(title=f"Subnet: {cidr}", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Alan", style="bold white", min_width=20)
    table.add_column("Deger", style="#a78bfa")

    table.add_row("Ag Adresi", str(net.network_address))
    table.add_row("Broadcast", str(net.broadcast_address))
    table.add_row("Netmask", str(net.netmask))
    table.add_row("Hostmask", str(net.hostmask))
    table.add_row("Prefix", f"/{net.prefixlen}")
    table.add_row("Toplam IP", str(net.num_addresses))
    table.add_row("Kullanilabilir", str(max(0, net.num_addresses - 2)))
    table.add_row("Ozel Ag", "Evet" if net.is_private else "Hayir")

    console.print()
    console.print(table)

    if net.num_addresses <= 256:
        console.print("\n[#818cf8]  Kullanilabilir IP'ler:[/]")
        hosts = list(net.hosts())
        for h in hosts[:20]:
            console.print(f"  [dim]{h}[/]")
        if len(hosts) > 20:
            console.print(f"  [dim]... ve {len(hosts) - 20} IP daha[/]")
