"""Programmatic SEO (pSEO) Blog & Case Study Generator.

Assembles search-optimized, high-converting Markdown articles targeting
local business owners and scaling brands across specific cities and niches.
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

import jinja2

from src.config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class PSEOGenerator:
    """Generates programmatic SEO articles and case studies from structured seed data."""

    def __init__(self, data_file: Optional[Path] = None, template_file: Optional[Path] = None):
        self.data_file = data_file or (config.content_dir / "blog_topics.json")
        self.template_file = template_file or (config.templates_dir / "blog_template.md")
        self.topics_data = self._load_topics_data()
        self.output_dir = config.portfolio_blog_path
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.output_dir / "manifest.json"
        self.manifest = self._load_manifest()

        # Setup Jinja environment
        template_dir = self.template_file.parent
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _load_topics_data(self) -> Dict[str, Any]:
        """Loads cities, niches, and comparison seed datasets."""
        if not self.data_file.exists():
            raise FileNotFoundError(f"Topics seed file not found: {self.data_file}")
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_manifest(self) -> Dict[str, Any]:
        """Loads the registry of previously generated articles to prevent duplicates."""
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning("Could not read manifest, initializing fresh: %s", e)
        return {"articles": [], "last_generated": None}

    def _save_manifest(self) -> None:
        """Persists the updated manifest to disk."""
        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(self.manifest, f, indent=2)

    def _slugify(self, text: str) -> str:
        """Converts strings to clean URL slugs."""
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_-]+", "-", text)
        return text.strip("-")

    def get_next_city_and_niche(
        self, preferred_city_id: Optional[str] = None, preferred_niche_id: Optional[str] = None
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Selects the next target city and niche using intelligent rotation."""
        cities = self.topics_data.get("cities", [])
        niches = self.topics_data.get("niches", [])

        if not cities or not niches:
            raise ValueError("Seed dataset must contain at least one city and one niche.")

        # If user explicitly provided city/niche
        selected_city = None
        if preferred_city_id:
            for c in cities:
                if c["id"].lower() == preferred_city_id.lower() or c["name"].lower() == preferred_city_id.lower():
                    selected_city = c
                    break

        selected_niche = None
        if preferred_niche_id:
            for n in niches:
                if n["id"].lower() == preferred_niche_id.lower() or n["name"].lower() == preferred_niche_id.lower():
                    selected_niche = n
                    break

        # If not manually provided, find least generated combination from manifest
        existing_pairs = {
            f"{a.get('city_id')}:{a.get('niche_id')}" for a in self.manifest.get("articles", [])
        }

        if not selected_city or not selected_niche:
            unvisited_pairs = [
                (c, n) for c in cities for n in niches if f"{c['id']}:{n['id']}" not in existing_pairs
            ]
            if unvisited_pairs:
                c_chosen, n_chosen = random.choice(unvisited_pairs)
                selected_city = selected_city or c_chosen
                selected_niche = selected_niche or n_chosen
            else:
                # All combinations covered, pick random rotation
                selected_city = selected_city or random.choice(cities)
                selected_niche = selected_niche or random.choice(niches)

        return selected_city, selected_niche

    def build_article_context(
        self,
        city: Dict[str, Any],
        niche: Dict[str, Any],
        angle: str = "local_speed",
    ) -> Dict[str, Any]:
        """Constructs data context for template rendering."""
        today_str = datetime.date.today().isoformat()

        if angle == "tech_comparison":
            title = f"{niche['name']} in {city['name']}: Laravel vs Shopify & WordPress (Speed & Profit Breakdown)"
            description = (
                f"A comprehensive technical comparison of Laravel vs Shopify and WordPress for "
                f"{niche['plural']} in {city['name']}. Discover how sub-second speeds unlock higher conversion rates."
            )
            category = "E-Commerce Architecture & Performance"
        elif angle == "automation":
            title = f"How Custom Laravel Applications Automate {niche['name']} Operations in {city['name']}"
            description = (
                f"Learn how local {niche['plural']} in {city['name']} automate customer bookings, "
                f"WhatsApp notifications, and backend operations without third-party monthly SaaS fees."
            )
            category = "Custom Web Applications & Automation"
        else:  # local_speed default
            title = f"Why {city['name']} {niche['name']} Businesses Lose Customers to Slow Mobile Websites"
            description = (
                f"Over 65% of mobile visitors abandon slow websites in {city['name']}. "
                f"Here is how migrating {niche['plural']} to custom Laravel engineering slashes load times to 0.4s."
            )
            category = "Mobile Performance & Core Web Vitals"

        slug = self._slugify(f"{city['id']}-{niche['id']}-{angle}")

        # WhatsApp Click-to-Chat deep link with customized context message
        custom_wa_message = (
            f"Hi {config.brand_name}! I read your article on {city['name']} {niche['plural']} "
            f"and would love a free 5-point website speed audit."
        )
        whatsapp_message_encoded = quote_plus(custom_wa_message)

        keywords = [
            f"{city['name']} {niche['singular']} web development",
            f"high speed website for {niche['plural']} {city['name']}",
            f"Laravel web app {city['name']}",
            f"{city['name']} website speed audit",
            f"Shopify alternative for {niche['name']}",
            f"custom booking dashboard {city['name']}",
        ]

        return {
            "title": title,
            "slug": slug,
            "date": today_str,
            "author": config.brand_name,
            "category": category,
            "description": description,
            "keywords": keywords,
            "city": city,
            "niche": niche,
            "angle": angle,
            "whatsapp_number": config.whatsapp_phone_number,
            "whatsapp_message_encoded": whatsapp_message_encoded,
            "intake_form_url": config.google_form_intake_url,
            "brand_name": config.brand_name,
            "brand_handle": config.brand_handle,
            "website_url": config.website_url,
        }

    def generate_article(
        self,
        city_id: Optional[str] = None,
        niche_id: Optional[str] = None,
        angle: str = "local_speed",
        save: bool = True,
    ) -> Dict[str, Any]:
        """Generates a complete markdown blog article and records it in the manifest."""
        city, niche = self.get_next_city_and_niche(city_id, niche_id)
        context = self.build_article_context(city, niche, angle)

        template = self.jinja_env.get_template(self.template_file.name)
        markdown_content = template.render(**context)

        filename = f"{context['slug']}.md"
        filepath = self.output_dir / filename

        if save:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            logger.info("Successfully generated pSEO article: %s", filepath)

            # Update manifest
            manifest_entry = {
                "slug": context["slug"],
                "filename": filename,
                "title": context["title"],
                "city_id": city["id"],
                "city_name": city["name"],
                "niche_id": niche["id"],
                "niche_name": niche["name"],
                "angle": angle,
                "date": context["date"],
                "path": str(filepath),
            }
            # Remove any existing entry for this slug
            self.manifest["articles"] = [
                a for a in self.manifest["articles"] if a.get("slug") != context["slug"]
            ]
            self.manifest["articles"].append(manifest_entry)
            self.manifest["last_generated"] = manifest_entry
            self._save_manifest()

        return {
            "context": context,
            "content": markdown_content,
            "filepath": filepath,
            "filename": filename,
        }

    def generate_batch(self, count: int = 3) -> List[Dict[str, Any]]:
        """Generates a batch of articles cycling through available angles and niches."""
        angles = ["local_speed", "tech_comparison", "automation"]
        results = []
        for i in range(count):
            angle = angles[i % len(angles)]
            result = self.generate_article(angle=angle, save=True)
            results.append(result)
        return results


def main() -> None:
    """CLI execution entrypoint."""
    parser = argparse.ArgumentParser(description="Programmatic SEO Blog Article Generator")
    parser.add_argument("--city", type=str, help="Target city ID or name (e.g., goa, mumbai, bangalore)")
    parser.add_argument("--niche", type=str, help="Target niche ID (e.g., restaurants, boutique-hotels)")
    parser.add_argument(
        "--angle",
        type=str,
        default="local_speed",
        choices=["local_speed", "tech_comparison", "automation", "random"],
        help="Content angle for generation",
    )
    parser.add_argument("--count", type=int, default=1, help="Number of articles to generate")
    args = parser.parse_args()

    generator = PSEOGenerator()

    if args.count > 1:
        generator.generate_batch(count=args.count)
    else:
        chosen_angle = (
            random.choice(["local_speed", "tech_comparison", "automation"])
            if args.angle == "random"
            else args.angle
        )
        result = generator.generate_article(
            city_id=args.city, niche_id=args.niche, angle=chosen_angle, save=True
        )
        print(f"\n[Generated Article]\nTitle: {result['context']['title']}")
        print(f"File: {result['filepath']}\n")


if __name__ == "__main__":
    main()
