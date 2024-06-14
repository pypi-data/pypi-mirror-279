import subprocess
import os
import platform

def overlay_audio(input_video_path, overlay_audio_path, output_video_path, original_vol=100, overlay_vol=50, use_shortest_flag=True):
    original_volume = original_vol / 100.0
    overlay_volume = overlay_vol / 100.0

    shortest_option = '-shortest' if use_shortest_flag else ''

    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-i', overlay_audio_path,
        '-filter_complex', f'[0:a]volume={original_volume}[out1];[1:a]volume={overlay_volume}[out2];[out1][out2]amix=inputs=2[a]',
        '-map', '0:v',
        '-map', '[a]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        shortest_option,
        output_video_path
    ]

    # Удаляем пустые строки из команды
    command = [arg for arg in command if arg]

    subprocess.run(command)

def clear_console():
    # Очистка консоли в зависимости от ОС
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def main():
    while True:
        print("Made by Avinion")
        print("Telegram: @akrim")
        input_video_path = input("Введите путь к входному видео файлу: ")
        overlay_audio_path = input("Введите путь к аудио файлу для наложения: ")
        output_video_path = input("Введите путь для сохранения выходного видео файла: ")
        original_vol = float(input("Введите громкость исходной аудиодорожки в процентах (по умолчанию 100): ") or 100)
        overlay_vol = float(input("Введите громкость наложенной аудиодорожки в процентах (по умолчанию 50): ") or 50)
        use_shortest_str = input("Использовать опцию -shortest для сокращения длительности до минимальной из входных файлов? (y/n): ")
        use_shortest_flag = (use_shortest_str.lower() == 'y')

        overlay_audio(input_video_path, overlay_audio_path, output_video_path, original_vol, overlay_vol, use_shortest_flag)

        continue_work = input("Хотите продолжить работу? (Y/N): ").strip().lower()
        if continue_work != 'y':
            break
        clear_console()

if __name__ == "__main__":
    main()
