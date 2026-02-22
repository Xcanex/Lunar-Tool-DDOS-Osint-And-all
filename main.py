import os
import sys
import time
import random
import math

os.environ["PYTHONIOENCODING"] = "utf-8"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console(force_terminal=True)


MODULES = {
    "01": ("IP Lookup",        "modules.ip_lookup"),
    "02": ("Ping Tool",        "modules.ping_tool"),
    "03": ("Port Scanner",     "modules.port_scanner"),
    "04": ("Mass IP Pinger",   "modules.mass_ping"),
    "05": ("DNS Lookup",       "modules.dns_lookup"),
    "06": ("Subdomain Finder", "modules.subdomain_finder"),
    "07": ("HTTP Headers",     "modules.http_headers"),
    "08": ("Proxy Checker",    "modules.proxy_checker"),
    "09": ("Reverse DNS",      "modules.reverse_dns"),
    "10": ("Website Scanner",  "modules.website_vuln_scanner"),
    "11": ("Website Info",     "modules.website_info_scanner"),
    "12": ("IP Geolocation",   "modules.geolocation"),
    "13": ("WHOIS Lookup",     "modules.whois_lookup"),
    "14": ("Phone Lookup",     "modules.phone_lookup"),
    "15": ("Email Validator",  "modules.email_validator"),
    "16": ("MAC Lookup",       "modules.mac_lookup"),
    "17": ("Social Scraper",   "modules.social_scraper"),
    "18": ("Leak Check",       "modules.leak_check"),
    "19": ("Tech Detector",    "modules.tech_detector"),
    "20": ("Google Dorking",   "modules.google_dorking"),
    "21": ("Exploit Scanner",  "modules.exploit_scanner"),
    "22": ("Username Tracker", "modules.username_tracker"),
    "23": ("Instagram OSINT",  "modules.instagram_osint"),
    "24": ("Name Tracker",     "modules.name_tracker"),
    "25": ("Email Tracker",    "modules.email_tracker_osint"),
    "26": ("Image EXIF",       "modules.image_exif"),
    "27": ("TikTok OSINT",     "modules.tiktok_osint"),
    "28": ("Steam OSINT",      "modules.steam_osint"),
    "29": ("Valorant OSINT",   "modules.valorant_osint"),
    "30": ("Token Checker",    "modules.discord_checker"),
    "31": ("Webhook Spammer",  "modules.webhook_spammer"),
    "32": ("Token Nuker",      "modules.token_nuker"),
    "33": ("Token Leaver",     "modules.token_leaver"),
    "34": ("Token Login",      "modules.token_login"),
    "35": ("Token Spammer",    "modules.token_spammer"),
    "36": ("Mass DM",          "modules.mass_dm"),
    "37": ("Delete Friends",   "modules.delete_friends"),
    "38": ("Block Friends",    "modules.block_friends"),
    "39": ("Delete DMs",       "modules.delete_dms"),
    "40": ("Status Changer",   "modules.status_changer"),
    "41": ("Theme Changer",    "modules.theme_changer"),
    "42": ("Server Info",      "modules.server_info"),
    "43": ("Webhook Info",     "modules.webhook_info"),
    "44": ("Webhook Deleter",  "modules.webhook_deleter"),
    "45": ("Nitro Generator",  "modules.nitro_generator"),
    "46": ("Mass Report",      "modules.mass_report"),
    "47": ("Server Raid",      "modules.server_raid"),
    "48": ("Create Channels",  "modules.mass_create_channels"),
    "49": ("Create Roles",     "modules.mass_create_roles"),
    "50": ("Ping Channels",    "modules.mass_ping_channels"),
    "51": ("Del Channels",     "modules.delete_all_channels"),
    "52": ("Del Roles",        "modules.delete_all_roles"),
    "53": ("Del Emojis",       "modules.delete_all_emojis"),
    "54": ("Mass Kick",        "modules.mass_kick"),
    "55": ("Mass Ban",         "modules.mass_ban"),
    "56": ("Email Bomber",     "modules.email_bomber"),
    "57": ("Email Reset Bomb", "modules.email_bomber_reset"),
    "58": ("DDoS IP",          "modules.ddos_ip"),
    "59": ("DDoS Website",     "modules.ddos_website"),
    "60": ("Amazon Gift",      "modules.amazon_giftcard"),
    "61": ("Netflix Gift",     "modules.netflix_giftcard"),
    "62": ("Apple Gift",       "modules.apple_giftcard"),
    "63": ("Steam Gift",       "modules.steam_giftcard"),
    "64": ("Google Play Gen",  "modules.google_play_gen"),
    "65": ("Spotify Gift",     "modules.spotify_gift_gen"),
    "66": ("Hash Generator",   "modules.hash_generator"),
    "67": ("Password Gen",     "modules.password_generator"),
    "68": ("Base64 Tool",      "modules.base64_tool"),
    "69": ("String Tools",     "modules.string_tools"),
    "70": ("QR Code Gen",      "modules.qr_generator"),
    "71": ("URL Shortener",    "modules.url_shortener"),
    "72": ("WiFi Passwords",   "modules.wifi_passwords"),
    "73": ("Fake Info Gen",    "modules.fake_info"),
    "74": ("System Info",      "modules.system_info"),
    "75": ("Dox Creator",      "modules.dox_creator"),
    "76": ("Simple Dox",       "modules.simple_dox_creator"),
    "77": ("Search Database",  "modules.search_database"),
    "78": ("SQL Injection",    "modules.sql_injection"),
    "79": ("XSS Scanner",      "modules.xss_scanner"),
    "80": ("Pass Cracker",     "modules.password_cracker"),
    "81": ("File Integrity",   "modules.file_integrity"),
    "82": ("DNS Spoof Detect", "modules.dns_spoof_detector"),
    "83": ("Crypto Wallet",    "modules.crypto_wallet"),
    "84": ("Steganography",    "modules.steganography"),
    "85": ("IP Rotator",       "modules.ip_rotator"),
    "86": ("ARP Spoofing",     "modules.arp_spoof"),
    "87": ("Packet Sniffer",   "modules.packet_sniffer"),
    "88": ("Brute Force",      "modules.brute_force"),
    "89": ("Roblox User Info", "modules.roblox_user_info"),
    "90": ("Roblox Cookie",    "modules.roblox_cookie_info"),
    "91": ("Game Server Scan", "modules.game_server_scanner"),
    "92": ("Social Scanner",   "modules.social_media_scanner"),
    "93": ("Dark Web Links",   "modules.dark_web_links"),
    "94": ("IP Scanner",       "modules.ip_scanner"),
    "95": ("Network Analyzer", "modules.network_analyzer"),
    "96": ("Subnet Calculator","modules.subnet_calculator"),
    "97": ("VPN Checker",      "modules.vpn_checker"),
    "98": ("IP Generator",     "modules.ip_generator"),
    "100": ("Language Changer", "modules.language_changer"),
    "101": ("Phishing Sim",     "modules.phishing_simulator"),
    "102": ("Hash Analyzer",    "modules.hash_analyzer"),
    "103": ("MAC Spoofer",      "modules.mac_spoofer"),
    "104": ("Roblox ID Info",   "modules.roblox_id_info"),
    "105": ("Profile Analyzer", "modules.player_profile_analyzer"),
    "106": ("Item Value Check", "modules.item_value_checker"),
    "107": ("Trade History",    "modules.trade_history_tracker"),
    "108": ("Virus Builder",    "modules.virus_builder"),
    "109": ("D0x Tracker",      "modules.dox_tracker"),
    "110": ("Bot Invite-ID",    "modules.bot_invite_to_id"),
    "111": ("House Changer",    "modules.house_changer"),
    "112": ("Token-to-ID",      "modules.token_to_id"),
    "113": ("Webhook Gen",      "modules.webhook_generator"),
    "114": ("ZIP Cracker",      "modules.zip_cracker"),
    "115": ("Roblox Cookie Log","modules.roblox_cookie_login"),
    "116": ("URL Scanner",      "modules.website_url_scanner"),
}

CATEGORIES = {
    "NETWORK":    ["01","02","03","04","05","06","07","08","09","10","11","94","95","96","97","98","116"],
    "OSINT":      ["12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","109"],
    "DISCORD":    ["30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","100","110","111","112","113"],
    "NUKER":      ["48","49","50","51","52","53","54","55"],
    "BOMBING":    ["56","57","58","59"],
    "GENERATOR":  ["60","61","62","63","64","65"],
    "UTILITY":    ["66","67","68","69","70","71","72","73","74","75","76","77"],
    "SECURITY":   ["78","79","80","81","82","101","102","103","114"],
    "HACKING":    ["83","84","85","86","87","88"],
    "GAME OSINT": ["89","90","91","92","104","105","106","107","115"],
    "DARK WEB":   ["93"],
    "BUILDER":    ["108"],
}

CAT_ICONS = {
    "NETWORK":    "*",
    "OSINT":      "*",
    "DISCORD":    "*",
    "NUKER":      "*",
    "BOMBING":    "*",
    "GENERATOR":  "*",
    "UTILITY":    "*",
    "SECURITY":   "*",
    "HACKING":    "*",
    "GAME OSINT": "*",
    "DARK WEB":   "*",
    "BUILDER":    "*",
}

CAT_COLORS = {
    "NETWORK":    "#c084fc",
    "OSINT":      "#a78bfa",
    "DISCORD":    "#818cf8",
    "NUKER":      "#f87171",
    "BOMBING":    "#fb923c",
    "GENERATOR":  "#34d399",
    "UTILITY":    "#7c3aed",
    "SECURITY":   "#38bdf8",
    "HACKING":    "#ef4444",
    "GAME OSINT": "#facc15",
    "DARK WEB":   "#6b7280",
    "BUILDER":    "#dc2626",
}

ITEMS_PER_PAGE = 21
MOON_PHASES = ["()", "()", "()", "()", "(o)", "(o)", "(o)", "()"]

BANNER_ART = [
    "  ╦  ╦ ╦╔╗╔╔═╗╦═╗",
    "  ║  ║ ║║║║╠═╣╠╦╝",
    "  ╩═╝╚═╝╝╚╝╩ ╩╩╚═",
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def tw():
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 80


def center(text, width=None):
    w = width or tw()
    lines = text.split("\n") if isinstance(text, str) else [text]
    return "\n".join(line.center(w) for line in lines)


def gradient_bar(width=46):
    colors = ["#1e1b4b", "#312e81", "#4338ca", "#6366f1",
              "#818cf8", "#a5b4fc", "#818cf8", "#6366f1",
              "#4338ca", "#312e81", "#1e1b4b"]
    seg = max(1, width // len(colors))
    t = Text()
    for c in colors:
        t.append("━" * seg, style=c)
    return t


def key_to_cat(key):
    for cat, keys in CATEGORIES.items():
        if key in keys:
            return cat
    return None


def total_pages():
    return math.ceil(len(MODULES) / ITEMS_PER_PAGE)



def animated_intro():
    clear()
    frames = [
        "░░░░░░░░░░░░░░░░░░░░",
        "▓▓▓░░░░░░░░░░░░░░░░░",
        "▓▓▓▓▓▓░░░░░░░░░░░░░░",
        "▓▓▓▓▓▓▓▓▓░░░░░░░░░░░",
        "▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░",
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░",
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░",
        "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
    ]
    for i, bar in enumerate(frames):
        clear()
        w = tw()
        console.print()
        console.print()
        console.print(Align.center("[bold #818cf8](o)  L U N A R  (o)[/]"))
        console.print()
        console.print(Align.center(f"[#6366f1][{bar}][/]"))
        console.print(Align.center("[dim #a5b4fc]Yukleniyor...[/]"))
        time.sleep(0.08)
    time.sleep(0.2)
    clear()



def print_banner():
    console.print()
    for line in BANNER_ART:
        console.print(Align.center(f"[bold #818cf8]{line}[/]"))
    console.print(Align.center(gradient_bar(40)))
    console.print(Align.center(
        "[bold #a5b4fc](o) T O O L  F R A M E W O R K (o)[/]"
    ))
    console.print(Align.center(
        f"[dim italic #6366f1]v3.5  |  {len(MODULES)} Modules  |  Lunar Team[/]"
    ))
    console.print(Align.center(gradient_bar(40)))
    console.print()



def print_menu(page):
    all_keys = sorted(MODULES.keys(), key=lambda x: int(x))
    tp = total_pages()
    start = (page - 1) * ITEMS_PER_PAGE
    end = min(start + ITEMS_PER_PAGE, len(all_keys))
    page_keys = all_keys[start:end]

    w = tw()
    col_w = 22
    cols = max(1, min(3, (w - 4) // col_w))
    pad_l = max(0, (w - cols * col_w) // 2)
    sp = " " * pad_l

    last_cat = None
    row_items = []

    def flush_row():
        nonlocal row_items
        if not row_items:
            return
        line_parts = []
        for key, name in row_items:
            cat = key_to_cat(key)
            cc = CAT_COLORS.get(cat, "#a78bfa")
            entry = f"[{cc}][[/][bold white]{key}[/][{cc}]][/] {name}"
            plain_len = len(f"[{key}] {name}")
            padding = col_w - plain_len
            line_parts.append(entry + " " * max(padding, 1))
        console.print(f"{sp}{''.join(line_parts)}")
        row_items = []

    for key in page_keys:
        cat = key_to_cat(key)
        if cat != last_cat:
            flush_row()
            if last_cat is not None:
                console.print()
            icon = CAT_ICONS.get(cat, "·")
            cc = CAT_COLORS.get(cat, "#a78bfa")
            bar_len = max(0, cols * col_w - len(cat) - 4)
            console.print(
                f"{sp}[bold {cc}]{icon} {cat}[/] "
                f"[dim #312e81]{'─' * bar_len}[/]"
            )
            last_cat = cat

        name = MODULES[key][0]
        row_items.append((key, name))
        if len(row_items) >= cols:
            flush_row()

    flush_row()
    console.print()

    nav_left = f"[bold #6366f1]<[/] [dim]geri[/]" if page > 1 else "[dim #312e81]     [/]"
    nav_right = f"[dim]ileri[/] [bold #6366f1]>[/]" if page < tp else "[dim #312e81]      [/]"
    page_info = f"[bold #a5b4fc]═══ Sayfa {page}/{tp} ═══[/]"

    console.print(Align.center(f"{nav_left}  {page_info}  {nav_right}"))
    console.print()

    console.print(
        f"{sp}[dim #312e81]{'─' * (cols * col_w)}[/]"
    )
    console.print(
        f"{sp}  [dim #818cf8][[/][white]00[/][dim #818cf8]][/] Temizle"
        f"      [dim #818cf8][[/][white]99[/][dim #818cf8]][/] Cikis"
        f"      [bold #ef4444][[/][white] > [/][bold #ef4444]][/] C2"
    )
    console.print(
        f"{sp}[dim #312e81]{'─' * (cols * col_w)}[/]"
    )
    console.print()



def run_module(choice):
    if choice not in MODULES:
        console.print("[red]  Gecersiz secim.[/red]")
        return

    name, module_path = MODULES[choice]
    console.print()
    console.print(Align.center(gradient_bar(36)))
    console.print(Align.center(f"[bold white on #4338ca] (o) {name} [/]"))
    console.print(Align.center(gradient_bar(36)))

    try:
        module = __import__(module_path, fromlist=["run"])
        module.run()
    except ImportError as e:
        console.print(f"[red]  Modul yuklenemedi: {str(e).replace('[', chr(92)+'[')}[/red]")
        console.print("[dim #818cf8]  pip install -r requirements.txt[/]")
    except KeyboardInterrupt:
        console.print("\n[dim]  Iptal edildi.[/dim]")
    except Exception as e:
        console.print(f"[red]  Hata: {str(e).replace('[', chr(92)+'[')}[/red]")

    console.print(Align.center(gradient_bar(36)))



def c2_panel():
    c2_mods = {
        "1": ("C2 Shell",       "modules.c2_shell"),
        "2": ("VDS Manager",    "modules.vds_manager"),
        "3": ("DDoS Panel",     "modules.ddos_tool"),
        "4": ("SSH Manager",    "modules.ssh_manager"),
        "5": ("Keylogger Gen",  "modules.keylogger"),
        "6": ("Persistence",    "modules.persistence"),
        "7": ("Botnet C2",      "modules.botnet"),
    }

    while True:
        clear()
        console.print()
        for line in BANNER_ART:
            console.print(Align.center(f"[bold #ef4444]{line}[/]"))
        console.print()
        console.print(Align.center(gradient_bar(40)))
        console.print(Align.center(
            "[bold #ef4444](o)  C 2   C O N T R O L   P A N E L  (o)[/]"
        ))
        console.print(Align.center(gradient_bar(40)))
        console.print()

        w = tw()
        pad_l = max(0, (w - 52) // 2)
        sp = " " * pad_l

        console.print(f"{sp}[bold #ef4444]💀 EXPLOIT[/] [dim #312e81]{'─' * 41}[/]")
        console.print(
            f"{sp}  [bold #ef4444][1][/] C2 Shell"
            f"              [bold #ef4444][2][/] VDS Manager"
        )
        console.print(
            f"{sp}  [bold #ef4444][3][/] DDoS Panel"
            f"            [bold #ef4444][4][/] SSH Manager"
        )
        console.print(
            f"{sp}  [bold #ef4444][5][/] Keylogger Gen"
            f"         [bold #ef4444][6][/] Persistence"
        )
        console.print(f"{sp}  [bold #ef4444][7][/] Botnet C2")
        console.print()
        console.print(f"{sp}[dim #312e81]{'─' * 52}[/]")
        console.print(f"{sp}  [dim #818cf8][[/][white]0[/][dim #818cf8]][/] Ana menuye don")
        console.print(f"{sp}[dim #312e81]{'─' * 52}[/]")
        console.print()

        try:
            choice = console.input(
                "[bold #ef4444]  >> c2 [/][bold white]> [/]"
            ).strip()

            if choice == "0" or choice.lower() == "back":
                clear()
                break

            if choice in c2_mods:
                name, mod_path = c2_mods[choice]
                console.print()
                console.print(Align.center(gradient_bar(36)))
                console.print(Align.center(
                    f"[bold white on #6b1010] (o) {name} [/]"
                ))
                console.print(Align.center(gradient_bar(36)))

                try:
                    module = __import__(mod_path, fromlist=["run"])
                    module.run()
                except ImportError as e:
                    console.print(f"[red]  Modul yuklenemedi: {str(e).replace('[', chr(92)+'[')}[/red]")
                except KeyboardInterrupt:
                    console.print("\n[dim]  Iptal edildi.[/dim]")
                except Exception as e:
                    console.print(f"[red]  Hata: {str(e).replace('[', chr(92)+'[')}[/red]")

                console.print(Align.center(gradient_bar(36)))
                console.print("\n[dim]  Enter'a basin...[/dim]")
                input()
            else:
                console.print("[red]  Gecersiz secim.[/red]")
                time.sleep(0.5)

        except KeyboardInterrupt:
            clear()
            break
        except EOFError:
            break



def main():
    animated_intro()
    current_page = 1
    tp = total_pages()

    while True:
        clear()
        print_banner()
        print_menu(current_page)

        try:
            choice = console.input(
                "[bold #818cf8]  >> lunar [/][bold white]> [/]"
            ).strip()

            if choice == "99":
                console.print("\n[bold #818cf8]  Lunar kapaniyor...[/]")
                time.sleep(0.4)
                clear()
                break
            elif choice == "00":
                clear()
                continue
            elif choice == ">":
                if current_page < tp:
                    current_page += 1
                else:
                    c2_panel()
                continue
            elif choice == "<":
                current_page = max(1, current_page - 1)
                continue
            elif choice.isdigit():
                if len(choice) <= 2:
                    choice = choice.zfill(2)
                if choice in MODULES:
                    run_module(choice)
                    console.print("\n[dim]  Enter'a basin...[/dim]")
                    input()
                    clear()
                else:
                    console.print("[red]  Gecersiz secim.[/red]")
                    time.sleep(0.5)
                    clear()
            else:
                console.print("[red]  Gecersiz secim.[/red]")
                time.sleep(0.5)
                clear()

        except KeyboardInterrupt:
            console.print("\n\n[bold #818cf8]  Lunar kapaniyor...[/]")
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
