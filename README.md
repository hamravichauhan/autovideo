# ExtrovertNerd — 24/7 Autonomous Client Acquisition Engine & Laravel Agency Hub

> **A 100% Free, Autonomous B2B Client Acquisition Engine & High-Performance Agency Hub** engineered by **ExtrovertNerd**. Attract local business owners, startup founders, and entrepreneurs who need custom high-speed Laravel e-commerce stores, automated dashboards, and modern web applications—running on zero-cost cloud automation without paid LLM APIs or manual intervention.

---

## 🌟 Architecture & Full System Overview

```
                                 ┌─────────────────────────────────────────────────────────┐
                                 │       GitHub Actions (Zero-Cost Cloud Cron Engine)      │
                                 │            Daily Trigger @ 09:00 UTC / Manual           │
                                 └──────────────────────────┬──────────────────────────────┘
                                                            │
                 ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
                 ▼                                          ▼                                          ▼
   ┌───────────────────────────┐              ┌───────────────────────────┐              ┌───────────────────────────┐
   │  Programmatic SEO Engine  │              │  Headless Graphic Engine  │              │ Local Prospecting Bot     │
   │ (`src/generator_pseo.py`) │              │(`src/generator_graphics.py│              │(`src/prospecting_engine.py│
   │                           │              │                           │              │                           │
   │ • City/Niche Matrix       │              │ • Human Tactile Aesthetic │              │ • Local Directory Scraper │
   │ • 1500+ Word Case Studies │              │ • Multi-Platform Renders  │              │ • Audit Dossier Builder   │
   │ • WhatsApp Audit CTA Links│              │   - Instagram 4:5         │              │ • WhatsApp & Cold Email   │
   └─────────────┬─────────────┘              │   - Twitter/X 16:9        │              │   Outreach Pitch Scripts  │
                 │                            │   - Square 1:1            │              └─────────────┬─────────────┘
                 │                            └─────────────┬─────────────┘                            │
                 ▼                                          ▼                                          ▼
   ┌───────────────────────────┐              ┌───────────────────────────┐              ┌───────────────────────────┐
   │ Dynamic Case Study Engine │              │ Multi-Channel Publisher   │              │ Ready Outreach Drafts     │
   │ (`laravel-portfolio/`)    │              │ (`src/publisher.py`)      │              │ (`output/outreach_drafts`)│
   │ • Auto-Scans `output/`    │              │                           │              │ • 1-Click Send via WA/Mail│
   │ • Interactive /speed-check│              │ • Meta Graph Carousel Post│              │ • Demo Audit Previews     │
   │ • Dark Boutique UI        │              │ • Twitter/X Auto-Threads  │              └───────────────────────────┘
   └───────────────────────────┘              │ • Auto-Commit to Git Repo │
                                              └───────────────────────────┘
```

---

## 📁 Repository Structure

```
.
├── laravel-portfolio/                # Boutique ExtrovertNerd Agency Website & Admin Hub
│   ├── app/
│   │   ├── Http/Controllers/
│   │   │   ├── HomeController.php             # Agency Landing Page Controller
│   │   │   ├── SpeedCheckerController.php     # Interactive Speed Checker Micro-Tool
│   │   │   ├── BlogController.php             # Dynamic pSEO Markdown Case Studies
│   │   │   ├── AdminDashboardController.php   # Mission Control & Chart.js Telemetry
│   │   │   ├── AdminContentController.php     # pSEO Article & Topic Matrix Editor
│   │   │   ├── AdminSocialController.php      # Carousel Gallery & Publishing Queue
│   │   │   ├── AdminProspectsController.php   # Local Lead CRM & Pitch Generator
│   │   │   ├── AdminDocumentsController.php   # File Vault & Markdown Scratchpad
│   │   │   └── AdminSystemController.php      # 1-Click CLI Automation & Config Editor
│   │   └── Services/
│   │       ├── MarkdownService.php            # Pure PHP Frontmatter & Markdown Parser
│   │       ├── ViewRenderer.php               # Standalone Blade Template Compiler
│   │       └── Router.php                     # Zero-Dependency Parameterized Router
│   ├── bootstrap/
│   │   └── app.php                            # App Bootstrap & Autoloader
│   ├── public/
│   │   ├── index.php                          # HTTP Front Controller
│   │   └── output                             # Symlink to /output (serves graphics & assets)
│   ├── resources/views/
│   │   ├── layouts/
│   │   │   ├── app.blade.php                  # Public Boutique Dark Aesthetic (`bg-slate-950`)
│   │   │   └── admin.blade.php                # Admin Mission Control Navigation Layout
│   │   ├── admin/
│   │   │   ├── dashboard.blade.php            # Telemetry, Metric Cards & Chart.js Trajectory
│   │   │   ├── content/                       # Article Table, In-Browser Editor, Topic Matrix
│   │   │   ├── social/                        # Carousel Previews & Multi-Channel Copy Queue
│   │   │   ├── prospects/                     # Lead CRM Pipeline & Outreach Drawers
│   │   │   ├── documents/                     # Secure Upload Vault & Markdown Scratchpad
│   │   │   └── system/                        # 1-Click Python Triggers, .env Editor, Log Viewer
│   │   ├── home.blade.php                     # Public Landing Page
│   │   ├── speed-checker.blade.php            # 24/100 vs 100/100 Side-by-Side Diagnostic
│   │   └── blog/                              # Dynamic Case Study Views
│   ├── routes/web.php                         # Application & Admin Web Routes
│   ├── composer.json                          # Package Configuration
│   └── .env.example                           # Agency Environment Configuration
├── src/                              # Python Automation Engine
│   ├── config.py                              # Central Settings & ExtrovertNerd Brand Defaults
│   ├── generator_pseo.py                      # Programmatic SEO Case Study Builder
│   ├── generator_graphics.py                  # Playwright Multi-Platform Image Renderer
│   ├── prospecting_engine.py                  # Local Directory & Maps Outbound Prospecting Bot
│   ├── publisher.py                           # Social Media API Uploader & Caption Generator
│   └── main.py                                # Master CLI Orchestrator
├── content/
│   ├── blog_topics.json                       # Seed Database (Goa, Mumbai, Bangalore, Dubai, etc.)
│   └── social_templates.json                  # High-Converting Caption & Thread Formulas
├── templates/
│   ├── blog_template.md                       # Jinja2 pSEO Markdown Case Study Template
│   ├── carousel_slide.html                    # Human Tactile Slide Template (Sticky Notes, Stamps)
│   └── tech_tip.html                          # High-Contrast Code Snippet Card Template
├── output/
│   ├── blogs/                                 # Auto-Generated Case Studies (`*.md`)
│   ├── graphics/                              # Multi-Platform Slide PNGs (`instagram/`, `twitter/`)
│   ├── outreach_drafts.md                     # Ready-to-Send Cold WhatsApp & Email Pitches
│   ├── prospects.json                         # Prospect Dossiers & Simulated Audit Data
│   └── automation_log.json                    # Execution Logs & Performance Metrics
├── .github/workflows/
│   └── daily_automation.yml                   # 24/7 Cloud Cron Runner (GitHub Actions)
├── requirements.txt                           # Python Dependencies (Playwright, Requests, Jinja2)
└── README.md
```

---

## ⚡ Key Highlights & Innovations

### 1. Boutique Agency Website (`laravel-portfolio/`)
- **Theme:** Sleek dark-mode aesthetic (`bg-slate-950`), glowing borders, typography pairing **Plus Jakarta Sans** with **Playfair Display (Italic)**.
- **Studio Attribution:** Branded under **ExtrovertNerd** (`@extrovertnerd`).
- **Interactive Speed Checker Micro-Tool (`/speed-checker`):**
  - Prospect enters any URL (e.g., `luxurygoavillas.com`).
  - Generates an instant side-by-side performance teardown: failing mobile score (`24/100`, 6.2s load, $7,500/mo estimated leak) vs. ExtrovertNerd's verified (`100/100`, 0.32s load) custom Laravel architecture.
  - Generates pre-populated WhatsApp deep links (`wa.me/15551234567?text=...`) for instant 1-click lead capture.
- **Dynamic pSEO Blog Engine (`/blog`):**
  - Automatically scans `output/blogs/*.md` files, parses YAML frontmatter, and renders rich case studies without requiring a database.

### 2. Multi-Platform Human-Centric Graphics Engine
- **Non-AI, Authentic Human Aesthetic:**
  - Real textured yellow Post-it sticky notes with frosted tape and handwritten font (`Caveat`).
  - Rubber stamp badges (`FAILED BENCHMARK` in crimson vs. `VERIFIED 100/100` in emerald).
  - SVG circular speedometer gauges with color-coded performance tiers.
  - Perforated VIP boarding pass CTA card for Slide 4 conversions.
- **Multi-Platform Formats:**
  - `instagram`: 4:5 vertical portrait ($1080 \times 1350\text{ px}$) — captures 25% more mobile feed height.
  - `twitter`: 16:9 widescreen timeline ($1200 \times 675\text{ px}$) — zero-crop preview.
  - `square`: 1:1 universal ($1080 \times 1080\text{ px}$) — ideal for multi-feed grids.
  - `--platform all`: Generates all platforms simultaneously.

### 3. Local Prospecting Bot (`src/prospecting_engine.py`)
- Simulates scanning local commercial directories (Goa, Mumbai, Bangalore, Dubai) for boutiques, luxury hotels, clinics, and fine-dining restaurants.
- Identifies slow mobile performance bottlenecks, estimated monthly revenue loss, and generates copy/paste cold outreach drafts in:
  - Direct WhatsApp messages with custom speed audit links.
  - Personalized B2B cold emails with executive subject lines.
  - Instagram / LinkedIn DM scripts.
  - Saved to `output/outreach_drafts.md` for immediate sales execution.

---

## 🚀 Quickstart Guide

### Step 1: Run the Agency Website (`laravel-portfolio/`)

The website is engineered to run seamlessly with zero required configuration:

```bash
# Navigate to the Laravel portfolio folder
cd laravel-portfolio

# Start the built-in development server
php -S 127.0.0.1:8000 -t public
```

Now open in your browser:
- **Agency Homepage:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Speed Checker:** [http://127.0.0.1:8000/speed-checker](http://127.0.0.1:8000/speed-checker)
- **Live Audit Demo:** [http://127.0.0.1:8000/speed-checker?url=luxurygoavillas.com](http://127.0.0.1:8000/speed-checker?url=luxurygoavillas.com)
- **pSEO Case Studies Archive:** [http://127.0.0.1:8000/blog](http://127.0.0.1:8000/blog)

---

### Step 2: Set Up Python Automation Environment

```bash
# In the root repository directory:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright Chromium headless browser
playwright install chromium
```

---

### Step 3: Run Automation CLI Commands

#### 1. Daily Autonomous Run (pSEO + Multi-Platform Graphics + Publisher)
```bash
python -m src.main --mode daily --platform all
```

#### 2. Run Local Prospecting Bot (Generate Cold Outreach Dossiers)
```bash
python -m src.main --mode prospect
# Or target a specific city:
python -m src.main --mode prospect --city goa
```
Check `output/outreach_drafts.md` for ready-to-send personalized WhatsApp and email outreach messages.

#### 3. Generate Programmatic SEO Case Studies Only
```bash
python -m src.main --mode pseo --city goa --niche boutique-hotels
```

#### 4. Render Multi-Platform Graphics Only
```bash
# Instagram 4:5 vertical (1080x1350)
python -m src.main --mode graphics --platform instagram

# Twitter 16:9 widescreen (1200x675)
python -m src.main --mode graphics --platform twitter

# All formats simultaneously
python -m src.main --mode graphics --platform all
```

---

## ⚙️ Environment Configuration

Copy `.env.example` to `.env` in the root and configure your contact points:

```ini
BRAND_NAME="ExtrovertNerd"
BRAND_HANDLE="@extrovertnerd"
WEBSITE_URL="https://extrovertnerd.com"
FOUNDER_NAME="ExtrovertNerd"
FOUNDER_ROLE="Web Architecture Studio"
WHATSAPP_PHONE_NUMBER="15551234567"
WHATSAPP_DEFAULT_MESSAGE="Hey ExtrovertNerd! I saw your engineering work and want a free 5-point website speed & UX audit."
```

---

## 🤖 Zero-Cost Cloud Deployment (GitHub Actions)

The `.github/workflows/daily_automation.yml` workflow runs completely free on GitHub's hosted Ubuntu runners.

1. Push your repository to GitHub.
2. In your GitHub repository settings, go to **Settings > Secrets and variables > Actions**.
3. Add the following repository secrets (optional for live social publishing):
   - `WHATSAPP_PHONE_NUMBER`: Your business WhatsApp number (with country code, no spaces).
   - `META_ACCESS_TOKEN` / `INSTAGRAM_ACCOUNT_ID`: For automated Instagram carousel publishing.
   - `TWITTER_API_KEY` / `TWITTER_API_SECRET` / `TWITTER_ACCESS_TOKEN` / `TWITTER_ACCESS_TOKEN_SECRET`: For automated X threads.
4. Enable GitHub Actions workflows. The engine will run daily at 09:00 UTC, generate new pSEO case studies, commit them to your repository, render multi-platform graphics, and compile prospecting dossiers.

---

## 📄 License & Attribution

Designed and engineered under **ExtrovertNerd**.  
Studio & Architectural Direction: **ExtrovertNerd** (`@extrovertnerd`).  
Licensed under the [MIT License](LICENSE).
