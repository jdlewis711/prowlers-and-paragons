import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import random
from datetime import datetime
from pathlib import Path

# ============================================================
# HERO CITY — PROWLERS & PARAGONS GM DASHBOARD
# ============================================================
#
# Standard-library only: tkinter + json + pathlib.
#
# Files created beside this script:
#   hero_city_data.json   -> campaign database
#   session log.txt       -> running session notes
#
# Run:
#   python hero_city_dashboard.py
# ============================================================

DATA_FILE = Path("hero_city_data.json")
SESSION_LOG = Path("session log.txt")


# ============================================================
# DEFAULT DATA
# ============================================================

DEFAULT_DATA = {
    "heroes": [
        {
            "name": "Sentinel",
            "aliases": ["The Sentinel", "Blue Guardian"],
            "powers": ["super strength", "flight", "enhanced durability"],
            "feats": ["Stopped a runaway armored truck downtown"],
            "affiliations": ["Independent"],
            "weaknesses": [],
            "civilian_identity": "Unknown",
            "reputation": "Generally admired",
            "sightings": [],
        },
        {
            "name": "Volt",
            "aliases": ["Voltage"],
            "powers": ["electricity manipulation", "electrical sensing"],
            "feats": ["Prevented a citywide blackout"],
            "affiliations": ["Independent"],
            "weaknesses": [],
            "civilian_identity": "Unknown",
            "reputation": "Generally positive",
            "sightings": [],
        },
        {
            "name": "Nightshade",
            "aliases": ["Shade"],
            "powers": ["shadow manipulation", "stealth", "enhanced agility"],
            "feats": ["Stopped a jewelry store robbery"],
            "affiliations": ["Unknown"],
            "weaknesses": [],
            "civilian_identity": "Unknown",
            "reputation": "Mysterious",
            "sightings": [],
        },
    ],
    "villains": [],
    "places": [
        {
            "name": "Downtown",
            "type": "District",
            "description": "The commercial heart of Hero City.",
            "tags": ["business", "skyscrapers", "crime"],
            "associated_people": [],
            "incidents": [],
        },
        {
            "name": "Old Harbor",
            "type": "Waterfront",
            "description": "Industrial docks, warehouses, bars, and shipping yards.",
            "tags": ["industrial", "waterfront", "smuggling"],
            "associated_people": [],
            "incidents": [],
        },
        {
            "name": "Hero City University",
            "type": "University",
            "description": "A major urban university campus.",
            "tags": ["students", "science", "research"],
            "associated_people": [],
            "incidents": [],
        },
        {
            "name": "Founders Park",
            "type": "Park",
            "description": "A massive public park in central Hero City.",
            "tags": ["park", "families", "events"],
            "associated_people": [],
            "incidents": [],
        },
        {
            "name": "Mercer Avenue",
            "type": "Street",
            "description": "A busy commercial avenue running through several neighborhoods.",
            "tags": ["shopping", "traffic", "restaurants"],
            "associated_people": [],
            "incidents": [],
        },
    ],
    "organizations": [
        {
            "name": "Hero City Police Department",
            "type": "Government",
            "description": "Municipal police department.",
            "members": [],
            "notes": "",
        },
        {
            "name": "Hero City University",
            "type": "University",
            "description": "Major research university.",
            "members": [],
            "notes": "",
        },
    ],
    "npcs": [
        {
            "name": "Maya Torres",
            "alias": "Pulse",
            "role": "Journalist / Influencer",
            "description": "Independent journalist with a reputation for being first to major superhero stories.",
            "relationships": [],
            "notes": "",
        },
    ],
    "social_users": [
        {
            "username": "Pulse",
            "display_name": "Maya Torres",
            "type": "journalist",
            "bio": "Independent journalist. Finger on the pulse of Hero City.",
            "weight": 8,
        },
        {
            "username": "CityWatchHC",
            "display_name": "Hero City Watch",
            "type": "news",
            "bio": "Local news, traffic, emergencies, and civic updates.",
            "weight": 4,
        },
        {
            "username": "HCFoodie",
            "display_name": "Sam Chen",
            "type": "local",
            "bio": "Food, neighborhoods, and trying not to get caught in superhuman fights.",
            "weight": 5,
        },
        {
            "username": "NightOwl92",
            "display_name": "Derek Miller",
            "type": "civilian",
            "bio": "Usually awake when the weird stuff happens.",
            "weight": 4,
        },
        {
            "username": "HeroFan4Life",
            "display_name": "Ashley Reed",
            "type": "fan",
            "bio": "I have opinions about every hero. Yes, including yours.",
            "weight": 5,
        },
        {
            "username": "HCTransit",
            "display_name": "Hero City Transit",
            "type": "official",
            "bio": "Service alerts for Hero City's public transportation system.",
            "weight": 3,
        },
        {
            "username": "OldTownLocal",
            "display_name": "Frank Delgado",
            "type": "local",
            "bio": "Third generation Hero City resident.",
            "weight": 3,
        },
        {
            "username": "ConspiracyCorner",
            "display_name": "TruthSeekerHC",
            "type": "conspiracy",
            "bio": "Asking the questions the heroes don't want you asking.",
            "weight": 2,
        },
        {
            "username": "HCScanner",
            "display_name": "ScannerRat",
            "type": "scanner",
            "bio": "Not affiliated with emergency services. Probably.",
            "weight": 4,
        },
    ],
    "posts": [],
}


LOCATION_TEMPLATES = [
    ("The Glass District", "District", "A wealthy neighborhood dominated by modern architecture.", ["wealth", "corporate", "nightlife"]),
    ("Blackstone Station", "Transit", "A major subway and commuter rail station.", ["transit", "crowds", "crime"]),
    ("Rook Street", "Street", "A narrow street known for pawn shops, bars, and unusual nightlife.", ["nightlife", "crime", "underground"]),
    ("Starlight Plaza", "Plaza", "A popular downtown gathering place surrounded by restaurants and shops.", ["tourism", "shopping", "events"]),
    ("Westbridge", "Neighborhood", "A dense residential neighborhood west of downtown.", ["residential", "families", "working-class"]),
    ("The Narrows", "Neighborhood", "A crowded waterfront district with a reputation for organized crime.", ["crime", "waterfront", "poverty"]),
    ("Mercy General Hospital", "Hospital", "One of Hero City's largest hospitals.", ["medical", "emergency", "heroes"]),
    ("Atlas Tower", "Building", "A 70-story corporate tower overlooking downtown.", ["corporate", "wealth", "technology"]),
    ("Hawthorne Bridge", "Bridge", "A major bridge connecting downtown with Westbridge.", ["traffic", "river", "infrastructure"]),
    ("Redline Subway", "Transit", "The city's oldest subway line.", ["transit", "underground", "crime"]),
]

HERO_TEMPLATES = [
    ("The Warden", ["Warden"], ["energy barriers", "enhanced strength"]),
    ("Mirage", ["The Mirage"], ["illusion generation", "disguise"]),
    ("Comet", ["Comet"], ["flight", "super speed", "energy projection"]),
    ("Ironclad", ["Ironclad"], ["super durability", "super strength"]),
    ("Specter", ["The Specter"], ["intangibility", "invisibility"]),
]

VILLAIN_TEMPLATES = [
    ("Blackout", ["The Blackout"], ["power absorption", "electrical disruption"]),
    ("Gravitas", ["Gravitas"], ["gravity manipulation"]),
    ("The Broker", ["Broker"], ["superhuman persuasion", "information networks"]),
    ("Razorwing", ["Razorwing"], ["flight", "energy blades"]),
    ("Morrow", ["Doctor Morrow"], ["biotechnology", "mutagenic science"]),
]

FEATS = [
    "Stopped a robbery before police arrived",
    "Rescued civilians from a collapsing building",
    "Prevented a major traffic accident",
    "Fought an unidentified superhuman in public",
    "Stopped an armed gang near a residential neighborhood",
    "Evacuated civilians during a superhuman incident",
    "Prevented a train derailment",
    "Destroyed a dangerous piece of supervillain technology",
    "Helped firefighters contain a major fire",
    "Interrupted a suspected weapons deal",
    "Protected civilians during a hostage situation",
    "Was seen fighting someone on a rooftop",
]

POST_TEMPLATES = {
    "sighting": [
        "Anyone else see {hero} near {place} tonight?",
        "Just saw {hero} heading toward {place}. Something is definitely happening.",
        "Possible {hero} sighting at {place}. Can anyone confirm?",
        "Okay, pretty sure that was {hero} flying over {place}.",
    ],
    "news": [
        "BREAKING: Reports of a superhuman incident near {place}.",
        "Emergency crews responding to an incident at {place}.",
        "Multiple witnesses reporting unusual activity around {place}.",
        "Police have closed several streets around {place}.",
    ],
    "fan": [
        "{hero} continues to prove why they're one of the best heroes in Hero City.",
        "I don't care what anyone says. {hero} is AWESOME.",
        "If {hero} is actually at {place}, somebody better get video.",
        "Hero City doesn't deserve {hero}.",
    ],
    "complaint": [
        "Can someone explain why {place} is closed AGAIN?",
        "Love living in Hero City. Nothing like hearing an explosion outside your window.",
        "Apparently superhuman property damage doesn't count as a parking violation.",
        "Would really appreciate it if superheroes stopped destroying {place}. Thanks.",
    ],
    "rumor": [
        "Hearing rumors that {hero} was involved in what happened at {place}.",
        "Friend of a friend says there were TWO heroes at {place}.",
        "Apparently {hero} wasn't alone at {place}.",
        "Something weird is going on at {place}. That's all I'm saying.",
    ],
    "pulse": [
        "I've spoken with three witnesses who independently described {hero} at {place}. Still trying to confirm what happened.",
        "NEW: Multiple sources tell me {hero} was seen at {place} shortly before the incident.",
        "I'm getting reports of unusual activity at {place}. If you're nearby, send me what you're seeing.",
        "I've been tracking reports of {hero} for the last few weeks. Tonight's sighting at {place} is the clearest one yet.",
        "People are asking whether {hero} is connected to the incident at {place}. At this point, that's unconfirmed.",
    ],
    "conspiracy": [
        "Funny how {hero} always shows up right after something happens at {place}.",
        "You're telling me nobody knows who {hero} really is?",
        "Something doesn't add up about {place}.",
        "Ask yourself who benefits from what happened at {place}.",
    ],
    "local": [
        "Anyone know if the businesses around {place} are still open?",
        "Had dinner near {place} and suddenly half the street was blocked off.",
        "Hero City really needs to figure out its superhuman insurance situation.",
        "Honestly, {place} was already weird BEFORE the superheroes showed up.",
    ],
    "scanner": [
        "Scanner traffic suggests units heading toward {place}.",
        "Hearing reports of a possible powered individual at {place}.",
        "Multiple emergency units moving toward {place}.",
        "Something big happening around {place}.",
    ],
}


# ============================================================
# DATA FUNCTIONS
# ============================================================

def fresh_data():
    return json.loads(json.dumps(DEFAULT_DATA))


def load_data():
    if not DATA_FILE.exists():
        return fresh_data()
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Add any new keys from later versions.
        defaults = fresh_data()
        for key, value in defaults.items():
            data.setdefault(key, value)
        return data
    except Exception:
        messagebox.showwarning(
            "Data Error",
            "Could not read hero_city_data.json. Starting with a fresh database."
        )
        return fresh_data()


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def weighted_user(data):
    users = data["social_users"]
    pool = []
    for user in users:
        pool.extend([user] * int(user.get("weight", 1)))
    return random.choice(pool)


def choose_person(data, include_villains=True):
    choices = []
    choices.extend([("hero", x) for x in data["heroes"]])
    if include_villains:
        choices.extend([("villain", x) for x in data["villains"]])
    return random.choice(choices) if choices else (None, None)


def choose_place(data):
    return random.choice(data["places"]) if data["places"] else None


def find_record(records, name):
    name = name.lower().strip()
    for record in records:
        if record.get("name", "").lower() == name:
            return record
    return None


# ============================================================
# SOCIAL FEED ENGINE
# ============================================================

def generate_post(data):
    user = weighted_user(data)
    _, person = choose_person(data)
    place = choose_place(data)

    if not person or not place:
        return None

    person_name = person["name"]
    place_name = place["name"]

    if user["username"] == "Pulse":
        category = "pulse"
    elif user["type"] == "fan":
        category = "fan"
    elif user["type"] == "conspiracy":
        category = "conspiracy"
    elif user["type"] == "scanner":
        category = "scanner"
    elif user["type"] == "news":
        category = "news"
    elif user["type"] == "local":
        category = random.choice(["local", "complaint"])
    else:
        category = random.choice(["sighting", "rumor", "local", "complaint"])

    text = random.choice(POST_TEMPLATES[category]).format(
        hero=person_name,
        place=place_name,
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    post = {
        "id": len(data["posts"]) + 1,
        "timestamp": now,
        "username": user["username"],
        "display_name": user["display_name"],
        "type": user["type"],
        "text": text,
        "person": person_name,
        "place": place_name,
        "category": category,
        "verified": user["username"] == "Pulse",
    }

    data["posts"].append(post)

    # Track sightings/incidents.
    if category in ("sighting", "pulse", "rumor", "scanner"):
        person.setdefault("sightings", []).append({
            "place": place_name,
            "timestamp": now,
            "source": user["username"],
            "confirmed": category == "pulse",
        })

        place.setdefault("incidents", []).append({
            "timestamp": now,
            "person": person_name,
            "source": user["username"],
            "description": text,
        })

    # Pulse occasionally turns a sighting into a recorded feat.
    if category == "pulse" and random.random() < 0.22:
        feat = random.choice(FEATS)
        if feat not in person.setdefault("feats", []):
            person["feats"].append(feat)
            post["database_update"] = feat

    return post


def generate_major_incident(data):
    _, person = choose_person(data)
    place = choose_place(data)

    if not person or not place:
        return []

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages = [
        f"Something just exploded near {place['name']}.",
        f"Police have blocked off {place['name']}.",
        f"People are running from {place['name']}.",
        f"I just saw {person['name']} near the scene.",
        f"Does anyone know what's happening at {place['name']}?",
        f"Emergency vehicles everywhere near {place['name']}.",
        f"Someone is fighting on top of a building near {place['name']}.",
        f"Power just went out around {place['name']}.",
    ]
    random.shuffle(messages)

    posts = []
    for message in messages[:random.randint(5, 7)]:
        user = weighted_user(data)
        post = {
            "id": len(data["posts"]) + 1,
            "timestamp": now,
            "username": user["username"],
            "display_name": user["display_name"],
            "type": user["type"],
            "text": message,
            "person": person["name"],
            "place": place["name"],
            "category": "major incident",
            "verified": user["username"] == "Pulse",
        }
        data["posts"].append(post)
        posts.append(post)

    person.setdefault("sightings", []).append({
        "place": place["name"],
        "timestamp": now,
        "source": "Major Incident",
        "confirmed": False,
    })

    place.setdefault("incidents", []).append({
        "timestamp": now,
        "person": person["name"],
        "source": "Major Incident",
        "description": f"Major incident involving possible {person['name']} activity.",
    })

    if random.random() < 0.7:
        feat = random.choice(FEATS)
        if feat not in person.setdefault("feats", []):
            person["feats"].append(feat)

    return posts


def introduce_hero(data):
    existing = {x["name"] for x in data["heroes"]}
    available = [x for x in HERO_TEMPLATES if x[0] not in existing]
    if not available:
        return None

    name, aliases, powers = random.choice(available)
    hero = {
        "name": name,
        "aliases": aliases,
        "powers": powers,
        "feats": [],
        "affiliations": ["Unknown"],
        "weaknesses": [],
        "civilian_identity": "Unknown",
        "reputation": "Unknown",
        "sightings": [],
    }
    data["heroes"].append(hero)
    return hero


def introduce_villain(data):
    existing = {x["name"] for x in data["villains"]}
    available = [x for x in VILLAIN_TEMPLATES if x[0] not in existing]
    if not available:
        return None

    name, aliases, powers = random.choice(available)
    villain = {
        "name": name,
        "aliases": aliases,
        "powers": powers,
        "feats": [],
        "affiliations": ["Unknown"],
        "weaknesses": [],
        "civilian_identity": "Unknown",
        "reputation": "Dangerous",
        "sightings": [],
        "crimes": [],
    }
    data["villains"].append(villain)
    return villain


def discover_place(data):
    existing = {x["name"] for x in data["places"]}
    available = [x for x in LOCATION_TEMPLATES if x[0] not in existing]
    if not available:
        return None

    name, kind, description, tags = random.choice(available)
    place = {
        "name": name,
        "type": kind,
        "description": description,
        "tags": tags,
        "associated_people": [],
        "incidents": [],
    }
    data["places"].append(place)
    return place


# ============================================================
# MAIN APPLICATION
# ============================================================

class HeroCityApp:
    BG = "#11151c"
    PANEL = "#1a2029"
    PANEL2 = "#202733"
    TEXT = "#e8edf2"
    MUTED = "#9aa6b2"
    ACCENT = "#4aa3ff"
    ACCENT2 = "#f0b429"
    DANGER = "#e35d6a"

    def __init__(self, root):
        self.root = root
        self.root.title("Hero City — Prowlers & Paragons GM Dashboard")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 650)

        self.data = load_data()
        self.current_page = "Social Feed"
        self.current_record = None

        self.configure_style()
        self.build_ui()
        self.show_page("Social Feed")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TButton",
            background=self.PANEL2,
            foreground=self.TEXT,
            padding=(12, 8),
            borderwidth=0,
        )
        style.map(
            "TButton",
            background=[("active", self.ACCENT)],
            foreground=[("active", "#ffffff")],
        )
        style.configure(
            "Treeview",
            background=self.PANEL,
            foreground=self.TEXT,
            fieldbackground=self.PANEL,
            rowheight=30,
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background=self.PANEL2,
            foreground=self.TEXT,
            padding=8,
        )
        style.map(
            "Treeview",
            background=[("selected", self.ACCENT)],
            foreground=[("selected", "#ffffff")],
        )

    def build_ui(self):
        self.root.configure(bg=self.BG)

        # ---------------- TOP BANNER ----------------
        banner = tk.Frame(self.root, bg="#0b0f14", height=70)
        banner.pack(fill="x", side="top")
        banner.pack_propagate(False)

        title = tk.Label(
            banner,
            text="HERO CITY",
            bg="#0b0f14",
            fg="#ffffff",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(side="left", padx=(22, 4))

        subtitle = tk.Label(
            banner,
            text="PROWLERS & PARAGONS • GM DASHBOARD",
            bg="#0b0f14",
            fg=self.MUTED,
            font=("Segoe UI", 9),
        )
        subtitle.pack(side="left", padx=8)

        nav = tk.Frame(banner, bg="#0b0f14")
        nav.pack(side="right", padx=15)

        buttons = [
            ("SOCIAL FEED", "Social Feed"),
            ("HEROES", "Heroes"),
            ("VILLAINS", "Villains"),
            ("PLACES", "Places"),
            ("SESSION NOTES", "Session Notes"),
        ]

        for label, page in buttons:
            b = tk.Button(
                nav,
                text=label,
                command=lambda p=page: self.show_page(p),
                bg="#18202a",
                fg=self.TEXT,
                activebackground=self.ACCENT,
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                padx=14,
                pady=11,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
            )
            b.pack(side="left", padx=3)

        # ---------------- MAIN AREA ----------------
        self.content = tk.Frame(self.root, bg=self.BG)
        self.content.pack(fill="both", expand=True)

        # ---------------- STATUS BAR ----------------
        self.status = tk.Label(
            self.root,
            text="Ready",
            bg="#0b0f14",
            fg=self.MUTED,
            anchor="w",
            padx=15,
            pady=5,
            font=("Segoe UI", 9),
        )
        self.status.pack(fill="x", side="bottom")

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def show_page(self, page):
        self.current_page = page
        self.clear_content()

        if page == "Social Feed":
            self.build_social_page()
        elif page == "Heroes":
            self.build_people_page("heroes", "HERO LEXICON")
        elif page == "Villains":
            self.build_people_page("villains", "VILLAIN DATABASE")
        elif page == "Places":
            self.build_places_page()
        elif page == "Session Notes":
            self.build_session_page()

        self.status.config(text=f"{page} • {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # ========================================================
    # SOCIAL FEED
    # ========================================================

    def build_social_page(self):
        left = tk.Frame(self.content, bg=self.BG)
        left.pack(side="left", fill="both", expand=True, padx=(18, 8), pady=18)

        right = tk.Frame(self.content, bg=self.PANEL, width=290)
        right.pack(side="right", fill="y", padx=(8, 18), pady=18)
        right.pack_propagate(False)

        header = tk.Frame(left, bg=self.BG)
        header.pack(fill="x", pady=(0, 10))

        tk.Label(
            header,
            text="LIVE HERO CITY FEED",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left")

        ttk.Button(
            header,
            text="Generate Post",
            command=self.add_generated_post,
        ).pack(side="right", padx=4)

        ttk.Button(
            header,
            text="Major Incident",
            command=self.add_major_incident,
        ).pack(side="right", padx=4)

        ttk.Button(
            header,
            text="Refresh",
            command=lambda: self.show_page("Social Feed"),
        ).pack(side="right", padx=4)

        self.feed_text = tk.Text(
            left,
            bg=self.PANEL,
            fg=self.TEXT,
            insertbackground="#ffffff",
            selectbackground=self.ACCENT,
            relief="flat",
            wrap="word",
            padx=18,
            pady=15,
            font=("Segoe UI", 10),
        )
        self.feed_text.pack(fill="both", expand=True)
        self.feed_text.configure(state="disabled")

        self.render_feed()

        self.make_panel_title(right, "CITY INTELLIGENCE")

        ttk.Button(
            right,
            text="Discover New Hero",
            command=self.add_hero,
        ).pack(fill="x", padx=18, pady=(10, 5))

        ttk.Button(
            right,
            text="Discover New Villain",
            command=self.add_villain,
        ).pack(fill="x", padx=18, pady=5)

        ttk.Button(
            right,
            text="Discover New Place",
            command=self.add_place,
        ).pack(fill="x", padx=18, pady=5)

        ttk.Button(
            right,
            text="Search Everything",
            command=self.search_everything,
        ).pack(fill="x", padx=18, pady=5)

        self.make_panel_title(right, "CAMPAIGN COUNTS")

        stats = (
            f"Heroes: {len(self.data['heroes'])}\n"
            f"Villains: {len(self.data['villains'])}\n"
            f"Places: {len(self.data['places'])}\n"
            f"NPCs: {len(self.data['npcs'])}\n"
            f"Organizations: {len(self.data['organizations'])}\n"
            f"Social posts: {len(self.data['posts'])}"
        )

        tk.Label(
            right,
            text=stats,
            bg=self.PANEL,
            fg=self.MUTED,
            justify="left",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=18, pady=8)

    def render_feed(self):
        self.feed_text.configure(state="normal")
        self.feed_text.delete("1.0", "end")

        for post in reversed(self.data["posts"][-100:]):
            verified = " ✓" if post.get("verified") else ""

            self.feed_text.insert(
                "end",
                f"@{post['username']}{verified}",
                ("username",),
            )
            self.feed_text.insert(
                "end",
                f"  {post['display_name']}  •  {post['timestamp']}\n",
                ("meta",),
            )
            self.feed_text.insert(
                "end",
                post["text"] + "\n",
            )

            if post.get("database_update"):
                self.feed_text.insert(
                    "end",
                    f"  [DATABASE UPDATE] {post['database_update']}\n",
                    ("update",),
                )

            self.feed_text.insert(
                "end",
                f"  #{post.get('category', '')}  •  {post.get('place', '')}\n\n",
                ("tag",),
            )

        self.feed_text.tag_configure(
            "username",
            foreground=self.ACCENT,
            font=("Segoe UI", 10, "bold"),
        )
        self.feed_text.tag_configure(
            "meta",
            foreground=self.MUTED,
        )
        self.feed_text.tag_configure(
            "update",
            foreground=self.ACCENT2,
        )
        self.feed_text.tag_configure(
            "tag",
            foreground="#6f7d8c",
            font=("Segoe UI", 9),
        )

        self.feed_text.configure(state="disabled")

    def add_generated_post(self):
        post = generate_post(self.data)
        if post:
            save_data(self.data)
            self.show_page("Social Feed")

    def add_major_incident(self):
        posts = generate_major_incident(self.data)
        if posts:
            save_data(self.data)
            self.show_page("Social Feed")

    # ========================================================
    # HEROES / VILLAINS
    # ========================================================

    def build_people_page(self, key, title):
        container = tk.Frame(self.content, bg=self.BG)
        container.pack(fill="both", expand=True, padx=18, pady=18)

        top = tk.Frame(container, bg=self.BG)
        top.pack(fill="x", pady=(0, 10))

        tk.Label(
            top,
            text=title,
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left")

        ttk.Button(
            top,
            text=f"Add {'Hero' if key == 'heroes' else 'Villain'}",
            command=self.manual_add_person,
        ).pack(side="right", padx=4)

        ttk.Button(
            top,
            text="Generate Random",
            command=(self.add_hero if key == "heroes" else self.add_villain),
        ).pack(side="right", padx=4)

        search_var = tk.StringVar()

        tk.Entry(
            top,
            textvariable=search_var,
            bg=self.PANEL,
            fg=self.TEXT,
            insertbackground="#ffffff",
            relief="flat",
            font=("Segoe UI", 10),
        ).pack(side="right", padx=8, ipadx=10, ipady=7)

        tk.Label(
            top,
            text="Search:",
            bg=self.BG,
            fg=self.MUTED,
        ).pack(side="right")

        tree_frame = tk.Frame(container, bg=self.PANEL)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=("name", "aliases", "powers", "affiliations", "reputation"),
            show="headings",
        )

        headings = {
            "name": "Name",
            "aliases": "Aliases",
            "powers": "Powers",
            "affiliations": "Affiliations",
            "reputation": "Reputation",
        }

        widths = {
            "name": 160,
            "aliases": 180,
            "powers": 320,
            "affiliations": 180,
            "reputation": 200,
        }

        for col in headings:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], anchor="w")

        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview,
        )
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        def populate(*_):
            for item in tree.get_children():
                tree.delete(item)

            query = search_var.get().lower()

            for record in self.data[key]:
                searchable = json.dumps(record).lower()
                if query and query not in searchable:
                    continue

                tree.insert(
                    "",
                    "end",
                    values=(
                        record.get("name", ""),
                        ", ".join(record.get("aliases", [])),
                        ", ".join(record.get("powers", [])),
                        ", ".join(record.get("affiliations", [])),
                        record.get("reputation", ""),
                    ),
                )

        search_var.trace_add("write", populate)
        populate()

        tree.bind(
            "<Double-1>",
            lambda event: self.open_person_record(key, tree),
        )

        tk.Label(
            container,
            text="Double-click a record to view/edit the full dossier.",
            bg=self.BG,
            fg=self.MUTED,
        ).pack(anchor="w", pady=(8, 0))

    def open_person_record(self, key, tree):
        selected = tree.selection()
        if not selected:
            return

        values = tree.item(selected[0], "values")
        if not values:
            return

        record = find_record(self.data[key], values[0])
        if not record:
            return

        self.person_editor(key, record)

    def person_editor(self, key, record):
        win = tk.Toplevel(self.root)
        win.title(f"{record['name']} — Dossier")
        win.geometry("700x650")
        win.configure(bg=self.BG)
        win.transient(self.root)

        fields = {}

        form = tk.Frame(win, bg=self.BG)
        form.pack(fill="both", expand=True, padx=20, pady=20)

        entries = [
            ("Name", "name"),
            ("Aliases (comma separated)", "aliases"),
            ("Powers (comma separated)", "powers"),
            ("Affiliations (comma separated)", "affiliations"),
            ("Weaknesses (comma separated)", "weaknesses"),
            ("Civilian Identity", "civilian_identity"),
            ("Public Reputation", "reputation"),
        ]

        for label, key_name in entries:
            tk.Label(
                form,
                text=label,
                bg=self.BG,
                fg=self.MUTED,
                anchor="w",
            ).pack(fill="x", pady=(7, 2))

            value = record.get(key_name, "")
            if isinstance(value, list):
                value = ", ".join(value)

            entry = tk.Entry(
                form,
                bg=self.PANEL,
                fg=self.TEXT,
                insertbackground="#ffffff",
                relief="flat",
            )
            entry.insert(0, value)
            entry.pack(fill="x", ipady=7)
            fields[key_name] = entry

        text_fields = [
            ("Known Feats", "feats"),
            ("Sightings", "sightings"),
        ]

        for label, key_name in text_fields:
            tk.Label(
                form,
                text=label,
                bg=self.BG,
                fg=self.MUTED,
                anchor="w",
            ).pack(fill="x", pady=(10, 2))

            text = tk.Text(
                form,
                height=5,
                bg=self.PANEL,
                fg=self.TEXT,
                insertbackground="#ffffff",
                relief="flat",
                wrap="word",
            )
            current = record.get(key_name, [])

            if key_name == "feats":
                text.insert("1.0", "\n".join(current))
            else:
                lines = []
                for item in current:
                    if isinstance(item, dict):
                        lines.append(
                            f"{item.get('timestamp', '')} — "
                            f"{item.get('place', '')} — "
                            f"{item.get('source', '')}"
                        )
                    else:
                        lines.append(str(item))
                text.insert("1.0", "\n".join(lines))

            text.pack(fill="both", expand=True)
            fields[key_name] = text

        def save():
            record["name"] = fields["name"].get().strip()
            for key_name in ["aliases", "powers", "affiliations", "weaknesses"]:
                record[key_name] = [
                    x.strip()
                    for x in fields[key_name].get().split(",")
                    if x.strip()
                ]

            record["civilian_identity"] = fields["civilian_identity"].get().strip()
            record["reputation"] = fields["reputation"].get().strip()

            record["feats"] = [
                x.strip()
                for x in fields["feats"].get("1.0", "end").splitlines()
                if x.strip()
            ]

            save_data(self.data)
            win.destroy()
            self.show_page("Heroes" if key == "heroes" else "Villains")

        ttk.Button(
            form,
            text="Save Dossier",
            command=save,
        ).pack(anchor="e", pady=12)

    def manual_add_person(self):
        key = "heroes" if self.current_page == "Heroes" else "villains"
        kind = "Hero" if key == "heroes" else "Villain"

        name = simpledialog.askstring(
            f"New {kind}",
            f"{kind} name:",
            parent=self.root,
        )

        if not name:
            return

        powers = simpledialog.askstring(
            f"New {kind}",
            "Powers (comma separated):",
            parent=self.root,
        ) or ""

        record = {
            "name": name,
            "aliases": [],
            "powers": [x.strip() for x in powers.split(",") if x.strip()],
            "feats": [],
            "affiliations": ["Unknown"],
            "weaknesses": [],
            "civilian_identity": "Unknown",
            "reputation": "Unknown",
            "sightings": [],
        }

        if key == "villains":
            record["crimes"] = []

        self.data[key].append(record)
        save_data(self.data)
        self.show_page("Heroes" if key == "heroes" else "Villains")

    def add_hero(self):
        hero = introduce_hero(self.data)
        if hero:
            save_data(self.data)
            messagebox.showinfo(
                "New Hero",
                f"{hero['name']} has been added to the Hero Lexicon."
            )
            self.show_page("Heroes")
        else:
            messagebox.showinfo(
                "No New Hero",
                "The random hero template pool has been exhausted."
            )

    def add_villain(self):
        villain = introduce_villain(self.data)
        if villain:
            save_data(self.data)
            messagebox.showinfo(
                "New Villain",
                f"{villain['name']} has been added to the Villain Database."
            )
            self.show_page("Villains")
        else:
            messagebox.showinfo(
                "No New Villain",
                "The random villain template pool has been exhausted."
            )

    # ========================================================
    # PLACES
    # ========================================================

    def build_places_page(self):
        container = tk.Frame(self.content, bg=self.BG)
        container.pack(fill="both", expand=True, padx=18, pady=18)

        top = tk.Frame(container, bg=self.BG)
        top.pack(fill="x", pady=(0, 10))

        tk.Label(
            top,
            text="HERO CITY PLACES",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left")

        ttk.Button(
            top,
            text="Discover Place",
            command=self.add_place,
        ).pack(side="right")

        tree_frame = tk.Frame(container, bg=self.PANEL)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tree_frame,
            columns=("name", "type", "description", "tags", "incidents"),
            show="headings",
        )

        headings = {
            "name": "Place",
            "type": "Type",
            "description": "Description",
            "tags": "Tags",
            "incidents": "Incidents",
        }

        widths = {
            "name": 190,
            "type": 120,
            "description": 420,
            "tags": 230,
            "incidents": 100,
        }

        for col in headings:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], anchor="w")

        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview,
        )
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        for place in self.data["places"]:
            tree.insert(
                "",
                "end",
                values=(
                    place["name"],
                    place["type"],
                    place["description"],
                    ", ".join(place.get("tags", [])),
                    len(place.get("incidents", [])),
                ),
            )

        tree.bind(
            "<Double-1>",
            lambda event: self.open_place_record(tree),
        )

        tk.Label(
            container,
            text="Double-click a location to view its incident history.",
            bg=self.BG,
            fg=self.MUTED,
        ).pack(anchor="w", pady=(8, 0))

    def open_place_record(self, tree):
        selected = tree.selection()
        if not selected:
            return

        values = tree.item(selected[0], "values")
        if not values:
            return

        place = find_record(self.data["places"], values[0])
        if not place:
            return

        win = tk.Toplevel(self.root)
        win.title(f"{place['name']} — Location Dossier")
        win.geometry("700x600")
        win.configure(bg=self.BG)

        tk.Label(
            win,
            text=place["name"],
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", padx=20, pady=(20, 2))

        tk.Label(
            win,
            text=f"{place['type']}  •  {', '.join(place.get('tags', []))}",
            bg=self.BG,
            fg=self.MUTED,
        ).pack(anchor="w", padx=20)

        desc = tk.Text(
            win,
            height=5,
            bg=self.PANEL,
            fg=self.TEXT,
            insertbackground="#ffffff",
            relief="flat",
            wrap="word",
        )
        desc.insert("1.0", place["description"])
        desc.pack(fill="x", padx=20, pady=15)

        tk.Label(
            win,
            text="INCIDENT HISTORY",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=20)

        incidents = tk.Text(
            win,
            bg=self.PANEL,
            fg=self.TEXT,
            relief="flat",
            wrap="word",
        )
        incidents.pack(fill="both", expand=True, padx=20, pady=8)

        for incident in place.get("incidents", []):
            incidents.insert(
                "end",
                f"{incident.get('timestamp', '')}\n"
                f"{incident.get('description', '')}\n"
                f"Source: {incident.get('source', '')}\n\n"
            )

        def save():
            place["description"] = desc.get("1.0", "end").strip()
            save_data(self.data)
            win.destroy()
            self.show_page("Places")

        ttk.Button(
            win,
            text="Save Location",
            command=save,
        ).pack(anchor="e", padx=20, pady=12)

    def add_place(self):
        place = discover_place(self.data)
        if place:
            save_data(self.data)
            messagebox.showinfo(
                "New Place",
                f"{place['name']} has been added to Hero City."
            )
            self.show_page("Places")
        else:
            messagebox.showinfo(
                "No New Place",
                "The random location template pool has been exhausted."
            )

    # ========================================================
    # SESSION NOTES
    # ========================================================

    def build_session_page(self):
        container = tk.Frame(self.content, bg=self.BG)
        container.pack(fill="both", expand=True, padx=18, pady=18)

        top = tk.Frame(container, bg=self.BG)
        top.pack(fill="x", pady=(0, 10))

        tk.Label(
            top,
            text="SESSION NOTES",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left")

        ttk.Button(
            top,
            text="Save Session Log",
            command=self.save_session_notes,
        ).pack(side="right", padx=4)

        ttk.Button(
            top,
            text="New Session Header",
            command=self.insert_session_header,
        ).pack(side="right", padx=4)

        ttk.Button(
            top,
            text="Open Session Log",
            command=self.load_session_notes,
        ).pack(side="right", padx=4)

        self.notes = tk.Text(
            container,
            bg=self.PANEL,
            fg=self.TEXT,
            insertbackground="#ffffff",
            selectbackground=self.ACCENT,
            relief="flat",
            wrap="word",
            undo=True,
            padx=20,
            pady=18,
            font=("Consolas", 11),
        )
        self.notes.pack(fill="both", expand=True)

        self.load_session_notes()

        tk.Label(
            container,
            text=f"Saved to: {SESSION_LOG.resolve()}",
            bg=self.BG,
            fg=self.MUTED,
        ).pack(anchor="w", pady=(8, 0))

    def load_session_notes(self):
        if SESSION_LOG.exists():
            try:
                text = SESSION_LOG.read_text(encoding="utf-8")
                self.notes.delete("1.0", "end")
                self.notes.insert("1.0", text)
                self.status.config(text=f"Loaded {SESSION_LOG.name}")
            except Exception as exc:
                messagebox.showerror(
                    "Load Error",
                    str(exc),
                )
        else:
            self.notes.delete("1.0", "end")
            self.notes.insert(
                "1.0",
                f"# HERO CITY SESSION LOG\n"
                f"# Created {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            )

    def save_session_notes(self):
        try:
            text = self.notes.get("1.0", "end-1c")
            SESSION_LOG.write_text(text, encoding="utf-8")
            self.status.config(
                text=f"Saved session notes to {SESSION_LOG.name}"
            )
        except Exception as exc:
            messagebox.showerror(
                "Save Error",
                str(exc),
            )

    def insert_session_header(self):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        header = (
            "\n\n"
            + "=" * 70
            + f"\nSESSION — {stamp}\n"
            + "=" * 70
            + "\n\n"
        )
        self.notes.insert("insert", header)

    # ========================================================
    # SEARCH
    # ========================================================

    def search_everything(self):
        query = simpledialog.askstring(
            "Hero City Search",
            "Search heroes, villains, places, NPCs, organizations, and posts:",
            parent=self.root,
        )

        if not query:
            return

        q = query.lower()
        results = []

        for category in ["heroes", "villains", "places", "npcs", "organizations"]:
            for record in self.data.get(category, []):
                if q in json.dumps(record).lower():
                    results.append(
                        f"[{category.upper()}] "
                        f"{record.get('name', 'Unnamed')}"
                    )

        for post in self.data["posts"]:
            if q in post.get("text", "").lower():
                results.append(
                    f"[SOCIAL] @{post['username']}: {post['text']}"
                )

        win = tk.Toplevel(self.root)
        win.title(f"Search — {query}")
        win.geometry("800x550")
        win.configure(bg=self.BG)

        text = tk.Text(
            win,
            bg=self.PANEL,
            fg=self.TEXT,
            relief="flat",
            wrap="word",
            padx=18,
            pady=18,
        )
        text.pack(fill="both", expand=True, padx=15, pady=15)

        if results:
            text.insert("1.0", "\n\n".join(results))
        else:
            text.insert("1.0", "No results found.")

    # ========================================================
    # UI HELPERS
    # ========================================================

    def make_panel_title(self, parent, title):
        tk.Label(
            parent,
            text=title,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 5))

    def on_close(self):
        if self.current_page == "Session Notes":
            self.save_session_notes()
        save_data(self.data)
        self.root.destroy()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = HeroCityApp(root)
    root.mainloop()
