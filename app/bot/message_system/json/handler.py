import pyautogui
import keyboard
import time

def main():
    running = True
    while running:
        # Шаг 1: Нажимаем на кнопку в правом верхнем углу (примерно)
        pyautogui.click(x=1920, y=0)

        # Шаг 2: Наводимся на центр экрана и кликаем в течение 5 секунд
        pyautogui.moveTo(960, 540)  # координаты центра экрана (может потребоваться коррекция)
        pyautogui.click(clicks=100, interval=0.05)  # кликаем 100 раз в течение 5 секунд

        # Шаг 3: Уводим курсор на край экрана справа и кликаем пару раз
        pyautogui.moveTo(1920, 540)  # край экрана справа (может потребоваться коррекция)
        pyautogui.click(clicks=2, interval=0.1)  # кликаем пару раз

        # Шаг 4: Проверяем, была ли нажата клавиша F2 для остановки
        if keyboard.is_pressed('f2'):
            running = False

if __name__ == "__main__":
    main()
