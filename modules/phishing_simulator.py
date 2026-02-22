import requests
import random
import string
import os
from rich.console import Console
console = Console()

def run():
    console.print("[#818cf8]  Phishing Simulator[/]")
    console.print("[dim]  Egitim amacli phishing sayfasi olusturur.[/]\n")
    template = console.input("[bold white]  Sablon: 1=Login, 2=Verify, 3=Custom: [/]").strip() or "1"
    title = console.input("[bold white]  Sayfa basligi (varsayilan 'Login'): [/]").strip() or "Login"
    webhook = console.input("[bold white]  Webhook URL (sonuclari almak icin): [/]").strip()

    templates = {
        "1": f'''<!DOCTYPE html><html><head><title>{title}</title>
<style>body{{font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;background:#1a1a2e;margin:0}}
.box{{background:#16213e;padding:40px;border-radius:10px;box-shadow:0 0 30px rgba(0,0,0,.3);width:350px}}
h2{{color:#e94560;text-align:center}}input{{width:100%;padding:12px;margin:8px 0;border:1px solid #333;border-radius:5px;background:#0f3460;color:#fff;box-sizing:border-box}}
button{{width:100%;padding:12px;background:#e94560;color:#fff;border:none;border-radius:5px;cursor:pointer;font-size:16px}}</style></head>
<body><div class="box"><h2>{title}</h2><form method="POST"><input name="email" placeholder="Email"><input name="password" type="password" placeholder="Password"><button>Login</button></form></div></body></html>''',
        "2": f'''<!DOCTYPE html><html><head><title>{title}</title>
<style>body{{font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;background:#0d1117;margin:0}}
.box{{background:#161b22;padding:40px;border-radius:10px;width:400px;text-align:center}}
h2{{color:#58a6ff}}p{{color:#8b949e}}input{{width:100%;padding:12px;margin:8px 0;border:1px solid #30363d;border-radius:5px;background:#0d1117;color:#fff;box-sizing:border-box}}
button{{width:100%;padding:12px;background:#238636;color:#fff;border:none;border-radius:5px;cursor:pointer}}</style></head>
<body><div class="box"><h2>Verify Your Account</h2><p>Please verify your identity</p><form method="POST"><input name="token" placeholder="Token"><button>Verify</button></form></div></body></html>''',
    }
    html = templates.get(template, templates["1"])

    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "phishing")
    os.makedirs(out_dir, exist_ok=True)
    fname = os.path.join(out_dir, f"page_{title.replace(' ', '_')}.html")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    console.print(f"[#818cf8]  Sayfa olusturuldu: output/phishing/{os.path.basename(fname)}[/]")
    console.print(f"[dim]  Webhook: {webhook or 'Girilmedi'}[/]")
