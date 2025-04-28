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
            # Ожидаем появления первого элемента с текстом "lowest listing"
            lowest_listing_element = await page.locator('span:text("lowest listing")').first()
            
            # Находим родительский div для этого элемента
            parent_div = await lowest_listing_element.locator('..')  # Это родительский элемент

            # Ищем цену в родительском div
            price_text = await parent_div.locator("span.font-bold").inner_text()
            
            # Преобразуем в число (с помощью регулярного выражения)
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
