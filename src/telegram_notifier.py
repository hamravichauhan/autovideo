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
        dev_chat_id: Optional[str] = None,
        news_chat_id: Optional[str] = None,
    ):
        self.bot_token = (
            bot_token
            or getattr(config, "telegram_bot_token", None)
            or os.getenv("TELEGRAM_BOT_TOKEN")
            or "8580208646:AAHbnjZm0ZhHrxXLkamH8yF7ozkmBX2zurw"
        ).strip()
        self.chat_id = (
            chat_id
            or getattr(config, "telegram_chat_id", None)
            or os.getenv("TELEGRAM_CHAT_ID")
            or "1432790039"
        ).strip()
        self.dev_chat_id = (
            dev_chat_id
            or getattr(config, "dev_chat_id", None)
            or os.getenv("TELEGRAM_DEV_CHAT_ID")
            or ""
        ).strip()
        self.news_chat_id = (
            news_chat_id
            or getattr(config, "news_chat_id", None)
            or os.getenv("TELEGRAM_NEWS_CHAT_ID")
            or self.chat_id
        ).strip()
        self.dev_topic_id = getattr(config, "telegram_dev_topic_id", None)
        self.news_topic_id = getattr(config, "telegram_news_topic_id", None)
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

    def send_message(
        self,
        text: str,
        parse_mode: str = "HTML",
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Sends a text message to the configured chat with retry handling."""
        target_chat = (chat_id or self.chat_id).strip()
        url = f"{self.base_url}/sendMessage"
        payload: Dict[str, Any] = {
            "chat_id": target_chat,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False,
        }
        if message_thread_id is not None:
            payload["message_thread_id"] = message_thread_id
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

    def send_photo(
        self,
        photo_path: Path | str,
        caption: Optional[str] = None,
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Sends a single photo using multipart/form-data with retry handling."""
        path = Path(photo_path)
        if not path.exists():
            return {"ok": False, "error": f"File not found: {path}"}

        target_chat = (chat_id or self.chat_id).strip()
        url = f"{self.base_url}/sendPhoto"
        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
        body = bytearray()

        # chat_id field
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{target_chat}\r\n'.encode("utf-8"))

        if message_thread_id is not None:
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="message_thread_id"\r\n\r\n{message_thread_id}\r\n'.encode("utf-8"))

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

    def send_media_group(
        self,
        photo_paths: List[Path | str],
        caption: Optional[str] = None,
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Sends a set of carousel slides as an interactive swipeable album (media group) with retry handling."""
        valid_paths = [Path(p) for p in photo_paths if Path(p).exists()]
        if not valid_paths:
            return {"ok": False, "error": "No valid photo paths provided."}

        # Telegram limits media groups to max 10 items
        valid_paths = valid_paths[:10]

        target_chat = (chat_id or self.chat_id).strip()
        url = f"{self.base_url}/sendMediaGroup"
        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
        body = bytearray()

        # chat_id
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{target_chat}\r\n'.encode("utf-8"))

        if message_thread_id is not None:
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="message_thread_id"\r\n\r\n{message_thread_id}\r\n'.encode("utf-8"))

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
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Sends an MP4 video (Instagram Reel / YouTube Short / TikTok) with retry handling."""
        path = Path(video_path)
        if not path.exists():
            return {"ok": False, "error": f"File not found: {path}"}

        target_chat = (chat_id or self.chat_id).strip()
        url = f"{self.base_url}/sendVideo"
        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
        body = bytearray()

        # chat_id
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{target_chat}\r\n'.encode("utf-8"))

        if message_thread_id is not None:
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="message_thread_id"\r\n\r\n{message_thread_id}\r\n'.encode("utf-8"))

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
            f"💬 Want any help in your business with websites, custom tools, or software? Send us a DM.\n\n"
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
            f"💬 Want any help in your business with websites, custom tools, or software? Send us a DM.\n\n"
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
            f"💬 Want any help in your business with websites, custom tools, or software? Send a DM.\n\n"
            f"RT to share with fellow developers 🔁\n"
            f"Follow @extrovertnerd for daily 0-latency architecture teardowns."
        )

    @staticmethod
    def build_tech_news_twitter_post(news: Dict[str, Any]) -> str:
        """Constructs a high-impact X (Twitter) breaking news alert thread opener."""
        headline = news.get("headline", "Breaking Web Architecture Update")
        category = news.get("category", "Web Standards")
        source = news.get("source", "Industry Telemetry")
        summary = news.get("summary", "")
        verdict = news.get("extrovertnerd_verdict", "")
        stack_impact = news.get("stack_impact", [])
        impact_fmt = "\n".join([f"• {p}" for p in stack_impact[:3]])

        return (
            f"📡 BREAKING WEB ARCHITECTURE ALERT // {category.upper()}\n\n"
            f"\"{headline}\"\n\n"
            f"📝 Industry Summary (via {source}):\n"
            f"{summary}\n\n"
            f"⚡ Production Impact:\n"
            f"{impact_fmt}\n\n"
            f"💡 ExtrovertNerd Engineering Verdict:\n"
            f"{verdict}\n\n"
            f"💬 Want any help in your business with websites, custom tools, or software? Send us a DM.\n\n"
            f"RT to keep engineering teams ahead 🔁\n"
            f"Follow @extrovertnerd for real-time web standards & architecture radar.\n\n"
            f"#TechNews #WebStandards #WebPerformance #SoftwareEngineering #Architecture #ExtrovertNerd"
        )

    @staticmethod
    def build_tech_news_linkedin_post(news: Dict[str, Any]) -> str:
        """Constructs an executive LinkedIn briefing for breaking industry news & web standards."""
        headline = news.get("headline", "Industry Architecture Update")
        category = news.get("category", "Web Standards")
        date = news.get("date", str(datetime.date.today()))
        source = news.get("source", "Web Platform Working Group")
        summary = news.get("summary", "")
        deep_dive = news.get("technical_deep_dive", "")
        verdict = news.get("extrovertnerd_verdict", "")
        stack_impact = news.get("stack_impact", [])
        impact_fmt = "\n".join([f"  {i+1}️⃣ {p}" for i, p in enumerate(stack_impact[:3])])

        return (
            f"📡 Web Architecture Radar: {headline}\n\n"
            f"🏷️ Domain: {category} | 📅 {date} | Source: {source}\n\n"
            f"\"{summary}\"\n\n"
            f"🔍 Technical Architecture Breakdown:\n"
            f"{deep_dive}\n\n"
            f"🛠️ Direct Production Impact:\n"
            f"{impact_fmt}\n\n"
            f"💡 ExtrovertNerd Engineering Verdict:\n"
            f"{verdict}\n\n"
            f"💬 Want any help in your business with websites, custom tools, or software? Send us a DM.\n\n"
            f"What impact does this update have on your current technical roadmap? Let's discuss below.\n\n"
            f"♻️ Repost to share with your technical network.\n"
            f"Follow @extrovertnerd for daily system architecture briefings.\n\n"
            f"#SoftwareEngineering #WebStandards #TechNews #SystemDesign #ExtrovertNerd"
        )

    @staticmethod
    def build_dev_tip_linkedin_post(tip: Dict[str, Any]) -> str:
        """Constructs an engineering performance blueprint for LinkedIn."""
        title = tip.get("title", "")
        category = tip.get("category", "Frontend Architecture")
        problem = tip.get("problem", "")
        impact = tip.get("measured_impact", "")
        pro_tip = tip.get("pro_tip", "")
        code = tip.get("code_snippet", "")

        return (
            f"🛠️ Engineering Blueprint: {title} [{category}]\n\n"
            f"🚨 The Architectural Bottleneck:\n"
            f"{problem}\n\n"
            f"📊 Measured Performance Impact:\n"
            f"⚡ {impact}\n\n"
            f"💻 Implementation Pattern:\n"
            f"{code}\n\n"
            f"💡 ExtrovertNerd Pro Tip:\n"
            f"{pro_tip}\n\n"
            f"💬 Want any help in your business with websites, custom tools, or software? Send us a DM.\n\n"
            f"Save this blueprint for your next system build 📌\n"
            f"Follow @extrovertnerd for daily production-tested engineering patterns.\n\n"
            f"#WebPerformance #SoftwareEngineering #CleanCode #FullStack #SystemDesign #ExtrovertNerd"
        )

    @staticmethod
    def build_dev_tip_instagram_caption(tip: Dict[str, Any]) -> str:
        """Constructs an Instagram caption for code & architecture tips."""
        title = tip.get("title", "")
        category = tip.get("category", "Engineering Pattern")
        problem = tip.get("problem", "")
        impact = tip.get("measured_impact", "")
        pro_tip = tip.get("pro_tip", "")

        return (
            f"⚡ Quick Engineering Pattern: {title}\n"
            f"🏷️ {category}\n\n"
            f"❌ THE BOTTLENECK:\n"
            f"{problem}\n\n"
            f"🚀 MEASURED PERFORMANCE LIFT:\n"
            f"⚡ {impact}\n\n"
            f"💡 EXTROVERTNERD PRO TIP:\n"
            f"{pro_tip}\n\n"
            f"📌 Save this post to reference in your codebase.\n"
            f"💬 Want any help in your business with websites, custom tools, or software? Send us a DM.\n\n"
            f"#WebDevelopment #SoftwareEngineering #CodeSnippets #CleanCode #Architecture #ExtrovertNerd #TechStack #WebPerformance"
        )

    # =========================================================================
    # DISPATCH METHODS
    # =========================================================================

    def dispatch_top100_for_platform(
        self,
        slides: List[Path | str],
        website: Dict[str, Any],
        platform: str,
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
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
        album_res = self.send_media_group(valid_slides, caption=album_caption, chat_id=chat_id, message_thread_id=message_thread_id)

        # Step 2: Send companion message with the exact copy-paste text formatted for that platform
        text_message = (
            f"📋 <b>READY-TO-POST {label} (Copy & Paste):</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<pre>{caption_text}</pre>"
        )
        msg_res = self.send_message(text_message, chat_id=chat_id, message_thread_id=message_thread_id)

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
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Dispatches Top 100 breakdown across platforms with platform-specific captions."""
        # Case A: Dict with multiple platforms { "instagram": [...], "linkedin": [...], "twitter": [...] }
        if isinstance(image_paths, dict):
            dispatches = {}
            for plat, slides in image_paths.items():
                res = self.dispatch_top100_for_platform(
                    slides, website, platform=plat, chat_id=chat_id, message_thread_id=message_thread_id
                )
                dispatches[plat] = res
            return {"ok": True, "dispatches": dispatches}

        # Case B: List or Path for a specific platform
        target_plat = platform or "instagram"
        slides = list(image_paths) if isinstance(image_paths, (list, tuple)) else [image_paths]
        return self.dispatch_top100_for_platform(
            slides, website, platform=target_plat, chat_id=chat_id, message_thread_id=message_thread_id
        )

    def dispatch_dev_track(
        self,
        top100_platforms: Optional[Dict[str, List[Path | str]]] = None,
        website: Optional[Dict[str, Any]] = None,
        dev_tip_path: Optional[Path | str] = None,
        dev_tip: Optional[Dict[str, Any]] = None,
        video_path: Optional[Path | str] = None,
        video_caption: Optional[str] = None,
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        force: bool = False,
    ) -> Dict[str, Any]:
        """Dispatches Track 1: Dev Content (Top 100 System Architecture + Performance Blueprints).
        
        Strictly isolated from Tech News and Local Business Audits.
        Target Platforms: LinkedIn (Engineering Network) & Instagram (Visual Carousel).
        """
        results = {}
        target_chat = (chat_id or self.dev_chat_id or "").strip()
        target_topic = message_thread_id or self.dev_topic_id

        # Safety Guards: protect news channel during automated daily execution
        if not force and not chat_id:
            if not getattr(config, "enable_dev_autoposting", False):
                logger.info("⏸️ Dev track auto-posting is temporarily PAUSED. Bypassing dispatch to protect news channel.")
                return {
                    "ok": True,
                    "status": "paused",
                    "message": "Dev track auto-posting is temporarily paused. Protected news channel.",
                }
            if not target_chat:
                logger.warning("⚠️ No dedicated TELEGRAM_DEV_CHAT_ID configured. Skipping dev dispatch to prevent posting to news channel.")
                return {
                    "ok": True,
                    "status": "skipped",
                    "message": "No dedicated TELEGRAM_DEV_CHAT_ID configured. Skipping to protect news channel from dev posts.",
                }

        if not target_chat:
            return {"ok": False, "error": "No target chat ID specified."}

        # 1. Prominent Isolation Banner
        banner = (
            f"🛠️ <b>════════════════════════════════════════</b>\n"
            f"🛠️ <b>TRACK 1: DEV CONTENT // SYSTEM ARCHITECTURE & CODE</b>\n"
            f"🛠️ <b>════════════════════════════════════════</b>\n"
            f"🎯 <b>PRIMARY PLATFORMS:</b> LinkedIn & Instagram (Engineering Network)\n"
            f"⚠️ <b>ISOLATION:</b> This is technical engineering & code architecture. Do NOT post to breaking news channels."
        )
        results["banner"] = self.send_message(banner, chat_id=target_chat, message_thread_id=target_topic)

        # 2. Dispatch Top 100 Breakdown for LinkedIn & Instagram
        if top100_platforms and website:
            top100_res = {}
            for plat in ("linkedin", "instagram"):
                if plat in top100_platforms:
                    res = self.dispatch_top100_for_platform(
                        top100_platforms[plat],
                        website,
                        platform=plat,
                        chat_id=target_chat,
                        message_thread_id=target_topic,
                    )
                    top100_res[plat] = res
            results["top100"] = top100_res

        # 3. Dispatch Performance Blueprint / Dev Tip (if available)
        if dev_tip_path and Path(dev_tip_path).exists() and dev_tip:
            tip_caption = (
                f"🛠️ <b>[FOR LINKEDIN & DEV COMMUNITY] Performance Blueprint & Code Fix</b>\n\n"
                f"⚡ <b>Title:</b> {dev_tip.get('title')}\n"
                f"🏷️ <b>Category:</b> {dev_tip.get('category')} ({dev_tip.get('tag')})\n"
                f"🚀 <b>Measured Impact:</b> {dev_tip.get('measured_impact')}\n\n"
                f"👉 <i>Full ready-to-copy LinkedIn / Dev post sent below 👇</i>"
            )
            res_photo = self.send_photo(dev_tip_path, caption=tip_caption, chat_id=target_chat, message_thread_id=target_topic)
            msg_text = (
                f"📋 <b>READY-TO-POST DEV BLUEPRINT // LINKEDIN (Copy & Paste):</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<pre>{self.build_dev_tip_linkedin_post(dev_tip)}</pre>"
            )
            res_msg = self.send_message(msg_text, chat_id=target_chat, message_thread_id=target_topic)
            results["dev_tip"] = {"photo": res_photo, "message": res_msg}

        # 4. Dispatch 60s Architecture Video Reel (if available)
        if video_path and Path(video_path).exists() and website:
            rank = website.get("global_rank", 1)
            name = website.get("name", "Website")
            domain = website.get("domain", "")
            telemetry = website.get("telemetry", {})

            v_caption = (
                f"🎬 <b>[DAY {rank}/100 REEL] 60-Second Web Architecture Teardown: {name}</b>\n"
                f"🌐 <b>Domain:</b> {domain} (Rank #{rank})\n"
                f"⚡ <b>Telemetry:</b> LCP {telemetry.get('lcp')} | INP {telemetry.get('inp')} | CLS {telemetry.get('cls')}\n\n"
                f"👉 <i>Full ready-to-post description sent below 👇</i>"
            )
            res_v = self.send_video(video_path, caption=v_caption, duration=60, chat_id=target_chat, message_thread_id=target_topic)
            v_msg = None
            if video_caption:
                caption_msg = (
                    f"📋 <b>READY-TO-POST TOP 100 REEL CAPTION // DAY {rank} (Copy & Paste):</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"<pre>{video_caption}</pre>"
                )
                v_msg = self.send_message(caption_msg, chat_id=target_chat, message_thread_id=target_topic)
            results["video_reel"] = {"video": res_v, "caption": v_msg}

        return {"ok": True, "track": "dev", "results": results}

    def dispatch_news_track(
        self,
        image_path: Path | str,
        news: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Dispatches Track 2: Breaking Tech News & Industry Radar.
        
        Strictly isolated from Dev Code Blueprints and Local Business Audits.
        Target Platforms: X (Twitter) & Tech News Communities.
        """
        results = {}
        target_chat = self.news_chat_id
        target_topic = self.news_topic_id

        # 1. Prominent Isolation Banner
        banner = (
            f"📡 <b>════════════════════════════════════════</b>\n"
            f"📡 <b>TRACK 2: TECH NEWS // BREAKING INDUSTRY RADAR</b>\n"
            f"📡 <b>════════════════════════════════════════</b>\n"
            f"🎯 <b>PRIMARY PLATFORMS:</b> X (Twitter) & Tech News Communities\n"
            f"⚠️ <b>ISOLATION:</b> This is breaking industry news & web standards. Do NOT post to developer code tip feeds."
        )
        results["banner"] = self.send_message(banner, chat_id=target_chat, message_thread_id=target_topic)

        # 2. Tech News Poster
        poster_caption = (
            f"📡 <b>[FOR X / TWITTER & TECH COMMUNITIES] Breaking Radar Card</b>\n\n"
            f"⚡ <b>Headline:</b> {news.get('headline')}\n"
            f"🏷️ <b>Category:</b> {news.get('category')}\n"
            f"📅 <b>Date:</b> {news.get('date')} | Source: {news.get('source')}\n\n"
            f"👉 <i>Ready-to-copy X (Twitter) breaking news post sent below 👇</i>"
        )
        res_poster = self.send_photo(image_path, caption=poster_caption, chat_id=target_chat, message_thread_id=target_topic)
        results["poster"] = res_poster

        # 3. Ready-To-Post on X (Twitter) Breaking News Post
        twitter_text = self.build_tech_news_twitter_post(news)
        tw_msg = (
            f"📋 <b>READY-TO-POST ON X (TWITTER) // BREAKING NEWS (Copy & Paste):</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<pre>{twitter_text}</pre>"
        )
        res_tw = self.send_message(tw_msg, chat_id=target_chat, message_thread_id=target_topic)
        results["twitter_post"] = res_tw

        # 4. Community Radar Bulletin
        bulletin_text = (
            f"📡 <b>TECH ARCHITECTURE RADAR BULLETIN:</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>{news.get('headline')}</b>\n\n"
            f"📝 <b>Summary:</b> {news.get('summary')}\n\n"
            f"⚡ <b>ExtrovertNerd Verdict:</b> {news.get('extrovertnerd_verdict')}\n\n"
            f"🌐 https://extrovertnerd.com"
        )
        results["bulletin"] = self.send_message(bulletin_text, chat_id=target_chat, message_thread_id=target_topic)

        return {"ok": True, "track": "news", "results": results}

    def dispatch_local_track(
        self,
        blog_data: Dict[str, Any],
        city: Dict[str, Any],
        niche: Dict[str, Any],
        carousel_slides: Optional[List[str]] = None,
        instagram_caption: Optional[str] = None,
        video_path: Optional[Path | str] = None,
        video_caption: Optional[str] = None,
        prospects: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Dispatches Track 3: Local B2B Client Acquisition Funnel.
        
        Strictly isolated from Dev Code Blueprints and Tech News.
        Target Platforms: ExtrovertNerd Website Blog, Local Instagram/FB, WhatsApp Outreach.
        """
        results = {}
        target_chat = self.chat_id

        # 1. Prominent Isolation Banner
        banner = (
            f"📍 <b>════════════════════════════════════════</b>\n"
            f"📍 <b>TRACK 3: LOCAL B2B CLIENT ACQUISITION FUNNEL</b>\n"
            f"📍 <b>════════════════════════════════════════</b>\n"
            f"🎯 <b>PRIMARY PLATFORMS:</b> ExtrovertNerd Website Blog, Local Instagram/FB, WhatsApp Outreach\n"
            f"⚠️ <b>ISOLATION:</b> This is local client conversion & pSEO case studies. Do NOT mix with dev architecture teardowns."
        )
        results["banner"] = self.send_message(banner, chat_id=target_chat)

        # 2. Local 4-Slide Case Study Carousel
        if carousel_slides:
            valid_slides = [Path(p) for p in carousel_slides if Path(p).exists()]
            if valid_slides:
                ig_album_caption = (
                    f"📸 <b>[FOR INSTAGRAM / FB] Local Case Study Carousel (4 Slides)</b>\n"
                    f"📍 <b>Market:</b> {city.get('name')} — {niche.get('name')}\n"
                    f"⚡ <b>Focus:</b> Mobile Speed Audit & Custom Rebuild\n\n"
                    f"👉 <i>Full ready-to-post local client acquisition caption sent below 👇</i>"
                )
                res_ig = self.send_media_group(valid_slides[:10], caption=ig_album_caption, chat_id=target_chat)
                results["carousel_album"] = res_ig

                if instagram_caption:
                    ig_msg = (
                        f"📋 <b>READY-TO-POST INSTAGRAM CAPTION // {city.get('name').upper()} (Copy & Paste):</b>\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"<pre>{instagram_caption}</pre>"
                    )
                    results["carousel_caption"] = self.send_message(ig_msg, chat_id=target_chat)

        # 3. Website Blog Publication Alert
        title = blog_data.get("title") or blog_data.get("context", {}).get("title", "Daily Performance Case Study")
        slug = blog_data.get("slug") or blog_data.get("context", {}).get("slug", "")
        blog_url = f"{config.website_url}/blog/{slug}" if slug else config.website_url

        metric_before = niche.get("metric_before", {"load_time": "5.8s", "pagespeed": 28})
        metric_after = niche.get("metric_after", {"load_time": "0.32s", "pagespeed": 100, "conversion_lift": 45})

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
            f"💬 <b>Want any help in your business with websites, custom tools, or software? Send us a DM or chat on WhatsApp:</b>\n"
            f"{config.whatsapp_click_to_chat_url}"
        )
        results["blog_dispatch"] = self.send_message(blog_message, chat_id=target_chat)

        # 4. 30s Local Video Reel
        if video_path and Path(video_path).exists():
            v_caption = (
                f"🎬 <b>[FOR REELS / SHORTS / TIKTOK] 30s High-Retention Video Reel</b>\n"
                f"📍 <b>Market:</b> {city.get('name')} — {niche.get('name')}\n"
                f"⚡ <b>Engine:</b> Edge-TTS Voiceover + Ken Burns Motion + Synced Captions\n\n"
                f"👉 <i>Copy-paste ready caption sent below 👇</i>"
            )
            res_v = self.send_video(video_path, caption=v_caption, duration=30, chat_id=target_chat)
            results["video_reel"] = res_v
            if video_caption:
                v_msg = (
                    f"📋 <b>READY-TO-POST REELS / SHORTS / TIKTOK CAPTION (Copy & Paste):</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"<pre>{video_caption}</pre>"
                )
                results["video_caption"] = self.send_message(v_msg, chat_id=target_chat)

        # 5. Daily High-Ticket Outbound Leads
        if prospects:
            leads_res = self.dispatch_outbound_leads(
                prospects=prospects,
                city_name=city.get("name", "Target City"),
                niche_name=niche.get("name", "High-Ticket Vertical"),
                chat_id=target_chat,
            )
            results["outbound_leads"] = leads_res

        return {"ok": True, "track": "local", "results": results}

    def dispatch_outbound_leads(
        self,
        prospects: List[Dict[str, Any]],
        city_name: str = "Target City",
        niche_name: str = "High-Ticket Vertical",
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Dispatches verified real business outbound dossiers to Telegram with 1-tap WhatsApp deep links."""
        target_chat = (chat_id or self.chat_id).strip()
        results = {}

        if not prospects:
            return {"ok": True, "count": 0}

        lead_banner = (
            f"🎯 <b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            f"🎯 <b>DAILY OUTBOUND LEADS // {city_name.upper()}</b>\n"
            f"🎯 <b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
            f"💼 <b>Vertical:</b> {niche_name}\n"
            f"📊 <b>Discovered:</b> {len(prospects)} businesses evaluated\n"
            f"⚡ <b>Action:</b> Tap the WhatsApp link to open the pre-filled message, or copy the pitch text below."
        )
        results["banner"] = self.send_message(lead_banner, chat_id=target_chat, message_thread_id=message_thread_id)

        for idx, lead in enumerate(prospects, 1):
            biz_name = lead.get("business_name", "Business")
            is_real = lead.get("is_real", False)
            badge = "🟢 VERIFIED REAL BUSINESS" if is_real else "🟡 SIMULATED TARGET"
            rating_str = f"({lead.get('rating')} ⭐, {lead.get('reviews')})" if lead.get("rating") else ""
            wa_number = lead.get("wa_number")
            phone_display = f"+{wa_number}" if wa_number else (lead.get("phone_raw") or "Not Listed")
            website = lead.get("website", "No Website")
            load_time = lead.get("current_load_time", "N/A")
            score = lead.get("current_pagespeed", "N/A")
            platform = lead.get("detected_platform", "WordPress")
            drafts = lead.get("outreach_drafts", {})
            wa_pitch = drafts.get("whatsapp", "")
            wa_link = drafts.get("whatsapp_1tap_url", "")

            msg = (
                f"🎯 <b>LEAD #{idx}: {biz_name}</b> [{badge}]\n"
                f"📍 <b>Location:</b> {lead.get('district', city_name)}, {city_name} {rating_str}\n"
                f"🌐 <b>Website:</b> {website}\n"
                f"⚙️ <b>Architecture:</b> {platform}\n"
                f"⏱️ <b>Live Mobile Speed:</b> <code>{load_time}</code> (Score: <code>{score}</code>)\n"
                f"📞 <b>Phone / WhatsApp:</b> <code>{phone_display}</code>\n\n"
                f"📋 <b>Ready-to-Send WhatsApp Pitch:</b>\n"
                f"<pre>{wa_pitch}</pre>"
            )

            if wa_link:
                msg += (
                    f"\n👉 <a href=\"{wa_link}\"><b>[⚡ TAP HERE TO OPEN WHATSAPP CHAT WITH OWNER]</b></a>\n"
                )

            results[f"lead_{idx}"] = self.send_message(msg, chat_id=target_chat, message_thread_id=message_thread_id)

        return {"ok": True, "count": len(prospects), "results": results}

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
        return self.dispatch_local_track(
            blog_data=blog_data,
            city=city,
            niche=niche,
            carousel_slides=carousel_slides,
            instagram_caption=instagram_caption,
        )

    def dispatch_latest_graphics(self, track: str = "all") -> Dict[str, Any]:
        """Dispatches the most recently generated assets with strict track isolation.
        
        Args:
            track: "all", "dev", "news", or "local".
        """
        track_norm = track.lower().strip()
        graphics_dir = config.graphics_output_path
        results = []

        # 1. TRACK 1: DEV CONTENT
        if track_norm in ("all", "dev"):
            top100_dir = graphics_dir / "top100"
            top100_platforms = {}
            detected_rank = None
            if top100_dir.exists():
                for plat in ("instagram", "linkedin", "twitter"):
                    plat_dir = top100_dir / plat
                    if plat_dir.exists():
                        slide1_files = sorted(list(plat_dir.glob("*_slide1.png")), key=lambda p: p.stat().st_mtime, reverse=True)
                        if slide1_files:
                            s1 = slide1_files[0]
                            s2 = Path(str(s1).replace("_slide1.png", "_slide2.png"))
                            top100_platforms[plat] = [str(s1), str(s2)] if s2.exists() else [str(s1)]
                            if detected_rank is None:
                                match = re.search(r"rank_(\d+)", s1.name)
                                if match:
                                    detected_rank = int(match.group(1))

            site = None
            if top100_platforms:
                try:
                    with open("content/top100_websites.json", "r", encoding="utf-8") as f:
                        websites = json.load(f)
                        if detected_rank is not None:
                            site = next((w for w in websites if w.get("global_rank") == detected_rank), None)
                        if site is None:
                            site = websites[0]
                except Exception:
                    pass

            # Find latest website tip / dev tip
            dev_tip_path = None
            dev_tip_data = None
            tips_dir = graphics_dir / "website_tips"
            if tips_dir.exists():
                posters = sorted(list(tips_dir.glob("*.png")), key=lambda p: p.stat().st_mtime, reverse=True)
                if posters:
                    dev_tip_path = posters[0]
                    try:
                        with open("content/website_tips.json", "r", encoding="utf-8") as f:
                            tips = json.load(f)
                            tip_id = dev_tip_path.stem.replace("tip_", "")
                            dev_tip_data = next((t for t in tips if t.get("id") == tip_id), tips[0])
                    except Exception:
                        pass

            # Find latest 60s top100 video reel
            video_dir = getattr(config, "video_output_path", Path("output/videos"))
            top100_vid = None
            top100_vid_caption = None
            if video_dir.exists():
                top_vids = sorted(list(video_dir.glob("*top100*.mp4")), key=lambda p: p.stat().st_mtime, reverse=True)
                if top_vids:
                    top100_vid = top_vids[0]
                    cap_f = top100_vid.with_suffix(".txt")
                    if cap_f.exists():
                        try:
                            with open(cap_f, "r", encoding="utf-8") as f:
                                top100_vid_caption = f.read().strip()
                        except Exception:
                            pass

            if top100_platforms or dev_tip_path:
                res_dev = self.dispatch_dev_track(
                    top100_platforms=top100_platforms,
                    website=site,
                    dev_tip_path=dev_tip_path,
                    dev_tip=dev_tip_data,
                    video_path=top100_vid,
                    video_caption=top100_vid_caption,
                )
                results.append({"type": "dev_track", "result": res_dev})

        # 2. TRACK 2: TECH NEWS
        if track_norm in ("all", "news"):
            tech_news_dir = graphics_dir / "tech_news"
            if tech_news_dir.exists():
                posters = sorted(list(tech_news_dir.glob("*.png")), key=lambda p: p.stat().st_mtime, reverse=True)
                if posters:
                    latest_poster = posters[0]
                    news_data = None
                    try:
                        with open("content/tech_news.json", "r", encoding="utf-8") as f:
                            news_items = json.load(f)
                            news_id = latest_poster.stem.replace("tech_news_", "")
                            news_data = next((n for n in news_items if n.get("id") == news_id), news_items[0])
                    except Exception:
                        pass
                    if not news_data:
                        news_data = {
                            "headline": latest_poster.stem.replace("tech_news_", "").replace("-", " ").title(),
                            "category": "Web Standards",
                            "source": "Chrome & W3C Telemetry",
                            "summary": "Key performance updates across web architecture and browser runtime engines.",
                            "extrovertnerd_verdict": "Keep server response times and script execution under 50ms.",
                            "stack_impact": ["Optimize asset bundles", "Audit main-thread work", "Verify Core Web Vitals"]
                        }
                    res_news = self.dispatch_news_track(latest_poster, news_data)
                    results.append({"type": "news_track", "result": res_news})

        # 3. TRACK 3: LOCAL B2B FUNNEL
        if track_norm in ("all", "local"):
            carousel_dirs = [d for d in graphics_dir.glob("*_carousel") if d.is_dir()]
            carousel_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
            if carousel_dirs:
                latest_dir = carousel_dirs[0]
                slides = sorted(list(latest_dir.glob("vertical_slide_*.png")) + list(latest_dir.glob("slide_*.png")))
                if not slides:
                    slides = sorted(list(latest_dir.glob("*.png")))
                meta = {}
                meta_file = latest_dir / "meta.json"
                if meta_file.exists():
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                    except Exception:
                        pass
                city = meta.get("city", {"name": "Local Commercial Hub"})
                niche = meta.get("niche", {"name": "Boutique Business"})
                caption = ""
                preview_file = Path("output/social_preview.json")
                if preview_file.exists():
                    try:
                        with open(preview_file, "r", encoding="utf-8") as f:
                            caption = json.load(f).get("caption", "")
                    except Exception:
                        pass
                # Find latest local 30s video reel
                local_vid = None
                local_vid_cap = None
                video_dir = getattr(config, "video_output_path", Path("output/videos"))
                if video_dir.exists():
                    vids = sorted(list(video_dir.glob("*.mp4")), key=lambda p: p.stat().st_mtime, reverse=True)
                    local_vids = [v for v in vids if "top100" not in v.name]
                    if local_vids:
                        local_vid = local_vids[0]
                        cap_f = local_vid.with_suffix(".txt")
                        if cap_f.exists():
                            try:
                                with open(cap_f, "r", encoding="utf-8") as f:
                                    local_vid_cap = f.read().strip()
                            except Exception:
                                pass
                # Load latest prospects if available
                latest_prospects = None
                p_file = config.portfolio_blog_path.parent / "prospects.json"
                if p_file.exists():
                    try:
                        with open(p_file, "r", encoding="utf-8") as pf:
                            p_json = json.load(pf)
                            latest_prospects = p_json.get("leads", [])[:3]
                    except Exception:
                        pass

                res_local = self.dispatch_local_track(
                    blog_data={"title": f"Why {city.get('name')} {niche.get('name')} Lose Customers to Slow Mobile Websites", "slug": f"{city.get('name', '').lower()}-{niche.get('name', '').lower()}"},
                    city=city,
                    niche=niche,
                    carousel_slides=[str(s) for s in slides[:4]],
                    instagram_caption=caption,
                    video_path=local_vid,
                    video_caption=local_vid_cap,
                    prospects=latest_prospects,
                )
                results.append({"type": "local_track", "result": res_local})

        return {"ok": True, "dispatches": results}

    def dispatch_video_reel(
        self,
        video_path: Path | str,
        city: Optional[Dict[str, Any]] = None,
        niche: Optional[Dict[str, Any]] = None,
        caption: Optional[str] = None,
        duration: Optional[int] = None,
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
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

        res_video = self.send_video(path, caption=video_caption, duration=duration, chat_id=chat_id, message_thread_id=message_thread_id)
        results = {"video": res_video}

        if caption:
            msg = (
                f"📋 <b>READY-TO-POST REELS / SHORTS / TIKTOK CAPTION (Copy & Paste):</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<pre>{caption}</pre>"
            )
            results["caption_message"] = self.send_message(msg, chat_id=chat_id, message_thread_id=message_thread_id)

        return {"ok": True, "results": results}

    def dispatch_top100_video_reel(
        self,
        video_path: Path | str,
        site: Dict[str, Any],
        caption: Optional[str] = None,
        duration: Optional[int] = None,
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
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

        res_video = self.send_video(path, caption=video_caption, duration=duration, chat_id=chat_id, message_thread_id=message_thread_id)
        results = {"video": res_video}

        if caption:
            msg = (
                f"📋 <b>READY-TO-POST TOP 100 REEL CAPTION // DAY {rank} (Copy & Paste):</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<pre>{caption}</pre>"
            )
            results["caption_message"] = self.send_message(msg, chat_id=chat_id, message_thread_id=message_thread_id)

        return {"ok": True, "results": results}

    def dispatch_tech_news(
        self,
        image_path: Path | str,
        news: Dict[str, Any],
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Dispatches a Tech News poster to Telegram using the dedicated news track."""
        return self.dispatch_news_track(image_path, news)

    def dispatch_website_tip(
        self,
        image_path: Path | str,
        tip: Dict[str, Any],
        chat_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Dispatches a Website Speed & UX Tip poster to Telegram."""
        target_chat = (chat_id or self.dev_chat_id).strip()
        target_topic = message_thread_id or self.dev_topic_id

        if not getattr(config, "enable_dev_autoposting", False) or not target_chat:
            logger.info("⏸️ Website tip dispatch skipped: Dev auto-posting is paused or no dedicated dev channel configured.")
            return {
                "ok": True,
                "status": "skipped",
                "message": "Dev auto-posting is paused or no dedicated dev chat configured; skipped to protect news channel.",
            }

        caption = (
            f"🛠️ <b>[PERFORMANCE TIP] ExtrovertNerd Blueprint: {tip.get('title')}</b>\n\n"
            f"🏷️ <b>Category:</b> {tip.get('category')} ({tip.get('tag')})\n"
            f"⚡ <b>Impact:</b> {tip.get('measured_impact')}\n\n"
            f"💡 <b>Pro Tip:</b> {tip.get('pro_tip')}\n\n"
            f"💬 <i>Want any help in your business with websites, custom tools, or software? Send us a DM.</i>\n\n"
            f"🏢 Studio: ExtrovertNerd Engineering\n"
            f"🌐 https://extrovertnerd.com"
        )
        return self.send_photo(image_path, caption=caption, chat_id=target_chat, message_thread_id=target_topic)


def main() -> None:
    """CLI testing and manual execution."""
    parser = argparse.ArgumentParser(description="Telegram Bot Graphic & Poster Dispatcher")
    parser.add_argument("--test", action="store_true", help="Test bot credentials and connection")
    parser.add_argument("--message", type=str, help="Send a test message")
    parser.add_argument("--image", type=str, help="Send a single image path")
    parser.add_argument("--latest", action="store_true", help="Send the latest generated carousel pack")
    parser.add_argument("--leads", action="store_true", help="Dispatch latest outbound lead dossiers to Telegram")
    parser.add_argument(
        "--track",
        choices=["all", "dev", "news", "local"],
        default="all",
        help="Isolate dispatch to specific track (dev, news, local, all)",
    )
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
    elif args.leads:
        p_file = config.portfolio_blog_path.parent / "prospects.json"
        if not p_file.exists():
            print("No prospects.json found. Run `python -m src.prospecting_engine` first.")
        else:
            with open(p_file, "r", encoding="utf-8") as pf:
                p_json = json.load(pf)
                leads = p_json.get("leads", [])
                city_name = leads[0].get("city", "Target Market") if leads else "Target Market"
                niche_name = leads[0].get("niche", "High-Ticket Vertical") if leads else "High-Ticket Vertical"
                res = notifier.dispatch_outbound_leads(leads, city_name=city_name, niche_name=niche_name)
                print("\n=== OUTBOUND LEADS DISPATCHED TO TELEGRAM ===")
                print(json.dumps(res, indent=2))
    elif args.message:
        res = notifier.send_message(args.message)
        print(json.dumps(res, indent=2))
    elif args.image:
        res = notifier.send_photo(args.image, caption="ExtrovertNerd Generated Poster")
        print(json.dumps(res, indent=2))
    elif args.latest:
        res = notifier.dispatch_latest_graphics(track=args.track)
        print(f"\n=== LATEST GRAPHICS DISPATCHED TO TELEGRAM [TRACK: {args.track.upper()}] ===")
        print(json.dumps(res, indent=2))
    else:
        # Default action: run test and dispatch latest
        test_res = notifier.test_connection()
        print(f"Bot Connection: {test_res.get('status')}")
        disp_res = notifier.dispatch_latest_graphics(track=args.track)
        print(f"Dispatch: {disp_res.get('ok')}")


if __name__ == "__main__":
    main()
