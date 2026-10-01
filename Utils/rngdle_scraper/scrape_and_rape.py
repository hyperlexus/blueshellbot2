import asyncio
import re
from datetime import datetime

from playwright.async_api import async_playwright


async def efficiency_max(route):
    if route.request.resource_type in ["image", "media", "font"]:
        await route.abort()
    else:
        await route.continue_()


async def scrape_rngdle_today(username: str, discord_id: int) -> tuple[str, datetime]:
    user_url = f"https://www.rngdle.com/u/{username}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-first-run",
                "--no-zygote",
                "--single-process",
            ],
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        await page.route("**/*", efficiency_max)
        await page.goto(user_url, wait_until="domcontentloaded")

        card = "a.block.polished-card-interactive.px-5.py-3"
        await page.wait_for_selector(card, timeout=15000)

        most_recent_roll = page.locator(card).first
        roll_link = await most_recent_roll.get_attribute("href")

        date_elem = most_recent_roll.locator("div.type-data.type-meta")
        roll_date = (await date_elem.inner_text()).strip()

        complete_url = f"https://www.rngdle.com{roll_link}"
        await page.goto(complete_url, wait_until="domcontentloaded")
        await page.wait_for_selector("span.font-roll", timeout=15000)

        roll_number = (await page.locator("span.font-roll").inner_text()).strip()

        rarity_elem = page.locator("span.type-label").first
        rarity_count = await rarity_elem.count()
        rarity = (
            (await rarity_elem.inner_text()).strip().upper()
            if rarity_count > 0
            else "COMMON"
        )

        rarity_square_map = {
            "TRASH": ":yellow_square:",
            "COMMON": ":white_large_square:",
            "UNCOMMON": ":green_square:",
            "RARE": ":blue_square:",
            "EPIC": ":purple_square:",
            "ANOMALY": ":orange_square:",
            "MYTHIC": ":red_square:",
        }
        rarity_square = rarity_square_map.get(rarity, ":white_large_square:")

        raw_ep = await page.locator("span.type-data").first.inner_text()
        ep_text = raw_ep.strip()

        badge_elements = await page.locator("a[href*='/badges/']").all()
        badge_lines = []

        for badge in badge_elements:
            div_class = (
                await badge.locator("div").first.get_attribute("class")
            ) or ""
            colour_circle = ":white_circle:"
            if any(
                c in div_class
                for c in ["bg-green-50", "dark:bg-emerald-950/40", "text-green-700"]
            ):
                colour_circle = ":green_circle:"
            if any(
                c in div_class
                for c in ["bg-blue-50", "dark:bg-blue-950/40", "text-blue-700"]
            ):
                colour_circle = ":blue_circle:"

            spans = await badge.locator("span").all()
            if len(spans) >= 2:
                emoji = (await spans[0].inner_text()).strip()
                title = (await spans[1].inner_text()).strip()
                badge_lines.append(f"{colour_circle} {emoji} {title}")

        more_btn = page.locator("button.type-label").filter(has_text="MORE")
        more_badges_text = ""
        if await more_btn.count() > 0:
            btn_raw = (await more_btn.inner_text()).strip()
            maybe_regex_match = re.search(r"\+(\d+)\s+MORE", btn_raw, re.IGNORECASE)
            if maybe_regex_match:
                more_badges_text = f"+{maybe_regex_match.group(1)} more\n"

        await browser.close()

        output_text = (
            f"<@{discord_id}> played RNGdle:\n"
            f"# {roll_number}\n\n"
            f"{rarity_square} {rarity}\n\n"
            + "\n".join(badge_lines)
            + f"\n{more_badges_text}\n"
            f"{ep_text}",
            datetime.strptime(roll_date, "%d/%m/%Y")
        )

        return output_text

async def rape_lightweight(username: str, discord_id: int):
    return (await scrape_rngdle_today(username, discord_id))[0].split("\n")[1].replace("# ", "").replace("\n\n", "")

if __name__ == "__main__":
    print(asyncio.run(scrape_rngdle_today("hyperlexus", 422800248935546880)))
