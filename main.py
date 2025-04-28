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
        elements = await page.locator('span:has-text("lowest listing")').all()  # Находим все элементы с текстом "lowest listing"
        
        if elements:
            # Для первого элемента ищем родительский div
            parent_div = await elements[0].evaluate('el => el.closest("div")')
            
            # Получаем цену из родительского div
            price_text = await page.locator('span.font-bold').inner_text()  # Извлекаем текст из первого элемента span с классом font-bold
            price = re.search(r"\$(\d+)", price_text)
            
            if price:
                print(f"Lowest listing price: ${price.group(1)}")
            else:
                print("Price not found")
        else:
            print("No 'lowest listing' element found")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
