import asyncio
import signal
from playwright.async_api import async_playwright, expect
import datetime
import random

print("Скрипт main.py запущен!")

stop_flag = asyncio.Event()

def signal_handler(signum, frame):
    print(f"[{datetime.datetime.now()}] Получен сигнал остановки ({signal.Signals(signum).name}).")
    stop_flag.set()

async def main():
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        async with async_playwright() as p:
            print("Playwright инициализирован.")
            try:
                browser = await p.chromium.launch(headless=True)
                print("Браузер запущен.")
                try:
                    page = await browser.new_page()
                    print("Страница создана.")
                    try:
                        await page.goto("https://www.dyli.io/drop/1930", timeout=60000)
                        print(f"[{datetime.datetime.now()}] Страница успешно загружена.")

                        while not stop_flag.is_set():
                            print(f"[{datetime.datetime.now()}] Начинаю проверку цены...")
                            try:
                                await page.wait_for_selector('span.text-\[var\(--text-slate-700\)\]:has-text("lowest listing")', timeout=10000)
                                print(f"[{datetime.datetime.now()}] Элемент 'lowest listing' найден.")

                                price = await page.evaluate('''() => {
                                    const lowestListingSpan = document.querySelector('span.text-\[var\(--text-slate-700\)\]:has-text("lowest listing")');
                                    if (lowestListingSpan) {
                                        const parentDiv = lowestListingSpan.parentElement;
                                        if (parentDiv) {
                                            const priceSpan = parentDiv.querySelector('span.font-bold');
                                            if (priceSpan) {
                                                return priceSpan.textContent;
                                            } else {
                                                console.log('Не нашли span с классом "font-bold" в родительском элементе.');
                                            }
                                        } else {
                                            console.log('У span "lowest listing" нет родительского элемента.');
                                        }
                                    } else {
                                        console.log('Не нашли span с текстом "lowest listing".');
                                    }
                                    return null;
                                }''')

                                if price:
                                    print(f"[{datetime.datetime.now()}] Lowest listing price (via JS): {price}")
                                else:
                                    print(f"[{datetime.datetime.now()}] Не удалось извлечь цену.")

                            except Exception as e:
                                print(f"[{datetime.datetime.now()}] Ошибка при проверке цены: {e}")

                            await asyncio.sleep(5)

                    except Exception as e:
                        print(f"Ошибка при работе со страницей: {e}")
                    finally:
                        if browser and browser.is_connected:
                            await browser.close()
                            print(f"[{datetime.datetime.now()}] Браузер закрыт.")
                except Exception as e:
                    print(f"Ошибка при запуске браузера или создании страницы: {e}")
            except Exception as e:
                print(f"Ошибка при инициализации Playwright: {e}")
        except Exception as e:
            print(f"Общая ошибка в main: {e}")

    if __name__ == "__main__":
        asyncio.run(main())
