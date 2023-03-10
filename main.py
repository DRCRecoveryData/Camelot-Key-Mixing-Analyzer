import os
import colorama
from colorama import Fore
import librosa

# Define the colors for each Camelot key
COLORS = {
    "1A": Fore.RED,
    "1B": Fore.RED,
    "2A": Fore.BLUE,
    "2B": Fore.BLUE,
    "3A": Fore.GREEN,
    "3B": Fore.GREEN,
    "4A": Fore.YELLOW,
    "4B": Fore.YELLOW,
    "5A": Fore.CYAN,
    "5B": Fore.CYAN,
    "6A": Fore.MAGENTA,
    "6B": Fore.MAGENTA,
    "7A": Fore.WHITE,
    "7B": Fore.WHITE,
    "8A": Fore.RED,
    "8B": Fore.RED,
    "9A": Fore.BLUE,
    "9B": Fore.BLUE,
    "10A": Fore.GREEN,
    "10B": Fore.GREEN,
}

def get_energy_level(filename):
    # Load the audio file
    y, sr = librosa.load(filename)
    
    # Compute the tempo and key
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    key, mode = librosa.key.detect(y=y, sr=sr)
    
    # Calculate the energy level
    rms = librosa.feature.rms(y=y)[0]
    energy = librosa.core.amplitude_to_db(rms, ref=0.01)
    level = int(round(librosa.util.normalize(energy, axis=0)[0] * 9)) + 1
    if level < 1:
        level = 1
    elif level > 10:
        level = 10
    
    # Convert the key to the Camelot notation and colorize it
    if mode == "major":
        key_camelot = str((key % 12) + 1) + "A"
    else:
        key_camelot = str((key + 3) % 12 + 1) + "B"
    key_color = COLORS.get(key_camelot, Fore.RESET)
    key_camelot_colored = f"{key_color}{key_camelot}{Fore.RESET}"
    
    return tempo, key_camelot_colored, level

# Initialize colorama
colorama.init()

# Get the input directory path from the user
dir_path = input("Enter the path to the directory containing audio files: ")

# Get a list of all audio files in the directory
audio_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".mp3") or f.endswith(".wav")]

# Analyze each audio file and print the results
for file in audio_files:
    # Calculate the tempo, key, and energy level
    tempo, key, level = get_energy_level(file)

    # Print the results
    print(f"File: {os.path.basename(file)}")
    print(f"Tempo: {int(round(tempo))} BPM")
    print(f"Key: {key}")
    print(f"Energy Level: {level}")
    print("\n") # Add a newline between each file's results

# Deinitialize colorama
colorama.deinit()
