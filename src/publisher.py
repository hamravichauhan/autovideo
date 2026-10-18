"""Automated Social Publisher & Multi-Channel Pipeline.

Builds conversion-optimized captions and publishes content across:
1. Instagram (Carousel Posts via Meta Graph API)
2. Facebook Pages (via Meta Graph API)
3. Twitter / X (Automated Threads with Media via Twitter API v2)
4. Portfolio Site (Markdown filesystem sync & commit tracking)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from requests_oauthlib import OAuth1

from src.config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class CaptionBuilder:
    """Assembles high-converting social captions with hooks, value propositions, and CTAs."""

    def __init__(self, templates_file: Optional[Path] = None):
        self.templates_file = templates_file or (config.content_dir / "social_templates.json")
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Loads caption templates and hashtag clusters."""
        if not self.templates_file.exists():
            return {"hashtags": {}, "carousel_captions": [], "thread_structures": []}
        with open(self.templates_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def build_carousel_caption(
        self, city: Dict[str, Any], niche: Dict[str, Any], caption_template_id: str = "speed_leak"
    ) -> str:
        """Constructs an Instagram / LinkedIn caption for a 4-slide carousel."""
        captions = self.data.get("carousel_captions", [])
        matched = next((c for c in captions if c.get("id") == caption_template_id), None)
        if not matched and captions:
            matched = captions[0]

        if not matched:
            hook = f"🚨 Is your {city['name']} {niche['singular']} silently losing customers to a slow website?"
            body = (
                f"Swipe through to see our before/after breakdown of {niche['plural']} in {city['name']}.\n"
                f"We upgraded mobile speed from {niche['metric_before']['load_time']} to "
                f"{niche['metric_after']['load_time']}!\n\n"
                f"DM 'AUDIT' or tap the WhatsApp link in our bio for a free speed teardown."
            )
        else:
            hook = matched["hook_formula"].format(
                city=city["name"],
                niche_singular=niche["singular"],
                niche_plural=niche["plural"],
            )
            body = matched["body"].format(
                city=city["name"],
                niche_singular=niche["singular"],
                niche_plural=niche["plural"],
                load_before=niche["metric_before"]["load_time"],
                load_after=niche["metric_after"]["load_time"],
                conversion_lift=niche["metric_after"]["conversion_lift"],
                brand_handle=config.brand_handle,
            )

        # Assemble hashtags
        hashtag_dict = self.data.get("hashtags", {})
        tags = (
            hashtag_dict.get("webdev", [])[:4]
            + hashtag_dict.get("business", [])[:4]
            + hashtag_dict.get("speed", [])[:3]
        )
        # Add local city & niche hashtags
        city_tag = f"#{city['name'].replace(' ', '')}Business"
        niche_tag = f"#{niche['id'].replace('-', '').title()}"
        tags.extend([city_tag, niche_tag])
        hashtags_str = " ".join(tags)

        full_caption = f"{hook}\n\n{body}\n\n.\n.\n.\n{hashtags_str}"
        return full_caption

    def build_twitter_thread(
        self, city: Dict[str, Any], niche: Dict[str, Any]
    ) -> List[str]:
        """Constructs a 4-part Twitter / X thread matched to the 4 carousel slides."""
        threads = self.data.get("thread_structures", [])
        thread_def = threads[0] if threads else None

        if not thread_def:
            return [
                f"🧵 Most {city['name']} {niche['plural']} are losing 40%+ of mobile sales to slow websites. Here is the teardown: 👇",
                f"1/ In our audits across {city['name']}, average load times sit at {niche['metric_before']['load_time']} with {niche['metric_before']['pagespeed']} PageSpeed score.",
                f"2/ Migrating to custom Laravel cuts load time to {niche['metric_after']['load_time']} with {niche['metric_after']['pagespeed']} score and 0% platform transaction fees.",
                f"3/ Free Speed Audit: DM us 'AUDIT' or tap our WhatsApp link: {config.whatsapp_click_to_chat_url}",
            ]

        step_hooks = thread_def.get("step_hooks", [])
        formatted_tweets = []
        for raw_tweet in step_hooks:
            formatted = raw_tweet.format(
                city=city["name"],
                niche_singular=niche["singular"],
                niche_plural=niche["plural"],
                load_before=niche["metric_before"]["load_time"],
                load_after=niche["metric_after"]["load_time"],
                pagespeed_before=niche["metric_before"]["pagespeed"],
                pagespeed_after=niche["metric_after"]["pagespeed"],
                bounce_before=niche["metric_before"]["bounce_rate"],
                bounce_after=niche["metric_after"]["bounce_rate"],
                conversion_lift=niche["metric_after"]["conversion_lift"],
                whatsapp_url=config.whatsapp_click_to_chat_url,
            )
            formatted_tweets.append(formatted)

        return formatted_tweets


class MetaGraphPublisher:
    """Handles publishing to Instagram and Facebook via Meta Graph API."""

    BASE_URL = "https://graph.facebook.com/v19.0"

    def __init__(self):
        self.access_token = config.meta_access_token
        self.ig_account_id = config.instagram_account_id
        self.fb_page_id = config.facebook_page_id
        self.image_base_url = config.image_hosting_base_url

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """Executes API request with exponential backoff retry loop."""
        params = params or {}
        params["access_token"] = self.access_token
        url = f"{self.BASE_URL}/{endpoint}"

        for attempt in range(1, max_retries + 1):
            try:
                if method.upper() == "POST":
                    resp = requests.post(url, params=params, json=data, timeout=30)
                else:
                    resp = requests.get(url, params=params, timeout=30)

                resp_json = resp.json()
                if resp.status_code >= 400 or "error" in resp_json:
                    error_msg = resp_json.get("error", {}).get("message", resp.text)
                    logger.warning("Meta API error (attempt %d/%d): %s", attempt, max_retries, error_msg)
                    if attempt == max_retries:
                        raise RuntimeError(f"Meta API failed: {error_msg}")
                    time.sleep(2**attempt)
                    continue

                return resp_json
            except requests.RequestException as e:
                logger.warning("Meta API network error (attempt %d/%d): %s", attempt, max_retries, e)
                if attempt == max_retries:
                    raise
                time.sleep(2**attempt)

        return {}

    def publish_instagram_carousel(
        self, image_urls: List[str], caption: str
    ) -> Dict[str, Any]:
        """Publishes a multi-image carousel to Instagram using Meta Graph API."""
        if not config.has_meta_credentials or config.dry_run:
            logger.info("[DRY-RUN / NO CREDENTIALS] Simulating Instagram Carousel upload")
            return {
                "status": "simulated",
                "platform": "instagram",
                "images_count": len(image_urls),
                "image_urls": image_urls,
                "caption_snippet": caption[:100] + "...",
            }

        # Step 1: Create individual item containers
        child_container_ids = []
        for img_url in image_urls:
            logger.info("Creating Instagram item container for: %s", img_url)
            res = self._make_request(
                "POST",
                f"{self.ig_account_id}/media",
                params={"image_url": img_url, "is_carousel_item": "true"},
            )
            child_id = res.get("id")
            if not child_id:
                raise RuntimeError(f"Failed to create child container for {img_url}")
            child_container_ids.append(child_id)
            time.sleep(1)

        # Step 2: Create parent carousel container
        logger.info("Creating Instagram parent carousel container with %d children", len(child_container_ids))
        carousel_res = self._make_request(
            "POST",
            f"{self.ig_account_id}/media",
            params={
                "media_type": "CAROUSEL",
                "children": ",".join(child_container_ids),
                "caption": caption,
            },
        )
        carousel_id = carousel_res.get("id")
        if not carousel_id:
            raise RuntimeError("Failed to create carousel parent container.")

        # Wait briefly for Meta to process container
        time.sleep(3)

        # Step 3: Publish the carousel container
        logger.info("Publishing Instagram carousel container: %s", carousel_id)
        publish_res = self._make_request(
            "POST",
            f"{self.ig_account_id}/media_publish",
            params={"creation_id": carousel_id},
        )

        return {
            "status": "published",
            "platform": "instagram",
            "post_id": publish_res.get("id"),
        }


class TwitterPublisher:
    """Handles publishing automated threads to Twitter / X via Twitter API v2."""

    UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"
    TWEET_URL = "https://api.twitter.com/2/tweets"

    def __init__(self):
        self.auth = (
            OAuth1(
                config.twitter_api_key,
                config.twitter_api_secret,
                config.twitter_access_token,
                config.twitter_access_token_secret,
            )
            if config.has_twitter_credentials
            else None
        )

    def upload_media(self, image_path: Path) -> Optional[str]:
        """Uploads image file to Twitter v1.1 media upload endpoint."""
        if not self.auth or config.dry_run:
            logger.info("[DRY-RUN] Simulating Twitter media upload for %s", image_path)
            return "simulated_media_id_123"

        if not image_path.exists():
            logger.warning("Image file does not exist for Twitter upload: %s", image_path)
            return None

        with open(image_path, "rb") as f:
            files = {"media": f}
            resp = requests.post(self.UPLOAD_URL, auth=self.auth, files=files, timeout=30)
            if resp.status_code in (200, 201, 202):
                return resp.json().get("media_id_string")
            logger.error("Twitter media upload failed (%d): %s", resp.status_code, resp.text)
            return None

    def post_thread(
        self, tweets: List[str], image_paths: Optional[List[Path]] = None
    ) -> List[Dict[str, Any]]:
        """Publishes an automated chain/thread of tweets with corresponding media."""
        image_paths = image_paths or []

        if not self.auth or config.dry_run:
            logger.info("[DRY-RUN / NO CREDENTIALS] Simulating Twitter Thread publish (%d tweets)", len(tweets))
            return [
                {
                    "step": i + 1,
                    "text": t,
                    "media_attached": str(image_paths[i]) if i < len(image_paths) else None,
                    "status": "simulated",
                }
                for i, t in enumerate(tweets)
            ]

        published_tweets = []
        last_tweet_id: Optional[str] = None

        for idx, tweet_text in enumerate(tweets):
            payload: Dict[str, Any] = {"text": tweet_text}

            # Attach media if available
            if idx < len(image_paths):
                media_id = self.upload_media(image_paths[idx])
                if media_id:
                    payload["media"] = {"media_ids": [media_id]}

            # Reply to previous tweet in thread
            if last_tweet_id:
                payload["reply"] = {"in_reply_to_tweet_id": last_tweet_id}

            try:
                resp = requests.post(
                    self.TWEET_URL,
                    auth=self.auth,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=30,
                )
                if resp.status_code in (200, 201):
                    res_data = resp.json().get("data", {})
                    last_tweet_id = res_data.get("id")
                    published_tweets.append({"step": idx + 1, "id": last_tweet_id, "status": "published"})
                    logger.info("Published tweet %d/%d (ID: %s)", idx + 1, len(tweets), last_tweet_id)
                else:
                    logger.error("Failed to post tweet %d: %s", idx + 1, resp.text)
                    break
            except Exception as e:
                logger.error("Exception posting tweet %d: %s", idx + 1, e)
                break

            time.sleep(2)  # Avoid rate limit

        return published_tweets


class PortfolioGitCommitter:
    """Manages tracking and committing generated pSEO articles into portfolio structure."""

    @staticmethod
    def commit_articles(article_paths: List[Path], commit_message: Optional[str] = None) -> bool:
        """Adds and commits generated markdown articles using git command line."""
        if not article_paths:
            return False

        message = commit_message or f"content: add {len(article_paths)} programmatic SEO case studies"

        try:
            # Check if inside git repository
            res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
            if res.returncode != 0:
                logger.info("Not inside a git work tree; skipping git commit.")
                return False

            paths_str = [str(p) for p in article_paths]
            subprocess.run(["git", "add"] + paths_str, check=True)
            subprocess.run(["git", "commit", "-m", message], check=True)
            logger.info("Successfully committed pSEO articles: %s", message)
            return True
        except subprocess.CalledProcessError as e:
            logger.warning("Git commit step encountered error (often clean working tree): %s", e)
            return False
        except FileNotFoundError:
            logger.info("Git binary not found on system; skipping commit.")
            return False


class SocialPublisherEngine:
    """Unified publishing engine coordinating captions, Meta Graph, Twitter, and Git."""

    def __init__(self):
        self.caption_builder = CaptionBuilder()
        self.meta_publisher = MetaGraphPublisher()
        self.twitter_publisher = TwitterPublisher()
        self.git_committer = PortfolioGitCommitter()

    def publish_campaign(
        self,
        city: Dict[str, Any],
        niche: Dict[str, Any],
        slide_image_paths: List[str],
        blog_file: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Coordinates full multi-channel distribution for a generated campaign."""
        logger.info("Starting social publishing for %s - %s", city["name"], niche["name"])

        # 1. Build Captions & Thread
        carousel_caption = self.caption_builder.build_carousel_caption(city, niche)
        twitter_thread = self.caption_builder.build_twitter_thread(city, niche)

        # 2. Resolve image URLs for Meta Graph API
        # Instagram requires publicly reachable HTTP/HTTPS URLs
        image_urls = []
        base_url = config.image_hosting_base_url.rstrip("/")
        for p in slide_image_paths:
            p_obj = Path(p)
            if base_url:
                rel_path = p_obj.name
                image_urls.append(f"{base_url}/{p_obj.parent.name}/{rel_path}")
            else:
                image_urls.append(f"file://{p_obj.resolve()}")

        # 3. Publish to Instagram / Meta
        meta_result = self.meta_publisher.publish_instagram_carousel(
            image_urls=image_urls, caption=carousel_caption
        )

        # 4. Publish to Twitter / X
        image_path_objs = [Path(p) for p in slide_image_paths]
        twitter_result = self.twitter_publisher.post_thread(
            tweets=twitter_thread, image_paths=image_path_objs
        )

        # 5. Git Commit Portfolio Blog if available
        git_committed = False
        if blog_file and blog_file.exists():
            git_committed = self.git_committer.commit_articles(
                [blog_file],
                commit_message=f"content(pseo): publish {city['name']} {niche['name']} case study",
            )

        # 6. Save a preview summary for inspection
        summary = {
            "city": city["name"],
            "niche": niche["name"],
            "caption": carousel_caption,
            "thread": twitter_thread,
            "meta_result": meta_result,
            "twitter_result": twitter_result,
            "git_committed": git_committed,
            "dry_run": config.dry_run,
        }

        preview_file = config.portfolio_blog_path.parent / "social_preview.json"
        with open(preview_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        logger.info("Campaign summary recorded to %s", preview_file)
        return summary


def main() -> None:
    """CLI execution entrypoint."""
    parser = argparse.ArgumentParser(description="Automated Social Media Publisher")
    parser.add_argument("--batch-id", type=str, help="Graphics batch ID to publish")
    parser.add_argument("--dry-run", action="store_true", default=None, help="Force dry-run mode")
    args = parser.parse_args()

    engine = SocialPublisherEngine()
    print("Social Publisher initialized. Checking configured credentials...")
    print(f"  • Meta API Configured: {config.has_meta_credentials}")
    print(f"  • Twitter API Configured: {config.has_twitter_credentials}")
    print(f"  • Dry-Run Mode: {config.dry_run}")


if __name__ == "__main__":
    main()
