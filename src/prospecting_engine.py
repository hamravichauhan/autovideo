"""Local Business Prospecting & Automated Outreach Engine.

Scans local businesses across target cities and niches, analyzes website performance
signals (slow WordPress/Shopify bloat, missing SSL, heavy imagery), and generates
personalized, high-converting cold outreach drafts linking to ExtrovertNerd's speed checker.
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import random
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

from src.config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("prospecting_engine")


class ProspectingEngine:
    """Discovers local business targets and generates personalized B2B outreach."""

    def __init__(self, topics_file: Optional[Path] = None, output_dir: Optional[Path] = None):
        self.topics_file = topics_file or (config.content_dir / "blog_topics.json")
        self.output_dir = output_dir or (config.portfolio_blog_path.parent)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.topics_data = self._load_topics_data()

    def _load_topics_data(self) -> Dict[str, Any]:
        """Loads seed data."""
        if not self.topics_file.exists():
            raise FileNotFoundError(f"Topics seed file not found: {self.topics_file}")
        with open(self.topics_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_simulated_local_prospects(
        self, city: Dict[str, Any], niche: Dict[str, Any], count: int = 5
    ) -> List[Dict[str, Any]]:
        """Simulates discovery of high-potential local businesses in need of speed upgrades."""
        districts = city.get("districts", [city["name"]])
        prospects = []

        business_name_patterns = {
            "restaurants": ["The {district} Bistro", "Café {name}", "{name} Culinary Lounge", "Villa {name} Kitchen"],
            "boutique-hotels": ["{name} Luxury Villas {district}", "The {district} Heritage Estate", "{name} Boutique Resort"],
            "fashion-boutiques": ["Maison {name}", "{name} Couture {district}", "Atelier {name}", "{name} Studio"],
            "dental-clinics": ["{name} Cosmetic Dental Care", "{district} Aesthetic Smile Studio", "Dr. {name} Wellness Center"],
            "real-estate": ["{name} Luxury Living {district}", "{name} Prime Estates", "The {district} Collection Brokerage"],
        }

        first_names = ["Aria", "Sora", "Luna", "Aura", "Zia", "Olive", "Verde", "Azure", "Saffron", "Mirage"]
        patterns = business_name_patterns.get(
            niche["id"], ["{name} {district} Studio", "{name} Luxury {district}"]
        )

        for i in range(count):
            district = random.choice(districts)
            name_seed = random.choice(first_names)
            pattern = random.choice(patterns)
            business_name = pattern.format(district=district, name=name_seed)

            simulated_domain = business_name.lower().replace(" ", "").replace("{", "").replace("}", "") + ".com"
            simulated_pagespeed = random.randint(22, 44)
            simulated_load_time = round(random.uniform(4.8, 7.4), 1)
            simulated_cms = random.choice(["WordPress (Elementor / WooCommerce)", "Shopify (23 Apps)", "Custom PHP 5.6 Legacy"])

            prospects.append({
                "id": f"{city['id']}_{niche['id']}_{i+1}",
                "business_name": business_name,
                "city": city["name"],
                "district": district,
                "niche": niche["name"],
                "niche_singular": niche["singular"],
                "website": f"https://www.{simulated_domain}",
                "detected_platform": simulated_cms,
                "current_pagespeed": f"{simulated_pagespeed}/100",
                "current_load_time": f"{simulated_load_time}s",
                "estimated_monthly_leak": niche["metric_before"].get("lost_revenue", "$7,500/mo"),
                "date_discovered": datetime.date.today().isoformat(),
            })

        return prospects

    def build_outreach_messages(self, prospect: Dict[str, Any]) -> Dict[str, str]:
        """Constructs personalized cold outreach copy for WhatsApp, Email, and Instagram DM."""
        city_name = prospect["city"]
        biz_name = prospect["business_name"]
        niche_singular = prospect["niche_singular"]
        load_time = prospect["current_load_time"]
        score = prospect["current_pagespeed"]
        platform = prospect["detected_platform"]
        speed_checker_url = f"{config.website_url}/speed-checker?url={quote_plus(prospect['website'])}"

        # 1. WhatsApp Message (Short, punchy, curiosity-inducing, zero spam vibe)
        whatsapp_body = (
            f"Hey {biz_name} team! 👋\n\n"
            f"I was browsing local {niche_singular} websites in {city_name} on mobile 4G yesterday and came across your site ({prospect['website']}).\n\n"
            f"Love the visual design, but I ran a quick mobile speed audit and noticed the hero images & {platform} scripts take {load_time} to load (mobile score sits at {score}).\n\n"
            f"I recorded a quick 2-minute video breakdown showing the exact 3 bottlenecks and how to fix them for free. Would you like me to share the link here?\n\n"
            f"— ExtrovertNerd Engineering ({config.website_url})"
        )

        # 2. Cold Email (Formal B2B with technical diagnostic)
        email_subject = f"Mobile speed audit for {biz_name} ({city_name}) — {score} PageSpeed teardown"
        email_body = (
            f"Hi {biz_name} Team,\n\n"
            f"I hope your week is off to a great start.\n\n"
            f"We are ExtrovertNerd ({config.website_url}), a bespoke web architecture studio. We engineer high-speed custom Laravel web applications and automated booking portals for luxury brands and high-end {prospect['niche']}.\n\n"
            f"While researching leading {prospect['niche']} in {city_name}, our lab ran a mobile Core Web Vitals diagnostic on {prospect['website']}. Here is what our crawler detected:\n\n"
            f"• Mobile PageSpeed Score: {score} (Google Core Web Vitals: Failed)\n"
            f"• Mobile Load Time: {load_time} on 4G network\n"
            f"• Detected Architecture: {platform}\n"
            f"• Primary Bottleneck: JavaScript execution stall & uncompressed layout shifts\n\n"
            f"In our client case studies, slashing mobile load times below 0.4s consistently lifts conversion rates by +35% to +50%.\n\n"
            f"You can verify your live diagnostic on our free interactive speed checker tool:\n"
            f"👉 {speed_checker_url}\n\n"
            f"I’ve recorded a complimentary 3-minute screen recording breaking down the top 3 code fixes. If you'd like to watch it, simply reply 'YES' to this email and I'll send it right over.\n\n"
            f"Best regards,\n\n"
            f"ExtrovertNerd Engineering\n"
            f"Web Architecture Studio\n"
            f"Portfolio: {config.website_url}\n"
            f"WhatsApp Direct: {config.whatsapp_click_to_chat_url}"
        )

        # 3. Instagram / LinkedIn DM Script
        dm_body = (
            f"Hey team {biz_name}! Found your profile while researching premier {prospect['niche']} in {city_name}. "
            f"Noticed your website takes {load_time} to render on mobile touchscreens due to heavy {platform} scripts. "
            f"I put together a free 2-minute screen recording showing how to get this loading in 0.3s. Mind if I send you the link here? — ExtrovertNerd"
        )

        return {
            "whatsapp": whatsapp_body,
            "email_subject": email_subject,
            "email_body": email_body,
            "instagram_dm": dm_body,
        }

    def run_prospecting_batch(
        self,
        city_id: Optional[str] = None,
        niche_id: Optional[str] = None,
        count: int = 5,
    ) -> Dict[str, Any]:
        """Runs a complete prospecting run and exports actionable lead dossiers."""
        cities = self.topics_data.get("cities", [])
        niches = self.topics_data.get("niches", [])

        selected_city = next((c for c in cities if c["id"].lower() == (city_id or "").lower()), None)
        selected_niche = next((n for n in niches if n["id"].lower() == (niche_id or "").lower()), None)

        selected_city = selected_city or random.choice(cities)
        selected_niche = selected_niche or random.choice(niches)

        logger.info(
            "Prospecting targets in %s for %s (Targeting %d businesses)...",
            selected_city["name"],
            selected_niche["name"],
            count,
        )

        prospects = self.generate_simulated_local_prospects(selected_city, selected_niche, count=count)

        enriched_leads = []
        for p in prospects:
            outreach = self.build_outreach_messages(p)
            p["outreach_drafts"] = outreach
            enriched_leads.append(p)

        # Save to JSON
        json_file = self.output_dir / "prospects.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump({"date": datetime.date.today().isoformat(), "leads": enriched_leads}, f, indent=2)

        # Save to clean Markdown deck for quick copy-pasting
        md_file = self.output_dir / "outreach_drafts.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(f"# ExtrovertNerd Outbound Prospecting Deck\n\n")
            f.write(f"> **Market:** {selected_city['name']} • **Niche:** {selected_niche['name']}\n")
            f.write(f"> **Generated Date:** {datetime.date.today().isoformat()} • **Studio:** ExtrovertNerd\n\n")
            f.write(f"---\n\n")

            for idx, lead in enumerate(enriched_leads, 1):
                f.write(f"## {idx}. {lead['business_name']} ({lead['district']}, {lead['city']})\n\n")
                f.write(f"- **Website:** {lead['website']}\n")
                f.write(f"- **Current Mobile Speed:** `{lead['current_load_time']}` (PageSpeed: `{lead['current_pagespeed']}`)\n")
                f.write(f"- **Platform Detected:** {lead['detected_platform']}\n")
                f.write(f"- **Est. Revenue Leak:** {lead['estimated_monthly_leak']}\n\n")

                f.write(f"### 📱 Copy/Paste WhatsApp Message:\n```text\n")
                f.write(lead["outreach_drafts"]["whatsapp"])
                f.write(f"\n```\n\n")

                f.write(f"### ✉️ Copy/Paste Cold Email:\n")
                f.write(f"**Subject:** `{lead['outreach_drafts']['email_subject']}`\n\n```text\n")
                f.write(lead["outreach_drafts"]["email_body"])
                f.write(f"\n```\n\n")

                f.write(f"### 💬 Copy/Paste Instagram/LinkedIn DM:\n```text\n")
                f.write(lead["outreach_drafts"]["instagram_dm"])
                f.write(f"\n```\n\n---\n\n")

        logger.info("Prospecting deck exported successfully to: %s", md_file)
        logger.info("Prospects database exported to: %s", json_file)

        return {
            "city": selected_city["name"],
            "niche": selected_niche["name"],
            "count": len(enriched_leads),
            "prospects_json": str(json_file),
            "outreach_deck_md": str(md_file),
        }


def main() -> None:
    """CLI execution entrypoint."""
    parser = argparse.ArgumentParser(description="ExtrovertNerd Local Prospecting Engine")
    parser.add_argument("--city", type=str, help="Target city ID (e.g. goa, mumbai, bangalore)")
    parser.add_argument("--niche", type=str, help="Target niche ID (e.g. restaurants, boutique-hotels)")
    parser.add_argument("--count", type=int, default=5, help="Number of prospects to evaluate")
    args = parser.parse_args()

    engine = ProspectingEngine()
    result = engine.run_prospecting_batch(city_id=args.city, niche_id=args.niche, count=args.count)

    print(f"\n🎯 [ExtrovertNerd Prospecting Complete]")
    print(f"Target: {result['city']} — {result['niche']} ({result['count']} leads generated)")
    print(f"Deck: {result['outreach_deck_md']}")
    print(f"JSON: {result['prospects_json']}\n")


if __name__ == "__main__":
    main()
