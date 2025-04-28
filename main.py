import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    async with async_playwright() as p:
        # Запускаем браузер
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Переходим на нужную страницу
        await page.goto('https://www.dyli.io/drop/1930')  # Измените на нужный URL

        # Ждем, пока страница полностью загрузится
        await page.wait_for_selector('text="lowest listing"')  # Ждем, что текст "lowest listing" появится на странице

        # Получаем весь текст страницы
        content = await page.content()

        # Ищем цену перед "lowest listing" с помощью регулярного выражения
        match = re.search(r"\$(\d+)\s*lowest listing", content, re.IGNORECASE)
        
        if match:
            price = match.group(1)  # Извлекаем цену из группы
            print(f"Lowest listing price: ${price}")
        else:
            print("Lowest listing not found.")

        # Закрываем браузер
        await browser.close()

# Запускаем асинхронный цикл
asyncio.run(main())
