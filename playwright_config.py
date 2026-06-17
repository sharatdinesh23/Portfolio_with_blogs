from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"
LINKEDIN_FEED_URL = "https://www.linkedin.com/feed/"


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _load_credentials(email: str | None, password: str | None) -> tuple[str, str]:
    load_dotenv()

    resolved_email = email or os.getenv("LINKEDIN_EMAIL")
    resolved_password = password or os.getenv("LINKEDIN_PASSWORD")

    if not resolved_email or not resolved_password:
        raise ValueError("Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD before posting to LinkedIn.")

    return resolved_email, resolved_password


def _login(page, email: str, password: str) -> None:
    page.goto(LINKEDIN_LOGIN_URL, wait_until="domcontentloaded")

    if "/feed" in page.url:
        return

    page.locator("#username").wait_for(timeout=30000)
    page.locator("#username").fill(email)
    page.locator("#password").fill(password)
    page.locator("button[type='submit']").click()
    page.wait_for_url("**/feed/**", timeout=60000)


def _open_post_dialog(page):
    page.goto(LINKEDIN_FEED_URL, wait_until="domcontentloaded")

    start_post_button = page.get_by_role(
        "button",
        name=re.compile("Start a post", re.IGNORECASE),
    ).first
    start_post_button.wait_for(timeout=60000)
    start_post_button.click()

    composer = page.locator("div[role='textbox']").last
    composer.wait_for(timeout=30000)
    return composer


def post_to_linkedin(
    post_text: str,
    *,
    email: str | None = None,
    password: str | None = None,
    headless: bool | None = None,
) -> None:
    cleaned_post = post_text.strip()
    if not cleaned_post:
        raise ValueError("LinkedIn post content cannot be empty.")

    resolved_email, resolved_password = _load_credentials(email, password)
    run_headless = _env_flag("LINKEDIN_HEADLESS") if headless is None else headless

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as err:
        raise RuntimeError(
            "Playwright is not installed. Add the dependency and install the Chromium browser first.",
        ) from err

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=run_headless)
        context = browser.new_context()
        page = context.new_page()

        try:
            _login(page, resolved_email, resolved_password)
            composer = _open_post_dialog(page)
            composer.fill(cleaned_post)

            post_button = page.get_by_role(
                "button",
                name=re.compile(r"^Post$", re.IGNORECASE),
            ).last
            post_button.wait_for(timeout=30000)
            post_button.click()
            post_button.wait_for(state="hidden", timeout=60000)
        finally:
            context.close()
            browser.close()


def _read_post_text(post_file: str | None) -> str:
    if post_file:
        return Path(post_file).read_text(encoding="utf-8")
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Post LinkedIn content through Playwright automation.",
    )
    parser.add_argument(
        "post_file",
        nargs="?",
        help="Optional path to a text file containing the final LinkedIn post body.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Force headless browser mode for this run.",
    )
    args = parser.parse_args(argv)

    post_text = _read_post_text(args.post_file)
    if not post_text.strip():
        raise ValueError("No LinkedIn post content provided.")

    post_to_linkedin(post_text, headless=True if args.headless else None)
    print("Posted to LinkedIn successfully.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as err:
        print(str(err), file=sys.stderr)
        raise SystemExit(1)
