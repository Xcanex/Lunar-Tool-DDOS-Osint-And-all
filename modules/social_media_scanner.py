import requests
from rich.console import Console
from rich.table import Table

console = Console()

PLATFORMS = [
    ("GitHub", "https://github.com/{}", 200),
    ("Twitter/X", "https://twitter.com/{}", 200),
    ("Instagram", "https://www.instagram.com/{}/", 200),
    ("TikTok", "https://www.tiktok.com/@{}", 200),
    ("Reddit", "https://www.reddit.com/user/{}", 200),
    ("YouTube", "https://www.youtube.com/@{}", 200),
    ("Twitch", "https://www.twitch.tv/{}", 200),
    ("Pinterest", "https://www.pinterest.com/{}/", 200),
    ("LinkedIn", "https://www.linkedin.com/in/{}/", 200),
    ("Snapchat", "https://www.snapchat.com/add/{}", 200),
    ("Telegram", "https://t.me/{}", 200),
    ("SoundCloud", "https://soundcloud.com/{}", 200),
    ("Medium", "https://medium.com/@{}", 200),
    ("DeviantArt", "https://www.deviantart.com/{}", 200),
    ("Tumblr", "https://{}.tumblr.com/", 200),
    ("Spotify", "https://open.spotify.com/user/{}", 200),
]


def run():
    username = console.input("[bold white]  Kullanici adi: [/]").strip()
    if not username:
        console.print("[red]  Bos olamaz.[/]")
        return

    console.print(f"[#818cf8]  '{username}' araniyor ({len(PLATFORMS)} platform)...[/]")

    table = Table(title=f"📱 Social Media Scan: {username}",
                  border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Platform", style="bold white", min_width=14)
    table.add_column("Durum", min_width=10)
    table.add_column("Link", style="dim")

    found = 0
    for name, url_tpl, ok_code in PLATFORMS:
        url = url_tpl.format(username)
        try:
            r = requests.get(url, timeout=5,
                             headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=False)
            if r.status_code == ok_code:
                table.add_row(name, "[green]Bulundu[/]", url)
                found += 1
            else:
                table.add_row(name, "[dim]Yok[/]", "")
        except Exception:
            table.add_row(name, "[dim]Hata[/]", "")

    console.print()
    console.print(table)
    console.print(f"\n[#818cf8]  {found}/{len(PLATFORMS)} platformda bulundu.[/]")
