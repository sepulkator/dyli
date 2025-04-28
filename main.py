import asyncio
from playwright.async_api import async_playwright

async def main():
    try:
        async with async_playwright() as p:
            try:
                # Запускаем браузер
                browser = await p.chromium.launch(headless=True)
                try:
                    page = await browser.new_page()
                    try:
                        # Переходим на нужную страницу
                        await page.goto("https://www.dyli.io/drop/1930", timeout=60000)
                        print("Страница успешно загружена.")

                        # Ожидаем появления элемента с текстом "lowest listing"
                        try:
                            await page.wait_for_selector('span:has-text("lowest listing")', timeout=60000)
                            print("Элемент 'lowest listing' найден.")

                            # Используем селектор, привязываясь к тексту "lowest listing" и следующему div с ценой
                            price = await page.locator('div:has(span:has-text("lowest listing")) + div span.font-bold').text_content()
                            print(f"Lowest listing price: {price}")

                        except Exception as e:
                            print(f"Ошибка при поиске или извлечении цены: {e}")

                    except Exception as e:
                        print(f"Ошибка при работе со страницей: {e}")
                    finally:
                        if browser and browser.is_connected:
                            await browser.close()
                            print("Браузер закрыт.")
                except Exception as e:
                    print(f"Ошибка при запуске браузера или создании страницы: {e}")
            except Exception as e:
                print(f"Ошибка при инициализации Playwright: {e}")
    except Exception as e:
        print(f"Общая ошибка в main: {e}")

# Запуск асинхронной функции
asyncio.run(main())
