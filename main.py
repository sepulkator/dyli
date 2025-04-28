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

                        # Выполняем JavaScript для получения текста цены (попытка 3)
                        try:
                            price = await page.evaluate('''() => {
                                const spans = document.querySelectorAll('span');
                                for (const span of spans) {
                                    if (span.textContent && span.textContent.trim() === 'lowest listing') {
                                        console.log('Нашли span с текстом "lowest listing":', span); // Для отладки

                                        let parent = span.parentElement;
                                        while (parent) {
                                            const priceSpan = parent.querySelector('span.font-bold');
                                            if (priceSpan) {
                                                console.log('Нашли span с ценой:', priceSpan.textContent); // Для отладки
                                                return priceSpan.textContent;
                                            }
                                            parent = parent.parentElement;
                                        }
                                        console.log('Не нашли span с ценой в родительских элементах.'); // Для отладки
                                        return null;
                                    }
                                }
                                console.log('Не нашли span с текстом "lowest listing".'); // Для отладки
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
