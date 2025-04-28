import asyncio
from playwright.async_api import async_playwright

async def main():
    print("Скрипт запущен ✅")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Здесь урл страницы на dyli
        await page.goto("https://www.dyli.io/drop/1930")

        # Немного подождём для уверенности (если нужно)
        await page.wait_for_timeout(2000)

        # Ищем нужный элемент по тексту
        element = await page.locator("text=lowest listing").first()
        if element:
            price_text = await element.text_content()
            print(f"Найденное значение: {price_text}")
        else:
            print("Не удалось найти элемент с текстом 'lowest listing'")

        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
