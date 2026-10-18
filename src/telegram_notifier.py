"""Telegram Bot Notifier for ExtrovertNerd.

Automatically sends generated carousels, posters, and tech tips
directly to the user's Telegram chat or channel using the Telegram Bot API.
"""

from __future__ import annotations

import argparse
import glob
import json
import logging
import os
import sys
import datetime
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid

from src.config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("telegram_notifier")


class TelegramNotifier:
    """Dispatches rendered marketing graphics and alert notifications to Telegram."""

    def __init__(
        self,
        bot_token: Optional[str] = None,
        chat_id: Optional[str] = None,
    ):
        self.bot_token = (
            bot_token
            or os.getenv("TELEGRAM_BOT_TOKEN")
            or "80208646:AAHbnjZm0ZhHrxXLkamH8yF7ozkmBX2zurw"
        ).strip()
        self.chat_id = (
            chat_id
            or os.getenv("TELEGRAM_CHAT_ID")
            or "1432790039"
        ).strip()
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def test_connection(self) -> Dict[str, Any]:
        """Tests whether the configured bot token is valid and returns bot profile."""
        url = f"{self.base_url}/getMe"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ExtrovertNerdBot/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                return {
                    "ok": True,
                    "status": "connected",
                    "bot": data.get("result", {}),
                    "token_prefix": self.bot_token[:10] + "...",
                }
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            logger.warning("Telegram Bot HTTP error: %s (%s)", e.code, error_body)
            return {
                "ok": False,
                "status": f"HTTP {e.code}",
                "error": error_body,
                "hint": "Check if token was revoked or has missing digits in bot ID.",
            }
        except Exception as e:
            logger.warning("Telegram Bot connection error: %s", e)
            return {
                "ok": False,
                "status": "connection_error",
                "error": str(e),
            }

    def send_message(self, text: str, parse_mode: str = "HTML") -> Dict[str, Any]:
        """Sends a text message to the configured chat with retry handling."""
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False,
        }
        data = urllib.parse.urlencode(payload).encode("utf-8")

        for attempt in range(1, 4):
            try:
                time.sleep(0.8)  # Polite pause between Telegram calls
                req = urllib.request.Request(url, data=data, headers={"User-Agent": "ExtrovertNerdBot/1.0", "Connection": "close"})
                with urllib.request.urlopen(req, timeout=20) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8", errors="ignore")
                logger.warning("Telegram send_message HTTP %d (attempt %d/3): %s", e.code, attempt, error_body)
                if attempt == 3:
                    return {"ok": False, "error": error_body, "code": e.code}
                time.sleep(2.0 * attempt)
            except Exception as e:
                logger.warning("Telegram send_message network error (attempt %d/3): %s", attempt, e)
                if attempt == 3:
                    return {"ok": False, "error": str(e)}
                time.sleep(2.0 * attempt)
        return {"ok": False, "error": "Max retries exceeded"}

    def send_photo(self, photo_path: Path | str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Sends a single photo using multipart/form-data with retry handling."""
        path = Path(photo_path)
        if not path.exists():
            return {"ok": False, "error": f"File not found: {path}"}

        url = f"{self.base_url}/sendPhoto"
        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
        body = bytearray()

        # chat_id field
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{self.chat_id}\r\n'.encode("utf-8"))

        # caption field
        if caption:
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend('Content-Disposition: form-data; name="caption"\r\n\r\n'.encode("utf-8"))
            body.extend(f"{caption}\r\n".encode("utf-8"))
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend('Content-Disposition: form-data; name="parse_mode"\r\n\r\nHTML\r\n'.encode("utf-8"))

        # photo file
        filename = path.name
        content_type = "image/png" if filename.lower().endswith(".png") else "image/jpeg"
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="photo"; filename="{filename}"\r\n'.encode("utf-8"))
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        with open(path, "rb") as f:
            body.extend(f.read())
        body.extend(b"\r\n")

        # closing boundary
        body.extend(f"--{boundary}--\r\n".encode("utf-8"))

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "ExtrovertNerdBot/1.0",
            "Connection": "close",
        }

        for attempt in range(1, 4):
            try:
                time.sleep(1.2)  # Allow socket to settle
                req = urllib.request.Request(url, data=bytes(body), headers=headers)
                with urllib.request.urlopen(req, timeout=35) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    logger.info("✅ Sent photo to Telegram: %s", filename)
                    return result
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8", errors="ignore")
                logger.warning("Telegram send_photo HTTP %d (attempt %d/3): %s", e.code, attempt, error_body)
                if attempt == 3:
                    return {"ok": False, "error": error_body, "code": e.code}
                time.sleep(2.5 * attempt)
            except Exception as e:
                logger.warning("Telegram send_photo network error (attempt %d/3): %s", attempt, e)
                if attempt == 3:
                    return {"ok": False, "error": str(e)}
                time.sleep(2.5 * attempt)
        return {"ok": False, "error": "Max retries exceeded"}

    def send_media_group(self, photo_paths: List[Path | str], caption: Optional[str] = None) -> Dict[str, Any]:
        """Sends a set of carousel slides as an interactive swipeable album (media group) with retry handling."""
        valid_paths = [Path(p) for p in photo_paths if Path(p).exists()]
        if not valid_paths:
            return {"ok": False, "error": "No valid photo paths provided."}

        # Telegram limits media groups to max 10 items
        valid_paths = valid_paths[:10]

        url = f"{self.base_url}/sendMediaGroup"
        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
        body = bytearray()

        # chat_id
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{self.chat_id}\r\n'.encode("utf-8"))

        # media JSON array
        media_list = []
        for i, path in enumerate(valid_paths):
            attach_name = f"photo_{i}"
            item = {
                "type": "photo",
                "media": f"attach://{attach_name}",
            }
            if i == 0 and caption:
                item["caption"] = caption
                item["parse_mode"] = "HTML"
            media_list.append(item)

        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="media"\r\n\r\n{json.dumps(media_list)}\r\n'.encode("utf-8"))

        # attach each image file
        for i, path in enumerate(valid_paths):
            attach_name = f"photo_{i}"
            filename = path.name
            content_type = "image/png" if filename.lower().endswith(".png") else "image/jpeg"
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="{attach_name}"; filename="{filename}"\r\n'.encode("utf-8"))
            body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
            with open(path, "rb") as f:
                body.extend(f.read())
            body.extend(b"\r\n")

        body.extend(f"--{boundary}--\r\n".encode("utf-8"))

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "ExtrovertNerdBot/1.0",
            "Connection": "close",
        }

        for attempt in range(1, 4):
            try:
                time.sleep(1.5)  # Allow socket to settle for multi-image upload
                req = urllib.request.Request(url, data=bytes(body), headers=headers)
                with urllib.request.urlopen(req, timeout=50) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    logger.info("✅ Sent carousel album (%d slides) to Telegram", len(valid_paths))
                    return result
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8", errors="ignore")
                logger.warning("Telegram send_media_group HTTP %d (attempt %d/3): %s", e.code, attempt, error_body)
                if attempt == 3:
                    return {"ok": False, "error": error_body, "code": e.code}
                time.sleep(3.0 * attempt)
            except Exception as e:
                logger.warning("Telegram send_media_group network error (attempt %d/3): %s", attempt, e)
                if attempt == 3:
                    return {"ok": False, "error": str(e)}
                time.sleep(3.0 * attempt)
        return {"ok": False, "error": "Max retries exceeded"}

    def send_video(
        self,
        video_path: Path | str,
        caption: Optional[str] = None,
        duration: Optional[int] = None,
        width: int = 1080,
        height: int = 1920,
    ) -> Dict[str, Any]:
        """Sends an MP4 video (Instagram Reel / YouTube Short / TikTok) with retry handling."""
        path = Path(video_path)
        if not path.exists():
            return {"ok": False, "error": f"File not found: {path}"}

        url = f"{self.base_url}/sendVideo"
        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
        body = bytearray()

        # chat_id
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{self.chat_id}\r\n'.encode("utf-8"))

        # supports_streaming
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend('Content-Disposition: form-data; name="supports_streaming"\r\n\r\ntrue\r\n'.encode("utf-8"))

        # width & height
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="width"\r\n\r\n{width}\r\n'.encode("utf-8"))
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="height"\r\n\r\n{height}\r\n'.encode("utf-8"))

        if duration:
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="duration"\r\n\r\n{int(duration)}\r\n'.encode("utf-8"))

        # caption
        if caption:
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend('Content-Disposition: form-data; name="caption"\r\n\r\n'.encode("utf-8"))
            body.extend(f"{caption}\r\n".encode("utf-8"))
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend('Content-Disposition: form-data; name="parse_mode"\r\n\r\nHTML\r\n'.encode("utf-8"))

        # video file
        filename = path.name
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="video"; filename="{filename}"\r\n'.encode("utf-8"))
        body.extend(b"Content-Type: video/mp4\r\n\r\n")
        with open(path, "rb") as f:
            body.extend(f.read())
        body.extend(b"\r\n")

        # closing boundary
        body.extend(f"--{boundary}--\r\n".encode("utf-8"))

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "ExtrovertNerdBot/1.0",
            "Connection": "close",
        }

        for attempt in range(1, 4):
            try:
                time.sleep(1.5)
                req = urllib.request.Request(url, data=bytes(body), headers=headers)
                with urllib.request.urlopen(req, timeout=90) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    logger.info("✅ Sent video reel to Telegram: %s", filename)
                    return result
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8", errors="ignore")
                logger.warning("Telegram send_video HTTP %d (attempt %d/3): %s", e.code, attempt, error_body)
                if attempt == 3:
                    return {"ok": False, "error": error_body, "code": e.code}
                time.sleep(3.0 * attempt)
            except Exception as e:
                logger.warning("Telegram send_video network error (attempt %d/3): %s", attempt, e)
                if attempt == 3:
                    return {"ok": False, "error": str(e)}
                time.sleep(3.0 * attempt)
        return {"ok": False, "error": "Max retries exceeded"}

    # =========================================================================
    # PLATFORM-SPECIFIC CAPTION BUILDERS
    # =========================================================================

    @staticmethod
    def build_top100_instagram_caption(website: Dict[str, Any]) -> str:
        """Constructs an Instagram-optimized caption with hooks, carousel cues, and hashtags."""
        rank = website.get("global_rank", 1)
        name = website.get("name", "Architecture")
        domain = website.get("domain", "")
        category = website.get("category", "Web Architecture")
        what = website.get("what_it_does", "")
        hook = website.get("hook", "")
        why = website.get("why_they_are_best", "")
        stack = ", ".join(website.get("architecture_stack", [])[:4])
        telemetry = website.get("telemetry", {})
        verdict = website.get("extrovertnerd_verdict", "")

        return (
            f"🏆 TOP 100 WEBSITES IN THE WORLD // TEARDOWN #{rank}\n"
            f"⚡ {name.upper()} ({domain})\n"
            f"🏷️ {category}\n\n"
            f"🔥 THE 100X QUESTION:\n"
            f"\"{hook}\"\n\n"
            f"📌 WHAT DOES IT DO?\n"
            f"{what}\n\n"
            f"👉 SWIPE LEFT through this carousel to inspect the architecture:\n"
            f"• Slide 1: Core Function & The Engineering Challenge\n"
            f"• Slide 2: Why They Lead The World, Tech Stack & Core Web Vitals\n\n"
            f"🛠️ Production Stack:\n{stack}\n\n"
            f"📊 Verified Real-World Telemetry:\n"
            f"• Largest Contentful Paint (LCP): {telemetry.get('lcp', 'N/A')}\n"
            f"• Interaction to Next Paint (INP): {telemetry.get('inp', 'N/A')}\n"
            f"• Cumulative Layout Shift (CLS): {telemetry.get('cls', 'N/A')}\n"
            f"• Server TTFB: {telemetry.get('ttfb', 'N/A')}\n\n"
            f"💡 ExtrovertNerd Engineering Verdict:\n"
            f"\"{verdict}\"\n\n"
            f"📌 Save this post to reference during your next system build.\n"
            f"💬 Want your website audited for sub-second mobile conversions? Tap the link in our bio (@extrovertnerd) or visit extrovertnerd.com\n\n"
            f"#WebDevelopment #SoftwareEngineering #{name.replace(' ', '')} #CoreWebVitals #FrontendArchitecture #SystemDesign #ExtrovertNerd #TechStack #WebPerformance"
        )

    @staticmethod
    def build_top100_linkedin_post(website: Dict[str, Any]) -> str:
        """Constructs an executive LinkedIn document briefing tailored for technical leaders."""
        rank = website.get("global_rank", 1)
        name = website.get("name", "Architecture")
        domain = website.get("domain", "")
        category = website.get("category", "Web Architecture")
        what = website.get("what_it_does", "")
        hook = website.get("hook", "")
        why = website.get("why_they_are_best", "")
        reasons = website.get("key_reasons", [])
        stack = " • ".join(website.get("architecture_stack", []))
        telemetry = website.get("telemetry", {})
        verdict = website.get("extrovertnerd_verdict", "")

        reasons_fmt = "\n".join([f"  {i+1}️⃣ {r}" for i, r in enumerate(reasons[:3])])

        return (
            f"Why {name}’s Web Architecture Leads Globally [Engineering Briefing #{rank}/100]\n\n"
            f"\"{hook}\"\n\n"
            f"🏢 Organization Scope & Core Function:\n"
            f"{what}\n\n"
            f"Most engineering leaders assume latency is primarily network roundtrips. But at planetary scale, main-thread script evaluation and unmanaged DOM layout shifts kill user conversion.\n\n"
            f"Here is why {name} ({domain}) holds the benchmark in web engineering:\n"
            f"{why}\n\n"
            f"Key Architectural Decisions:\n"
            f"{reasons_fmt}\n\n"
            f"🛠️ Production Stack:\n{stack}\n\n"
            f"📊 Verified Real-World Benchmarks:\n"
            f"• Largest Contentful Paint (LCP): {telemetry.get('lcp', 'N/A')}\n"
            f"• Interaction to Next Paint (INP): {telemetry.get('inp', 'N/A')}\n"
            f"• Cumulative Layout Shift (CLS): {telemetry.get('cls', 'N/A')}\n"
            f"• Server Time to First Byte (TTFB): {telemetry.get('ttfb', 'N/A')}\n\n"
            f"💡 ExtrovertNerd Engineering Verdict:\n"
            f"{verdict}\n\n"
            f"What architectural principles do your teams prioritize when building high-concurrency flows? Let's discuss in the comments.\n\n"
            f"♻️ Repost this breakdown to share with your engineering network.\n"
            f"Follow @extrovertnerd for daily system architecture briefings (1–100).\n\n"
            f"#SoftwareArchitecture #WebPerformance #SystemDesign #EngineeringLeadership #TechStack #ExtrovertNerd"
        )

    @staticmethod
    def build_top100_twitter_post(website: Dict[str, Any]) -> str:
        """Constructs an X (Twitter) thread opener and breakdown card."""
        rank = website.get("global_rank", 1)
        name = website.get("name", "Architecture")
        domain = website.get("domain", "")
        what = website.get("what_it_does", "")
        hook = website.get("hook", "")
        reasons = website.get("key_reasons", [])
        stack = ", ".join(website.get("architecture_stack", [])[:3])
        telemetry = website.get("telemetry", {})
        verdict = website.get("extrovertnerd_verdict", "")

        r1 = reasons[0] if len(reasons) > 0 else "Optimized execution pipeline"
        r2 = reasons[1] if len(reasons) > 1 else "Zero main-thread blocking"
        r3 = reasons[2] if len(reasons) > 2 else "Strict Core Web Vitals telemetry"

        return (
            f"\"{hook}\" 🧵👇\n\n"
            f"Teardown #{rank} of 100 in the @extrovertnerd Web Architecture Series:\n\n"
            f"Why {name} ({domain}) dominates global performance:\n"
            f"1/ {r1}\n"
            f"2/ {r2}\n"
            f"3/ {r3}\n\n"
            f"🛠️ Production Stack: {stack}\n"
            f"⚡ Verified Telemetry: LCP {telemetry.get('lcp')} | INP {telemetry.get('inp')} | CLS {telemetry.get('cls')} | TTFB {telemetry.get('ttfb')}\n\n"
            f"💡 ExtrovertNerd Verdict: {verdict}\n\n"
            f"RT to share with fellow developers 🔁\n"
            f"Follow @extrovertnerd for daily 0-latency architecture teardowns."
        )

    # =========================================================================
    # DISPATCH METHODS
    # =========================================================================

    def dispatch_top100_for_platform(
        self,
        slides: List[Path | str],
        website: Dict[str, Any],
        platform: str,
    ) -> Dict[str, Any]:
        """Dispatches a Top 100 2-slide pair with explicit platform badge and platform-specific caption."""
        platform_normalized = platform.lower()
        rank = website.get("global_rank", 1)
        name = website.get("name", "Architecture")

        valid_slides = [Path(p) for p in slides if Path(p).exists()]
        if not valid_slides:
            return {"ok": False, "error": f"No valid slides found for platform {platform}"}

        # 1. Platform-specific album header
        if platform_normalized == "instagram":
            album_caption = (
                f"📸 <b>[FOR INSTAGRAM FEED / CAROUSEL]</b>\n"
                f"🏆 <b>Top 100 Teardown: #{rank} {name}</b>\n"
                f"🏷️ <i>Format: 4:5 Portrait Carousel (2 Slides)</i>\n\n"
                f"👉 <i>Full ready-to-copy Instagram caption sent below 👇</i>"
            )
            caption_text = self.build_top100_instagram_caption(website)
            label = "INSTAGRAM CAROUSEL"

        elif platform_normalized == "linkedin":
            album_caption = (
                f"💼 <b>[FOR LINKEDIN DOCUMENT POST]</b>\n"
                f"🏆 <b>Top 100 Teardown: #{rank} {name}</b>\n"
                f"🏷️ <i>Format: 4:5 Engineering Document Briefing (2 Slides)</i>\n\n"
                f"👉 <i>Full ready-to-copy LinkedIn post sent below 👇</i>"
            )
            caption_text = self.build_top100_linkedin_post(website)
            label = "LINKEDIN DOCUMENT"

        elif platform_normalized in ("twitter", "x"):
            album_caption = (
                f"🐦 <b>[FOR X / TWITTER POST & THREAD]</b>\n"
                f"🏆 <b>Top 100 Teardown: #{rank} {name}</b>\n"
                f"🏷️ <i>Format: 4:5 Thread Cards 1 & 2</i>\n\n"
                f"👉 <i>Full ready-to-copy X Thread sent below 👇</i>"
            )
            caption_text = self.build_top100_twitter_post(website)
            label = "X (TWITTER) THREAD"
        else:
            album_caption = f"🏆 <b>Top 100 Teardown: #{rank} {name}</b> ({platform.upper()})"
            caption_text = self.build_top100_instagram_caption(website)
            label = platform.upper()

        # Step 1: Send the 2 slides as an interactive album
        album_res = self.send_media_group(valid_slides, caption=album_caption)

        # Step 2: Send companion message with the exact copy-paste text formatted for that platform
        text_message = (
            f"📋 <b>READY-TO-POST {label} (Copy & Paste):</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<pre>{caption_text}</pre>"
        )
        msg_res = self.send_message(text_message)

        return {
            "ok": True,
            "platform": platform_normalized,
            "album_result": album_res,
            "message_result": msg_res,
        }

    def dispatch_top100(
        self,
        image_paths: Any,
        website: Dict[str, Any],
        platform: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Dispatches Top 100 breakdown across platforms with platform-specific captions."""
        # Case A: Dict with multiple platforms { "instagram": [...], "linkedin": [...], "twitter": [...] }
        if isinstance(image_paths, dict):
            dispatches = {}
            for plat, slides in image_paths.items():
                res = self.dispatch_top100_for_platform(slides, website, platform=plat)
                dispatches[plat] = res
            return {"ok": True, "dispatches": dispatches}

        # Case B: List or Path for a specific platform
        target_plat = platform or "instagram"
        slides = list(image_paths) if isinstance(image_paths, (list, tuple)) else [image_paths]
        return self.dispatch_top100_for_platform(slides, website, platform=target_plat)

    def dispatch_blog_and_x(
        self,
        blog_data: Dict[str, Any],
        city: Dict[str, Any],
        niche: Dict[str, Any],
        twitter_thread: Optional[List[str]] = None,
        carousel_slides: Optional[List[str]] = None,
        instagram_caption: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Dispatches daily website blog article launch notification + ready-to-post X (Twitter) thread."""
        title = blog_data.get("title") or blog_data.get("context", {}).get("title", "Daily Performance Case Study")
        slug = blog_data.get("slug") or blog_data.get("context", {}).get("slug", "")
        blog_url = f"{config.website_url}/blog/{slug}" if slug else config.website_url

        metric_before = niche.get("metric_before", {"load_time": "5.8s", "pagespeed": 28})
        metric_after = niche.get("metric_after", {"load_time": "0.32s", "pagespeed": 100, "conversion_lift": 45})

        results = {}

        # 1. If 4-slide local carousel was generated, send to Telegram with clear Instagram label
        if carousel_slides:
            valid_slides = [Path(p) for p in carousel_slides if Path(p).exists()]
            if valid_slides:
                ig_album_caption = (
                    f"📸 <b>[FOR INSTAGRAM / FB] Local Case Study Carousel (4 Slides)</b>\n"
                    f"📍 <b>Market:</b> {city.get('name')} — {niche.get('name')}\n"
                    f"⚡ <b>Focus:</b> Mobile Speed Audit & Custom Rebuild\n\n"
                    f"👉 <i>Full ready-to-post local client acquisition caption sent below 👇</i>"
                )
                res_ig = self.send_media_group(valid_slides[:10], caption=ig_album_caption)
                results["carousel_album"] = res_ig

                if instagram_caption:
                    ig_msg = (
                        f"📋 <b>READY-TO-POST INSTAGRAM CAPTION // {city.get('name').upper()} (Copy & Paste):</b>\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"<pre>{instagram_caption}</pre>"
                    )
                    results["carousel_caption"] = self.send_message(ig_msg)

        # 2. Send the Website Blog Publication Briefing
        blog_message = (
            f"📰 <b>NEW BLOG ARTICLE PUBLISHED ON EXTROVERTNERD.COM</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ <b>Title:</b> {title}\n"
            f"🌐 <b>Live Article URL:</b> {blog_url}\n"
            f"📍 <b>Target Market:</b> {city.get('name')} — {niche.get('name')}\n\n"
            f"📊 <b>Forensic Latency & Architecture Diagnosis:</b>\n"
            f"• Legacy Baseline: {metric_before.get('pagespeed')}/100 PageSpeed ({metric_before.get('load_time')} mobile load)\n"
            f"• ExtrovertNerd Rebuild: {metric_after.get('pagespeed')}/100 PageSpeed ({metric_after.get('load_time')} mobile load)\n"
            f"• Projected Conversion Lift: +{metric_after.get('conversion_lift')}% direct bookings/sales\n\n"
            f"💬 <b>Direct Consultation WhatsApp Link:</b>\n"
            f"{config.whatsapp_click_to_chat_url}"
        )
        results["blog_dispatch"] = self.send_message(blog_message)

        # 3. Send the Ready-To-Post X (Twitter) Promo Thread
        if twitter_thread:
            thread_formatted = "\n\n".join([f"<b>Tweet {i+1}/{len(twitter_thread)}:</b>\n{tweet}" for i, tweet in enumerate(twitter_thread)])
            twitter_message = (
                f"🐦 <b>READY-TO-POST ON X (TWITTER) // PROMO THREAD</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<i>Copy and post this thread to X to promote the new blog article:</i>\n\n"
                f"{thread_formatted}"
            )
            results["twitter_thread"] = self.send_message(twitter_message)

        return {"ok": True, "results": results}

    def dispatch_latest_graphics(self) -> Dict[str, Any]:
        """Dispatches the most recently generated carousel, Top 100 platform packs, and blog briefs."""
        graphics_dir = config.graphics_output_path
        results = []

        # 1. Find latest local business carousel (Instagram 4-slide set)
        if graphics_dir.exists():
            carousel_dirs = [d for d in graphics_dir.glob("*_carousel") if d.is_dir()]
            carousel_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)

            if carousel_dirs:
                latest_dir = carousel_dirs[0]
                slides = sorted(list(latest_dir.glob("vertical_slide_*.png")) + list(latest_dir.glob("slide_*.png")))
                if not slides:
                    slides = sorted(list(latest_dir.glob("*.png")))

                # Check meta and social preview
                meta_file = latest_dir / "meta.json"
                meta = {}
                if meta_file.exists():
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                    except Exception:
                        pass

                city = meta.get("city", {"name": "Local Commercial Hub"})
                niche = meta.get("niche", {"name": "Boutique Business"})

                # Read caption & thread from social_preview.json
                caption = ""
                thread = []
                preview_file = Path("output/social_preview.json")
                if preview_file.exists():
                    try:
                        with open(preview_file, "r", encoding="utf-8") as f:
                            p_data = json.load(f)
                            caption = p_data.get("caption", "")
                            thread = p_data.get("thread", [])
                    except Exception:
                        pass

                res_carousel = self.dispatch_blog_and_x(
                    blog_data={"title": f"Why {city.get('name')} {niche.get('name')} Lose Customers to Slow Mobile Websites", "slug": f"{city.get('name', '').lower()}-{niche.get('name', '').lower()}"},
                    city=city,
                    niche=niche,
                    twitter_thread=thread,
                    carousel_slides=[str(s) for s in slides[:4]],
                    instagram_caption=caption,
                )
                results.append({"type": "daily_carousel_and_blog", "result": res_carousel})

        # 2. Find and dispatch latest Top 100 breakdown slides for Instagram, LinkedIn, and Twitter
        top100_dir = graphics_dir / "top100"
        if top100_dir.exists():
            top100_platforms = {}
            detected_rank = None
            for plat in ("instagram", "linkedin", "twitter"):
                plat_dir = top100_dir / plat
                if plat_dir.exists():
                    slide1_files = sorted(list(plat_dir.glob("*_slide1.png")), key=lambda p: p.stat().st_mtime, reverse=True)
                    if slide1_files:
                        s1 = slide1_files[0]
                        s2 = Path(str(s1).replace("_slide1.png", "_slide2.png"))
                        if s2.exists():
                            top100_platforms[plat] = [str(s1), str(s2)]
                        else:
                            top100_platforms[plat] = [str(s1)]

                        if detected_rank is None:
                            match = re.search(r"rank_(\d+)", s1.name)
                            if match:
                                detected_rank = int(match.group(1))

            if top100_platforms:
                # Load website data from content/top100_websites.json
                try:
                    with open("content/top100_websites.json", "r", encoding="utf-8") as f:
                        websites = json.load(f)
                        if detected_rank is not None:
                            site = next((w for w in websites if w.get("global_rank") == detected_rank), None)
                        else:
                            site = None
                        if site is None:
                            day_of_year = datetime.date.today().timetuple().tm_yday
                            site = websites[(day_of_year - 1) % len(websites)]
                except Exception:
                    site = {"global_rank": 1, "name": "Stripe", "domain": "stripe.com", "category": "Fintech & Payments Infrastructure", "what_it_does": "Global payments infrastructure", "hook": "How does Stripe process $1T at 60fps?", "why_they_are_best": "Hardware accelerated WebGL", "key_reasons": ["WebGL offloads visuals to GPU", "Multi-region edge routing", "0.00 CLS"], "architecture_stack": ["Ruby/Sorbet", "Go", "React"], "telemetry": {"lcp": "0.62s", "inp": "24ms", "cls": "0.00", "ttfb": "85ms"}, "extrovertnerd_verdict": "Isolate state machines."}

                res_top100 = self.dispatch_top100(top100_platforms, site)
                results.append({"type": "top100_platforms", "result": res_top100})

        # 3. Find any latest Tech News poster
        tech_news_dir = graphics_dir / "tech_news"
        if tech_news_dir.exists():
            posters = sorted(list(tech_news_dir.glob("*.png")), key=lambda p: p.stat().st_mtime, reverse=True)
            if posters:
                latest_poster = posters[0]
                caption = (
                    f"📡 <b>[FOR TECH NEWS / COMMUNITY] Tech Architecture Radar</b>\n\n"
                    f"⚡ <b>File:</b> {latest_poster.name}\n"
                    f"🏢 Studio: ExtrovertNerd Engineering\n"
                    f"🌐 https://extrovertnerd.com"
                )
                res = self.send_photo(latest_poster, caption=caption)
                results.append({"type": "tech_news", "file": str(latest_poster), "result": res})

        # 4. Find any latest Website Speed & UX Tip poster
        website_tips_dir = graphics_dir / "website_tips"
        if website_tips_dir.exists():
            posters = sorted(list(website_tips_dir.glob("*.png")), key=lambda p: p.stat().st_mtime, reverse=True)
            if posters:
                latest_poster = posters[0]
                caption = (
                    f"🛠️ <b>[FOR DEVELOPERS / BUILDERS] Performance Blueprint Tip</b>\n\n"
                    f"⚡ <b>File:</b> {latest_poster.name}\n"
                    f"🏢 Studio: ExtrovertNerd Engineering\n"
                    f"🌐 https://extrovertnerd.com"
                )
                res = self.send_photo(latest_poster, caption=caption)
                results.append({"type": "website_tip", "file": str(latest_poster), "result": res})

        # 5. Find any latest 30s Video Reel (Reels / Shorts / TikTok)
        video_dir = getattr(config, "video_output_path", Path("output/videos"))
        if video_dir.exists():
            videos = sorted(list(video_dir.glob("*.mp4")), key=lambda p: p.stat().st_mtime, reverse=True)
            if videos:
                latest_video = videos[0]
                caption_file = latest_video.with_suffix(".txt")
                caption_text = ""
                if caption_file.exists():
                    try:
                        with open(caption_file, "r", encoding="utf-8") as f:
                            caption_text = f.read().strip()
                    except Exception:
                        pass
                res_v = self.dispatch_video_reel(
                    video_path=latest_video,
                    city={"name": "Target Local Market"},
                    niche={"name": "High-Ticket Vertical"},
                    caption=caption_text,
                )
                results.append({"type": "video_reel", "file": str(latest_video), "result": res_v})

        return {"ok": True, "dispatches": results}

    def dispatch_video_reel(
        self,
        video_path: Path | str,
        city: Optional[Dict[str, Any]] = None,
        niche: Optional[Dict[str, Any]] = None,
        caption: Optional[str] = None,
        duration: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Dispatches an automated 30s video reel to Telegram with clear platform labels and copy-paste caption."""
        path = Path(video_path)
        if not path.exists():
            return {"ok": False, "error": f"Video file not found: {path}"}

        city_name = (city or {}).get("name", "Target Local Market")
        niche_name = (niche or {}).get("name", "High-Ticket Vertical")

        video_caption = (
            f"🎬 <b>[FOR REELS / SHORTS / TIKTOK] 30s High-Retention Video Reel</b>\n"
            f"📍 <b>Market:</b> {city_name} — {niche_name}\n"
            f"⚡ <b>Engine:</b> Edge-TTS Voiceover + Ken Burns Motion + Synced Captions\n\n"
            f"👉 <i>Copy-paste ready caption sent below 👇</i>"
        )

        res_video = self.send_video(path, caption=video_caption, duration=duration)
        results = {"video": res_video}

        if caption:
            msg = (
                f"📋 <b>READY-TO-POST REELS / SHORTS / TIKTOK CAPTION (Copy & Paste):</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<pre>{caption}</pre>"
            )
            results["caption_message"] = self.send_message(msg)

        return {"ok": True, "results": results}

    def dispatch_top100_video_reel(
        self,
        video_path: Path | str,
        site: Dict[str, Any],
        caption: Optional[str] = None,
        duration: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Dispatches an automated 60s Top 100 video reel to Telegram."""
        path = Path(video_path)
        if not path.exists():
            return {"ok": False, "error": f"Video file not found: {path}"}

        rank = site.get("global_rank", 1)
        name = site.get("name", "Website")
        domain = site.get("domain", "")
        telemetry = site.get("telemetry", {})

        video_caption = (
            f"🎬 <b>[DAY {rank}/100 REEL] 60-Second Web Architecture Teardown: {name}</b>\n"
            f"🌐 <b>Domain:</b> {domain} (Rank #{rank})\n"
            f"⚡ <b>Telemetry:</b> LCP {telemetry.get('lcp')} | INP {telemetry.get('inp')} | CLS {telemetry.get('cls')} | TTFB {telemetry.get('ttfb')}\n\n"
            f"👉 <i>Full ready-to-post description sent below 👇</i>"
        )

        res_video = self.send_video(path, caption=video_caption, duration=duration)
        results = {"video": res_video}

        if caption:
            msg = (
                f"📋 <b>READY-TO-POST TOP 100 REEL CAPTION // DAY {rank} (Copy & Paste):</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<pre>{caption}</pre>"
            )
            results["caption_message"] = self.send_message(msg)

        return {"ok": True, "results": results}

    def dispatch_tech_news(self, image_path: Path | str, news: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches a Tech News poster to Telegram."""
        caption = (
            f"📡 <b>[TECH NEWS] Tech Architecture Radar: {news.get('headline')}</b>\n\n"
            f"🏷️ <b>Category:</b> {news.get('category')}\n"
            f"📅 <b>Date:</b> {news.get('date')} | Source: {news.get('source')}\n\n"
            f"📝 <b>Summary:</b> {news.get('summary')}\n\n"
            f"⚡ <b>ExtrovertNerd Verdict:</b> {news.get('extrovertnerd_verdict')}\n\n"
            f"🏢 Studio: ExtrovertNerd Engineering\n"
            f"🌐 https://extrovertnerd.com"
        )
        return self.send_photo(image_path, caption=caption)

    def dispatch_website_tip(self, image_path: Path | str, tip: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches a Website Speed & UX Tip poster to Telegram."""
        caption = (
            f"🛠️ <b>[PERFORMANCE TIP] ExtrovertNerd Blueprint: {tip.get('title')}</b>\n\n"
            f"🏷️ <b>Category:</b> {tip.get('category')} ({tip.get('tag')})\n"
            f"⚡ <b>Impact:</b> {tip.get('measured_impact')}\n\n"
            f"💡 <b>Pro Tip:</b> {tip.get('pro_tip')}\n\n"
            f"🏢 Studio: ExtrovertNerd Engineering\n"
            f"🌐 https://extrovertnerd.com"
        )
        return self.send_photo(image_path, caption=caption)


def main() -> None:
    """CLI testing and manual execution."""
    parser = argparse.ArgumentParser(description="Telegram Bot Graphic & Poster Dispatcher")
    parser.add_argument("--test", action="store_true", help="Test bot credentials and connection")
    parser.add_argument("--message", type=str, help="Send a test message")
    parser.add_argument("--image", type=str, help="Send a single image path")
    parser.add_argument("--latest", action="store_true", help="Send the latest generated carousel pack")
    args = parser.parse_args()

    notifier = TelegramNotifier()

    if args.test:
        res = notifier.test_connection()
        print("\n=== TELEGRAM BOT CONNECTION TEST ===")
        print(json.dumps(res, indent=2))
        if res.get("ok"):
            print("\n✅ Successfully connected to Telegram Bot!")
        else:
            print("\n⚠️ Failed to connect to Telegram. See error details above.")
    elif args.message:
        res = notifier.send_message(args.message)
        print(json.dumps(res, indent=2))
    elif args.image:
        res = notifier.send_photo(args.image, caption="ExtrovertNerd Generated Poster")
        print(json.dumps(res, indent=2))
    elif args.latest:
        res = notifier.dispatch_latest_graphics()
        print("\n=== LATEST GRAPHICS DISPATCHED TO TELEGRAM ===")
        print(json.dumps(res, indent=2))
    else:
        # Default action: run test and dispatch latest
        test_res = notifier.test_connection()
        print(f"Bot Connection: {test_res.get('status')}")
        disp_res = notifier.dispatch_latest_graphics()
        print(f"Dispatch: {disp_res.get('ok')}")


if __name__ == "__main__":
    main()
