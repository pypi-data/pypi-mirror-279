import os
import subprocess
import json

messages = {
    "en": {
        "choose_language": "Choose the language for the script / Выберите язык для скрипта (E/R): ",
        "ffmpeg_not_installed": "ffmpeg or ffprobe are not installed. Please install them and try again.",
        "enter_video_path": "Enter the path to the video file or its name: ",
        "file_not_found": "File {file} not found.",
        "add_another_file": "Add another file? (Y/N): ",
        "best_video": "\nBest video: {file}",
        "video_info": "Information about the best video:",
        "stream_info": "\n{stream_type} stream:",
        "continue_script": "Continue with the script? (Y/N): ",
        "made_by": "\nMade by Avinion",
        "telegram": "Telegram: @akrim",
        "invalid_input": "Invalid input. Please enter 'E' for English or 'R' for Russian."
    },
    "ru": {
        "choose_language": "Choose the language for the script / Выберите язык для скрипта (E/R): ",
        "ffmpeg_not_installed": "ffmpeg или ffprobe не установлены. Пожалуйста, установите их и повторите попытку.",
        "enter_video_path": "Введите путь к видео файлу или его имя: ",
        "file_not_found": "Файл {file} не найден.",
        "add_another_file": "Добавить еще один файл? (Y/N): ",
        "best_video": "\nЛучшее видео: {file}",
        "video_info": "Информация о лучшем видео:",
        "stream_info": "\n{stream_type} поток:",
        "continue_script": "Продолжить работу со скриптом? (Y/N): ",
        "made_by": "\nСделано Avinion",
        "telegram": "Telegram: @akrim",
        "invalid_input": "Неправильный ввод. Пожалуйста, введите 'E' для английского или 'R' для русского."
    }
}

def check_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["ffprobe", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print(messages[lang]["ffmpeg_not_installed"])
        exit(1)

def get_video_info(video_path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0 or not result.stdout:
        print(f"Ошибка при обработке файла {video_path}: {result.stderr.decode('utf-8')}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Невозможно декодировать JSON для файла {video_path}")
        return None

def check_and_correct_file_path(input_path):
    possible_extensions = ['.mp4', '.mkv', '.avi']
    if os.path.exists(input_path):
        return input_path
    else:
        for ext in possible_extensions:
            if os.path.exists(f"{input_path}{ext}"):
                return f"{input_path}{ext}"
            elif os.path.exists(f"{os.getcwd()}/{input_path}{ext}"):
                return f"{os.getcwd()}/{input_path}{ext}"
    return None

def compare_videos(video_paths):
    video_infos = [get_video_info(path) for path in video_paths if path is not None]
    video_infos = [info for info in video_infos if info is not None]

    if not video_infos:
        return None, None

    criteria = ["bit_rate", "width", "height"]
    audio_criteria = ["bit_rate"]

    results = []
    for info in video_infos:
        video_result = {}
        audio_result = {}
        for stream in info["streams"]:
            if stream["codec_type"] == "video":
                video_result = {key: (round(int(stream.get(key, 0)) / 8000, 2) if key == "bit_rate" else stream.get(key, "N/A")) for key in criteria}
            elif stream["codec_type"] == "audio":
                audio_result = {key: round(int(stream.get(key, 0)) / 8000, 2) for key in audio_criteria}
        results.append({"video": video_result, "audio": audio_result})

    best_video_index = sorted(
        range(len(results)),
        key=lambda i: (int(results[i]["video"].get("bit_rate", 0)) * int(results[i]["video"].get("width", "0")) * int(results[i]["video"].get("height", "0")))
    )[-1]

    return video_paths[best_video_index], results[best_video_index]

def clear_console():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS, Linux, Termux (Android)
        os.system('clear')

def main():
    global lang
    while True:
        lang_choice = input("Choose the language for the script / Выберите язык для скрипта (E/R): ").upper()
        if lang_choice == 'E':
            lang = 'en'
            break
        elif lang_choice == 'R':
            lang = 'ru'
            break
        else:
            print("Invalid input. Please enter 'E' for English or 'R' for Russian.\nНеправильный ввод. Пожалуйста, введите 'E' для английского или 'R' для русского.")

    check_ffmpeg_installed()

    while True:
        video_paths = []
        while True:
            user_input = input(messages[lang]["enter_video_path"])
            corrected_path = check_and_correct_file_path(user_input)
            if corrected_path:
                video_paths.append(corrected_path)
            else:
                print(messages[lang]["file_not_found"].format(file=user_input))
            continue_adding = input(messages[lang]["add_another_file"]).upper()
            if continue_adding != "Y":
                break

        best_video, best_video_info = compare_videos(video_paths)
        if best_video and best_video_info:
            print(messages[lang]["best_video"].format(file=best_video))
            print(messages[lang]["video_info"])
            for stream_type, info in best_video_info.items():
                print(messages[lang]["stream_info"].format(stream_type=stream_type.capitalize()))
                for key, value in info.items():
                    print(f"{key}: {value}")
        else:
            print("Не удалось сравнить видео файлы.")

        print(messages[lang]["made_by"])
        print(messages[lang]["telegram"])

        continue_script = input(messages[lang]["continue_script"]).upper()
        if continue_script != "Y":
            break
        clear_console()

if __name__ == "__main__":
    main()
