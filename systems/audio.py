import random
from pathlib import Path

import pygame


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"
SFX_DIR = ASSET_DIR / "SFX"
SOUNDTRACK_DIR = ASSET_DIR / "soundtracks"

SFX_FILES = {
    "wave_start": SFX_DIR / "startwave.mp3",
    "wave_over": SFX_DIR / "waveover.mp3",
    "game_over": SFX_DIR / "gameover.mp3",
    "cannon_turret": SFX_DIR / "cannonshot.mp3",
    "laser_turret": SFX_DIR / "lasershot.mp3"
}
EXPLOSION_FILES = sorted(SFX_DIR.glob("explosion*.mp3"))
SOUNDTRACK_FILES = sorted(SOUNDTRACK_DIR.glob("*.mp3"))
MUSIC_PAUSE_MS = 2000

effects_volume = 1.0
music_volume = 1.0
audio_enabled = True
music_started = False
waiting_for_music = False
next_music_at = 0
sound_cache = {}
current_soundtrack = None


def configure(new_effects_volume=None, new_music_volume=None):
    global effects_volume, music_volume

    if new_effects_volume is not None:
        effects_volume = _volume_to_float(new_effects_volume)
        for sound in sound_cache.values():
            sound.set_volume(effects_volume)

    if new_music_volume is not None:
        music_volume = _volume_to_float(new_music_volume)
        if _mixer_ready():
            pygame.mixer.music.set_volume(music_volume)


def play_sfx(sound_name):
    sound_path = SFX_FILES.get(sound_name)
    if sound_path is None:
        return

    sound = _load_sound(sound_path)
    if sound:
        sound.play()


def play_random_explosion():
    if not EXPLOSION_FILES:
        return

    sound = _load_sound(random.choice(EXPLOSION_FILES))
    if sound:
        sound.play()


def start_music():
    global music_started

    music_started = True
    if not _mixer_ready() or pygame.mixer.music.get_busy():
        return

    _schedule_next_soundtrack()


def update_music():
    if not music_started or not _mixer_ready():
        return

    if not pygame.mixer.music.get_busy() and not waiting_for_music:
        _schedule_next_soundtrack()

    if waiting_for_music and pygame.time.get_ticks() >= next_music_at:
        _play_random_soundtrack()


def _schedule_next_soundtrack():
    global waiting_for_music, next_music_at

    waiting_for_music = True
    next_music_at = pygame.time.get_ticks() + MUSIC_PAUSE_MS


def _play_random_soundtrack():
    global current_soundtrack, waiting_for_music

    if not SOUNDTRACK_FILES:
        waiting_for_music = False
        return

    next_soundtrack = random.choice(SOUNDTRACK_FILES)

    if len(SOUNDTRACK_FILES) > 1:
        while next_soundtrack == current_soundtrack:
            next_soundtrack = random.choice(SOUNDTRACK_FILES)

    try:
        pygame.mixer.music.load(next_soundtrack)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play()
        current_soundtrack = next_soundtrack
        waiting_for_music = False
    except pygame.error:
        waiting_for_music = False
        _disable_audio()


def _load_sound(sound_path):
    if not _mixer_ready() or not sound_path.exists():
        return None

    if sound_path not in sound_cache:
        try:
            sound_cache[sound_path] = pygame.mixer.Sound(sound_path)
        except pygame.error:
            _disable_audio()
            return None

    sound = sound_cache[sound_path]
    sound.set_volume(effects_volume)
    return sound


def _mixer_ready():
    if not audio_enabled:
        return False

    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
    except pygame.error:
        _disable_audio()
        return False

    return True


def _disable_audio():
    global audio_enabled
    audio_enabled = False


def _volume_to_float(volume):
    return max(0, min(100, int(volume))) / 100
