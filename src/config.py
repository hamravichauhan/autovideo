"""Configuration and environment management for the automation engine.

Loads variables from .env or system environment with robust fallbacks.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Base project paths
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Config:
    """Central configuration container."""

    # Brand & Inbound Lead Funnel
    brand_name: str = os.getenv("BRAND_NAME", "ExtrovertNerd")
    brand_handle: str = os.getenv("BRAND_HANDLE", "@extrovertnerd")
    founder_name: str = os.getenv("FOUNDER_NAME", "Ravi")
    founder_title: str = os.getenv("FOUNDER_TITLE", "Lead Web Architect")
    website_url: str = os.getenv("WEBSITE_URL", "https://extrovertnerd.com")
    whatsapp_phone_number: str = os.getenv("WHATSAPP_PHONE_NUMBER", "15551234567")
    whatsapp_default_message: str = os.getenv(
        "WHATSAPP_DEFAULT_MESSAGE",
        "Hey Ravi! I saw ExtrovertNerd's website audit and want a free 5-point speed & UX teardown for my business."
    )
    google_form_intake_url: str = os.getenv(
        "GOOGLE_FORM_INTAKE_URL",
        "https://forms.gle/your-free-speed-audit-intake"
    )

    # Output paths
    portfolio_blog_path: Path = BASE_DIR / os.getenv("PORTFOLIO_BLOG_PATH", "output/blogs")
    graphics_output_path: Path = BASE_DIR / os.getenv("GRAPHICS_OUTPUT_PATH", "output/graphics")
    templates_dir: Path = BASE_DIR / "templates"
    content_dir: Path = BASE_DIR / "content"

    # Meta Graph API (Instagram & Facebook)
    meta_access_token: str = os.getenv("META_ACCESS_TOKEN", "").strip()
    instagram_account_id: str = os.getenv("INSTAGRAM_ACCOUNT_ID", "").strip()
    facebook_page_id: str = os.getenv("FACEBOOK_PAGE_ID", "").strip()
    image_hosting_base_url: str = os.getenv("IMAGE_HOSTING_BASE_URL", "").strip()

    # Twitter / X API v2 Credentials
    twitter_api_key: str = os.getenv("TWITTER_API_KEY", "").strip()
    twitter_api_secret: str = os.getenv("TWITTER_API_SECRET", "").strip()
    twitter_access_token: str = os.getenv("TWITTER_ACCESS_TOKEN", "").strip()
    twitter_access_token_secret: str = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "").strip()
    twitter_bearer_token: str = os.getenv("TWITTER_BEARER_TOKEN", "").strip()

    # Automation Flags
    dry_run: bool = os.getenv("DRY_RUN", "true").lower() in ("true", "1", "yes")

    @property
    def whatsapp_message_encoded(self) -> str:
        """URL-encoded default message for WhatsApp click-to-chat links."""
        return quote_plus(self.whatsapp_default_message)

    @property
    def whatsapp_click_to_chat_url(self) -> str:
        """Formatted WhatsApp click-to-chat URL."""
        return f"https://wa.me/{self.whatsapp_phone_number}?text={self.whatsapp_message_encoded}"

    @property
    def has_meta_credentials(self) -> bool:
        """Returns True if Meta API credentials are fully populated."""
        return bool(self.meta_access_token and self.instagram_account_id)

    @property
    def has_twitter_credentials(self) -> bool:
        """Returns True if Twitter API credentials are fully populated."""
        return bool(
            self.twitter_api_key
            and self.twitter_api_secret
            and self.twitter_access_token
            and self.twitter_access_token_secret
        )


# Global singleton instance
config = Config()
