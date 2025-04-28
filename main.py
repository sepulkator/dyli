import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Перейти на страницу
        await page.goto('https://www.dyli.io/drop/1930')
        
        # Ждем, что элемент "lowest listing" появится на странице
        element_locator = await page.locator('span:text("lowest listing")').first()  # Находим первый элемент с текстом "lowest listing"
        parent_div = await element_locator.evaluate('el => el.closest("div")')  # Находим родительский div для этого элемента
        
        # Получаем цену из родительского div
        price_text = await parent_div.locator('span.font-bold').inner_text()  # Извлекаем текст из первого элемента span с классом font-bold
        price = re.search(r"\$(\d+)", price_text)
        
        if price:
            print(f"Lowest listing price: ${price.group(1)}")
        else:
            print("Price not found")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
