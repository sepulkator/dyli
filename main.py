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

            # Ожидаем появления элемента с текстом lowest listing
            try:
                await page.wait_for_selector('span.text-[var(--text-slate-700)]', timeout=60000)  # Ждем "lowest listing"
                print("Элемент 'lowest listing' найден!")
            except PlaywrightTimeoutError:
                print("Не удалось найти элемент 'lowest listing' на странице. Попробуй позже.")
                return

            # Ищем родительский div для lowest listing
            parent_div = await page.locator('span:text("lowest listing")').locator('..')  # Находим родительский div

            # Извлекаем цену из первого span внутри родительского div
            price_element = await parent_div.locator('span.font-bold').text_content()  # Получаем цену

            # Если цена найдена, выводим
            if price_element:
                print(f"Lowest listing: {price_element.strip()}")
            else:
                print("Не удалось найти цену.")

            await browser.close()

    except PlaywrightTimeoutError as e:
        print(f"Ошибка: Истекло время ожидания при загрузке страницы или элемент не найден. {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск асинхронной функции
asyncio.run(main())
