"""Headless Graphic & Carousel Renderer.

Uses Playwright headless Chromium to render Jinja2/Tailwind CSS templates
into platform-optimized PNG image assets:
- Instagram: 1080 x 1350 px (4:5 Portrait - maximum feed screen real estate)
- LinkedIn: 1080 x 1350 px (4:5 Portrait - optimal for swipeable PDF slide docs)
- Twitter / X: 1200 x 675 px (16:9 Landscape - native feed preview without cropping)
- Square: 1080 x 1080 px (1:1 Universal)
"""

from __future__ import annotations

import argparse
import asyncio
import datetime
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

PLATFORM_PRESETS: Dict[str, Dict[str, Any]] = {
    "vertical": {
        "width": 1080,
        "height": 1350,
        "aspect_ratio": "4:5",
        "name": "Universal Vertical Poster (4:5)",
        "description": "Standard high-impact portrait format for Instagram, LinkedIn, and X/Twitter feeds",
    },
    "instagram": {
        "width": 1080,
        "height": 1350,
        "aspect_ratio": "4:5",
        "name": "Instagram Portrait Post (4:5)",
        "description": "Optimal 4:5 vertical post (1080x1350) for maximum feed screen real estate",
    },
    "linkedin": {
        "width": 1080,
        "height": 1350,
        "aspect_ratio": "4:5",
        "name": "LinkedIn Vertical Carousel (4:5)",
        "description": "Professional 4:5 vertical format for high-authority slide carousels",
    },
    "twitter": {
        "width": 1080,
        "height": 1350,
        "aspect_ratio": "4:5",
        "name": "X / Twitter Vertical Post (4:5)",
        "description": "Full vertical 4:5 poster (1080x1350) commanding maximum mobile feed attention",
    },
    "story": {
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "name": "Story & Reel Fullscreen Poster (9:16)",
        "description": "Full-height vertical 9:16 poster (1080x1920) for Stories and Reels",
    },
    "square": {
        "width": 1080,
        "height": 1080,
        "aspect_ratio": "1:1",
        "name": "Universal Square (1:1)",
        "description": "Classic 1:1 square for Facebook, Instagram, and general feeds",
    },
    "twitter_landscape": {
        "width": 1600,
        "height": 900,
        "aspect_ratio": "16:9",
        "name": "Twitter / X Desktop Landscape (16:9)",
        "description": "Desktop 16:9 format fitting Twitter web in-stream cards",
    },
}


class GraphicsRenderer:
    """Renders HTML templates into multi-platform PNG image graphics using Playwright."""

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
        self.top100_data = self._load_top100_data()
        self.tech_news_data = self._load_tech_news_data()
        self.website_tips_data = self._load_website_tips_data()

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

    def _load_top100_data(self) -> List[Dict[str, Any]]:
        """Loads the Top 100 Websites breakdown dataset."""
        path = config.content_dir / "top100_websites.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _load_tech_news_data(self) -> List[Dict[str, Any]]:
        """Loads the Tech News and Industry Updates dataset."""
        path = config.content_dir / "tech_news.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _load_website_tips_data(self) -> List[Dict[str, Any]]:
        """Loads the Website Performance & UX Tips dataset."""
        path = config.content_dir / "website_tips.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

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
        self,
        city: Dict[str, Any],
        niche: Dict[str, Any],
        platform: str = "instagram",
    ) -> List[Dict[str, Any]]:
        """Constructs data contexts for the 4 carousel slides customized by platform."""
        preset = PLATFORM_PRESETS.get(platform, PLATFORM_PRESETS["instagram"])
        total_slides = 4
        slides = []

        base_ctx = {
            "brand_name": config.brand_name,
            "brand_handle": config.brand_handle,
            "founder_name": config.founder_name,
            "founder_title": config.founder_title,
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
            "platform": platform,
            "aspect_ratio": preset["aspect_ratio"],
            "width": preset["width"],
            "height": preset["height"],
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
        height: int = 1350,
        device_scale_factor: int = 2,
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
            await page.wait_for_timeout(450)

            # Screenshot exact canvas element or full viewport
            canvas = await page.query_selector("#slide-canvas") or await page.query_selector(".poster-canvas")
            if canvas:
                await canvas.screenshot(path=str(output_file), type="png")
            else:
                await page.screenshot(path=str(output_file), type="png")

            await browser.close()

        logger.info("Saved graphic asset [%dx%d @%dx]: %s", width, height, device_scale_factor, output_file)
        return output_file

    def render_carousel_set(
        self,
        city_id: Optional[str] = None,
        niche_id: Optional[str] = None,
        batch_id: Optional[str] = None,
        platform: str = "vertical",
    ) -> Dict[str, Any]:
        """Synchronously renders all 4 slides of a carousel customized for a target platform."""
        city, niche = self._get_city_and_niche(city_id, niche_id)

        target_platforms = (
            ["vertical", "story", "square"] if platform == "all" else [platform]
        )

        batch_name = batch_id or f"{city['id']}_{niche['id']}_carousel"
        batch_folder = self.output_dir / batch_name
        batch_folder.mkdir(parents=True, exist_ok=True)

        template = self.jinja_env.get_template("carousel_slide.html")
        all_rendered_images: List[str] = []

        async def _run_for_platform(plt: str) -> List[Path]:
            preset = PLATFORM_PRESETS.get(plt, PLATFORM_PRESETS["vertical"])
            slides_context = self.build_carousel_slides_context(city, niche, platform=plt)
            tasks = []
            for slide_ctx in slides_context:
                html = template.render(**slide_ctx)
                slide_num = slide_ctx["slide_number"]
                filename = (
                    f"slide_{slide_num}.png"
                    if len(target_platforms) == 1
                    else f"{plt}_slide_{slide_num}.png"
                )
                slide_path = batch_folder / filename
                tasks.append(
                    self._render_html_to_png(
                        html,
                        slide_path,
                        width=preset["width"],
                        height=preset["height"],
                        device_scale_factor=2,
                    )
                )
            return await asyncio.gather(*tasks)

        # Run async event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            for plt in target_platforms:
                imgs = loop.run_until_complete(_run_for_platform(plt))
                all_rendered_images.extend([str(p) for p in imgs])
        finally:
            loop.close()

        meta_info = {
            "batch_id": batch_name,
            "city": city,
            "niche": niche,
            "platform": platform,
            "total_slides": len(all_rendered_images),
            "slide_paths": all_rendered_images,
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
        platform: str = "vertical",
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
        preset = PLATFORM_PRESETS.get(platform, PLATFORM_PRESETS["vertical"])

        context = {
            "brand_name": config.brand_name,
            "brand_handle": config.brand_handle,
            "founder_name": config.founder_name,
            "founder_title": config.founder_title,
            "tip_title": selected_tip["title"],
            "tip_summary": selected_tip["summary"],
            "problem_code": selected_tip["problem_code"],
            "solution_code": selected_tip["solution_code"],
            "explanation": selected_tip["explanation"],
            "width": preset["width"],
            "height": preset["height"],
        }

        template = self.jinja_env.get_template("tech_tip.html")
        html = template.render(**context)

        file_name = output_filename or f"tech_tip_{selected_tip['id']}.png"
        output_file = self.output_dir / "tech_tips" / file_name

        async def _run() -> Path:
            return await self._render_html_to_png(
                html,
                output_file,
                width=preset["width"],
                height=preset["height"],
                device_scale_factor=2,
            )

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

    def render_top100_breakdown(
        self,
        website_id: Optional[Any] = None,
        output_filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Renders a 4:5 vertical poster breaking down one of the Top 100 Websites in the world.

        By default, rotates automatically daily (1 website daily).
        """
        websites = self.top100_data
        if not websites:
            raise ValueError("No websites found in content/top100_websites.json")

        selected_site = None
        if website_id is not None:
            w_str = str(website_id).strip().lower()
            for site in websites:
                if (
                    str(site.get("global_rank")) == w_str
                    or str(site.get("id")) == w_str
                    or site.get("name", "").lower() == w_str
                    or site.get("domain", "").lower() == w_str
                ):
                    selected_site = site
                    break

        if not selected_site:
            day_of_year = datetime.date.today().timetuple().tm_yday
            selected_idx = (day_of_year - 1) % len(websites)
            selected_site = websites[selected_idx]

        context = {
            "website": selected_site,
            "today_date": datetime.date.today().strftime("%B %d, %Y"),
            "brand_name": config.brand_name,
            "brand_handle": config.brand_handle,
            "website_url": config.website_url,
        }

        template = self.jinja_env.get_template("poster_top100_breakdown.html")
        html = template.render(**context)

        slug = selected_site["name"].lower().replace(" ", "_").replace("/", "_")
        file_name = output_filename or f"top100_rank_{selected_site['global_rank']:03d}_{slug}.png"
        output_file = self.output_dir / "top100" / file_name

        async def _run() -> Path:
            return await self._render_html_to_png(
                html,
                output_file,
                width=1080,
                height=1350,
                device_scale_factor=2,
            )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            rendered_path = loop.run_until_complete(_run())
        finally:
            loop.close()

        return {
            "type": "top100",
            "website": selected_site,
            "image_path": str(rendered_path),
        }

    def render_tech_news(
        self,
        news_id: Optional[str] = None,
        output_filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Renders a 4:5 vertical poster for breaking tech news and architecture updates."""
        news_list = self.tech_news_data
        if not news_list:
            raise ValueError("No tech news articles found in content/tech_news.json")

        selected_news = None
        if news_id:
            for item in news_list:
                if item["id"].lower() == news_id.lower():
                    selected_news = item
                    break

        if not selected_news:
            day_of_year = datetime.date.today().timetuple().tm_yday
            selected_news = news_list[(day_of_year - 1) % len(news_list)]

        context = {
            "news": selected_news,
            "brand_name": config.brand_name,
            "brand_handle": config.brand_handle,
            "website_url": config.website_url,
        }

        template = self.jinja_env.get_template("poster_tech_news.html")
        html = template.render(**context)

        file_name = output_filename or f"tech_news_{selected_news['id']}.png"
        output_file = self.output_dir / "tech_news" / file_name

        async def _run() -> Path:
            return await self._render_html_to_png(
                html,
                output_file,
                width=1080,
                height=1350,
                device_scale_factor=2,
            )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            rendered_path = loop.run_until_complete(_run())
        finally:
            loop.close()

        return {
            "type": "tech_news",
            "news": selected_news,
            "image_path": str(rendered_path),
        }

    def render_website_tip(
        self,
        tip_id: Optional[str] = None,
        output_filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Renders a 4:5 vertical poster for website speed, UX, and Core Web Vitals tips."""
        tips = self.website_tips_data
        if not tips:
            raise ValueError("No website tips found in content/website_tips.json")

        selected_tip = None
        if tip_id:
            for item in tips:
                if item["id"].lower() == tip_id.lower():
                    selected_tip = item
                    break

        if not selected_tip:
            day_of_year = datetime.date.today().timetuple().tm_yday
            selected_tip = tips[(day_of_year - 1) % len(tips)]

        context = {
            "tip": selected_tip,
            "brand_name": config.brand_name,
            "brand_handle": config.brand_handle,
            "website_url": config.website_url,
        }

        template = self.jinja_env.get_template("poster_website_tip.html")
        html = template.render(**context)

        file_name = output_filename or f"tip_{selected_tip['id']}.png"
        output_file = self.output_dir / "website_tips" / file_name

        async def _run() -> Path:
            return await self._render_html_to_png(
                html,
                output_file,
                width=1080,
                height=1350,
                device_scale_factor=2,
            )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            rendered_path = loop.run_until_complete(_run())
        finally:
            loop.close()

        return {
            "type": "website_tip",
            "tip": selected_tip,
            "image_path": str(rendered_path),
        }


def main() -> None:
    """CLI execution entrypoint."""
    parser = argparse.ArgumentParser(description="Headless Graphic & Carousel Renderer")
    parser.add_argument(
        "--type",
        choices=["top100", "tech_news", "website_tip", "carousel", "tech_tip", "all"],
        default="top100",
        help="Type of graphic to render (top100, tech_news, website_tip, carousel, tech_tip, all)",
    )
    parser.add_argument("--website-id", type=str, help="Target website rank or ID for Top 100 breakdown")
    parser.add_argument("--news-id", type=str, help="Target news article ID for tech news")
    parser.add_argument("--tip-id", type=str, help="Target tip ID for website tips")
    parser.add_argument("--city", type=str, help="Target city ID for carousels (e.g. goa, mumbai)")
    parser.add_argument("--niche", type=str, help="Target niche ID for carousels (e.g. restaurants)")
    parser.add_argument(
        "--platform",
        choices=["vertical", "instagram", "linkedin", "twitter", "story", "square", "twitter_landscape", "all"],
        default="vertical",
        help="Target platform preset (default: vertical 1080x1350 4:5)",
    )
    parser.add_argument("--batch-id", type=str, help="Custom folder name for carousel slides")
    parser.add_argument("--dispatch-telegram", action="store_true", help="Auto-dispatch rendered graphics to Telegram")
    args = parser.parse_args()

    renderer = GraphicsRenderer()

    telegram_notifier = None
    if args.dispatch_telegram:
        try:
            from src.telegram_notifier import TelegramNotifier
            telegram_notifier = TelegramNotifier()
        except Exception as e:
            logger.warning("Could not initialize TelegramNotifier: %s", e)

    if args.type == "top100":
        result = renderer.render_top100_breakdown(website_id=args.website_id)
        print(f"\n[Generated Top 100 Website Breakdown #{result['website']['global_rank']}]")
        print(f"Website: {result['website']['name']} ({result['website']['domain']})")
        print(f"Path: {result['image_path']}\n")
        if telegram_notifier:
            telegram_notifier.dispatch_top100(result["image_path"], result["website"])
            print("🚀 Successfully pushed Top 100 breakdown to Telegram!\n")

    elif args.type == "tech_news":
        result = renderer.render_tech_news(news_id=args.news_id)
        print(f"\n[Generated Tech News Poster]")
        print(f"Headline: {result['news']['headline']}")
        print(f"Path: {result['image_path']}\n")
        if telegram_notifier:
            telegram_notifier.dispatch_tech_news(result["image_path"], result["news"])
            print("🚀 Successfully pushed Tech News poster to Telegram!\n")

    elif args.type == "website_tip":
        result = renderer.render_website_tip(tip_id=args.tip_id)
        print(f"\n[Generated Website Speed Tip Poster]")
        print(f"Title: {result['tip']['title']}")
        print(f"Path: {result['image_path']}\n")
        if telegram_notifier:
            telegram_notifier.dispatch_website_tip(result["image_path"], result["tip"])
            print("🚀 Successfully pushed Website Tip poster to Telegram!\n")

    elif args.type == "tech_tip":
        result = renderer.render_tech_tip(tip_id=args.tip_id, platform=args.platform)
        print(f"\n[Generated Tech Tip Graphic]\nTitle: {result['tip']['title']}")
        print(f"Path: {result['image_path']}\n")

    elif args.type == "all":
        # Render 1 of each of the 3 primary pillars + carousel
        print("\n🚀 [Rendering Master Multi-Pillar Suite]...")
        top100_res = renderer.render_top100_breakdown()
        print(f"✅ Top 100 Breakdown: {top100_res['image_path']}")

        news_res = renderer.render_tech_news()
        print(f"✅ Tech News: {news_res['image_path']}")

        tip_res = renderer.render_website_tip()
        print(f"✅ Website Tip: {tip_res['image_path']}")

        carousel_res = renderer.render_carousel_set(
            city_id=args.city, niche_id=args.niche, batch_id=args.batch_id, platform=args.platform
        )
        print(f"✅ Local Carousel ({carousel_res['total_slides']} slides): {carousel_res['output_dir']}\n")

        if telegram_notifier:
            telegram_notifier.dispatch_top100(top100_res["image_path"], top100_res["website"])
            telegram_notifier.dispatch_tech_news(news_res["image_path"], news_res["news"])
            telegram_notifier.dispatch_website_tip(tip_res["image_path"], tip_res["tip"])
            print("🚀 All 3 daily pillars pushed to Telegram!\n")

    else:
        result = renderer.render_carousel_set(
            city_id=args.city,
            niche_id=args.niche,
            batch_id=args.batch_id,
            platform=args.platform,
        )
        print(f"\n[Generated Carousel Set for {args.platform.upper()}]")
        print(f"Target: {result['city']['name']} - {result['niche']['name']}")
        print(f"Slides generated ({result['total_slides']}):")
        for p in result["slide_paths"]:
            print(f"  - {p}")
        print()


if __name__ == "__main__":
    main()
