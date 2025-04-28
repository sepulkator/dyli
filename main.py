from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio

async def main():
    try:
        # Запуск Playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Переход на страницу
            await page.goto("https://www.dyli.io/drop/1930")  # URL твоей страницы
            
            try:
                # Локатор для lowest listing
                lowest_listing_element = await page.locator('text=lowest listing')
                lowest_listing = await lowest_listing_element.inner_text()  # Получаем текст из элемента
                print(f"Lowest listing: {lowest_listing}")
            except PlaywrightTimeoutError as e:
                print(f"Ошибка: Не удалось найти элемент 'lowest listing' на странице. {e}")
            except Exception as e:
                print(f"Произошла неизвестная ошибка при извлечении данных: {e}")
            
            # Закрываем браузер
            await browser.close()

    except PlaywrightTimeoutError as e:
        print(f"Ошибка: Истекло время ожидания при запуске или переходе на страницу: {e}")
    except Exception as e:
        print(f"Произошла ошибка при работе с Playwright: {e}")

# Запуск асинхронной функции
asyncio.run(main())
