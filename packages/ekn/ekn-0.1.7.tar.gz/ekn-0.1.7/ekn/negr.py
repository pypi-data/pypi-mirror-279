from PIL import Image
from pathlib import Path
import pkg_resources


def helpp():
    # Определяем путь к файлу 1.txt
    txt_path = pkg_resources.resource_filename(__name__, 'data/1.txt')

    try:
        # Открытие и чтение файла
        with open(txt_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)  # Вывод содержимого файла
    except FileNotFoundError:
        print(f"File not found: {txt_path}")


def teor(num):
    # Определяем путь к изображению относительно текущего пакета
    base_path = Path(__file__).parent / 'data' / 'teor'
    pt = base_path / f'Screenshot_{num}.png'

    try:
        # Открытие изображения
        img = Image.open(pt)
        img.show()  # Отображение изображения
        return pt
    except FileNotFoundError:
        print(f"File not found: {pt}")
        return None
