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

            try:
                # Ожидаем появления элемента с текстом "lowest listing"
                await page.wait_for_selector("text=lowest listing", timeout=60000)  # Увеличиваем время ожидания до 60 секунд
                print("Элемент 'lowest listing' найден!")
            except PlaywrightTimeoutError:
                print("Не удалось найти элемент 'lowest listing' на странице. Попробуй позже.")

            # Получаем все элементы с текстом "lowest listing"
            elements = await page.locator("text=lowest listing").all_text_contents()

            # Если найдено больше одного элемента, извлекаем первый
            if elements:
                lowest_listing_text = elements[0]  # Берем первый найденный элемент
                match = re.search(r"\$(\d+)\s*lowest listing", lowest_listing_text, re.IGNORECASE)
                if match:
                    lowest_listing = match.group(1)  # Извлекаем цену из группы
                    print(f"Lowest listing: ${lowest_listing}")
                else:
                    print("Не удалось извлечь цену из текста.")
            else:
                print("Не найдено элементов с текстом 'lowest listing'.")

            await browser.close()

    except PlaywrightTimeoutError as e:
        print(f"Ошибка: Истекло время ожидания при загрузке страницы или элемент не найден. {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск асинхронной функции
asyncio.run(main())
