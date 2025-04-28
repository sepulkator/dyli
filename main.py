import asyncio
import re
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def main():
    try:
        # Запуск Playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Переход на нужную страницу
            await page.goto('https://www.dyli.io/drop/1930')  # URL твоей страницы

            # Ждем, пока страница полностью загрузится
            await page.wait_for_timeout(5000)  # Ждем 5 секунд для полной загрузки страницы

            # Получаем весь HTML контент страницы
            content = await page.content()

            # Используем регулярное выражение для поиска текста
            match = re.search(r"\$(\d+)\s*lowest listing", content, re.IGNORECASE)

            if match:
                lowest_listing = match.group(1)  # Извлекаем цену из группы
                print(f"Lowest listing: ${lowest_listing}")
            else:
                print("Lowest listing not found.")

            await browser.close()

    except PlaywrightTimeoutError as e:
        print(f"Ошибка: Истекло время ожидания при загрузке страницы или элемент не найден. {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск асинхронной функции
asyncio.run(main())
