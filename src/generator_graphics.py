"""Headless Graphic & Carousel Renderer.

Uses Playwright headless Chromium to render Jinja2/Tailwind CSS templates
into high-resolution 1080x1080 PNG assets for social media carousels and posts.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import jinja2

from src.config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class GraphicsRenderer:
    """Renders HTML templates into 1080x1080 PNG image graphics using Playwright."""

    def __init__(
        self,
        templates_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None,
        topics_file: Optional[Path] = None,
    ):
        self.templates_dir = templates_dir or config.templates_dir
        self.output_dir = output_dir or config.graphics_output_path
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.topics_file = topics_file or (config.content_dir / "blog_topics.json")
        self.topics_data = self._load_topics_data()

        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _load_topics_data(self) -> Dict[str, Any]:
        """Loads seed data for topics and cities."""
        if not self.topics_file.exists():
            raise FileNotFoundError(f"Topics seed file not found: {self.topics_file}")
        with open(self.topics_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_city_and_niche(
        self, city_id: Optional[str] = None, niche_id: Optional[str] = None
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Picks city and niche from seed data."""
        cities = self.topics_data.get("cities", [])
        niches = self.topics_data.get("niches", [])

        selected_city = None
        if city_id:
            for c in cities:
                if c["id"].lower() == city_id.lower() or c["name"].lower() == city_id.lower():
                    selected_city = c
                    break

        selected_niche = None
        if niche_id:
            for n in niches:
                if n["id"].lower() == niche_id.lower() or n["name"].lower() == niche_id.lower():
                    selected_niche = n
                    break

        selected_city = selected_city or random.choice(cities)
        selected_niche = selected_niche or random.choice(niches)
        return selected_city, selected_niche

    def build_carousel_slides_context(
        self, city: Dict[str, Any], niche: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Constructs data contexts for the 4 carousel slides."""
        total_slides = 4
        slides = []

        base_ctx = {
            "brand_name": config.brand_name,
            "brand_handle": config.brand_handle,
            "website_url": config.website_url,
            "city_name": city["name"],
            "niche_name": niche["name"],
            "niche_singular": niche["singular"],
            "niche_plural": niche["plural"],
            "lost_revenue": niche["metric_before"].get("lost_revenue", "$8,500/mo"),
            "pagespeed_before": niche["metric_before"].get("pagespeed", "28/100"),
            "load_before": niche["metric_before"].get("load_time", "5.6s"),
            "bounce_before": niche["metric_before"].get("bounce_rate", "72%"),
            "pagespeed_after": niche["metric_after"].get("pagespeed", "99/100"),
            "load_after": niche["metric_after"].get("load_time", "0.38s"),
            "bounce_after": niche["metric_after"].get("bounce_rate", "24%"),
            "conversion_lift": niche["metric_after"].get("conversion_lift", "+42%"),
            "total_slides": total_slides,
        }

        # Slide 1: Hook / Problem Statement
        slide_1 = dict(base_ctx)
        slide_1.update({
            "slide_number": 1,
            "slide_type": "hook",
            "slide_badge": f"AUDIT // {city['name'].upper()} {niche['singular'].upper()}",
            "title": f"Is Your {city['name']} {niche['singular']} Losing 40% of Mobile Sales?",
        })
        slides.append(slide_1)

        # Slide 2: UX & Speed Flaw Analysis (Before)
        slide_2 = dict(base_ctx)
        slide_2.update({
            "slide_number": 2,
            "slide_type": "flaw",
            "slide_badge": "THE BEFORE AUDIT // LEGACY STACK",
            "title": f"Why Existing {niche['plural']} Struggle on Mobile",
        })
        slides.append(slide_2)

        # Slide 3: Laravel Redesign (After)
        slide_3 = dict(base_ctx)
        slide_3.update({
            "slide_number": 3,
            "slide_type": "solution",
            "slide_badge": "THE AFTER STATE // CUSTOM LARAVEL",
            "title": "Sub-Second Speed & Zero Platform Taxes",
        })
        slides.append(slide_3)

        # Slide 4: Call-To-Action (Lead Capture)
        slide_4 = dict(base_ctx)
        slide_4.update({
            "slide_number": 4,
            "slide_type": "cta",
            "slide_badge": "INBOUND CLIENT FUNNEL // NEXT STEP",
            "title": "Claim Your Free 5-Point Website Audit",
        })
        slides.append(slide_4)

        return slides

    async def _render_html_to_png(
        self,
        html_content: str,
        output_file: Path,
        width: int = 1080,
        height: int = 1080,
        device_scale_factor: int = 1,
    ) -> Path:
        """Loads HTML content into headless Playwright browser and captures screenshot."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            raise RuntimeError(
                "Playwright is not installed. Please run: pip install playwright && playwright install chromium"
            )

        output_file.parent.mkdir(parents=True, exist_ok=True)

        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
                )
            except Exception as e:
                logger.error("Failed to launch Playwright Chromium: %s", e)
                logger.error(
                    "You may need to run: python -m playwright install chromium"
                )
                raise

            context = await browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=device_scale_factor,
            )
            page = await context.new_page()

            # Set HTML content and wait for network/styles to settle
            await page.set_content(html_content, wait_until="networkidle", timeout=15000)

            # Extra short pause to allow web fonts/Tailwind CSS animations to paint
            await page.wait_for_timeout(400)

            # Screenshot exact canvas element or full viewport
            canvas = await page.query_selector("#slide-canvas")
            if canvas:
                await canvas.screenshot(path=str(output_file), type="png")
            else:
                await page.screenshot(path=str(output_file), type="png")

            await browser.close()

        logger.info("Saved graphic asset: %s", output_file)
        return output_file

    def render_carousel_set(
        self,
        city_id: Optional[str] = None,
        niche_id: Optional[str] = None,
        batch_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Synchronously renders all 4 slides of a carousel."""
        city, niche = self._get_city_and_niche(city_id, niche_id)
        slides_context = self.build_carousel_slides_context(city, niche)

        batch_name = batch_id or f"{city['id']}_{niche['id']}_carousel"
        batch_folder = self.output_dir / batch_name
        batch_folder.mkdir(parents=True, exist_ok=True)

        template = self.jinja_env.get_template("carousel_slide.html")
        rendered_images = []

        async def _run_all() -> List[Path]:
            tasks = []
            for slide_ctx in slides_context:
                html = template.render(**slide_ctx)
                slide_num = slide_ctx["slide_number"]
                slide_path = batch_folder / f"slide_{slide_num}.png"
                tasks.append(self._render_html_to_png(html, slide_path))
            return await asyncio.gather(*tasks)

        # Run async event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            rendered_images = loop.run_until_complete(_run_all())
        finally:
            loop.close()

        meta_info = {
            "batch_id": batch_name,
            "city": city,
            "niche": niche,
            "total_slides": len(rendered_images),
            "slide_paths": [str(p) for p in rendered_images],
            "directory": str(batch_folder),
        }

        # Save metadata manifest inside batch folder
        with open(batch_folder / "meta.json", "w", encoding="utf-8") as f:
            json.dump(meta_info, f, indent=2)

        return meta_info

    def render_tech_tip(
        self,
        tip_id: Optional[str] = None,
        output_filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Renders a code snippet / tech tip graphic (Pillar 3)."""
        tips = self.topics_data.get("tech_tips", [])
        if not tips:
            raise ValueError("No tech tips found in seed data.")

        selected_tip = None
        if tip_id:
            for t in tips:
                if t["id"].lower() == tip_id.lower():
                    selected_tip = t
                    break

        selected_tip = selected_tip or random.choice(tips)

        context = {
            "brand_name": config.brand_name,
            "brand_handle": config.brand_handle,
            "tip_title": selected_tip["title"],
            "tip_summary": selected_tip["summary"],
            "problem_code": selected_tip["problem_code"],
            "solution_code": selected_tip["solution_code"],
            "explanation": selected_tip["explanation"],
        }

        template = self.jinja_env.get_template("tech_tip.html")
        html = template.render(**context)

        file_name = output_filename or f"tech_tip_{selected_tip['id']}.png"
        output_file = self.output_dir / "tech_tips" / file_name

        async def _run() -> Path:
            return await self._render_html_to_png(html, output_file)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            rendered_path = loop.run_until_complete(_run())
        finally:
            loop.close()

        return {
            "tip": selected_tip,
            "image_path": str(rendered_path),
        }


def main() -> None:
    """CLI execution entrypoint."""
    parser = argparse.ArgumentParser(description="Headless Graphic & Carousel Renderer")
    parser.add_argument("--type", choices=["carousel", "tech_tip"], default="carousel")
    parser.add_argument("--city", type=str, help="Target city ID (e.g. goa, mumbai)")
    parser.add_argument("--niche", type=str, help="Target niche ID (e.g. restaurants)")
    parser.add_argument("--tip", type=str, help="Tech tip ID for code snippet graphic")
    parser.add_argument("--batch-id", type=str, help="Custom folder name for carousel slides")
    args = parser.parse_args()

    renderer = GraphicsRenderer()

    if args.type == "tech_tip":
        result = renderer.render_tech_tip(tip_id=args.tip)
        print(f"\n[Generated Tech Tip Graphic]\nTitle: {result['tip']['title']}")
        print(f"Path: {result['image_path']}\n")
    else:
        result = renderer.render_carousel_set(
            city_id=args.city, niche_id=args.niche, batch_id=args.batch_id
        )
        print(f"\n[Generated Carousel Set]")
        print(f"Target: {result['city']['name']} - {result['niche']['name']}")
        print(f"Slides generated ({result['total_slides']}):")
        for p in result["slide_paths"]:
            print(f"  - {p}")
        print()


if __name__ == "__main__":
    main()
