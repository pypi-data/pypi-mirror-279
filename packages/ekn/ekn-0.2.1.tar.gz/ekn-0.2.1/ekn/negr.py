from PIL import Image
from IPython.display import display

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
    # Определяем путь к изображению относительно пакета
    filename = f'Screenshot_{num}.png'
    pt = pkg_resources.resource_filename(__name__, f'data/teor/{filename}')

    try:
        # Открытие изображения
        img = Image.open(pt)
        display(img)  # Отображение изображения в Jupyter Notebook
        return pt
    except FileNotFoundError:
        print(f"File not found: {pt}")
        return None