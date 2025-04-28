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

                        # Выполняем JavaScript для получения текста цены (с учетом новой структуры)
                        try:
                            price = await page.evaluate('''() => {
                                const lowestListingSpan = document.querySelector('span.text-\[var\(--text-slate-700\)\]:has-text("lowest listing")');
                                if (lowestListingSpan) {
                                    const parentDiv = lowestListingSpan.parentElement;
                                    if (parentDiv) {
                                        const priceSpan = parentDiv.querySelector('span.font-bold');
                                        if (priceSpan) {
                                            return priceSpan.textContent;
                                        }
                                    }
                                }
                                return null;
                            }''')

                            if price:
                                print(f"Lowest listing price (via JS): {price}")
                            else:
                                print("Не удалось найти цену 'lowest listing' с помощью JavaScript.")

                        except Exception as e:
                            print(f"Ошибка при выполнении JavaScript: {e}")

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
