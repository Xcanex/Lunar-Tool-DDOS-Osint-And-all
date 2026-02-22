import requests
from rich.console import Console

console = Console()

SEARCH_APIS = [
    "https://api.github.com/search/users?q={}",
    "https://api.mojang.com/users/profiles/minecraft/{}",
]


def run():
    name = console.input("[bold white]  Isim (ad soyad): [/]").strip()
    if not name:
        console.print("[red]  Isim bos olamaz.[/]")
        return

    console.print(f"[#818cf8]  '{name}' araniyor...[/]")

    try:
        r = requests.get(f"https://api.github.com/search/users?q={name.replace(' ', '+')}",
                         timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            data = r.json()
            items = data.get("items", [])[:5]
            if items:
                console.print(f"\n[#818cf8]  GitHub sonuclari ({data.get('total_count', 0)}):[/]")
                for u in items:
                    console.print(f"  [#a78bfa]@{u['login']}[/] - {u['html_url']}")
    except Exception:
        pass

    console.print(f"\n[#818cf8]  Arama onerileri:[/]")
    console.print(f"  [dim]Google: https://www.google.com/search?q={name.replace(' ', '+')}[/]")
    console.print(f"  [dim]LinkedIn: https://www.linkedin.com/search/results/all/?keywords={name.replace(' ', '%20')}[/]")
    console.print(f"  [dim]Facebook: https://www.facebook.com/search/top?q={name.replace(' ', '%20')}[/]")
    console.print(f"  [dim]Twitter: https://twitter.com/search?q={name.replace(' ', '%20')}[/]")
    console.print(f"  [dim]Pipl: https://pipl.com/search/?q={name.replace(' ', '+')}[/]")
