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
        """Sends a text message to the configured chat."""
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False,
        }
        data = urllib.parse.urlencode(payload).encode("utf-8")
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": "ExtrovertNerdBot/1.0"})
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            logger.error("Failed to send message: %s (%s)", e.code, error_body)
            return {"ok": False, "error": error_body, "code": e.code}
        except Exception as e:
            logger.error("Failed to send message: %s", e)
            return {"ok": False, "error": str(e)}

    def send_photo(self, photo_path: Path | str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Sends a single photo using multipart/form-data."""
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
        }

        try:
            req = urllib.request.Request(url, data=bytes(body), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                logger.info("✅ Sent photo to Telegram: %s", filename)
                return result
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            logger.error("Failed to send photo: %s (%s)", e.code, error_body)
            return {"ok": False, "error": error_body, "code": e.code}
        except Exception as e:
            logger.error("Failed to send photo: %s", e)
            return {"ok": False, "error": str(e)}

    def send_media_group(self, photo_paths: List[Path | str], caption: Optional[str] = None) -> Dict[str, Any]:
        """Sends a set of carousel slides as an interactive swipeable album (media group)."""
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
        }

        try:
            req = urllib.request.Request(url, data=bytes(body), headers=headers)
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
                logger.info("✅ Sent carousel album (%d slides) to Telegram", len(valid_paths))
                return result
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            logger.error("Failed to send media group: %s (%s)", e.code, error_body)
            return {"ok": False, "error": error_body, "code": e.code}
        except Exception as e:
            logger.error("Failed to send media group: %s", e)
            return {"ok": False, "error": str(e)}

    def dispatch_latest_graphics(self) -> Dict[str, Any]:
        """Dispatches the most recently generated carousel and tech-tip graphics."""
        graphics_dir = config.graphics_output_path
        if not graphics_dir.exists():
            return {"ok": False, "error": f"Graphics directory not found: {graphics_dir}"}

        # 1. Find all carousel directories sorted by modification time
        carousel_dirs = [d for d in graphics_dir.glob("*_carousel") if d.is_dir()]
        carousel_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)

        results = []

        if carousel_dirs:
            latest_dir = carousel_dirs[0]
            slides = sorted(list(latest_dir.glob("slide_*.png")) + list(latest_dir.glob("instagram_slide_*.png")))
            if not slides:
                slides = sorted(list(latest_dir.glob("*.png")))

            # Read meta if available
            meta_file = latest_dir / "meta.json"
            meta = {}
            if meta_file.exists():
                try:
                    with open(meta_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except Exception:
                    pass

            city_name = meta.get("city", {}).get("name", "Local Commercial Hub")
            niche_name = meta.get("niche", {}).get("name", "Boutique Business")

            caption = (
                f"🎨 <b>ExtrovertNerd Automated Poster Pack</b>\n\n"
                f"📍 <b>Market:</b> {city_name} — {niche_name}\n"
                f"⚡ <b>Architecture:</b> Bespoke Sub-Second Rebuild\n"
                f"📊 <b>Core Web Vitals:</b> Verified Sub-Second Benchmarks\n\n"
                f"💬 Studio Contact: <a href=\"https://wa.me/15551234567\">WhatsApp Consultation</a>\n"
                f"🌐 Portfolio Hub: https://extrovertnerd.com"
            )

            res = self.send_media_group(slides[:10], caption=caption)
            results.append({"type": "carousel", "dir": str(latest_dir), "result": res})

        # 2. Find any latest tech tip
        tech_tips_dir = graphics_dir / "tech_tips"
        if tech_tips_dir.exists():
            tips = sorted(list(tech_tips_dir.glob("*.png")), key=lambda p: p.stat().st_mtime, reverse=True)
            if tips:
                latest_tip = tips[0]
                caption = (
                    f"⚡ <b>ExtrovertNerd Tech Tip & Code Breakdown</b>\n\n"
                    f"🛠️ <b>Architecture Optimization:</b> Sub-second latency\n"
                    f"🏢 Studio: ExtrovertNerd Engineering\n"
                    f"🌐 https://extrovertnerd.com"
                )
                res = self.send_photo(latest_tip, caption=caption)
                results.append({"type": "tech_tip", "file": str(latest_tip), "result": res})

        # 3. Find any latest Top 100 breakdown poster
        top100_dir = graphics_dir / "top100"
        if top100_dir.exists():
            posters = sorted(list(top100_dir.glob("*.png")), key=lambda p: p.stat().st_mtime, reverse=True)
            if posters:
                latest_poster = posters[0]
                caption = (
                    f"🏆 <b>ExtrovertNerd Top 100 Websites Breakdown</b>\n\n"
                    f"⚡ <b>File:</b> {latest_poster.name}\n"
                    f"🏢 Studio: ExtrovertNerd Engineering\n"
                    f"🌐 https://extrovertnerd.com"
                )
                res = self.send_photo(latest_poster, caption=caption)
                results.append({"type": "top100", "file": str(latest_poster), "result": res})

        # 4. Find any latest Tech News poster
        tech_news_dir = graphics_dir / "tech_news"
        if tech_news_dir.exists():
            posters = sorted(list(tech_news_dir.glob("*.png")), key=lambda p: p.stat().st_mtime, reverse=True)
            if posters:
                latest_poster = posters[0]
                caption = (
                    f"📡 <b>ExtrovertNerd Tech Architecture Radar</b>\n\n"
                    f"⚡ <b>File:</b> {latest_poster.name}\n"
                    f"🏢 Studio: ExtrovertNerd Engineering\n"
                    f"🌐 https://extrovertnerd.com"
                )
                res = self.send_photo(latest_poster, caption=caption)
                results.append({"type": "tech_news", "file": str(latest_poster), "result": res})

        # 5. Find any latest Website Speed & UX Tip poster
        website_tips_dir = graphics_dir / "website_tips"
        if website_tips_dir.exists():
            posters = sorted(list(website_tips_dir.glob("*.png")), key=lambda p: p.stat().st_mtime, reverse=True)
            if posters:
                latest_poster = posters[0]
                caption = (
                    f"🛠️ <b>ExtrovertNerd Performance Blueprint Tip</b>\n\n"
                    f"⚡ <b>File:</b> {latest_poster.name}\n"
                    f"🏢 Studio: ExtrovertNerd Engineering\n"
                    f"🌐 https://extrovertnerd.com"
                )
                res = self.send_photo(latest_poster, caption=caption)
                results.append({"type": "website_tip", "file": str(latest_poster), "result": res})

        return {"ok": True, "dispatches": results}

    def dispatch_top100(self, image_path: Path | str, website: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches a Top 100 Website breakdown poster to Telegram."""
        caption = (
            f"🏆 <b>Top 100 Websites Breakdown: #{website.get('global_rank', 1)} {website.get('name')}</b>\n\n"
            f"🌐 <b>Domain:</b> {website.get('domain')}\n"
            f"🏷️ <b>Category:</b> {website.get('category')}\n"
            f"⚡ <b>Stack:</b> {', '.join(website.get('architecture_stack', [])[:3])}\n"
            f"📊 <b>Telemetry:</b> LCP {website.get('telemetry', {}).get('lcp')} | INP {website.get('telemetry', {}).get('inp')} | CLS {website.get('telemetry', {}).get('cls')}\n\n"
            f"💡 <b>ExtrovertNerd Verdict:</b> {website.get('extrovertnerd_verdict')}\n\n"
            f"🏢 Studio: ExtrovertNerd Engineering\n"
            f"🌐 https://extrovertnerd.com"
        )
        return self.send_photo(image_path, caption=caption)

    def dispatch_tech_news(self, image_path: Path | str, news: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches a Tech News poster to Telegram."""
        caption = (
            f"📡 <b>Tech Architecture Radar: {news.get('headline')}</b>\n\n"
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
            f"🛠️ <b>ExtrovertNerd Performance Blueprint: {tip.get('title')}</b>\n\n"
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
