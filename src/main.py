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

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import config
from src.generator_graphics import GraphicsRenderer
from src.generator_pseo import PSEOGenerator
from src.prospecting_engine import ProspectingEngine
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
        self.prospecting_engine = ProspectingEngine()

    def run_daily_funnel(
        self,
        city_id: Optional[str] = None,
        niche_id: Optional[str] = None,
        angle: str = "local_speed",
        render_graphics: bool = True,
        platform: str = "vertical",
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

        # 3. Render High-Resolution Visual Carousel (Local Niche Funnel)
        graphics_result: Dict[str, Any] = {}
        top100_result: Dict[str, Any] = {}
        if render_graphics:
            logger.info("\n--- [STEP 2/5] Headless Rendering Visual Assets (%s) ---", platform)
            try:
                # 3a. Local Business Case Study Carousel (4 Slides)
                graphics_result = self.graphics_renderer.render_carousel_set(
                    city_id=city["id"], niche_id=niche["id"], platform=platform
                )
                logger.info(
                    "✅ Rendered %d Local Carousel Slides to: %s",
                    graphics_result.get("total_slides", 0),
                    graphics_result.get("directory"),
                )

                # 3b. Daily Top 100 Website Teardown (2 Slides across Instagram, LinkedIn, and X)
                top100_result = self.graphics_renderer.render_top100_breakdown(platform="all")
                logger.info(
                    "✅ Rendered Daily Top 100 Teardown: #%d %s (6 slides across 3 platforms)",
                    top100_result["website"]["global_rank"],
                    top100_result["website"]["name"],
                )

                # 3c. Automated 30-Second Video Reel (Edge-TTS + Ken Burns Motion + Synced Captions)
                slide_paths = graphics_result.get("slide_paths", [])
                if len(slide_paths) >= 4:
                    video_generator = VideoReelGenerator()
                    video_result = video_generator.render_reel(
                        slide_images=slide_paths[:4],
                        city=city,
                        niche=niche,
                        aspect_ratio="9:16",
                    )
                    logger.info("✅ Rendered 30s Video Reel: %s (%.2f MB)", video_result["video_path"], video_result["filesize_mb"])

                top100_video_result = None
                if top100_result and top100_result.get("website"):
                    try:
                        from src.generator_video import VideoReelGenerator
                        top100_gen = VideoReelGenerator()
                        top100_video_result = top100_gen.render_top100_reel(
                            website_id=top100_result["website"]["global_rank"],
                            aspect_ratio="9:16",
                        )
                        logger.info("✅ Rendered 60s Top 100 Video Reel: %s (%.2f MB)", top100_video_result["video_path"], top100_video_result["filesize_mb"])
                    except Exception as e_top_v:
                        logger.warning("Could not render Top 100 video reel: %s", e_top_v)
            except Exception as e:
                logger.error("⚠️ Graphic/Video rendering encountered error: %s", e)
                logger.info("Continuing pipeline in text-mode...")
                graphics_result = {
                    "total_slides": 0,
                    "slide_paths": [],
                    "directory": None,
                    "error": str(e),
                }
        else:
            logger.info("\n--- [STEP 2/5] Graphic rendering skipped via flag ---")
            graphics_result = {"total_slides": 0, "slide_paths": []}

        # 4. Social Media Caption Building & Distribution
        logger.info("\n--- [STEP 3/5] Assembling Captions & Multi-Channel Distribution ---")
        slide_paths = graphics_result.get("slide_paths", [])
        campaign_summary = self.publisher_engine.publish_campaign(
            city=city,
            niche=niche,
            slide_image_paths=slide_paths,
            blog_file=blog_result["filepath"],
        )
        logger.info("✅ Social Campaign Assembled (Status: %s)", "Dry Run / Simulated" if config.dry_run else "Live")

        # 5. Telegram Automated Multi-Platform Dispatch
        logger.info("\n--- [STEP 4/5] Telegram Multi-Platform Dispatch (8:00 AM Pack) ---")
        try:
            from src.telegram_notifier import TelegramNotifier
            notifier = TelegramNotifier()

            # 5a. Dispatch Top 100 Teardown with dedicated platform labels & captions (IG, LinkedIn, X)
            if top100_result and top100_result.get("platform_slides"):
                tg_top100 = notifier.dispatch_top100(
                    top100_result["platform_slides"],
                    top100_result["website"],
                )
                logger.info("📲 Telegram Top 100 Dispatch: %s", "Dispatched" if tg_top100.get("ok") else tg_top100.get("error"))

            # 5b. Dispatch Local Carousel (Instagram) + Live Blog on Website + X (Twitter) Promo Thread
            thread_tweets = campaign_summary.get("twitter_thread") or self.publisher_engine.build_twitter_thread(city, niche)
            tg_blog = notifier.dispatch_blog_and_x(
                blog_data=blog_result,
                city=city,
                niche=niche,
                twitter_thread=thread_tweets,
                carousel_slides=slide_paths[:4],
                instagram_caption=campaign_summary.get("caption"),
            )
            logger.info("📲 Telegram Blog & X Thread Dispatch: %s", "Dispatched" if tg_blog.get("ok") else tg_blog.get("error"))

            # 5c. Dispatch 30s High-Retention Video Reel to Telegram (Reels / Shorts / TikTok)
            if video_result and video_result.get("video_path"):
                tg_vid = notifier.dispatch_video_reel(
                    video_path=video_result["video_path"],
                    city=city,
                    niche=niche,
                    caption=video_result.get("caption_text"),
                    duration=int(video_result.get("duration", 30)),
                )
                logger.info("📲 Telegram Video Reel Dispatch: %s", "Dispatched" if tg_vid.get("ok") else tg_vid.get("error"))

            # 5d. Dispatch 60s Top 100 Video Reel to Telegram (Reels / Shorts / TikTok)
            if top100_video_result and top100_video_result.get("video_path"):
                tg_top_vid = notifier.dispatch_top100_video_reel(
                    video_path=top100_video_result["video_path"],
                    site=top100_result["website"],
                    caption=top100_video_result.get("caption_text"),
                    duration=int(top100_video_result.get("duration", 60)),
                )
                logger.info("📲 Telegram Top 100 Video Reel Dispatch: %s", "Dispatched" if tg_top_vid.get("ok") else tg_top_vid.get("error"))
        except Exception as tg_err:
            logger.warning("Telegram dispatch encountered warning: %s", tg_err)

        # 6. Outbound Local Prospecting & Outreach Generation
        logger.info("\n--- [STEP 5/5] Running Local Prospecting Engine ---")
        prospecting_result = self.prospecting_engine.run_prospecting_batch(
            city_id=city["id"], niche_id=niche["id"], count=5
        )
        logger.info("✅ Generated %d Local Outreach Drafts: %s", prospecting_result["count"], prospecting_result["outreach_deck_md"])

        # 7. Pipeline Summary & Metrics
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info("\n--- [STEP 5/5] Finalizing Run Log ---")

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
            "prospecting": {
                "leads_count": prospecting_result["count"],
                "deck": prospecting_result["outreach_deck_md"],
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
        choices=["daily", "all", "video", "top100", "tech_news", "website_tip", "pseo", "graphics", "tech_tip", "social", "prospect", "telegram"],
        default="daily",
        help="Pipeline execution mode",
    )
    parser.add_argument("--city", type=str, help="Specific target city ID (e.g., goa, mumbai, bangalore)")
    parser.add_argument("--niche", type=str, help="Specific target niche ID (e.g., restaurants, boutique-hotels)")
    parser.add_argument("--website-id", type=str, help="Website rank/ID for top100 breakdown")
    parser.add_argument("--news-id", type=str, help="News article ID for tech news poster")
    parser.add_argument("--tip-id", type=str, help="Tip ID for website performance poster")
    parser.add_argument(
        "--angle",
        choices=["local_speed", "tech_comparison", "automation", "random"],
        default="local_speed",
        help="Content angle for pSEO generation",
    )
    parser.add_argument(
        "--platform",
        choices=["vertical", "instagram", "linkedin", "twitter", "story", "square", "twitter_landscape", "all"],
        default="vertical",
        help="Target platform layout (vertical/instagram/linkedin/twitter: 1080x1350, story: 1080x1920, square: 1080x1080, all: multi-format)",
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
    elif args.mode == "top100":
        res = engine.graphics_renderer.render_top100_breakdown(
            website_id=args.website_id,
            platform=args.platform,
        )
        print(f"\n[ExtrovertNerd Top 100 Breakdown] #{res['website']['global_rank']} {res['website']['name']}")
        print(f"Target Platforms: {', '.join(res.get('target_platforms', []))}")
        for plat, slides in res.get("platform_slides", {}).items():
            print(f"  • {plat.upper()}:")
            for s in slides:
                print(f"      - {s}")
        try:
            from src.telegram_notifier import TelegramNotifier
            TelegramNotifier().dispatch_top100(
                res.get("platform_slides", res.get("image_paths", res.get("image_path"))),
                res["website"],
            )
            print("🚀 Pushed multi-slide albums with platform captions to Telegram channel!")
        except Exception as e:
            print(f"Telegram notice: {e}")
    elif args.mode == "tech_news":
        res = engine.graphics_renderer.render_tech_news(news_id=args.news_id)
        print(f"\n[ExtrovertNerd Tech News Poster] {res['news']['headline']}")
        print(f"File: {res['image_path']}")
        try:
            from src.telegram_notifier import TelegramNotifier
            TelegramNotifier().dispatch_tech_news(res["image_path"], res["news"])
            print("🚀 Pushed to Telegram channel!")
        except Exception as e:
            print(f"Telegram notice: {e}")
    elif args.mode == "website_tip":
        res = engine.graphics_renderer.render_website_tip(tip_id=args.tip_id)
        print(f"\n[ExtrovertNerd Website Tip Poster] {res['tip']['title']}")
        print(f"File: {res['image_path']}")
        try:
            from src.telegram_notifier import TelegramNotifier
            TelegramNotifier().dispatch_website_tip(res["image_path"], res["tip"])
            print("🚀 Pushed to Telegram channel!")
        except Exception as e:
            print(f"Telegram notice: {e}")
    elif args.mode == "prospect":
        res = engine.prospecting_engine.run_prospecting_batch(
            city_id=args.city, niche_id=args.niche, count=5
        )
        print(f"\n[ExtrovertNerd Prospecting Complete]")
        print(f"Target: {res['city']} — {res['niche']}")
        print(f"Deck: {res['outreach_deck_md']}")
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
        try:
            from src.telegram_notifier import TelegramNotifier
            tg_res = TelegramNotifier().dispatch_latest_graphics()
            print(f"\n[Telegram Bot Dispatch] Status: {tg_res.get('ok')}")
        except Exception as tg_err:
            print(f"\n[Telegram Bot Dispatch] Note: {tg_err}")
    elif args.mode == "telegram":
        from src.telegram_notifier import TelegramNotifier
        notifier = TelegramNotifier()
        test_info = notifier.test_connection()
        print("\n[Telegram Bot Status]")
        print(json.dumps(test_info, indent=2))
        res = notifier.dispatch_latest_graphics()
        print("\n[Telegram Dispatch Results]")
        print(json.dumps(res, indent=2))
    elif args.mode == "video":
        from src.generator_video import VideoReelGenerator
        gen = VideoReelGenerator()
        if args.website_id:
            res = gen.render_top100_reel(website_id=args.website_id, aspect_ratio=args.platform if args.platform in ("9:16", "4:5") else "9:16")
        else:
            res = gen.render_latest_carousel_reel(aspect_ratio=args.platform if args.platform in ("9:16", "4:5") else "9:16")

        print("\n=== VIDEO REEL GENERATION COMPLETE ===")
        print(f"🎬 Video File:    {res['video_path']}")
        print(f"⏱️ Duration:      {res['duration']}s")
        print(f"💾 File Size:     {res['filesize_mb']} MB")
        print(f"📐 Resolution:    {res['resolution']}")
        print(f"📋 Caption File:  {res['caption_path']}")
        try:
            from src.telegram_notifier import TelegramNotifier
            notifier = TelegramNotifier()
            if res.get("type") == "top100_60s_reel":
                notifier.dispatch_top100_video_reel(
                    video_path=res["video_path"],
                    site=res["website"],
                    caption=res["caption_text"],
                    duration=int(res["duration"]),
                )
                print("🚀 Pushed 60s Top 100 Video Reel to Telegram channel!")
            else:
                notifier.dispatch_video_reel(
                    video_path=res["video_path"],
                    city=res["city"],
                    niche=res["niche"],
                    caption=res["caption_text"],
                    duration=int(res["duration"]),
                )
                print("🚀 Pushed 30s Video Reel to Telegram channel!")
        except Exception as e:
            print(f"Telegram notice: {e}")
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
