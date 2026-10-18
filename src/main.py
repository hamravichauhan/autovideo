"""Automated Client Acquisition Funnel & Content Engine - Central Orchestrator.

Runs the complete 24/7 content automation lifecycle:
1. Selects city and business niche from database rotation.
2. Generates rich Programmatic SEO (pSEO) Markdown article.
3. Renders 4-slide high-resolution (1080x1080) visual carousel via Playwright.
4. Builds conversion captions, hashtags, and social threads.
5. Publishes to Meta (Instagram/Facebook), Twitter/X, and commits pSEO articles to Git.
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from src.config import config
from src.generator_graphics import GraphicsRenderer
from src.generator_pseo import PSEOGenerator
from src.publisher import SocialPublisherEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("orchestrator")


class AutomationEngine:
    """End-to-end automation engine coordinator."""

    def __init__(self):
        self.pseo_generator = PSEOGenerator()
        self.graphics_renderer = GraphicsRenderer()
        self.publisher_engine = SocialPublisherEngine()

    def run_daily_funnel(
        self,
        city_id: Optional[str] = None,
        niche_id: Optional[str] = None,
        angle: str = "local_speed",
        render_graphics: bool = True,
        platform: str = "instagram",
    ) -> Dict[str, Any]:
        """Executes full daily client acquisition funnel."""
        start_time = datetime.datetime.now()
        logger.info("=======================================================")
        logger.info("🚀 STARTING AUTOMATED CLIENT ACQUISITION FUNNEL RUN")
        logger.info("=======================================================")

        # 1. Select City and Niche
        city, niche = self.pseo_generator.get_next_city_and_niche(city_id, niche_id)
        logger.info("📍 Target Market Selected: %s (%s, %s)", city["name"], city["region"], city["country"])
        logger.info("🏢 Target Business Niche: %s", niche["name"])
        logger.info("📱 Target Social Platform: %s", platform.upper())

        # 2. Generate Programmatic SEO Blog
        logger.info("\n--- [STEP 1/4] Generating Programmatic SEO Article ---")
        blog_result = self.pseo_generator.generate_article(
            city_id=city["id"], niche_id=niche["id"], angle=angle, save=True
        )
        logger.info("✅ Blog Article Created: %s", blog_result["filepath"])

        # 3. Render High-Resolution Visual Carousel
        graphics_result: Dict[str, Any] = {}
        if render_graphics:
            logger.info("\n--- [STEP 2/4] Headless Rendering 4-Slide Visual Carousel (%s) ---", platform)
            try:
                graphics_result = self.graphics_renderer.render_carousel_set(
                    city_id=city["id"], niche_id=niche["id"], platform=platform
                )
                logger.info(
                    "✅ Rendered %d Carousel Slides to: %s",
                    graphics_result.get("total_slides", 0),
                    graphics_result.get("directory"),
                )
            except Exception as e:
                logger.error("⚠️ Graphic rendering encountered error: %s", e)
                logger.info("Continuing pipeline in text-mode...")
                graphics_result = {
                    "total_slides": 0,
                    "slide_paths": [],
                    "directory": None,
                    "error": str(e),
                }
        else:
            logger.info("\n--- [STEP 2/4] Graphic rendering skipped via flag ---")
            graphics_result = {"total_slides": 0, "slide_paths": []}

        # 4. Social Media Caption Building & Distribution
        logger.info("\n--- [STEP 3/4] Assembling Captions & Multi-Channel Distribution ---")
        slide_paths = graphics_result.get("slide_paths", [])
        campaign_summary = self.publisher_engine.publish_campaign(
            city=city,
            niche=niche,
            slide_image_paths=slide_paths,
            blog_file=blog_result["filepath"],
        )
        logger.info("✅ Social Campaign Dispatched (Status: %s)", "Dry Run / Simulated" if config.dry_run else "Live")

        # 5. Pipeline Summary & Metrics
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info("\n--- [STEP 4/4] Finalizing Run Log ---")

        run_log = {
            "timestamp": start_time.isoformat(),
            "duration_seconds": round(duration, 2),
            "target_city": city["name"],
            "target_niche": niche["name"],
            "blog_article": {
                "title": blog_result["context"]["title"],
                "file": str(blog_result["filepath"]),
                "slug": blog_result["context"]["slug"],
            },
            "graphics": {
                "total_slides": graphics_result.get("total_slides", 0),
                "paths": graphics_result.get("slide_paths", []),
            },
            "social": {
                "caption_preview": campaign_summary.get("caption", "")[:120] + "...",
                "dry_run": config.dry_run,
                "meta_status": campaign_summary.get("meta_result", {}).get("status"),
            },
            "lead_capture": {
                "whatsapp_cta": config.whatsapp_click_to_chat_url,
                "intake_form": config.google_form_intake_url,
            },
        }

        # Save run log
        log_file = config.portfolio_blog_path.parent / "automation_log.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(run_log, f, indent=2)

        logger.info("🏁 Pipeline completed successfully in %.2f seconds!", duration)
        logger.info("Log file updated: %s\n", log_file)
        return run_log


def main() -> None:
    """CLI orchestrator entrypoint."""
    parser = argparse.ArgumentParser(
        description="24/7 Automated Client Acquisition Funnel & Content Engine"
    )
    parser.add_argument(
        "--mode",
        choices=["daily", "all", "pseo", "graphics", "tech_tip", "social"],
        default="daily",
        help="Pipeline execution mode",
    )
    parser.add_argument("--city", type=str, help="Specific target city ID (e.g., goa, mumbai, bangalore)")
    parser.add_argument("--niche", type=str, help="Specific target niche ID (e.g., restaurants, boutique-hotels)")
    parser.add_argument(
        "--angle",
        choices=["local_speed", "tech_comparison", "automation", "random"],
        default="local_speed",
        help="Content angle for pSEO generation",
    )
    parser.add_argument(
        "--platform",
        choices=["instagram", "linkedin", "twitter", "square", "all"],
        default="instagram",
        help="Target platform layout (instagram: 1080x1350, twitter: 1200x675, square: 1080x1080, all: multi-format)",
    )
    parser.add_argument("--no-graphics", action="store_true", help="Skip Playwright graphic rendering")
    parser.add_argument("--dry-run", action="store_true", default=None, help="Force dry-run simulation mode")

    args = parser.parse_args()

    engine = AutomationEngine()

    if args.mode in ("daily", "all"):
        engine.run_daily_funnel(
            city_id=args.city,
            niche_id=args.niche,
            angle=args.angle,
            render_graphics=not args.no_graphics,
            platform=args.platform,
        )
    elif args.mode == "pseo":
        res = engine.pseo_generator.generate_article(
            city_id=args.city, niche_id=args.niche, angle=args.angle
        )
        print(f"\n[pSEO Generated] {res['context']['title']}")
        print(f"Path: {res['filepath']}")
    elif args.mode == "graphics":
        res = engine.graphics_renderer.render_carousel_set(
            city_id=args.city, niche_id=args.niche, platform=args.platform
        )
        print(f"\n[Graphics Generated] {res['batch_id']}")
        for p in res["slide_paths"]:
            print(f"  - {p}")
    elif args.mode == "tech_tip":
        res = engine.graphics_renderer.render_tech_tip()
        print(f"\n[Tech Tip Generated] {res['tip']['title']}")
        print(f"Path: {res['image_path']}")
    elif args.mode == "social":
        city, niche = engine.pseo_generator.get_next_city_and_niche(args.city, args.niche)
        caption = engine.publisher_engine.caption_builder.build_carousel_caption(city, niche)
        print("\n=== GENERATED CAPTION ===")
        print(caption)
        print("\n=== GENERATED TWITTER THREAD ===")
        thread = engine.publisher_engine.caption_builder.build_twitter_thread(city, niche)
        for i, t in enumerate(thread, 1):
            print(f"\n[Tweet {i}]\n{t}")


if __name__ == "__main__":
    main()
