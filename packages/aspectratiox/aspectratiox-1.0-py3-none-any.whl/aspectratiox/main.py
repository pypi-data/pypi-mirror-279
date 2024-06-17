import os
import platform
import subprocess

# Определяем команды для очистки консоли в зависимости от операционной системы
clear_command = 'cls' if platform.system() == 'Windows' else 'clear'

def clear_console():
    os.system(clear_command)

def get_aspect_ratio_dimensions(ratio_choice):
    # Реалистичные размеры для различных пропорций
    dimensions = {
        1: (1080, 1080),  # 1:1
        2: (1080, 1350),  # 4:5
        3: (1920, 1080),  # 16:9
        4: (1080, 1920),  # 9:16
        5: (1080, 720),   # 3:2
        6: (720, 1080),   # 2:3
        7: (1080, 1500),  # 5:7
        8: (1500, 1080)   # 7:5
    }
    return dimensions.get(ratio_choice, (1080, 1080))

def get_extension(ext_choice):
    extensions = {
        1: 'jpg',
        2: 'png',
        3: 'bmp',
        4: 'webp',
        5: 'tiff'
    }
    return extensions.get(ext_choice, 'jpg')

def resize_image(input_path, output_path, width, height):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'scale={width}:{height},crop={width}:{height}',
        '-q:v', '2',  # Устанавливаем качество JPEG
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Image successfully saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print(f"Command: {' '.join(command)}")

def main():
    print("Made by Avinion")
    print("Telegram: @akrim")
    language = None
    while True:
        if not language:
            language = input("Choose language / Выберите язык (E/R): ").strip().upper()
        
        if language == 'E':
            print("You chose English.")
            img_path_prompt = "Enter the local path to the image or the name of the image: "
            ratio_prompt = "Choose the number for the aspect ratio:\n" \
                           "1 - 1:1 (1080x1080)\n" \
                           "2 - 4:5 (1080x1350)\n" \
                           "3 - 16:9 (1920x1080)\n" \
                           "4 - 9:16 (1080x1920)\n" \
                           "5 - 3:2 (1080x720)\n" \
                           "6 - 2:3 (720x1080)\n" \
                           "7 - 5:7 (1080x1500)\n" \
                           "8 - 7:5 (1500x1080)\n"
            ext_prompt = "Choose the number for the extension:\n" \
                         "1 - jpg\n" \
                         "2 - png\n" \
                         "3 - bmp\n" \
                         "4 - webp\n" \
                         "5 - tiff\n"
            save_path_prompt = "Enter the local path to the directory to save the image (or just the name to save in the current directory): "
            continue_prompt = "Do you want to continue? (Y/N): "
        elif language == 'R':
            print("Вы выбрали русский.")
            img_path_prompt = "Введите локальный путь к изображению или имя изображения: "
            ratio_prompt = "Выберите номер для пропорции:\n" \
                           "1 - 1:1 (1080x1080)\n" \
                           "2 - 4:5 (1080x1350)\n" \
                           "3 - 16:9 (1920x1080)\n" \
                           "4 - 9:16 (1080x1920)\n" \
                           "5 - 3:2 (1080x720)\n" \
                           "6 - 2:3 (720x1080)\n" \
                           "7 - 5:7 (1080x1500)\n" \
                           "8 - 7:5 (1500x1080)\n"
            ext_prompt = "Выберите номер для расширения:\n" \
                         "1 - jpg\n" \
                         "2 - png\n" \
                         "3 - bmp\n" \
                         "4 - webp\n" \
                         "5 - tiff\n"
            save_path_prompt = "Введите локальный путь к директории для сохранения изображения (или просто имя для сохранения в текущей директории): "
            continue_prompt = "Вы хотите продолжить? (Y/N): "
        else:
            print("Invalid choice. Please choose E or R. / Неправильный выбор. Пожалуйста, выберите E или R.")
            language = None
            continue

        input_path = input(img_path_prompt).strip().replace('"', '')
        print(ratio_prompt)
        ratio_choice = int(input().strip())
        width, height = get_aspect_ratio_dimensions(ratio_choice)
        print(ext_prompt)
        ext_choice = int(input().strip())
        extension = get_extension(ext_choice)
        save_path = input(save_path_prompt).strip().replace('"', '')
        
        if not os.path.isdir(os.path.dirname(save_path)) and os.path.dirname(save_path):
            os.makedirs(os.path.dirname(save_path))

        if os.path.isdir(save_path) or save_path == "":
            output_path = os.getcwd() if save_path == "" else save_path
            output_file = os.path.join(output_path, f"converted_image.{extension}")
        else:
            output_file = save_path if save_path.endswith(f".{extension}") else f"{save_path}.{extension}"

        resize_image(input_path, output_file, width, height)
        
        continue_choice = input(continue_prompt).strip().upper()
        if continue_choice != 'Y':
            break
        
        clear_console()

if __name__ == "__main__":
    main()
