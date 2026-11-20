"""Global mobile-first CSS, PWA tags, and reusable HTML components."""
from html import escape
import streamlit as st
import streamlit.components.v1 as components

CSS = """
<style>
:root{--b1:#0B2E59;--b2:#1E5AA8;--b3:#4A90E2;--b4:#DCEAFB;--b5:#F4F8FD;--ok:#2E9E6B;--warn:#F5A623}
[data-testid="stSidebar"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"]{display:none}
header[data-testid="stHeader"]{background:transparent}
.block-container{max-width:560px;padding:1rem 1rem 6.5rem 1rem}
html{font-size:17px}
h1,h2,h3{color:var(--b1);letter-spacing:-.01em}
.stButton>button,.stLinkButton>a,[data-testid="stFormSubmitButton"]>button{min-height:46px;border-radius:14px;font-weight:600;transition:transform .12s ease,box-shadow .12s ease}
.stButton>button:active{transform:scale(.97)}
.stButton>button[kind="primary"],.stLinkButton>a[kind="primary"]{background:linear-gradient(135deg,var(--b2),var(--b3));border:0;color:#fff}
.stTabs [data-baseweb="tab-list"]{overflow-x:auto;gap:.25rem}
.stTabs [data-baseweb="tab"]{min-height:44px;white-space:nowrap}
.sb-hero{background:linear-gradient(135deg,var(--b1),var(--b2) 60%,var(--b3));color:#fff;border-radius:22px;padding:1.1rem 1.2rem;margin-bottom:.9rem;animation:rise .5s ease both}
.sb-hero .eyebrow{font-size:.7rem;letter-spacing:.12em;opacity:.8}
.sb-hero h1{color:#fff;font-size:1.5rem;margin:.2rem 0}
.sb-hero p{margin:0;opacity:.92;font-size:.95rem}
.sb-card{background:#fff;border:1px solid var(--b4);border-radius:18px;padding:.9rem 1rem;margin:.4rem 0;box-shadow:0 2px 10px rgba(30,90,168,.08);animation:rise .4s ease both}
.sb-card h4{margin:0 0 .2rem 0;color:var(--b1)}
.sb-card p{margin:0;color:#35557f;font-size:.93rem}
.sb-mascot-row{display:flex;gap:.7rem;align-items:center;margin:.3rem 0 .8rem}
.sb-mascot{position:relative;flex:0 0 64px;width:64px;height:64px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 30% 25%,#8EC5FF,var(--b3) 55%,var(--b2));box-shadow:0 6px 14px rgba(30,90,168,.35);animation:float 3s ease-in-out infinite}
.sb-mascot:before,.sb-mascot:after{content:"";position:absolute;top:24px;width:9px;height:12px;border-radius:50%;background:#fff;animation:blink 4.5s infinite}
.sb-mascot:before{left:17px}.sb-mascot:after{right:17px}
.sb-mascot i{position:absolute;left:23px;top:40px;width:18px;height:9px;border-bottom:3px solid #fff;border-radius:0 0 18px 18px}
.sb-mascot.big{width:96px;height:96px;flex:0 0 96px;margin:0 auto}
.sb-mascot.big:before,.sb-mascot.big:after{top:36px;width:13px;height:18px}
.sb-mascot.big:before{left:26px}.sb-mascot.big:after{right:26px}
.sb-mascot.big i{left:34px;top:60px;width:28px;height:13px;border-bottom-width:4px}
.sb-bubble{background:#fff;border:1px solid var(--b4);border-radius:16px 16px 16px 4px;padding:.6rem .8rem;font-size:.92rem;color:var(--b1);box-shadow:0 2px 8px rgba(30,90,168,.08);animation:rise .5s ease both}
.sb-stepper{display:flex;gap:6px;margin:.4rem 0 .2rem}
.sb-step{flex:1;height:10px;border-radius:6px;background:var(--b4)}
.sb-step.seen{background:var(--b3)}.sb-step.done{background:var(--ok)}
.sb-step.now{background:var(--b2);box-shadow:0 0 0 3px rgba(30,90,168,.25);animation:pulse 1.6s infinite}
.sb-ring{--p:0;width:96px;height:96px;border-radius:50%;background:conic-gradient(var(--ok) calc(var(--p)*1%),var(--b4) 0);display:grid;place-items:center;flex:0 0 96px}
.sb-ring span{width:74px;height:74px;border-radius:50%;background:#fff;display:grid;place-items:center;font-weight:700;color:var(--b1);font-size:1.15rem}
.sb-stage-icon{font-size:2.4rem;animation:float 3s ease-in-out infinite;display:inline-block}
.sb-badges{display:flex;flex-wrap:wrap;gap:.4rem;margin:.3rem 0}
.sb-badge{padding:.3rem .6rem;border-radius:999px;font-size:.8rem;background:#fff;border:1px solid var(--b4);color:#7a8ea8}
.sb-badge.on{background:linear-gradient(135deg,#FFF3D1,#FFE29A);border-color:#F5C451;color:#6B4A00;font-weight:600;animation:pop .5s ease both}
.sb-note{background:#FFF7E6;border-left:4px solid var(--warn);border-radius:10px;padding:.55rem .75rem;font-size:.85rem;color:#5b4300;margin:.5rem 0}
.sb-term{background:linear-gradient(135deg,#E6F0FB,#fff);border:1px dashed var(--b3);border-radius:16px;padding:.8rem 1rem}
.sb-landing{position:relative;overflow:hidden;border-radius:28px;background:linear-gradient(160deg,#0B2E59,#1E5AA8 55%,#4A90E2);background-size:200% 200%;animation:drift 12s ease infinite;padding:1.6rem 1.2rem 1.2rem;text-align:center;color:#fff;margin-bottom:1rem}
.sb-landing h1{color:#fff;font-size:1.8rem;margin:.6rem 0 .3rem}
.sb-landing p{margin:.2rem auto;max-width:30ch;opacity:.95}
.sb-landing .l1,.sb-landing .l2,.sb-landing .l3{opacity:0;animation:rise .8s ease forwards}
.sb-landing .l1{animation-delay:.3s}.sb-landing .l2{animation-delay:.9s}.sb-landing .l3{animation-delay:1.5s}
.sb-wave{display:inline-block;font-size:2rem;transform-origin:70% 70%;animation:wave 2.4s ease-in-out infinite;animation-delay:1s}
.sb-bubbles span{position:absolute;bottom:-24px;left:var(--x);width:var(--s);height:var(--s);border-radius:50%;background:rgba(255,255,255,.22);animation:bubble 8s linear infinite;animation-delay:var(--d)}
.sb-bridge{position:relative;height:74px;margin-top:1.2rem}
.sb-bridge .arc{position:absolute;left:8%;right:8%;bottom:8px;height:50px;border:4px solid rgba(255,255,255,.85);border-bottom:0;border-radius:200px 200px 0 0}
.sb-bridge .deck{position:absolute;left:2%;right:2%;bottom:4px;height:4px;background:rgba(255,255,255,.9);border-radius:2px}
.sb-bridge .cellx{position:absolute;bottom:10px;left:2%;width:14px;height:14px;border-radius:50%;background:#BFE0FF;box-shadow:0 0 10px #8EC5FF;animation:cross 6s linear infinite,hop 6s ease-in-out infinite;animation-delay:var(--d)}
.sb-dots{display:flex;justify-content:center;gap:6px;margin:.2rem 0 .6rem}
.sb-dots b{width:9px;height:9px;border-radius:50%;background:var(--b4)}.sb-dots b.on{background:var(--b2);width:24px;border-radius:6px}
.st-key-bottomnav{position:fixed;left:0;right:0;bottom:0;z-index:999;background:rgba(255,255,255,.97);border-top:1px solid var(--b4);padding:.3rem .4rem calc(.3rem + env(safe-area-inset-bottom));box-shadow:0 -4px 16px rgba(11,46,89,.08)}
.st-key-bottomnav [data-testid="stHorizontalBlock"]{flex-wrap:nowrap;gap:.2rem;max-width:560px;margin:0 auto}
.st-key-bottomnav [data-testid="stColumn"]{min-width:0!important;flex:1 1 0!important}
.st-key-bottomnav .stButton>button{min-height:54px;padding:.1rem;font-size:.68rem;line-height:1.15;border:0;background:transparent;color:var(--b1)}
.st-key-bottomnav .stButton>button[kind="primary"]{background:var(--b4);color:var(--b2);background-image:none}
.st-key-bottomnav p{font-size:.68rem!important;line-height:1.2!important;margin:0}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes blink{0%,92%,100%{transform:scaleY(1)}96%{transform:scaleY(.1)}}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes pop{0%{transform:scale(.6)}70%{transform:scale(1.12)}100%{transform:scale(1)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 3px rgba(30,90,168,.25)}50%{box-shadow:0 0 0 6px rgba(30,90,168,.1)}}
@keyframes wave{0%,60%,100%{transform:rotate(0)}10%{transform:rotate(16deg)}20%{transform:rotate(-8deg)}30%{transform:rotate(16deg)}40%{transform:rotate(-4deg)}50%{transform:rotate(10deg)}}
@keyframes bubble{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(-420px);opacity:0}}
@keyframes drift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
@keyframes cross{from{left:2%}to{left:94%}}
@keyframes hop{0%,100%{margin-bottom:0}50%{margin-bottom:46px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.sb-landing .l1,.sb-landing .l2,.sb-landing .l3{opacity:1}}
@media (min-width:900px){.block-container{max-width:640px}}
</style>
"""

PWA_JS = """
<script>
const d = window.parent.document;
if (!d.querySelector('link[rel=manifest]')) {
  const add = (tag, attrs) => { const e = d.createElement(tag); Object.entries(attrs).forEach(([k,v]) => e.setAttribute(k,v)); d.head.appendChild(e); };
  add('link', {rel:'manifest', href:'/app/static/manifest.webmanifest'});
  add('link', {rel:'apple-touch-icon', href:'/app/static/icon-192.png'});
  add('meta', {name:'theme-color', content:'#1E5AA8'});
  add('meta', {name:'apple-mobile-web-app-capable', content:'yes'});
  add('meta', {name:'mobile-web-app-capable', content:'yes'});
  add('meta', {name:'apple-mobile-web-app-title', content:'StemBridge'});
}
</script>
"""

_BUBBLES = "".join(f'<span style="--x:{x}%;--s:{s}px;--d:{d}s"></span>'
                   for x, s, d in [(8, 14, 0), (22, 22, 2), (38, 10, 4), (55, 18, 1), (70, 12, 3), (84, 24, 5), (94, 10, 6)])
_CELLS = "".join(f'<span class="cellx" style="--d:{d}s"></span>' for d in (0, 2, 4))


def inject():
    st.markdown(CSS, unsafe_allow_html=True)
    components.html(PWA_JS, height=0)


def landing(title, line1, line2, step=None, steps=3):
    dots = ""
    if step is not None:
        dots = '<div class="sb-dots">' + "".join(f'<b class="{"on" if i == step else ""}"></b>' for i in range(steps)) + "</div>"
    st.markdown(
        f'<div class="sb-landing"><div class="sb-bubbles">{_BUBBLES}</div>'
        f'<div class="sb-wave">👋</div><div class="sb-mascot big"><i></i></div>'
        f'<h1 class="l1">{escape(title)}</h1><p class="l2">{escape(line1)}</p><p class="l3">{escape(line2)}</p>'
        f'<div class="sb-bridge"><div class="arc"></div><div class="deck"></div>{_CELLS}</div></div>{dots}',
        unsafe_allow_html=True)


def hero(title, subtitle, eyebrow="STEMBRIDGE"):
    st.markdown(f'<div class="sb-hero"><div class="eyebrow">{escape(eyebrow)}</div>'
                f'<h1>{escape(title)}</h1><p>{escape(subtitle)}</p></div>', unsafe_allow_html=True)


def mascot(message):
    st.markdown(f'<div class="sb-mascot-row"><div class="sb-mascot"><i></i></div>'
                f'<div class="sb-bubble">{escape(message)}</div></div>', unsafe_allow_html=True)


def note(text):
    st.markdown(f'<div class="sb-note">{escape(text)}</div>', unsafe_allow_html=True)


def ring(pct):
    st.markdown(f'<div class="sb-ring" style="--p:{int(pct)}"><span>{int(pct)}%</span></div>', unsafe_allow_html=True)


def stepper(total, now, seen, done):
    cells = []
    for i in range(total):
        cls = "done" if i in done else ("now" if i == now else ("seen" if i in seen else ""))
        cells.append(f'<div class="sb-step {cls}"></div>')
    st.markdown(f'<div class="sb-stepper">{"".join(cells)}</div>', unsafe_allow_html=True)


def badges(defs, earned_ids):
    html = "".join(
        f'<span class="sb-badge {"on" if b[0] in earned_ids else ""}" title="{escape(b[3])}">{b[1]} {escape(b[2])}</span>'
        for b in defs)
    st.markdown(f'<div class="sb-badges">{html}</div>', unsafe_allow_html=True)


def dots(step, steps=3):
    st.markdown('<div class="sb-dots">' + "".join(f'<b class="{"on" if i == step else ""}"></b>' for i in range(steps)) + "</div>",
                unsafe_allow_html=True)
