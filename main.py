import asyncio
import re
from playwright.async_api import async_playwright

# Настройки
DYLI_URL = "https://www.dyli.io/drop/1930"
CHECK_INTERVAL = 300  # проверять каждые 300 секунд (5 минут)

async def check_lowest_listing(page):
    await page.goto(DYLI_URL, wait_until="networkidle")
    content = await page.content()

    # Ищем "$<число> lowest listing" через регулярку
    match = re.search(r"\$(\d+)\s*lowest listing", content, re.IGNORECASE)

    if match:
        price_usd = int(match.group(1))
        print(f"✅ Lowest listing найден: ${price_usd}")
        if price_usd > 0:
            print(f"Токен выставлен за ${price_usd}")
            # Здесь можно вставить отправку уведомления в Telegram
        else:
            print("❌ Lowest listing = 0 (нет активного листинга).")
    else:
        print("❌ Lowest listing не найден на странице.")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        while True:
            try:
                await check_lowest_listing(page)
            except Exception as e:
                print(f"Ошибка: {e}")
            await asyncio.sleep(CHECK_INTERVAL)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
