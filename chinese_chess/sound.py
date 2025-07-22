import pygame
import os

pygame.mixer.init()

_sound_cache = {}

def play_sound_async(filepath: str) -> None:
    if not os.path.isfile(filepath):
        print(f"[播放错误] 文件不存在: {filepath}")
        return

    abs_path = os.path.abspath(filepath)

    # 如果已缓存，则使用缓存的 Sound 对象
    if abs_path in _sound_cache:
        sound = _sound_cache[abs_path]
    else:
        try:
            sound = pygame.mixer.Sound(abs_path)
            _sound_cache[abs_path] = sound
        except Exception as e:
            print(f"[播放错误] 加载失败: {e}")
            return

    try:
        sound.play()
    except Exception as e:
        print(f"[播放错误] 播放失败: {e}")


