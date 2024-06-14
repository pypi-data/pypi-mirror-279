import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import sys
from tqdm import tqdm

def clear_console():
    # Функция для очистки консоли
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def download_image(image_url, save_directory):
    try:
        with requests.get(image_url, stream=True) as response:
            response.raise_for_status()
            if save_directory:
                os.makedirs(save_directory, exist_ok=True)
                filename = os.path.join(save_directory, image_url.split('/')[-1])
            else:
                filename = image_url.split('/')[-1]

            with open(filename, 'wb') as image_file:
                for data in response.iter_content(1024):
                    image_file.write(data)
            return response.headers.get('content-length', 0)
    except requests.RequestException as e:
        print(f"Ошибка при попытке скачать изображение {image_url}: {e}")
        return 0

def download_full_size_images(url, save_directory="", extension=".jpg"):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        images_urls = []

        for img in img_tags:
            full_image_url = img.get('data-original') or img.get('src')

            parent_link = img.find_parent('a')
            if parent_link and parent_link.get('href'):
                full_image_url = parent_link.get('href')

            full_image_url = urljoin(url, full_image_url)
            if full_image_url.lower().endswith(extension.lower()):
                images_urls.append(full_image_url)

        total_images = len(images_urls)
        print(f"Найдено изображений: {total_images}")

        progress_bar = tqdm(total=total_images, unit='file', desc="Загрузка изображений")

        for image_url in images_urls:
            download_image(image_url, save_directory)
            progress_bar.update(1)
        progress_bar.close()

    except requests.RequestException as e:
        print(f"Ошибка при попытке получить HTML страницы {url}: {e}")

def main():
    clear_console()
    print("Made by Avinion\nTelegram: @akrim")
    print("Программа для скачивания изображений с веб-страницы.")
    while True:
        url = input("Введите URL веб-страницы: ")
        save_directory = input("Введите путь или название папки для сохранения изображений (оставьте пустым, чтобы сохранить в текущей директории): ")
        extension = input("Введите расширение изображений для скачивания (например, .jpg): ")

        if save_directory and not os.path.isabs(save_directory):
            save_directory = os.path.join(os.getcwd(), save_directory)

        download_full_size_images(url, save_directory, extension)

        answer = input("Продолжить работу? (Y/N): ").strip().lower()
        if answer == 'n':
            break
        elif answer != 'y':
            print("Пожалуйста, введите 'Y' или 'N'.")
        clear_console()

if __name__ == "__main__":
    main()
