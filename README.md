# 24/7 Automated Client Acquisition Funnel & Content Engine

> **A 100% Free, Autonomous Client Acquisition & Content Engine** engineered for web development studios, software agencies, and freelance engineers. Attract local business owners, startup founders, and entrepreneurs who need custom high-speed Laravel e-commerce stores, automated management dashboards, and modern web applications—running on zero-cost cloud automation without paid LLM APIs or manual intervention.

---

## 🌟 Key Architecture & Capabilities

```
                  ┌────────────────────────────────────────┐
                  │    GitHub Actions (Zero-Cost Cron)     │
                  │   Daily Trigger @ 09:00 UTC / Manual   │
                  └──────────────────┬─────────────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼                                                   ▼
┌───────────────────────────┐                       ┌───────────────────────────┐
│ Programmatic SEO Engine   │                       │ Headless Playwright Engine│
│ (`src/generator_pseo.py`) │                       │(`src/generator_graphics.py│
│                           │                       │                           │
│ • City/Niche Matrix       │                       │ • Dark Luxury Aesthetic   │
│ • High-Intent Markdown    │                       │ • 1080x1080 PNG Renderer  │
│ • Inbound WhatsApp Funnel │                       │ • 4-Slide Carousels       │
└──────────┬────────────────┘                       └─────────────┬─────────────┘
           │                                                      │
           ▼                                                      ▼
┌───────────────────────────┐                       ┌───────────────────────────┐
│ Portfolio Repository      │                       │ Multi-Channel Publisher   │
│ Auto-Committed Markdown   │                       │ (`src/publisher.py`)      │
│ Articles & Manifest       │                       │                           │
│ (`output/blogs/*.md`)     │                       │ • Instagram Carousel Post │
└───────────────────────────┘                       │ • Twitter / X Auto-Thread │
                                                    │ • Facebook Page Updates   │
                                                    └─────────────┬─────────────┘
                                                                  │
                                                                  ▼
                                                    ┌───────────────────────────┐
                                                    │ Inbound Lead Capture      │
                                                    │ • WhatsApp Click-to-Chat  │
                                                    │ • 60-Sec Audit Form       │
                                                    │ • Direct Messages         │
                                                    └───────────────────────────┘
```

### 1. The Four Core Content Pillars
1. **Programmatic SEO (pSEO) Articles & Case Studies:** Generates rich, long-form Markdown articles comparing web stacks (*"Laravel vs Shopify for Boutique E-Commerce"*) and targeting local high-intent keywords (*"Why Goa Restaurant Businesses Lose Customers to Slow Mobile Websites"*).
2. **Before / After Website Redesign Carousels:** Playwright-rendered $1080 \times 1080\text{ px}$ dark-mode visual carousels breaking down legacy speed flaws (32/100 PageSpeed, 5.8s load) vs. custom Laravel rebuilds (99/100 PageSpeed, 0.4s load, +42% conversion lift).
3. **Tech Tips & Code Snippets:** High-contrast syntax-highlighted visual cards demonstrating real-world backend engineering fixes (e.g., solving N+1 Eloquent queries, Redis RAM caching, AVIF image pipelines).
4. **Automated Social Threads:** Multi-tweet value threads posted directly to Twitter/X paired with visual graphics and direct WhatsApp audit booking links.

---

## 📁 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── daily_automation.yml      # Zero-cost cloud cron runner (GitHub Actions)
├── content/
│   ├── blog_topics.json              # Structured data matrix (cities, niches, metrics, comparisons)
│   └── social_templates.json         # High-converting caption formulas, thread steps & hashtags
├── templates/
│   ├── blog_template.md              # Jinja2 template for programmatic SEO articles
│   ├── carousel_slide.html           # Dark luxury 1080x1080 Tailwind CSS visual slide template
│   └── tech_tip.html                 # Code snippet & developer tip visual template
├── src/
│   ├── __init__.py
│   ├── config.py                     # Configuration loader with fallback values
│   ├── generator_pseo.py             # Programmatic SEO blog article builder
│   ├── generator_graphics.py         # Playwright headless browser PNG renderer
│   ├── publisher.py                  # Meta Graph & Twitter/X API uploader + Caption builder
│   └── main.py                       # Central orchestrator CLI
├── output/
│   ├── blogs/                        # Generated markdown articles and manifest
│   └── graphics/                     # Generated 1080x1080 PNG slide sets
├── .env.example                      # Configuration and API key documentation
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## 🚀 Quickstart & Local Installation

### 1. Clone & Set Up Virtual Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-folder>

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright Chromium headless browser
playwright install chromium
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` to configure your brand, WhatsApp number, and audit links:

```ini
BRAND_NAME="Apex Velocity Labs"
BRAND_HANDLE="@apexvelocitylabs"
WEBSITE_URL="https://apexvelocity.dev"
WHATSAPP_PHONE_NUMBER="15551234567"
WHATSAPP_DEFAULT_MESSAGE="Hey! I saw your post and want a free 5-point website speed & UX audit."
GOOGLE_FORM_INTAKE_URL="https://forms.gle/your-free-speed-audit-intake"

# Set to true to test locally without calling live APIs
DRY_RUN=true
```

---

## 🛠️ Usage & CLI Commands

### 1. Run Complete Daily Funnel (pSEO + Carousels + Social Captions)

```bash
# Runs full autonomous pipeline with intelligent city/niche rotation
python -m src.main --mode daily

# Target a specific city and niche
python -m src.main --mode daily --city goa --niche restaurants

# Target a tech comparison angle
python -m src.main --mode daily --city mumbai --niche fashion-boutiques --angle tech_comparison
```

### 2. Generate Programmatic SEO Articles Only

```bash
# Generate 1 article for next rotated city/niche
python -m src.generator_pseo

# Generate a batch of 3 articles across angles
python -m src.generator_pseo --count 3

# Specific target
python -m src.generator_pseo --city bangalore --niche dental-clinics --angle automation
```

### 3. Render High-Resolution Visual Carousels (Multi-Platform Sizing)

Choose your target social platform format:
- **`instagram`**: $1080 \times 1350\text{ px}$ (4:5 Portrait — captures 25% more screen real estate on mobile feeds)
- **`linkedin`**: $1080 \times 1350\text{ px}$ (4:5 Portrait — optimal for swipeable PDF document carousels)
- **`twitter`**: $1200 \times 675\text{ px}$ (16:9 Landscape — fits Twitter feed previews without cropping)
- **`square`**: $1080 \times 1080\text{ px}$ (1:1 Universal)
- **`all`**: Automatically generates multi-format sets for Instagram, Twitter, and Square simultaneously!

```bash
# Render 4:5 Portrait Carousels for Instagram (Default)
python -m src.generator_graphics --type carousel --city goa --niche restaurants --platform instagram

# Render 16:9 Landscape Carousels for Twitter / X Threads
python -m src.generator_graphics --type carousel --city mumbai --niche fashion-boutiques --platform twitter

# Render 4:5 Document Carousels for LinkedIn
python -m src.generator_graphics --type carousel --city bangalore --niche dental-clinics --platform linkedin

# Render Multi-Platform Sets simultaneously (Instagram 4:5, Twitter 16:9, and Square 1:1)
python -m src.generator_graphics --type carousel --city dubai --niche real-estate --platform all

# Render a Code Snippet / Tech Tip graphic (Pillar 3)
python -m src.generator_graphics --type tech_tip
```

Generated images will be saved under:
- `output/graphics/{city}_{niche}_carousel/slide_1.png`
- `output/graphics/{city}_{niche}_carousel/slide_2.png`
- `output/graphics/{city}_{niche}_carousel/slide_3.png`
- `output/graphics/{city}_{niche}_carousel/slide_4.png`

### 4. Inspect Captions & Social Threads

```bash
python -m src.main --mode social --city dubai --niche real-estate
```

---

## ☁️ Zero-Cost Cloud Scheduler (GitHub Actions)

The workflow file `.github/workflows/daily_automation.yml` runs **100% free** using GitHub's monthly allocation of GitHub Actions runner minutes:

1. **Automatic Daily Trigger:** Fires every day at `09:00 UTC` (14:30 IST / 05:00 EDT).
2. **Intelligent Rotation:** Cycles through your database of cities and business niches, preventing repetitive content.
3. **Automatic Git Commits:** Auto-commits newly generated markdown articles into `output/blogs/` and updates `manifest.json`.
4. **Artifact Retention:** Each run archives generated $1080 \times 1080\text{ px}$ PNG slides as workflow artifacts for 14 days, letting you download them anytime directly from GitHub Actions.
5. **Safe Dry-Run:** If API secrets are not configured, the workflow gracefully runs in simulation mode, generating graphics and blog articles without throwing errors.

### Setting Up GitHub Repository Secrets

Under your GitHub Repository, navigate to **Settings > Secrets and variables > Actions** and add:

| Secret Name | Description | Optional? |
| :--- | :--- | :--- |
| `WHATSAPP_PHONE_NUMBER` | Your WhatsApp business number (e.g. `15551234567`) | Optional (has default) |
| `GOOGLE_FORM_INTAKE_URL` | Your free audit intake form URL | Optional (has default) |
| `META_ACCESS_TOKEN` | Long-lived Facebook Page token with Instagram publishing permissions | Required for live Instagram posts |
| `INSTAGRAM_ACCOUNT_ID` | Instagram Professional / Creator account ID | Required for live Instagram posts |
| `TWITTER_API_KEY` | Twitter Developer App API Key | Required for live Twitter threads |
| `TWITTER_API_SECRET` | Twitter Developer App API Secret | Required for live Twitter threads |
| `TWITTER_ACCESS_TOKEN` | Twitter User OAuth 1.0a Access Token | Required for live Twitter threads |
| `TWITTER_ACCESS_TOKEN_SECRET`| Twitter User OAuth 1.0a Access Secret | Required for live Twitter threads |

---

## 🎯 Conversion Architecture (The Inbound Funnel)

Every piece of content is engineered with direct response psychology:
1. **The Hook:** Highlights specific revenue leaks (e.g., *“Is your Assagao boutique losing 40% of mobile sales to slow 5.8s load times?”*).
2. **The Contrast:** Pits sluggish plugin-heavy WordPress/Shopify stores against sub-400ms custom Laravel web apps.
3. **The Irresistible Offer:** A **Free 5-Point Website Speed & UX Teardown** (with a 3-minute personalized Loom/screen recording).
4. **Zero Friction CTA:** Single-tap WhatsApp click-to-chat link pre-populated with a personalized inquiry message (`wa.me/number?text=...`).
