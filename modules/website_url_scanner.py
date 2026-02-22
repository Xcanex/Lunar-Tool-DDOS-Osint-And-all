import requests
import re
from urllib.parse import urljoin
from rich.console import Console
from rich.table import Table
console = Console()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
]


def extract_links(html, base_url, domain):
    links = set()
    
    for attr in re.findall(r'(?:href|src|action)\s*=\s*["\']([^"\']+)["\']', html, re.I):
        full = urljoin(base_url, attr)
        if domain in full and not any(full.endswith(e) for e in [".png", ".jpg", ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf"]):
            links.add(full)
    
    for url in re.findall(r'https?://[^\s"\'<>]+', html):
        if domain in url:
            links.add(url.rstrip("'\"`;,)}]"))
    return links


def run():
    console.print("[bold #818cf8]  WEBSITE URL SCANNER[/]")
    console.print("[dim]  Web sitesindeki tum linkleri bulur.[/]\n")

    url = console.input("[bold white]  Website URL: [/]").strip()
    if not url:
        console.print("[red]  URL bos olamaz.[/]")
        return
    if not url.startswith("http"):
        url = "https://" + url

    domain = re.sub(r'^https?://', '', url).split('/')[0]

    console.print("  [white]1.[/] Sadece ana sayfa")
    console.print("  [white]2.[/] Tum site (derinlemesine)\n")
    mode = console.input("[bold white]  Mod (1/2): [/]").strip() or "1"

    headers = {"User-Agent": USER_AGENTS[0]}
    all_links = set()
    visited = set()

    def scan(target_url):
        if target_url in visited:
            return set()
        visited.add(target_url)
        try:
            r = requests.get(target_url, headers=headers, timeout=10, allow_redirects=True)
            if r.status_code != 200:
                return set()
            links = extract_links(r.text, target_url, domain)
            return links
        except Exception:
            return set()

    with console.status(f"[#818cf8]  {url} taraniyor...[/]"):
        found = scan(url)
        all_links.update(found)

        if mode == "2":
            depth = 0
            to_visit = list(found)
            while to_visit and depth < 3:
                depth += 1
                next_batch = []
                for link in to_visit[:50]:  
                    new = scan(link)
                    for n in new:
                        if n not in all_links:
                            all_links.add(n)
                            next_batch.append(n)
                to_visit = next_batch

    if all_links:
        
        pages = [l for l in all_links if re.search(r'\.(html|php|asp)$|/$', l)]
        scripts = [l for l in all_links if l.endswith(('.js', '.css'))]
        other = [l for l in all_links if l not in pages and l not in scripts]

        console.print(f"\n[bold #818cf8]  Toplam: {len(all_links)} URL bulundu[/]")
        console.print(f"[dim]  Sayfalar: {len(pages)} | Script: {len(scripts)} | Diger: {len(other)}[/]\n")

        
        if pages:
            console.print("[bold white]  -- Sayfalar --[/]")
            for l in sorted(pages)[:30]:
                console.print(f"  {l}")

        if scripts:
            console.print("\n[bold white]  -- Script/CSS --[/]")
            for l in sorted(scripts)[:20]:
                console.print(f"  {l}")

        if other:
            console.print("\n[bold white]  -- Diger --[/]")
            for l in sorted(other)[:30]:
                console.print(f"  {l}")

        if len(all_links) > 80:
            console.print(f"\n[dim]  ... ve {len(all_links) - 80} link daha[/]")
    else:
        console.print("[yellow]  Link bulunamadi.[/]")
