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

                        # Выполняем JavaScript для получения текста цены (с дополнительным логированием)
                        try:
                            price = await page.evaluate('''() => {
                                console.log('Начинаем поиск цены...');
                                const lowestListingSpans = document.querySelectorAll('span');
                                let foundListingSpan = null;
                                for (const span of lowestListingSpans) {
                                    if (span.textContent && span.textContent.trim() === 'lowest listing') {
                                        console.log('Нашли span с текстом "lowest listing":', span);
                                        foundListingSpan = span;
                                        break;
                                    }
                                }

                                if (foundListingSpan) {
                                    const parentDiv = foundListingSpan.parentElement;
                                    if (parentDiv) {
                                        const priceSpan = parentDiv.querySelector('span.font-bold');
                                        if (priceSpan) {
                                            console.log('Нашли span с ценой:', priceSpan.textContent);
                                            return priceSpan.textContent;
                                        } else {
                                            console.log('Не нашли span с классом "font-bold" в родительском элементе.');
                                        }
                                    } else {
                                        console.log('У span "lowest listing" нет родительского элемента.');
                                    }
                                } else {
                                    console.log('Не нашли ни одного span с текстом "lowest listing".');
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
