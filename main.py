import asyncio
import re
from playwright.async_api import async_playwright

async def fetch_lowest_listing_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Переходим на страницу товара
        await page.goto("https://www.dyli.io/drop/1930")  # Вставь нужный URL
        
        try:
            # Ожидаем появления элемента с текстом lowest listing
            await page.wait_for_selector("span:text('lowest listing')")
            
            # Ищем родительский div для lowest listing
            parent_div = await page.locator('span:text("lowest listing")').locator('..')  # Родительский div
            
            # Извлекаем цену из предыдущего элемента, который является числом перед lowest listing
            price_text = await parent_div.locator("span.font-bold").inner_text()
            
            # Преобразуем в число
            match = re.search(r"\$(\d+)", price_text)
            if match:
                price = match.group(1)
                print(f"Lowest Listing Price: ${price}")
            else:
                print("Price not found.")
        
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

async def main():
    await fetch_lowest_listing_price()

if __name__ == "__main__":
    asyncio.run(main())
