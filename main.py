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
            # Ждем появления элемента "lowest listing" и убеждаемся, что это нужный элемент
            await page.wait_for_selector('span.text-\[var\(--text-slate-700\)\]:has-text("lowest listing")', timeout=60000)

            # Используем более специфичный CSS-селектор для получения цены
            price = await page.locator('div:has(span.text-\[var\(--text-slate-700\)\]:has-text("lowest listing")) + div span.font-bold').text_content()
            print(f"Lowest listing price: {price}")
        except Exception as e:
            print(f"Ошибка: {e}")

        # Закрываем браузер
        await browser.close()

# Запуск асинхронной функции
asyncio.run(main())
