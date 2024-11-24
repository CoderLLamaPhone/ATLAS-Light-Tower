import os
import wave
import numpy as np
import time
import threading
import pyaudio
from stupidArtnet import StupidArtnet

def play_wav_file(wav_file):
    # Open the WAV file
    wf = wave.open(wav_file, 'rb')
    # Create a PyAudio object
    p = pyaudio.PyAudio()
    # Open a stream to play the audio
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    # Read data in chunks
    chunk = 1024
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Close PyAudio
    p.terminate()
    
    
    
# Convert the peak frequency to a color
def frequency_to_color(frequency):
    # Normalize the frequency to the visible spectrum (400-700 THz)
    min_freq = -300
    max_freq = 600
    normalized_freq = (frequency - min_freq) / (max_freq - min_freq)
    # Convert the normalized frequency to RGB values
    if normalized_freq < 0.5:
        r = int(255 * (1 - normalized_freq / 0.5))
        g = int(128 * (normalized_freq / 0.5))  # Reduce the green component
        b = 0
    else:
        r = 0
        g = int(128 * (1 - (normalized_freq - 0.5) / 0.5))  # Reduce the green component
        b = int(255 * ((normalized_freq - 0.5) / 0.5))
    
    # Adjust brightness based on volume
    volume = np.abs(frequency)  # Use the absolute value of the frequency as a proxy for volume
    brightness = min(255, int(volume * 255 / (max_freq - min_freq)))  # Normalize volume to the range 0-255
    r = max(min(255, r + brightness),0)
    g = max(min(255, g + brightness),0)
    b = max(min(255, b + brightness),0)

    packet[LT_RED] = r
    packet[LT_GREEN] = g
    packet[LT_BLUE] = b
    
    return f'\x1b[38;2;{r};{g};{b}m'

def print_noise_level(wav_file, instance):
    # Open the WAV file
    with wave.open(wav_file, 'rb') as wf:
        # Set the position to the given instance
        wf.setpos(instance)
        # Read data in chunks
        chunk = 1024
        data = wf.readframes(chunk)
        while data:
            # Convert the frame to an array of integers
            frame = np.frombuffer(data, dtype=np.int16)
            # Calculate the noise level (RMS)
            if len(frame) > 0:
                # Perform FFT to get the frequency spectrum
                freqs = np.fft.fftfreq(len(frame), 1 / wf.getframerate())
                fft_spectrum = np.fft.fft(frame)
                # Get the frequency with the highest amplitude
                peak_freq = freqs[np.argmax(np.abs(fft_spectrum))]
            else:
                peak_freq = 0
            color = frequency_to_color(peak_freq)
            #print(color + f'Frequency: {peak_freq:.2f} Hz' + '\x1b[0m')
            # Create a color box in the terminal
            print(color + ('█' * 20 + '\n') * 5 + '\x1b[0m', end='\n', flush=True)
            # Read the next chunk
            data = wf.readframes(chunk)
            time.sleep(chunk / wf.getframerate() + 0.027)

target_ip = os.getenv('ARTNET_TARGET_IP', '127.0.0.1')

universe = 0                     # see docs
packet_size = 10            # it is not necessary to send whole universe

LT_RED = 0
LT_GREEN = 1
LT_BLUE = 2

# CREATING A STUPID ARTNET OBJECT
# SETUP NEEDS A FEW ELEMENTS
# TARGET_IP   = DEFAULT 127.0.0.1
# UNIVERSE    = DEFAULT 0
# PACKET_SIZE = DEFAULT 512
# FRAME_RATE  = DEFAULT 30
a = StupidArtnet(target_ip, universe, packet_size)

# MORE ADVANCED CAN BE SET WITH SETTERS IF NEEDED
# NET         = DEFAULT 0
# SUBNET      = DEFAULT 0

# CHECK INIT
print(a)

# YOU CAN CREATE YOUR OWN BYTE ARRAY OF PACKET_SIZE
packet = bytearray(packet_size)      # create packet for Artnet
a.set(packet)                        # only on changes

# TO SEND PERSISTANT SIGNAL YOU CAN START THE THREAD
a.start()

# Example usage
wav_file = 'around_the_world-atc.wav'
instance = 1000  # Change this to the desired instance

# Create a thread to play the WAV file
play_thread = threading.Thread(target=play_wav_file, args=(wav_file,))
play_thread.start()

# Print noise level in the main thread
print_noise_level(wav_file, instance)

# Wait for the play thread to finish
play_thread.join()

# Example usage
#wav_file = 'around_the_world-atc.wav'
#instance = 1000  # Change this to the desired instance
#print_noise_level(wav_file, instance)