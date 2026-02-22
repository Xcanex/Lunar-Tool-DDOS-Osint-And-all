import requests
from rich.console import Console

console = Console()


def run():
    email = console.input("[bold white]  Email adresi: [/]").strip()
    if not email or "@" not in email:
        console.print("[red]  Gecersiz email.[/]")
        return

    console.print(f"[#818cf8]  '{email}' araniyor...[/]")

    
    try:
        r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                         headers={"User-Agent": "Lunar-Tool"}, timeout=10)
        if r.status_code == 200:
            breaches = r.json()
            console.print(f"[red]  {len(breaches)} ihlalde bulundu![/]")
            for b in breaches[:10]:
                console.print(f"  [#a78bfa]{b.get('Name', '?')}[/] - {b.get('BreachDate', '?')}")
        elif r.status_code == 404:
            console.print("[green]  Hicbir ihlalde bulunamadi.[/]")
    except Exception:
        console.print("[dim]  HIBP API yanit vermedi.[/]")

    
    try:
        r = requests.get(f"https://api.github.com/search/users?q={email}",
                         timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            items = r.json().get("items", [])[:3]
            if items:
                console.print(f"\n[#818cf8]  GitHub sonuclari:[/]")
                for u in items:
                    console.print(f"  [#a78bfa]@{u['login']}[/] - {u['html_url']}")
    except Exception:
        pass

    
    import hashlib
    email_hash = hashlib.md5(email.lower().encode()).hexdigest()
    console.print(f"\n[#818cf8]  Gravatar: https://www.gravatar.com/{email_hash}[/]")

    console.print(f"\n[#818cf8]  Arama onerileri:[/]")
    console.print(f"  [dim]Google: https://www.google.com/search?q=\"{email}\"[/]")
    console.print(f"  [dim]Hunter.io: https://hunter.io/email-verifier/{email}[/]")
