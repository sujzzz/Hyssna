"""Builds the Hyssna International static site.

Every page shares one header, flyout menu, floating "Talk to us" panel and
footer, so they are defined once here and written into each page. Run:

    python3 build.py

and the .html files are written to the repository root.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
PHONE = "+971 2 676 7525"
PHONE_HREF = "tel:+97126767525"
FAX = "+971 2 676 7526"
EMAIL = "info@hyssnauae.com"
ADDRESS = "New Sadaf Fashion Building, Mezzanine Floor, Office 06<br>Electra Road, P.O. Box 46641<br>Abu Dhabi, United Arab Emirates"
MAPS = "https://maps.app.goo.gl/vsJa6yL4E75g4B186"   # head office pin from the client
FILM_ID = "iToQFLRS8SY"   # company film on YouTube
FILM_START = 11           # seconds, from the link the client shared

_ARROW_SVG = '<svg viewBox="0 0 15 11" aria-hidden="true"><path d="M0 5.5h13M8.5 1l4.5 4.5L8.5 10"/></svg>'
ARROW = f'<span class="arr">{_ARROW_SVG}{_ARROW_SVG}</span>'
HOME_ICON = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5 1 7.2V15h5v-4.5h4V15h5V7.2z"/></svg>'

ICONS = {
    "check": "M5 12l5 5L20 7",
    "bank": "M3 10l9-6 9 6M5 10v8M9.7 10v8M14.3 10v8M19 10v8M3 21h18",
    "building": "M5 21V4h10v17M15 9h4v12M3 21h18M8.5 8h3M8.5 12h3M8.5 16h3",
    "pencil": "M4 20l4.5-1L19 8.5 15.5 5 5 15.5 4 20zM13.5 7l3.5 3.5",
    "cube": "M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3zM12 12l8-4.5M12 12v9M12 12L4 7.5",
    "shield": "M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3zM9 12l2 2 4-4",
    "users": "M9 11a3.5 3.5 0 100-7 3.5 3.5 0 000 7zM2.5 20c0-3.6 2.9-6.5 6.5-6.5s6.5 2.9 6.5 6.5M16 4.3a3.5 3.5 0 010 6.4M21.5 20c0-3-2-5.6-4.8-6.3",
    "calendar": "M4 6h16v14H4zM4 10h16M8 3v4M16 3v4",
    "box": "M3 7.5l9-4.5 9 4.5-9 4.5-9-4.5zM3 7.5v9l9 4.5 9-4.5v-9M12 12v9",
    "leaf": "M5 19C5 11 11 5 19 5c0 8-6 14-14 14zM5 19l7-7",
    "bolt": "M13 2L4 14h7l-1 8 9-12h-7l1-8z",
    "home": "M3 11l9-8 9 8M5 9.5V21h14V9.5M10 21v-6h4v6",
    "chart": "M4 20V11M10 20V5M16 20v-6M2 20h20",
    "health": "M4 21V5h16v16M12 9v6M9 12h6M2 21h20",
    "school": "M2 9l10-5 10 5-10 5L2 9zM6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5",
    "store": "M3 9l2-5h14l2 5M4 9v11h16V9M3 9h18M9 20v-6h6v6",
    "cup": "M4 8h13v5a6 6 0 01-6 6h-1a6 6 0 01-6-6V8zM17 10h2a2 2 0 010 4h-2",
    "factory": "M3 21V10l6 4v-4l6 4V5h6v16H3zM7 17h2M12 17h2",
    "ruler": "M3 17L17 3l4 4L7 21l-4-4zM7 13l2 2M10 10l2 2M13 7l2 2",
    "layers": "M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5M3 17l9 5 9-5",
    "light": "M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0012 3z",
    "globe": "M12 21a9 9 0 100-18 9 9 0 000 18zM3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z",
}

NAV = [
    ("what-we-do.html", "What we do", "adib-3", [
        ("fit-out.html", "Interior fit-out", "adib-2"),
        ("interior-design.html", "Interior design", "adnoc-4"),
        ("joinery.html", "Joinery manufacturing", "nbad-2"),
    ]),
    ("projects.html", "Projects", "enbd-1", []),
    ("about.html", "About", "adcb-1", []),
    ("team.html", "Our team", "adnoc-2", []),
    ("contact.html", "Contact", "fab-1", []),
]

PROJECTS = [
    {
        "slug": "adib", "client": "Abu Dhabi Islamic Bank", "short": "ADIB", "sector": "Banking",
        "title": "A branch network delivered across the UAE",
        "summary": "More than 25 branch fit-outs for ADIB, including Al Ain Al Qua'a, Sharjah Matajer and Baniyas.",
        "scope": ["Customer halls and teller counters", "Private banking suites", "ATM lobbies", "Bespoke joinery from our factory"],
        "location": "Across the UAE",
        "banner": "adib-5",
        "images": ["adib-2", "adib-4", "adib-1", "adib-5", "adib-3", "adib-6"],
        "body": [
            "Abu Dhabi Islamic Bank has trusted Hyssna with its branch network for years. Each branch follows the bank's design standards while adapting to a different building, footprint and community.",
            "Our factory produces the counters, wall panelling and feature joinery for every branch, so finishes stay consistent from Al Ain to Sharjah. Our planning team sequences each fit-out around the bank's opening dates.",
        ],
    },
    {
        "slug": "adcb", "client": "Abu Dhabi Commercial Bank", "short": "ADCB", "sector": "Banking",
        "title": "ADCB Excellency priority banking and Al Majlis",
        "summary": "A priority banking centre for ADCB Excellency, with relationship manager desks and a formal majlis.",
        "scope": ["Excellency reception and relationship desks", "Al Majlis guest lounge", "Feature wall cladding and timber fins", "Feature ceilings and lighting"],
        "location": "UAE",
        "images": ["adcb-1", "adcb-2", "adcb-3", "adcb-4"],
        "body": [
            "ADCB Excellency looks after the bank's priority clients, so every surface had to feel considered. Veined white wall cladding, vertical timber fins and slim linear lights give the centre a calm, premium character.",
            "The Al Majlis lounge offers a traditional welcome in a contemporary setting, with generous seating, a lectern and a layered feature ceiling.",
        ],
    },
    {
        "slug": "adnoc-digital-factory", "client": "ADNOC Upstream Digital Factory", "short": "ADNOC", "sector": "Energy",
        "title": "A control room for the Upstream Digital Factory",
        "summary": "An operations floor for ADNOC's Upstream Digital Factory, wrapped around a curved media wall.",
        "scope": ["Curved operator consoles", "Full-height media wall", "Feature ceilings and lighting", "Glazed meeting rooms"],
        "location": "Abu Dhabi",
        "images": ["adnoc-4", "adnoc-5", "adnoc-6"],
        "body": [
            "ADNOC's Upstream Digital Factory brings engineers and live data together in one room. Sweeping white consoles follow the curve of a full-height media wall, with lighting set into the ceiling and the console bases to match.",
            "Glass partitions keep the floor open while giving teams quiet places to meet.",
        ],
    },
    {
        "slug": "fab", "client": "First Abu Dhabi Bank", "short": "FAB", "sector": "Banking",
        "title": "A new-format branch built around the customer",
        "summary": "A contemporary FAB branch with a central lounge, glazed meeting pods and curved timber joinery.",
        "scope": ["Central customer lounge", "Glazed meeting pods", "Curved wall panelling and joinery", "Media walls and cove lighting"],
        "location": "UAE",
        "images": ["fab-1", "fab-3", "fab-2"],
        "body": [
            "FAB's new-format branch replaces rows of counters with a relaxed central lounge. Curved walls, warm timber and soft cove lighting lead customers from the entrance to the glazed meeting pods.",
            "Illuminated niches, built-in cabinets and numbered pods keep the space easy to find your way around, while the media wall carries the bank's brand.",
        ],
    },
    {
        "slug": "adnoc", "client": "ADNOC", "short": "ADNOC", "sector": "Energy",
        "title": "Workplace café and recreation floors",
        "summary": "Staff café, breakout and recreation spaces designed to bring people together.",
        "scope": ["Café and breakout areas", "Recreation and games floor", "Collaboration spaces", "Feature ceilings and lighting"],
        "location": "Abu Dhabi",
        "images": ["adnoc-2", "adnoc-1", "adnoc-3"],
        "body": [
            "For ADNOC we created social spaces that work hard for a large workforce: a bright café, a recreation floor and informal places to meet.",
            "Bold colour, durable finishes and carefully coordinated lighting and MEP services let the spaces handle heavy daily use while staying inviting.",
        ],
    },
    {
        "slug": "emirates-nbd", "client": "Emirates NBD", "short": "Emirates NBD", "sector": "Banking",
        "title": "A digital branch and refined meeting lounges",
        "summary": "A digital-first branch with interactive service zones, plus refined meeting lounges.",
        "scope": ["Digital service zones", "Meeting lounges", "Feature ceilings", "Glass partitions"],
        "location": "UAE",
        "images": ["enbd-1", "enbd-2"],
        "body": [
            "Emirates NBD's digital branch puts technology at the centre of the customer journey. We delivered the interactive zones, media walls and service counters that make it work.",
            "Alongside it, meeting lounges with sculpted lighting, timber floors and glass partitions give private conversations a calm setting.",
        ],
    },
    {
        "slug": "emirates-islamic", "client": "Emirates Islamic", "short": "Emirates Islamic", "sector": "Banking",
        "title": "An ATM lobby you can spot from the street",
        "summary": "A striking branded ATM lobby with illuminated feature walls.",
        "scope": ["ATM lobby", "Illuminated brand walls", "Shopfront and signage coordination"],
        "location": "UAE",
        "images": ["eib-1"],
        "body": [
            "Emirates Islamic wanted a lobby that is instantly recognisable from the street. Illuminated feature walls in the brand colour frame the ATMs and draw customers in, day or night.",
        ],
    },
    {
        "slug": "nbad", "client": "National Bank of Abu Dhabi", "short": "NBAD", "sector": "Banking",
        "title": "Branches, executive offices and lounges",
        "summary": "Branch fit-outs, executive offices and lounges with bespoke joinery.",
        "scope": ["ATM and customer areas", "Executive offices", "Lounges", "Bespoke desks and joinery"],
        "location": "Abu Dhabi",
        "images": ["nbad-3", "nbad-2", "nbad-1"],
        "body": [
            "For NBAD we delivered branches and executive areas that balance warmth and authority: timber floors, sculpted ceilings and bespoke desks made in our own factory.",
        ],
    },
]

CLIENTS = [
    ("adib", "Abu Dhabi Islamic Bank"), ("adnoc", "ADNOC"), ("fab", "First Abu Dhabi Bank"),
    ("emirates-nbd", "Emirates NBD"), ("emirates-islamic", "Emirates Islamic"), ("adcb", "ADCB"),
    ("mubadala", "Mubadala"), ("etihad", "Etihad Airways"), ("etisalat", "Etisalat"), ("du", "du"),
    ("emaar", "Emaar"), ("aldar", "Aldar"), ("dib", "Dubai Islamic Bank"), ("sib", "Sharjah Islamic Bank"),
    ("al-hilal", "Al Hilal Bank"), ("madame-coco", "Madame Coco"), ("adnic", "ADNIC"),
    ("nyuad", "NYU Abu Dhabi"), ("ad-airports", "Abu Dhabi Airports"), ("daman", "Daman"),
    ("emirates-insurance", "Emirates Insurance"), ("moi", "UAE Ministry of Interior"),
    ("unb", "Union National Bank"), ("tadweer", "Tadweer"), ("hct", "Higher Colleges of Technology"),
    ("dyncorp", "DynCorp International"), ("xerox", "Xerox"), ("oceaneering", "Oceaneering"),
]

GM = ("bassam-moussa", "Mr. Bassam Moussa", "General Manager")
GM_QUOTE = "Hyssna caters to understanding clients need &amp; addressing their need."
# the General Manager's message, as written on the current hyssnainternational.com
GM_MESSAGE = [
    "It is my pleasure to introduce Hyssna International LLC as a leading interior contracting and designing company in UAE. "
    "Over three decades, Hyssna has been providing a quality service to our customers who have been looking for a company "
    "that could provide excellent and competitive services.",
    "At Hyssna, we are committed to produce prominent and innovative interior design solutions especially for your working "
    "atmosphere. We are specialized in designing, planning and implementing of both domestic and commercial interiors. "
    "We enjoy good reputation for quality designs and high skills within your own budget and time scale.",
    "Hyssna is built a reputation for consistently achieving highly individual aesthetic results for a discerning local "
    "clientele. We place particular emphasis on understanding our clients\u2019 requirements prior to producing design "
    "solutions, which often surpass expectations. Our enthusiastic and experienced professionals, approach each project as "
    "a new challenge. We offer different style and innovative approach in our design concept and solutions.",
    "Hyssna has committed in completing each project to the highest standards, while taking on the challenge of capturing "
    "its unique individuality. We have extensive experience in materials and manufacturing techniques, both locally and "
    "internationally, and able to provide our clients with everything they aspire for, within the budget they choose.",
    "Hyssna offers you total solutions for Turnkey Projects under one roof. If you have an idea or concept you would like "
    "to discuss why not give us a call and see how we can start to play an active role to fulfill the design of your "
    "choice and liking.",
]

# departments and people, in the order of the Our Team page on the current site
TEAM = [
    ("admin", "Admin",
     "Experienced administrative management and a dedicated team, working in a fully computerised environment to support every project from start to completion.",
     [("nagesh", "Mr. Nagesh", "Admin Manager"), ("smitha-jobis", "Ms. Smitha Jobis", "Project Controller"),
      ("ahmed-suleiman", "Mr. Ahmed Suleiman", "PRO"), ("pauline", "Ms. Pauline", "Document Controller"),
      ("vittal", "Mr. Vittal", "Admin"), ("rica", "Ms. Rica", "Admin"),
      ("hanan", "Ms. Hanan", "Admin Assistant"), ("fatima", "Ms. Fatima", "Admin Assistant")]),
    ("finance", "Finance",
     "Experienced finance management, working alongside administration to give every project integrated management support.",
     [("ambili", "Ms. Ambili", "Senior Accountant"), ("diana", "Ms. Diana", "Accountant"), ("bindu", "Ms. Bindu", "Accountant")]),
    ("design", "Design",
     "Architects, interior designers and MEP designers with more than 35 years of collective experience, from 2D layouts to 3D perspectives and animation.",
     [("akbar", "Mr. Akbar", "Designer"), ("bivin", "Mr. Bivin", "Designer"),
      ("arbee", "Mr. Arbee", "Designer"), ("rommel", "Mr. Rommel", "MEP Designer")]),
    ("procurement", "Procurement",
     "Loose fittings, FF&amp;E, floor, wall and ceiling finishes and lighting, procured globally for each project in coordination with its project manager.",
     [("sain-basheer", "Mr. Sain Basheer", "Procurement Manager"), ("faye-salcedo", "Ms. Faye Salcedo", "Assistant Procurement")]),
    ("commercial", "Commercial",
     "Industry professionals with many years of experience across the interiors and construction sector, building strong and lasting partnerships.",
     [("sreenath", "Mr. Sreenath", "QA/QC Manager"), ("clyde", "Mr. Clyde", "QA/QC")]),
    ("planning", "Planning",
     "Contractual programmes built in Primavera P6 and tracked with earned value reports, to deliver every project on time and in budget.",
     [("robin-francisco", "Mr. Robin Francisco", "Planning Manager")]),
    ("projects", "Projects",
     "Your single point of contact on site, coordinating the programme, costs, approvals and every trade through to handover.",
     [("salas", "Mr. Salas", "Sr. Project Manager"), ("raja-guru", "Mr. Raja Guru", "Sr. MEP Manager"),
      ("abdallah", "Mr. Abdallah", "Project Manager"), ("suhil", "Mr. Suhil", "Site Engineer"),
      ("raj-kumar", "Mr. Raj Kumar", "Site Engineer"), ("nathaniel", "Mr. Nathaniel", "Site Engineer")]),
    ("hse", "HSE",
     "An occupational health and safety management system, with safe systems of work, safety checks and toolbox talks on every site.",
     [("dennis-mutasa", "Mr. Dennis Mutasa", "HSE Manager")]),
    ("factory", "Fit-out factory",
     "Our joinery division in Musaffah makes counters, cabinets, panelling, ceilings, wardrobes and wooden furniture for our projects.",
     [("hasan", "Mr. Hasan", "Joinery Manager")]),
]

PROCESS = [
    ("Briefing and site visit", "We meet you on site to understand the space, how it needs to work, the brand standards and the opening date."),
    ("Design", "Layouts, 3D perspectives and animations that bring the brief to life, with MEP design coordinated from the start."),
    ("Planning", "A contractual programme in Primavera P6, tracked with weekly and monthly earned value reports."),
    ("Procurement", "FF&amp;E, finishes and lighting sourced from around the world and checked for quality before they reach site."),
    ("Manufacture", "Counters, panelling and furniture made in our own joinery factory in Musaffah, Abu Dhabi."),
    ("Delivery and handover", "Project managers coordinate every trade on site, under a documented safety plan, through to snagging and handover."),
]


# ---------------------------------------------------------------- helpers

def img(name, alt="", lazy=True, folder="projects", cls=""):
    loading = ' loading="lazy"' if lazy else ""
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="assets/media/{folder}/{name}.jpg" alt="{escape(alt)}"{loading}>'


def media(name, alt="", plus=False, folder="projects", lazy=True):
    p = '<span class="plus" aria-hidden="true"></span>' if plus else ""
    return f'<div class="media">{img(name, alt, lazy, folder)}{p}</div>'


def btn(href, label, style="dark", extra=""):
    cls = f"btn btn-{style}" + (f" {extra}" if extra else "")
    return f'<a class="{cls}" href="{href}">{label} {ARROW}</a>'


def icon(name):
    return f'<span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="{ICONS[name]}"/></svg></span>'


def crumbs(items, light=False):
    lis = ['<li><a href="index.html" aria-label="Home">' + HOME_ICON + "</a></li>"]
    for i, (href, label) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{label}</li>')
        else:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
    cls = "crumbs light" if light else "crumbs"
    return f'<nav aria-label="Breadcrumb"><ol class="{cls}">{"".join(lis)}</ol></nav>'


def icon_list(items, cls=""):
    lis = "".join(f'<li>{icon(i)}<h3>{t}</h3><p>{d}</p></li>' for i, t, d in items)
    return f'<ul class="icons {cls}">{lis}</ul>'


def enquiry_form(prefix, title="Get in touch", heading_level=2):
    h = f'<h{heading_level}>{title}</h{heading_level}>'
    return f'''<form class="form" novalidate data-enquiry>
  {h}
  <div class="form-row">
    <div class="field"><label for="{prefix}-first">First name</label><input id="{prefix}-first" name="first" autocomplete="given-name" required><span class="error" id="{prefix}-first-err" hidden>Enter your first name.</span></div>
    <div class="field"><label for="{prefix}-last">Last name</label><input id="{prefix}-last" name="last" autocomplete="family-name"></div>
  </div>
  <div class="form-row">
    <div class="field"><label for="{prefix}-phone">Phone number <i>(optional)</i></label><input id="{prefix}-phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="{prefix}-email">Email</label><input id="{prefix}-email" name="email" type="email" autocomplete="email" required><span class="error" id="{prefix}-email-err" hidden>Enter an email address like name@company.com.</span></div>
  </div>
  <div class="field"><label for="{prefix}-type">Enquiry type</label>
    <select id="{prefix}-type" name="type"><option>Complete interior fit-out</option><option>Interior design</option><option>Joinery and furniture</option><option>Bank branch or ATM lobby</option><option>Careers</option><option>Something else</option></select></div>
  <div class="field"><label for="{prefix}-msg">Message</label><textarea id="{prefix}-msg" name="message" placeholder="Location, size, timeline and anything else we should know"></textarea></div>
  <div class="form-foot"><button class="btn btn-dark" type="submit">Send message {ARROW}</button><p class="form-status" role="status"></p></div>
</form>'''


def contact_grid():
    return f'''<div class="c-grid">
  <div><h3>Give us a call</h3><p><a class="u-red" href="{PHONE_HREF}">{PHONE}</a></p></div>
  <div><h3>Send us an email</h3><p><a class="u-red" href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <div><h3>Find us</h3><address>{ADDRESS}</address><p style="margin-top:14px"><a class="u-red" href="{MAPS}" target="_blank" rel="noopener">Get directions</a></p></div>
  <div><h3>Our joinery factory</h3><p>Musaffah, Abu Dhabi</p></div>
</div>'''


# ---------------------------------------------------------------- shared chrome

def header(active, light):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{l}</a></li>'
        for h, l, _, _ in NAV[:3]
    )
    fly = []
    for href, label, image, subs in NAV:
        cur = ' aria-current="page"' if href == active else ""
        sub = ""
        if subs:
            sub = '<ul class="fly-sub">' + "".join(
                f'<li><a href="{h}" data-image="assets/media/projects/{im}.jpg">{l}</a></li>' for h, l, im in subs) + "</ul>"
        fly.append(f'<li><a href="{href}" data-image="assets/media/projects/{image}.jpg"{cur}>{label}</a>{sub}</li>')
    cls = "site-header light" if light else "site-header"
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="{cls}">
  <div class="hdr">
    <div class="hdr-left">
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="flyout" data-menu-open><span></span></button>
      <ul class="hdr-links">{links}</ul>
    </div>
    <a class="hdr-logo" href="index.html" aria-label="Hyssna International, home">
      <img src="assets/media/logo-mark.svg" alt="" width="56" height="56">
    </a>
    <div class="hdr-right">{btn("contact.html", "Start your project", "dark", "hdr-cta")}</div>
  </div>
</header>
<div class="flyout" id="flyout" hidden role="dialog" aria-modal="true" aria-label="Menu" data-flyout>
  <button class="fly-close" type="button" data-menu-close><i aria-hidden="true"></i><span>Close</span></button>
  <div class="fly-main">
    <nav aria-label="Main"><ul class="fly-list">{"".join(fly)}</ul></nav>
    <div class="fly-extras">
      <a class="phone" href="{PHONE_HREF}">{PHONE}</a>
      <a class="u-red" href="mailto:{EMAIL}">{EMAIL}</a>
      {btn("contact.html", "Start your project")}
    </div>
  </div>
  <div class="fly-image"><img src="assets/media/projects/adib-3.jpg" alt="" data-fly-img></div>
</div>'''


def talk_panel():
    chat = '<svg class="chat" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4V5z"/></svg>'
    close = '<svg class="x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>'
    return f'''<button class="talk-fab" type="button" aria-expanded="false" aria-controls="talk" data-talk><span class="ic" aria-hidden="true">{chat}{close}</span><span data-talk-label>Talk to us</span></button>
<div class="talk-scrim" data-talk-close></div>
<section class="talk-sheet cream" id="talk" tabindex="-1" role="dialog" aria-modal="true" aria-labelledby="talk-title" data-talk-sheet>
  <div class="container">
    <div>
      <h2 id="talk-title">Ready to start your next project?</h2>
      <p>We have shaped interiors for the UAE's leading banks, energy companies and businesses since 1980. We would love to help create yours.</p>
      {contact_grid()}
    </div>
    <div class="form-card">{enquiry_form("t", "Tell us about your project", 3)}</div>
  </div>
</section>'''


def footer():
    nav = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l, _, _ in NAV)
    return f'''<footer class="site-footer">
  <div class="container">
    <h2>Ready to start your next project? <a class="u-red" href="contact.html">Talk to us</a></h2>
    <ul class="foot-nav">{nav}</ul>
    <div class="foot-info">
      <div><h3>Head office</h3><address>{ADDRESS}</address></div>
      <div><h3>Call us</h3><a href="{PHONE_HREF}">{PHONE}</a><br>Fax {FAX}</div>
      <div><h3>Email us</h3><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    </div>
    <div class="foot-base">
      <ul class="legal">
        <li>&copy; <span data-year>2026</span> Hyssna International L.L.C.</li>
        <li><a href="about.html#certifications">Certifications</a></li>
        <li><a href="about.html#hse">Health and safety</a></li>
      </ul>
      <ul class="badges" aria-label="Certifications">
        <li><b>ISO 9001</b>2015</li><li><b>ISO 14001</b>2015</li><li><b>ISO 45001</b>2018</li><li><b>USGBC</b>Member</li>
      </ul>
    </div>
  </div>
  <div class="foot-mark" aria-hidden="true">Hyssna</div>
</footer>'''


def page(filename, title, description, body, active, dark=True, light_header=True):
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="icon" href="assets/media/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body class="{"dark" if dark else "light"}">
{header(active, light_header)}
<main id="main">
{body}
</main>
{footer()}
{talk_panel()}
<dialog class="lightbox" id="lightbox" aria-labelledby="lb-title">
  <div class="lb-inner">
    <div class="lb-bar"><strong id="lb-title"></strong><button class="lb-close" type="button" data-close>Close</button></div>
    <img id="lb-img" alt="">
  </div>
</dialog>
<script src="assets/js/site.js"></script>
</body>
</html>
'''
    (ROOT / filename).write_text(html)
    return filename


# ---------------------------------------------------------------- sections

def intro(title, text, trail, image=None, alt=""):
    pic = f'<div class="media intro-media">{img(image, alt, lazy=False)}</div>' if image else ""
    return f'''<section class="intro">
  <div class="container">
    {crumbs(trail)}
    <div class="intro-copy"><h1>{title}</h1><p>{text}</p></div>
    {pic}
  </div>
</section>'''


def certs_block(panel_cls="", heading="Independently certified for quality, safety and the environment"):
    return f'''<section class="sec {panel_cls}" id="certifications" aria-labelledby="certs-title">
  <div class="container certs">
    <div class="reveal">
      <h2 id="certs-title">{heading}</h2>
      <p>Our management systems are certified for interior design implementation, electro-mechanical installation and maintenance, wallpaper fixing, false ceilings and light partitions. We are also a member of the U.S. Green Building Council.</p>
      <ul class="cert-badges">
        <li><b>ISO 9001:2015</b><span>Quality management</span></li>
        <li><b>ISO 14001:2015</b><span>Environmental management</span></li>
        <li><b>ISO 45001:2018</b><span>Occupational health and safety</span></li>
        <li><b>USGBC</b><span>Green building member</span></li>
      </ul>
    </div>
    <button class="cert-visual reveal" type="button" data-lightbox="assets/media/certificates.jpg" data-title="Hyssna International certificates">
      <span class="media"><img src="assets/media/certificates.jpg" alt="USGBC membership and ISO 14001, ISO 9001 and ISO 45001 certificates issued to Hyssna International LLC" loading="lazy"><span class="plus" aria-hidden="true"></span></span>
      <span class="cap">Select to view the certificates in full</span>
    </button>
  </div>
</section>'''


def service_cards():
    rows = [
        ("fit-out.html", "Interior fit-out", "adib-3", "Complete turnkey fit-out for offices, bank branches, retail and hospitality, with the associated MEP works."),
        ("interior-design.html", "Interior design", "adnoc-4", "Commercial, residential and institutional design, from 2D layouts and 3D visuals to furniture and exhibition design."),
        ("joinery.html", "Joinery manufacturing", "adcb-1", "Custom joinery and furniture made in our own factory in Musaffah, finished to the drawings and installed by our teams."),
    ]
    cards = "".join(
        f'<a class="card reveal" href="{h}">{media(im, "", plus=True)}<h3><span>{t}</span></h3><p>{d}</p></a>'
        for h, t, im, d in rows)
    return f'<div class="cards-3">{cards}</div>'


def project_card(p):
    return f'''<a class="pcard reveal" href="project-{p["slug"]}.html">
  {media(p["images"][0], p["client"] + " interior by Hyssna", plus=True)}
  <h3>{p["title"]}</h3>
  <p class="meta"><b>{p["short"]}</b>{p["location"]}</p>
</a>'''


def projects_panel(title, text, items, button=True):
    b = btn("projects.html", "All projects", "light") if button else ""
    return f'''<section class="sec dark panel" aria-labelledby="pp-title">
  <div class="container proj-grid">
    <div class="proj-intro reveal"><h2 id="pp-title">{title}</h2><p>{text}</p>{b}</div>
    {"".join(project_card(p) for p in items)}
  </div>
</section>'''


def clients_block(panel_cls="", title="Trusted by the organisations that shape the UAE"):
    lis = "".join(f'<li><img src="assets/media/clients/{s}.jpg" alt="{escape(n)}" loading="lazy"></li>' for s, n in CLIENTS)
    return f'''<section class="sec {panel_cls}" aria-labelledby="clients-title">
  <div class="container">
    <div class="sec-title reveal"><h2 id="clients-title">{title}</h2><p>Banks, government entities and global companies return to Hyssna for project after project.</p></div>
    <ul class="logos reveal">{lis}</ul>
  </div>
</section>'''


def process_block(panel_cls="cream panel", title="How we deliver, from first visit to handover"):
    lis = "".join(f"<li><div><h3>{t}</h3><p>{d}</p></div></li>" for t, d in PROCESS)
    return f'''<section class="sec {panel_cls}" aria-labelledby="process-title">
  <div class="container">
    <div class="sec-title reveal"><h2 id="process-title">{title}</h2><p>One team plans and controls every stage, so you deal with a single point of responsibility.</p></div>
    <ol class="process reveal">{lis}</ol>
  </div>
</section>'''


def film_block():
    """Company film from YouTube. site.js plays it muted when it scrolls into view and
    loops it before the end, so YouTube's end screen of other videos never appears."""
    watch = f"https://www.youtube.com/watch?v={FILM_ID}&amp;t={FILM_START}s"
    return f'''<section class="sec tight" aria-labelledby="film-title">
  <div class="container">
    <div class="film-head reveal">
      <h2 id="film-title">See our work in motion</h2>
      <p>A closer look at Hyssna International and the interiors we create for clients across the UAE.</p>
    </div>
    <div class="film reveal" data-film="{FILM_ID}" data-start="{FILM_START}">
      <div class="film-frame"><div id="film-player"></div></div>
      {img("adib-5", "", folder="projects", cls="film-poster")}
      <a class="film-big" href="{watch}" target="_blank" rel="noopener" data-film-big>
        <span class="film-big-icon" aria-hidden="true"><svg viewBox="0 0 12 12"><path d="M3 1.5l7.5 4.5L3 10.5z"/></svg></span>
        <span data-film-big-label>Watch on YouTube</span>
      </a>
      <div class="film-controls">
        <button class="video-toggle" type="button" data-film-play aria-pressed="false">
          <svg viewBox="0 0 12 12" aria-hidden="true"><rect x="2" y="1" width="3" height="10"/><rect x="7" y="1" width="3" height="10"/></svg>
          <span>Pause</span>
        </button>
        <button class="video-toggle" type="button" data-film-sound aria-pressed="false">
          <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M1 4h2.5L7 1v10L3.5 8H1z"/></svg>
          <span>Sound on</span>
        </button>
      </div>
    </div>
  </div>
</section>'''


def feature(image, title, text, href, label, alt=""):
    t = f"<p>{text}</p>" if text else ""
    return f'''<section class="feature" aria-label="{escape(title)}">
  {img(image, alt)}
  <div class="container reveal"><h2>{title}</h2>{t}{btn(href, label, "light")}</div>
</section>'''


# ---------------------------------------------------------------- pages

def home():
    body = f'''<section class="hero" aria-labelledby="hero-title">
  <video id="hero-video" autoplay muted loop playsinline preload="auto" poster="assets/media/hero-poster.jpg" aria-hidden="true">
    <source src="assets/media/hero.mp4" type="video/mp4">
  </video>
  <div class="hero-inner">
    <div class="hero-copy">
      <span class="kicker">Interior fit-out contractor, Abu Dhabi</span>
      <h1 id="hero-title">Crafting the UAE's interiors since 1980</h1>
      <p>Design, fit-out and joinery for banks, energy companies, government and business, delivered under one roof.</p>
      <div class="hero-actions">
        {btn("contact.html", "Start your project", "red")}
        <a class="btn btn-ghost" href="projects.html">View our projects</a>
      </div>
    </div>
    <div class="hero-foot">
      <ul>
        <li><b>40+ years</b>in UAE interiors</li>
        <li><b>25+</b>ADIB branches delivered</li>
        <li><b>In-house</b>joinery factory in Musaffah</li>
      </ul>
      <button class="video-toggle" type="button" data-video-toggle aria-pressed="false">
        <svg viewBox="0 0 12 12" aria-hidden="true"><rect x="2" y="1" width="3" height="10"/><rect x="7" y="1" width="3" height="10"/></svg>
        <span>Pause video</span>
      </button>
    </div>
  </div>
</section>
{certs_block()}
<section class="sec tight" aria-labelledby="services-title">
  <div class="container">
    <div class="sec-title reveal"><h2 id="services-title">Interior fit-out, interior design and joinery manufacturing, under one roof</h2></div>
    {service_cards()}
  </div>
</section>
{film_block()}
<section class="sec dark panel" aria-labelledby="usp-title">
  <div class="container">
    <div class="usp-intro reveal">
      <h2 id="usp-title">Delivering the finest interiors across the UAE since 1980</h2>
      <p>The UAE's leading banks, energy companies and government entities return to us for project after project. They trust us to deliver quality craftsmanship and a reliable service.</p>
      {btn("about.html", "About us", "light")}
    </div>
    <div class="cards-3">
      <div class="usp-card reveal">{media("adnoc-2")}<h3>Passionate people</h3><p>Architects, designers, engineers, planners and craftsmen who share strategies, knowledge and ideas across every department.</p></div>
      <div class="usp-card reveal">{media("nbad-2")}<h3>Our own factory</h3><p>Counters, panelling and furniture are made in our Musaffah joinery factory, so quality, finish and lead times stay in our hands.</p></div>
      <div class="usp-card reveal">{media("adib-3")}<h3>One point of responsibility</h3><p>Design, planning, procurement, manufacture, delivery and HSE under one roof, from the first layout to the final snag.</p></div>
    </div>
  </div>
</section>
<section class="sec" aria-labelledby="safety-title">
  <div class="container text-block">
    <h2 id="safety-title" class="reveal">Safety and quality, planned in from day one.</h2>
    <div class="reveal">
      <p>Every project has a documented safety plan. Subcontractors submit method statements and risk assessments for approval before work starts, and regular safety meetings, site checks and toolbox talks keep standards high.</p>
      <p>Our planning engineers build each programme in Primavera P6 and report progress weekly and monthly, so you always know where your project stands.</p>
      <p>It is why the UAE's most demanding clients trust us with their branches, headquarters and public spaces.</p>
      {btn("about.html#hse", "Our approach")}
    </div>
  </div>
</section>
{projects_panel("Interiors for the names the UAE banks on", "Discover some of our recent projects for the country's leading banks and energy companies.", PROJECTS)}
{clients_block()}
{feature("nbad-2", "Made to measure in our own joinery factory", "From reception counters to executive desks, every piece is built and checked in Musaffah before it reaches site.", "joinery.html", "Take a look", "Bespoke executive desk and joinery for NBAD")}'''
    return page("index.html", "Hyssna International | Interior Fit-Out, Design and Joinery in Abu Dhabi",
                "Hyssna International LLC is an Abu Dhabi interior fit-out, design and joinery company. Since 1980, trusted by the UAE's leading banks, energy and government clients.",
                body, "index.html", dark=False, light_header=True)


def what_we_do():
    signs = [
        ("fit-out.html", "Interior fit-out", "adib-3", "Complete turnkey fit-out for offices, bank branches, retail and hospitality."),
        ("interior-design.html", "Interior design", "adnoc-4", "Commercial, residential and institutional design, from 2D layouts to 3D animation."),
        ("joinery.html", "Joinery manufacturing", "adcb-1", "Bespoke counters, panelling and furniture made in our Musaffah factory."),
        ("projects.html", "Our projects", "fab-1", "Branches, workplaces and lounges for the UAE's leading organisations."),
    ]
    cards = "".join(
        f'<a class="sign" href="{h}">{img(im, "")}<div class="sign-copy"><h2>{t}</h2><p>{d}</p></div><span class="plus" aria-hidden="true"></span></a>'
        for h, t, im, d in signs)
    sectors = [
        ("bank", "Banking and finance", "Branches, ATM lobbies, private banking and head offices."),
        ("building", "Corporate offices", "Workplaces, boardrooms and collaboration floors."),
        ("bolt", "Energy and government", "Secure, durable interiors built to strict standards."),
        ("store", "Retail and malls", "Stores, showrooms and shopping centre interiors."),
        ("cup", "Hospitality", "Lounges, restaurants and guest spaces."),
        ("health", "Healthcare and education", "Hospitals, clinics and learning spaces."),
        ("home", "Residential and villas", "Homes, villa communities and residential towers."),
        ("factory", "Industrial and infrastructure", "Technical and large-scale facilities."),
    ]
    body = f'''{intro("Interior fit-out. Interior design. Precision joinery.", "Design-led fit-out and joinery for banks, offices, retail, hospitality and homes across the UAE, delivered by one team under one roof.", [("what-we-do.html", "What we do")])}
<section class="sec tight">
  <div class="container"><div class="signposts has-offset">{cards}</div></div>
</section>
<section class="sec" aria-labelledby="wwd-title">
  <div class="container text-block">
    <h2 id="wwd-title" class="reveal">Exceptional spaces, expertly delivered</h2>
    <div class="reveal">
      <p>At Hyssna, our in-house design, planning, procurement, factory, project and HSE departments work as one. That means a single point of responsibility for your interior, from the first layout to the final snag.</p>
      <p>We have delivered commercial and residential buildings, villa communities, hospitals, shopping malls, high-rise towers, infrastructure and industrial projects, and more than 25 branches for Abu Dhabi Islamic Bank alone.</p>
      <p>Because our own factory makes the joinery, programmes and quality stay under our control at every stage.</p>
    </div>
  </div>
</section>
{process_block()}
<section class="sec" aria-labelledby="sectors-title">
  <div class="container">
    <div class="sec-title reveal"><h2 id="sectors-title">Experience across every type of interior</h2></div>
    {icon_list(sectors)}
  </div>
</section>'''
    return page("what-we-do.html", "What we do | Hyssna International",
                "Interior fit-out, interior design and joinery manufacturing by Hyssna International in Abu Dhabi.", body, "what-we-do.html")


SERVICE_FAQ = {
    "fit-out.html": [
        ("Do you handle the MEP works as well?", "Yes. Our fit-outs include the associated mechanical, electrical and plumbing works, coordinated by our own MEP designers and project teams."),
        ("Can you fit out a bank branch to our brand standards?", "Yes. Bank branches are a particular strength. We have delivered more than 25 branches for Abu Dhabi Islamic Bank, along with work for Emirates NBD, Emirates Islamic, NBAD and Al Hilal Bank."),
        ("Where do you work?", "We are based in Abu Dhabi and deliver projects across the United Arab Emirates."),
        ("How do we get started?", "Call us on " + PHONE + " or send an enquiry. We will arrange a site visit and prepare a proposal."),
    ],
    "interior-design.html": [
        ("What design outputs can you provide?", "Space planning and 2D layouts, concept design, 3D perspectives and 3D animations, material and finish selections, and detailed drawings for construction."),
        ("Can you design and build?", "Yes. Our design team works alongside our fit-out and joinery departments, so the design you approve is the one we deliver."),
        ("Do you design furniture and exhibitions?", "Yes. We have completed furniture, exhibition and landscape design as well as commercial, residential and institutional interiors."),
        ("How do we get started?", "Send us your brief or call " + PHONE + " and our design team will arrange a meeting."),
    ],
    "joinery.html": [
        ("Where is your joinery made?", "In our own factory in Musaffah, Abu Dhabi, where every piece is checked before it reaches site."),
        ("Which materials do you work with?", "Engineered wood, laminated MDF, vinyl and veneer, finished to the architect's or designer's drawings."),
        ("Do you supply joinery to other contractors?", "Yes. We work closely with architects, interior designers and contractors on offices and homes across the UAE."),
        ("Do you install what you make?", "Yes. Our own teams install the joinery and coordinate with the other trades on site."),
    ],
}


def service_page(filename, title, intro_text, image, heading, paragraphs, items_title, items, gallery, related):
    paras = "".join(f"<p>{p}</p>" for p in paragraphs)
    icon_names = ["check", "layers", "ruler", "light", "cube", "pencil", "bolt", "box"]
    item_list = icon_list([(icon_names[i % len(icon_names)], t, d) for i, (t, d) in enumerate(items)])
    gal = "".join(
        f'<button type="button" data-lightbox="assets/media/projects/{g}.jpg" data-title="{escape(title)}">{media(g, title + " by Hyssna")}</button>'
        for g in gallery)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in SERVICE_FAQ[filename])
    rel = [p for p in PROJECTS if p["slug"] in related]
    body = f'''{intro(title, intro_text, [("what-we-do.html", "What we do"), (filename, title)], image, title)}
<section class="sec tight" aria-labelledby="svc-title">
  <div class="container text-block">
    <h2 id="svc-title" class="reveal">{heading}</h2>
    <div class="reveal">{paras}</div>
  </div>
</section>
<section class="sec cream-2 panel" aria-labelledby="items-title">
  <div class="container">
    <div class="sec-title reveal"><h2 id="items-title">{items_title}</h2></div>
    {item_list}
  </div>
</section>
<section class="sec" aria-labelledby="gal-title">
  <div class="container">
    <div class="sec-title reveal"><h2 id="gal-title">Selected work</h2></div>
    <div class="gallery lead-big reveal">{gal}</div>
  </div>
</section>
{projects_panel(title + " projects", "A selection of projects where this service played a leading part.", rel)}
{process_block("", "Our process, from first visit to handover")}
<section class="sec cream-2 panel" aria-labelledby="faq-title">
  <div class="container faq">
    <div class="reveal"><h2 id="faq-title">Frequently asked questions</h2><p>If you cannot find the answer to your question, email us at <a class="u-red" href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
    <div class="reveal">{faq}</div>
  </div>
</section>'''
    return page(filename, f"{title} | Hyssna International", intro_text, body, "what-we-do.html", dark=False, light_header=False)


def projects_page():
    cards = "".join(
        f'''<a class="sign" href="project-{p["slug"]}.html">{img(p["images"][0], p["client"] + " interior by Hyssna")}<div class="sign-copy"><span class="kick">{p["sector"]} | {p["location"]}</span><h2>{p["client"]}</h2><p>{p["summary"]}</p></div><span class="plus" aria-hidden="true"></span></a>'''
        for p in PROJECTS)
    body = f'''{intro("Built in Abu Dhabi. Trusted across the UAE.", "Branch networks, headquarters and workplaces for the UAE's leading banks, energy companies and businesses.", [("projects.html", "Projects")])}
<section class="sec tight">
  <div class="container"><div class="signposts has-offset">{cards}</div></div>
</section>
<section class="sec" aria-labelledby="cap-title">
  <div class="container text-block">
    <h2 id="cap-title" class="reveal">Our capability and experience offer a local focus with a proven track record</h2>
    <div class="reveal">
      <p>With a skilled team of designers, engineers, craftsmen and project managers, Hyssna delivers full-service interior fit-out and bespoke joinery across the UAE. From concept to completion, we turn briefs into spaces that perform.</p>
      <p>Our experience spans bank branches and ATM lobbies, corporate headquarters, staff amenities, executive offices and lounges, each tailored to the client's brand standards and operational needs. We have also worked for Al Hilal Bank, Madame Coco, Arabian Nights Village and many more.</p>
    </div>
  </div>
</section>
<section class="sec tight" aria-label="Key figures">
  <div class="container">
    <ul class="figures reveal">
      <li><b>1980</b><span>Founded in Abu Dhabi</span></li>
      <li><b>25<sup>+</sup></b><span>ADIB branches across the UAE</span></li>
      <li><b>35<sup>+</sup></b><span>Years of collective design experience</span></li>
      <li><b>3</b><span>ISO certified management systems</span></li>
    </ul>
  </div>
</section>
{clients_block("cream panel", "Clients we have worked with")}'''
    return page("projects.html", "Projects | Hyssna International",
                "Interior fit-out projects by Hyssna International for ADIB, ADCB, ADNOC, FAB, Emirates NBD, Emirates Islamic and NBAD.", body, "projects.html")


def project_page(i, p):
    others = [PROJECTS[(i + k) % len(PROJECTS)] for k in (1, 2)]
    paras = "".join(f"<p>{t}</p>" for t in p["body"])
    scope = "".join(f"<li>{s}</li>" for s in p["scope"])
    scope_dd = "".join(f"<span>{s}</span>" for s in p["scope"])
    imgs = p["images"]
    big = f'<section class="sec tight"><div class="container"><div class="img-block reveal">{img(imgs[1], p["client"] + " interior by Hyssna")}</div></div></section>' if len(imgs) > 1 else ""
    pair = ""
    if len(imgs) > 2:
        pair = f'<section class="sec tight"><div class="container img-2">{media(imgs[2], p["client"] + " interior detail")}{media(imgs[0], p["client"] + " interior")}</div></section>'
    gal = "".join(
        f'<button type="button" data-lightbox="assets/media/projects/{g}.jpg" data-title="{escape(p["client"])}">{media(g, p["client"] + " by Hyssna")}</button>'
        for g in imgs)
    body = f'''<section class="p-banner" aria-labelledby="p-title">
  {img(p.get("banner", imgs[0]), p["client"] + " interior by Hyssna", lazy=False)}
  <div class="container">
    {crumbs([("projects.html", "Projects"), ("project-" + p["slug"] + ".html", p["client"])], light=True)}
    <h1 id="p-title">{p["client"]}</h1>
    <p>{p["title"]}</p>
  </div>
</section>
<section class="sec">
  <div class="container key-info">
    <div class="reveal"><p class="lead">{p["summary"]}</p>{paras}</div>
    <dl class="facts reveal">
      <div><dt>Client</dt><dd>{p["client"]}</dd></div>
      <div><dt>Sector</dt><dd>{p["sector"]}</dd></div>
      <div><dt>Expertise</dt><dd>{scope_dd}</dd></div>
      <div><dt>Location</dt><dd>{p["location"]}</dd></div>
    </dl>
  </div>
</section>
{big}
<section class="sec" aria-labelledby="details-title">
  <div class="container text-block">
    <h2 id="details-title" class="reveal">Fit-out details</h2>
    <div class="reveal"><p>Our teams delivered the complete interior, coordinating every trade from first fix to handover. The main elements of this project were:</p><ul class="bullets">{scope}</ul></div>
  </div>
</section>
{pair}
<section class="sec cream panel" aria-labelledby="gallery-title">
  <div class="container">
    <div class="sec-title reveal"><h2 id="gallery-title">Project gallery</h2></div>
    <div class="gallery reveal">{gal}</div>
    <div class="inline-cta reveal" style="margin-top:100px">
      <div><h2>Planning a similar space?</h2><p>Tell us about your project and our team will arrange a site visit.</p></div>
      {btn("contact.html", "Talk to us")}
    </div>
  </div>
</section>
{projects_panel("More projects", "Explore more of our work for the UAE's leading organisations.", others)}'''
    return page(f'project-{p["slug"]}.html', f'{p["client"]} | Projects | Hyssna International', p["summary"], body, "projects.html")


def about():
    body = f'''{intro("A heritage built on four decades of craft and integrity.", "We all work together to create beautiful, functional spaces for our clients.", [("about.html", "About")], "enbd-2", "Meeting lounge by Hyssna for Emirates NBD")}
<section class="sec tight" aria-labelledby="ab-title">
  <div class="container text-block">
    <h2 id="ab-title" class="reveal">Crafting interiors across the UAE since 1980.</h2>
    <div class="reveal">
      <p>For more than four decades, Hyssna International has designed, planned and delivered commercial and domestic interiors across the United Arab Emirates.</p>
      <p>Our team brings together architects, interior designers, graphic designers, fit-out specialists, civil, electrical and mechanical engineers, technicians and administration staff.</p>
    </div>
  </div>
</section>
<section class="sec tight">
  <div class="container cards-3">
    <div class="usp-card reveal">{media("adnoc-2")}<h3>Passionate people</h3><p>Our strength lies in teamwork: sharing strategies, knowledge and ideas across every department, with an open flow of communication and real team spirit.</p></div>
    <div class="usp-card reveal">{media("nbad-2")}<h3>In-house manufacturing</h3><p>Our Musaffah joinery factory gives us control over quality, finish and lead times on every counter, panel and piece of furniture.</p></div>
    <div class="usp-card reveal">{media("adib-1")}<h3>Respect and diversity</h3><p>We respect the culture and values of the UAE, and that is reflected in our company and the multinational workforce we employ.</p></div>
  </div>
</section>
<section class="sec cream panel" aria-labelledby="legacy-title">
  <div class="container">
    <div class="text-block reveal">
      <h2 id="legacy-title">A legacy of excellence and integrity</h2>
      <div>
        <p>From a single bank branch to programmes rolled out across the Emirates, we offer an A to Z solution: design, planning, procurement, our own joinery factory, site delivery and HSE, all under one roof.</p>
        <p>Banks, government entities and global companies return to us for project after project, because we take responsibility for every stage.</p>
      </div>
    </div>
    <div class="img-2 reveal" style="margin-top:80px">{media("adib-2", "ADIB branch by Hyssna")}{media("nbad-3", "NBAD lounge by Hyssna")}</div>
  </div>
</section>
<div class="sec">{feature("adib-3", "Precision joinery made in our own factory", "", "joinery.html", "Take a look", "ADIB ATM lobby by Hyssna")}</div>
<section class="sec tight" aria-labelledby="people-title">
  <div class="container text-media">
    {media("adcb-2", "Al Majlis lounge by Hyssna for ADCB Excellency")}
    <div class="reveal">
      <h2 id="people-title">Our success is driven by our team's skill and passion</h2>
      <p>People who can deliver work to the standards our clients demand are hard to find. When they share our passion, sense of purpose and pride in precise craftsmanship, we look after them.</p>
      {btn("team.html", "Meet the team", "light")}
    </div>
  </div>
</section>
<section class="sec cream panel gap-top" id="hse" aria-labelledby="hse-title">
  <div class="container text-block">
    <h2 id="hse-title" class="reveal">Safety is planned in from day one</h2>
    <div class="reveal">
      <p>Our occupational health and safety management system covers every employee and subcontractor, whether office based or on site. It is led by our HSE Manager, Mr. Dennis Mutasa.</p>
      <p>Each project has a documented safety plan. Subcontractors submit method statements and risk assessments for approval before work starts, and regular safety meetings, safety checks and toolbox talks keep standards high.</p>
      <p>Early planning, effective prevention and control, personal protective equipment, accident reporting and good record keeping are all part of our safety policy.</p>
    </div>
  </div>
</section>
<section class="sec" aria-label="Key figures">
  <div class="container">
    <ul class="figures reveal">
      <li><b>1980</b><span>Founded in Abu Dhabi</span></li>
      <li><b>25<sup>+</sup></b><span>ADIB branches across the UAE</span></li>
      <li><b>35<sup>+</sup></b><span>Years of collective design experience</span></li>
      <li><b>3</b><span>ISO certified management systems</span></li>
    </ul>
  </div>
</section>
{certs_block("cream panel", "We set ourselves high standards in all that we do")}'''
    return page("about.html", "About | Hyssna International",
                "About Hyssna International, an Abu Dhabi interior fit-out and design company founded in 1980.", body, "about.html")


def team():
    count = sum(len(d[3]) for d in TEAM)
    pills = [f'<button type="button" data-team-filter="all" aria-pressed="true">All<span>{count}</span></button>']
    groups = []
    for n, (key, name, text, people) in enumerate(TEAM, 1):
        pills.append(f'<button type="button" data-team-filter="{key}" aria-pressed="false">{name}<span>{len(people)}</span></button>')
        crew = "".join(
            f'<li><div class="crew-photo">{img(slug, f"{who}, {role}", folder="team")}</div><b>{who}</b><span>{role}</span></li>'
            for slug, who, role in people)
        groups.append(f'''<div class="dept reveal" data-dept="{key}">
      <div class="dept-head"><span class="dept-no">{n:02d}</span><h3>{name}</h3><p>{text}</p></div>
      <ul class="crew">{crew}</ul>
    </div>''')
    message = "".join(f"<p>{para}</p>" for para in GM_MESSAGE)
    slug, gm_name, gm_role = GM
    body = f'''{intro("The people behind the work.", f"{count} specialists across nine departments, led by our General Manager, {gm_name}.", [("team.html", "Our team")])}
<section class="sec cream panel gm" aria-labelledby="gm-title">
  <div class="container gm-grid">
    <div class="gm-side reveal">
      <div class="gm-photo">{img(slug, f"{gm_name}, {gm_role} of Hyssna International", lazy=False, folder="team")}</div>
      <p class="gm-name"><b>{gm_name}</b>{gm_role}</p>
    </div>
    <div class="gm-body">
      <span class="kicker reveal">A message from our General Manager</span>
      <h2 id="gm-title" class="gm-quote reveal">{GM_QUOTE}</h2>
      <div class="gm-text reveal">{message}</div>
      <p class="gm-sign reveal"><b>{gm_name}</b>{gm_role}, Hyssna International LLC</p>
    </div>
  </div>
</section>
<section class="sec team" aria-labelledby="meet-title">
  <div class="container">
    <div class="sec-title reveal"><h2 id="meet-title">Meet the team</h2><p>Nine departments under one roof, from the first design sketch to the last piece of joinery.</p></div>
    <div class="team-filter" role="group" aria-label="Show a department">{"".join(pills)}</div>
    <div class="depts" id="team-list">
    {"".join(groups)}
    </div>
  </div>
</section>'''
    return page("team.html", "Our team | Hyssna International",
                f"Meet {gm_name}, General Manager, and the {count} people across design, planning, procurement, projects, HSE and joinery at Hyssna International.",
                body, "team.html")


def contact():
    body = f'''{intro("We'd love to hear from you", "We contribute to beautiful, functional spaces for clients across the UAE. We would love to help create yours.", [("contact.html", "Contact")])}
<section class="sec tight">
  <div class="container contact-area">
    <div class="contact-info reveal">
      <h2>Reach out and bring your vision to life.</h2>
      <p>Our head office is on Electra Road in Abu Dhabi, and our joinery factory is in Musaffah, giving us easy access to projects across the Emirates.</p>
      {contact_grid()}
    </div>
    <div class="form-card reveal">{enquiry_form("c")}</div>
  </div>
</section>
<section class="map-card" aria-labelledby="visit-title">
  {img("contact-bg", "")}
  <div class="container reveal">
    <h2 id="visit-title">Visit our office on Electra Road</h2>
    <p>New Sadaf Fashion Building, Mezzanine Floor, Office 06, Electra Road, Abu Dhabi.</p>
    <a class="btn btn-light" href="{MAPS}" target="_blank" rel="noopener">Get directions {ARROW}</a>
  </div>
</section>'''
    return page("contact.html", "Contact | Hyssna International",
                "Contact Hyssna International in Abu Dhabi: +971 2 676 7525, info@hyssnauae.com.", body, "contact.html", dark=False, light_header=False)


def build():
    out = [home(), what_we_do()]
    out.append(service_page(
        "fit-out.html", "Interior fit-out",
        "Complete turnkey fit-out for offices, bank branches, retail and hospitality across the UAE.", "adib-2",
        "Fit-out solutions that perform",
        ["We deliver complete interiors, ready to open, with every trade coordinated by one team. From strip-out and partitions to ceilings, floors, finishes and the associated mechanical, electrical and plumbing works, our project teams manage the whole fit-out.",
         "Our planning engineers sequence every area in Primavera P6, and our own factory supplies the joinery, so programmes and quality stay under our control.",
         "Bank branches are a particular strength. We have fitted out more than 25 branches for Abu Dhabi Islamic Bank alone, along with work for Emirates NBD, Emirates Islamic, NBAD and Al Hilal Bank."],
        "What we deliver",
        [("Office and corporate fit-out", "Workplaces, boardrooms and collaboration floors."),
         ("Bank branches and ATM lobbies", "Customer halls, teller counters and private banking."),
         ("Partitions and false ceilings", "Glazed and solid partitions, doors and feature ceilings."),
         ("Lighting and feature walls", "Coordinated lighting, media walls and illuminated brand walls."),
         ("Retail and showrooms", "Stores, kiosks and shopping centre interiors."),
         ("Hospitality and lounges", "Cafés, lounges and guest spaces."),
         ("Associated MEP works", "Mechanical, electrical and plumbing, designed and installed."),
         ("Finishes", "Floors, wall finishes, wallpaper and decorative details.")],
        ["adib-4", "fab-1", "adcb-1", "eib-1", "enbd-1"], ["adib", "fab"]))
    out.append(service_page(
        "interior-design.html", "Interior design",
        "Commercial, residential and institutional interior design by a collaborative in-house team.", "adnoc-4",
        "Design that is built to be delivered",
        ["Our designers bring more than 35 years of collective experience to every brief. The team is infused with a collaborative spirit that produces competitive solutions for our clients, proving that the sum of the whole is greater than its parts.",
         "We have completed commercial, residential and institutional projects, exhibition and furniture design, and landscaping, delivering striking results for owners and stakeholders alike.",
         "Whether you need a 2D layout, a 3D perspective or a 3D animation, Hyssna is the right partner to bring your space to life."],
        "Design services",
        [("Space planning", "2D layouts that make every square metre work."),
         ("Concept design", "Mood, materials and identity that express your brand."),
         ("3D perspectives", "Photo-real visuals and animations before work starts."),
         ("MEP design", "Mechanical, electrical and plumbing coordinated from day one."),
         ("Furniture design", "Bespoke pieces made in our own factory."),
         ("Material selection", "Finishes and samples chosen with you."),
         ("Exhibition design", "Stands and displays that draw people in."),
         ("Landscape design", "Outdoor spaces that complete the picture.")],
        ["adnoc-4", "adcb-2", "adnoc-2", "fab-2", "enbd-2"], ["adnoc-digital-factory", "adcb"]))
    out.append(service_page(
        "joinery.html", "Joinery manufacturing",
        "Custom joinery and furniture made in our own factory in Musaffah, Abu Dhabi.", "nbad-2",
        "From conceptualisation to execution",
        ["Hyssna Joinery handles everything from conceptualisation to execution. Working closely with architects and interior designers, we manufacture custom joinery and furniture for offices and homes across the UAE.",
         "We work in engineered wood, laminated MDF, vinyl and veneer, and every piece is checked in the factory before it reaches site.",
         "Combining our office interiors expertise with our own joinery production is what has made Hyssna a top-quality fit-out company across the UAE."],
        "What we make",
        [("Reception counters", "Teller counters, service desks and reception points."),
         ("Wall panelling", "Wooden panels and cladding in veneer and laminate."),
         ("Decorative ceilings", "Feature ceilings and timber details."),
         ("Podiums and kiosks", "Display units for branches and retail."),
         ("Wardrobes and cabinets", "Storage built to fit."),
         ("Doors and windows", "Kitchen doors, windows and frames."),
         ("Handrails and blinds", "Handrails and decorative blinds."),
         ("Furniture", "Executive desks, LCD stands, skirting and loose furniture.")],
        ["nbad-2", "adcb-3", "fab-3", "adib-2", "nbad-1"], ["nbad", "adcb"]))
    out.append(projects_page())
    out += [project_page(i, p) for i, p in enumerate(PROJECTS)]
    out += [about(), team(), contact()]
    return out


if __name__ == "__main__":
    for f in build():
        print("wrote", f)
