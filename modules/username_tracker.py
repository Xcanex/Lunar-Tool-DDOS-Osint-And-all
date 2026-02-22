import requests
from rich.console import Console
from rich.table import Table

console = Console()

SITES = [
    ("GitHub", "https://api.github.com/users/{}"),
    ("Twitter", "https://api.twitter.com/2/users/by/username/{}"),
    ("Instagram", "https://www.instagram.com/{}/"),
    ("TikTok", "https://www.tiktok.com/@{}/"),
    ("Reddit", "https://www.reddit.com/user/{}/about.json"),
    ("Steam", "https://steamcommunity.com/id/{}/"),
    ("Twitch", "https://www.twitch.tv/{}"),
    ("YouTube", "https://www.youtube.com/@{}/"),
    ("Pinterest", "https://www.pinterest.com/{}/"),
    ("Spotify", "https://open.spotify.com/user/{}"),
    ("SoundCloud", "https://soundcloud.com/{}"),
    ("Medium", "https://medium.com/@{}"),
    ("DeviantArt", "https://www.deviantart.com/{}"),
    ("Tumblr", "https://{}.tumblr.com/"),
    ("Flickr", "https://www.flickr.com/people/{}/"),
    ("VK", "https://vk.com/{}"),
    ("Roblox", "https://www.roblox.com/user.aspx?username={}"),
    ("Minecraft", "https://api.mojang.com/users/profiles/minecraft/{}"),
    ("Chess.com", "https://www.chess.com/member/{}"),
    ("Duolingo", "https://www.duolingo.com/profile/{}"),
]


def run():
    username = console.input("[bold white]  Kullanici adi: [/]").strip()
    if not username:
        console.print("[red]  Kullanici adi bos olamaz.[/]")
        return

    console.print(f"[#818cf8]  '{username}' araniyor ({len(SITES)} platform)...[/]")

    table = Table(title=f"🔍 {username}", border_style="#818cf8", header_style="bold #a5b4fc")
    table.add_column("Platform", style="bold white", min_width=14)
    table.add_column("Durum", style="#a78bfa")
    table.add_column("URL", style="dim")

    found = 0
    for name, url_template in SITES:
        url = url_template.format(username)
        try:
            r = requests.get(url, timeout=5,
                             headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
            if r.status_code == 200:
                table.add_row(name, "[green]Bulundu[/]", url)
                found += 1
            else:
                table.add_row(name, "[dim]Bulunamadi[/]", "")
        except Exception:
            table.add_row(name, "[dim]Hata[/]", "")

    console.print()
    console.print(table)
    console.print(f"\n[#818cf8]  {found}/{len(SITES)} platformda bulundu.[/]")
