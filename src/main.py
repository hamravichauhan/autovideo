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

    def run_dev_track(
        self,
        website_id: Optional[str] = None,
        tip_id: Optional[str] = None,
        render_graphics: bool = True,
        render_video: bool = True,
    ) -> Dict[str, Any]:
        """Executes isolated Track 1: Dev Content & Architecture.
        
        Renders Top 100 System Architecture breakdown (Instagram & LinkedIn),
        renders Developer Performance Blueprint code snippet,
        renders 60s Architecture Video Reel,
        and dispatches to Telegram under the strict Track 1 Dev Header.
        """
        logger.info("=======================================================")
        logger.info("🛠️ [TRACK 1] RUNNING DEV CONTENT & SYSTEM ARCHITECTURE")
        logger.info("=======================================================")

        from src.tracker import get_next_top100_rank
        daily_rank = int(website_id) if website_id else get_next_top100_rank(advance=True)

        top100_result: Dict[str, Any] = {}
        tip_result: Dict[str, Any] = {}
        top100_video_result: Optional[Dict[str, Any]] = None

        if render_graphics:
            try:
                top100_result = self.graphics_renderer.render_top100_breakdown(
                    website_id=str(daily_rank), platform="all"
                )
                logger.info("✅ Rendered Top 100 Teardown: #%d %s", top100_result["website"]["global_rank"], top100_result["website"]["name"])
            except Exception as e:
                logger.error("⚠️ Error rendering Top 100 slides: %s", e)

            try:
                tip_result = self.graphics_renderer.render_website_tip(tip_id=tip_id)
                logger.info("✅ Rendered Dev Performance Blueprint: %s", tip_result["tip"]["title"])
            except Exception as e:
                logger.error("⚠️ Error rendering Dev tip poster: %s", e)

            if render_video and top100_result and top100_result.get("website"):
                try:
                    from src.generator_video import VideoReelGenerator
                    top100_gen = VideoReelGenerator()
                    top100_video_result = top100_gen.render_top100_reel(
                        website_id=top100_result["website"]["global_rank"],
                        aspect_ratio="9:16",
                    )
                    logger.info("✅ Rendered 60s Top 100 Video Reel: %s", top100_video_result["video_path"])
                except Exception as e:
                    logger.warning("Could not render Top 100 video reel: %s", e)

        # Telegram Dispatch under strict Track 1 Isolation
        tg_res: Dict[str, Any] = {}
        try:
            from src.telegram_notifier import TelegramNotifier
            notifier = TelegramNotifier()
            tg_res = notifier.dispatch_dev_track(
                top100_platforms=top100_result.get("platform_slides"),
                website=top100_result.get("website"),
                dev_tip_path=tip_result.get("image_path"),
                dev_tip=tip_result.get("tip"),
                video_path=top100_video_result.get("video_path") if top100_video_result else None,
                video_caption=top100_video_result.get("caption_text") if top100_video_result else None,
            )
            logger.info("📲 Telegram Track 1 (Dev) Dispatched: %s", tg_res.get("ok"))
        except Exception as tg_err:
            logger.warning("Telegram Track 1 dispatch error: %s", tg_err)

        return {
            "track": "dev",
            "top100": top100_result,
            "tip": tip_result,
            "video": top100_video_result,
            "telegram": tg_res,
        }

    def run_news_track(
        self,
        news_id: Optional[str] = None,
        render_graphics: bool = True,
    ) -> Dict[str, Any]:
        """Executes isolated Track 2: Breaking Tech News & Industry Radar.
        
        Renders breaking Tech News poster, builds X (Twitter) breaking news post,
        and dispatches to Telegram under the strict Track 2 News Header.
        """
        logger.info("=======================================================")
        logger.info("📡 [TRACK 2] RUNNING BREAKING TECH NEWS & RADAR")
        logger.info("=======================================================")

        news_result: Dict[str, Any] = {}
        if render_graphics:
            try:
                news_result = self.graphics_renderer.render_tech_news(news_id=news_id)
                logger.info("✅ Rendered Tech News Poster: %s", news_result["news"]["headline"])
            except Exception as e:
                logger.error("⚠️ Error rendering Tech News poster: %s", e)

        tg_res: Dict[str, Any] = {}
        if news_result and news_result.get("image_path"):
            try:
                from src.telegram_notifier import TelegramNotifier
                notifier = TelegramNotifier()
                tg_res = notifier.dispatch_news_track(
                    image_path=news_result["image_path"],
                    news=news_result["news"],
                )
                logger.info("📲 Telegram Track 2 (News) Dispatched: %s", tg_res.get("ok"))
            except Exception as tg_err:
                logger.warning("Telegram Track 2 dispatch error: %s", tg_err)

        return {
            "track": "news",
            "news": news_result,
            "telegram": tg_res,
        }

    def run_local_track(
        self,
        city_id: Optional[str] = None,
        niche_id: Optional[str] = None,
        angle: str = "local_speed",
        render_graphics: bool = True,
        render_video: bool = True,
        platform: str = "vertical",
    ) -> Dict[str, Any]:
        """Executes isolated Track 3: Local B2B Client Acquisition Funnel.
        
        Generates pSEO blog case study, renders 4-slide local carousel,
        renders 30s local speed audit reel, runs outbound prospecting,
        and dispatches to Telegram under the strict Track 3 Local Header.
        """
        logger.info("=======================================================")
        logger.info("📍 [TRACK 3] RUNNING LOCAL B2B CLIENT ACQUISITION")
        logger.info("=======================================================")

        city, niche = self.pseo_generator.get_next_city_and_niche(city_id, niche_id)
        logger.info("📍 Target Market: %s — %s", city["name"], niche["name"])

        blog_result = self.pseo_generator.generate_article(
            city_id=city["id"], niche_id=niche["id"], angle=angle, save=True
        )

        graphics_result: Dict[str, Any] = {}
        video_result: Optional[Dict[str, Any]] = None

        if render_graphics:
            try:
                graphics_result = self.graphics_renderer.render_carousel_set(
                    city_id=city["id"], niche_id=niche["id"], platform=platform
                )
                slide_paths = graphics_result.get("slide_paths", [])
                if render_video and len(slide_paths) >= 4:
                    from src.generator_video import VideoReelGenerator
                    v_gen = VideoReelGenerator()
                    video_result = v_gen.render_reel(
                        slide_images=slide_paths[:4],
                        city=city,
                        niche=niche,
                        aspect_ratio="9:16",
                    )
            except Exception as e:
                logger.error("⚠️ Local graphics rendering error: %s", e)

        slide_paths = graphics_result.get("slide_paths", [])
        campaign_summary = self.publisher_engine.publish_campaign(
            city=city,
            niche=niche,
            slide_image_paths=slide_paths,
            blog_file=blog_result["filepath"],
        )

        tg_res: Dict[str, Any] = {}
        try:
            from src.telegram_notifier import TelegramNotifier
            notifier = TelegramNotifier()
            tg_res = notifier.dispatch_local_track(
                blog_data=blog_result,
                city=city,
                niche=niche,
                carousel_slides=slide_paths[:4],
                instagram_caption=campaign_summary.get("caption"),
                video_path=video_result.get("video_path") if video_result else None,
                video_caption=video_result.get("caption_text") if video_result else None,
            )
            logger.info("📲 Telegram Track 3 (Local) Dispatched: %s", tg_res.get("ok"))
        except Exception as tg_err:
            logger.warning("Telegram Track 3 dispatch error: %s", tg_err)

        prospecting_result = self.prospecting_engine.run_prospecting_batch(
            city_id=city["id"], niche_id=niche["id"], count=5
        )

        return {
            "track": "local",
            "city": city,
            "niche": niche,
            "blog": blog_result,
            "graphics": graphics_result,
            "video": video_result,
            "prospecting": prospecting_result,
            "telegram": tg_res,
        }

    def run_daily_funnel(
        self,
        city_id: Optional[str] = None,
        niche_id: Optional[str] = None,
        angle: str = "local_speed",
        render_graphics: bool = True,
        platform: str = "vertical",
    ) -> Dict[str, Any]:
        """Sequentially executes each isolated track with clean boundaries."""
        start_time = datetime.datetime.now()
        logger.info("=======================================================")
        logger.info("🚀 STARTING AUTOMATED MULTI-TRACK DAILY SUITE")
        logger.info("=======================================================")

        # Track 1: Dev Content & Architecture
        dev_res = self.run_dev_track(render_graphics=render_graphics, render_video=render_graphics)

        # Track 2: Breaking Tech News & Radar
        news_res = self.run_news_track(render_graphics=render_graphics)

        # Track 3: Local B2B Client Acquisition
        local_res = self.run_local_track(
            city_id=city_id, niche_id=niche_id, angle=angle, render_graphics=render_graphics, platform=platform
        )

        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()

        run_log = {
            "timestamp": start_time.isoformat(),
            "duration_seconds": round(duration, 2),
            "dev_track": {"status": "completed", "rank": dev_res.get("top100", {}).get("website", {}).get("global_rank")},
            "news_track": {"status": "completed", "headline": news_res.get("news", {}).get("news", {}).get("headline")},
            "local_track": {"status": "completed", "city": local_res.get("city", {}).get("name"), "niche": local_res.get("niche", {}).get("name")},
        }

        log_file = config.portfolio_blog_path.parent / "automation_log.json"
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(run_log, f, indent=2)
        except Exception:
            pass

        logger.info("🏁 Multi-track daily run completed successfully in %.2f seconds!", duration)
        return run_log


def main() -> None:
    """CLI orchestrator entrypoint."""
    parser = argparse.ArgumentParser(
        description="24/7 Automated Client Acquisition Funnel & Content Engine"
    )
    parser.add_argument(
        "--mode",
        choices=["daily", "dev", "news", "local", "all", "video", "top100", "tech_news", "website_tip", "pseo", "graphics", "tech_tip", "social", "prospect", "telegram"],
        default="daily",
        help="Pipeline execution mode: 'dev' (Dev content/code), 'news' (Tech news radar), 'local' (Client acquisition), 'daily' (All isolated tracks)",
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

    if args.mode == "dev":
        res = engine.run_dev_track(
            website_id=args.website_id,
            tip_id=args.tip_id,
            render_graphics=not args.no_graphics,
            render_video=not args.no_graphics,
        )
        print(f"\n[ExtrovertNerd Dev Track Complete]")
        print(f"Top 100 Rank: {res.get('top100', {}).get('website', {}).get('global_rank')}")
        print(f"Website Tip: {res.get('tip', {}).get('tip', {}).get('title')}")
        print("🚀 Dispatched strictly to LinkedIn & Instagram queue on Telegram!")

    elif args.mode == "news":
        res = engine.run_news_track(
            news_id=args.news_id,
            render_graphics=not args.no_graphics,
        )
        print(f"\n[ExtrovertNerd Tech News Track Complete]")
        print(f"Headline: {res.get('news', {}).get('news', {}).get('headline')}")
        print("🚀 Dispatched strictly to X (Twitter) queue on Telegram!")

    elif args.mode == "local":
        res = engine.run_local_track(
            city_id=args.city,
            niche_id=args.niche,
            angle=args.angle,
            render_graphics=not args.no_graphics,
            render_video=not args.no_graphics,
            platform=args.platform,
        )
        print(f"\n[ExtrovertNerd Local Acquisition Funnel Complete]")
        print(f"Target: {res['city']['name']} — {res['niche']['name']}")
        print(f"Blog: {res['blog']['filepath']}")
        print("🚀 Dispatched strictly to Website Blog & Local IG/FB queue on Telegram!")

    elif args.mode in ("daily", "all"):
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
