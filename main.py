from playwright.sync_api import sync_playwright
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scrape_lowest_price():
    with sync_playwright() as p:
        logger.info("Запуск браузера")
        browser = p.chromium.launch(headless=True)
        
        try:
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            logger.info("Переход на страницу https://www.dyli.io/drop/1930")
            page.goto("https://www.dyli.io/drop/1930", wait_until="networkidle")
            
            # Даём странице немного времени для полной загрузки всех элементов
            page.wait_for_timeout(2000)
            
            # Используем точный селектор на основе предоставленной HTML структуры
            logger.info("Поиск элемента с ценой")
            
            # Ищем span с классом font-bold, который находится рядом со span, содержащим текст "lowest listing"
            price_selector = "//span[contains(@class, 'font-bold')][following-sibling::span[contains(text(), 'lowest listing')]]"
            
            # Проверяем, существует ли элемент
            if page.locator(price_selector).count() > 0:
                lowest_price = page.locator(price_selector).inner_text()
                logger.info(f"Найдена цена: {lowest_price}")
                return lowest_price.strip()
            else:
                # Альтернативный селектор, если первый не сработал
                logger.info("Первый селектор не сработал, пробуем альтернативный")
                price_selector_alt = "//span[contains(text(), 'lowest listing')]/preceding-sibling::span[contains(@class, 'font-bold')]"
                
                if page.locator(price_selector_alt).count() > 0:
                    lowest_price = page.locator(price_selector_alt).inner_text()
                    logger.info(f"Найдена цена через альтернативный селектор: {lowest_price}")
                    return lowest_price.strip()
                
                # Еще более простой селектор
                logger.info("Пробуем прямой селектор по классу")
                direct_selector = "span.font-bold"
                
                if page.locator(direct_selector).count() > 0:
                    elements = page.locator(direct_selector).all()
                    for element in elements:
                        text = element.inner_text()
                        if text.startswith("$"):
                            logger.info(f"Найдена цена через прямой селектор: {text}")
                            return text.strip()
            
            # Если ничего не нашли, делаем скриншот для диагностики
            logger.warning("Не удалось найти элемент с ценой на странице")
            page.screenshot(path="debug_screenshot.png")
            
            return None
            
        except Exception as e:
            logger.error(f"Произошла ошибка: {str(e)}")
            return None
        finally:
            browser.close()
            logger.info("Браузер закрыт")

if __name__ == "__main__":
    price = scrape_lowest_price()
    if price:
        print(f"Lowest price: {price}")
    else:
        print("Не удалось получить цену")
