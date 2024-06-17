def helpp():
    # Открываем файл с указанием кодировки и обработкой ошибок
    f = open("data/1.txt", "r", encoding="utf-8", errors='ignore')
    for s in f:
        print(s, end="")


def teor(num):
    from PIL import Image

    # Открытие изображения
    img = Image.open(f'data/teor/Screenshot_{num}.png')

    # Вывод изображения
    img.show()


helpp()

