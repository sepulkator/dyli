import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Запускаем браузер
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Переходим на нужную страницу
        await page.goto("https://www.dyli.io/drop/1930")
        
        # Ожидаем появления нужного элемента на странице
        try:
            # Ждем появления элемента "lowest listing" на странице
            await page.wait_for_selector('span:has-text("lowest listing")', timeout=60000)  # Ждем 60 секунд
            
            # Локализуем элемент
            element_locator = await page.locator('span:has-text("lowest listing")').first()
            parent_div = await element_locator.locator('..')  # Ищем родительский элемент
            price = await parent_div.locator('span.font-bold').text_content()  # Извлекаем цену
            print(f"Lowest listing price: {price}")
        except Exception as e:
            print(f"Ошибка: {e}")
        
        # Закрываем браузер
        await browser.close()

# Запуск асинхронной функции
asyncio.run(main())
