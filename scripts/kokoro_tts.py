## Description: This script is used to run the Kokoro TTS locally.
"""
Modified version to run concurrently on an M2 Mac and save the final WAV file.
"""
# pip install -q uv && uv pip install kokoro tqdm soundfile
import re
import numpy as np
import soundfile as sf
from kokoro import KPipeline
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize the TTS pipeline once.
# (If you encounter thread-safety issues, consider initializing a pipeline inside the worker function.)
pipeline = KPipeline(lang_code="a")  # American English voice

# Input Text:
text = """
 Speech synthesis is the artificial production of human speech. A computer system used for this purpose is called a speech synthesizer, and can be implemented in software or hardware products. A text-to-speech (TTS) system converts normal language text into speech; other systems render symbolic linguistic representations like phonetic transcriptions into speech. The reverse process is speech recognition. 

 """

# Define a split pattern (splitting on one or more newline characters)
split_pattern = r"\n+"
# Split the text into individual chunks (skipping any empty chunks)
chunks = [chunk.strip() for chunk in re.split(split_pattern, text) if chunk.strip()]


# Helper function that processes a single chunk.
def process_chunk(index, chunk, debug=False):
    # Process the chunk using the pipeline. Disable splitting to get the entire audio.
    gen = pipeline(chunk, voice="af_heart", speed=1, split_pattern=None)
    # The generator should yield one tuple: (graphemes, phonemes, audio)
    gs, ps, audio = next(gen)
    # For debugging, you could print gs or ps, but here we omit any output.
    if debug:
        print(f"Chunk {index} | Graphemes: {gs}")
        print(f"Chunk {index} | Phonemes: {ps}")
    return index, audio


# Process all chunks concurrently.
results = []
with ThreadPoolExecutor() as executor:
    # Submit tasks for each chunk, tagging them with their index so we can reassemble them in order.
    futures = [
        executor.submit(process_chunk, i, chunk) for i, chunk in enumerate(chunks)
    ]
    for future in as_completed(futures):
        results.append(future.result())

# Sort the results by the original chunk order.
results.sort(key=lambda x: x[0])
# Extract the audio arrays in the correct order.
all_audio = [audio for _, audio in results]

# Combine all the audio chunks into one final audio array.
combined_audio = np.concatenate(all_audio)

# Save the combined audio as a WAV file.
sf.write("combined_output.wav", combined_audio, 24000)
print("Saved combined audio to combined_output.wav")
