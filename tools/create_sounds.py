import os
import wave
import struct
import math
import random

os.makedirs("assets/sounds", exist_ok=True)
SAMPLE_RATE = 22050

def save_wav(filename, samples):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1) # mono
        f.setsampwidth(2) # 16-bit
        f.setframerate(SAMPLE_RATE)
        data = bytearray()
        for s in samples:
            # clamp to -1.0 .. 1.0
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767)
            data.extend(struct.pack('<h', int_val))
        f.writeframes(data)

# 1. PUNCH HIT
def make_punch():
    duration = 0.12
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = (1.0 - i / n) ** 2.5
        # Transient click + low punch thud (140Hz dropping to 50Hz)
        freq = 140.0 - (t / duration) * 90.0
        tone = math.sin(2 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * max(0.0, 1.0 - t * 40.0)
        samples.append((tone * 0.7 + noise * 0.5) * env)
    save_wav("assets/sounds/punch.wav", samples)

# 2. HEAVY HIT (Finisher / Knockdown impact)
def make_heavy():
    duration = 0.22
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = (1.0 - i / n) ** 2.0
        freq = 110.0 - (t / duration) * 70.0
        # Distorted square/sine wave for punchy crunch
        s = math.sin(2 * math.pi * freq * t)
        s = max(-0.7, min(0.7, s * 2.0))
        noise = (random.random() * 2.0 - 1.0) * max(0.0, 1.0 - t * 25.0)
        samples.append((s * 0.75 + noise * 0.45) * env)
    save_wav("assets/sounds/heavy_hit.wav", samples)

# 3. WHOOSH / SWING
def make_whoosh():
    duration = 0.10
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (i / n))
        freq = 380.0 - (t / duration) * 200.0
        tone = math.sin(2 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * 0.7
        samples.append((tone * 0.3 + noise * 0.7) * env * 0.6)
    save_wav("assets/sounds/whoosh.wav", samples)

# 4. JUMP
def make_jump():
    duration = 0.14
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = (1.0 - i / n) ** 1.2
        # Ascending pitch
        freq = 150.0 + (t / duration) ** 0.8 * 280.0
        tone = math.sin(2 * math.pi * freq * t)
        samples.append(tone * env * 0.7)
    save_wav("assets/sounds/jump.wav", samples)

# 5. HURT / ENEMY GRUNT
def make_hurt():
    duration = 0.15
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = (1.0 - i / n) ** 2.0
        freq = 180.0 - (t / duration) * 90.0
        # Buzz wave
        s = math.sin(2 * math.pi * freq * t) + 0.5 * math.sin(4 * math.pi * freq * t)
        samples.append(s * env * 0.6)
    save_wav("assets/sounds/hurt.wav", samples)

# 6. KNOCKDOWN (Body slam onto asphalt)
def make_knockdown():
    duration = 0.30
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = (1.0 - i / n) ** 2.2
        freq = 90.0 - (t / duration) * 55.0
        tone = math.sin(2 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0) * max(0.0, 1.0 - t * 15.0)
        samples.append((tone * 0.8 + noise * 0.5) * env)
    save_wav("assets/sounds/knockdown.wav", samples)

# 7. SPECIAL ATTACK (Dragon Sweep power charge + spin)
def make_special():
    duration = 0.45
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * min(1.0, t * 4.0)) * (1.0 - t / duration)
        # Fast ascending arpeggio sweep
        freq = 200.0 + math.sin(t * 50.0) * 120.0 + t * 400.0
        s1 = math.sin(2 * math.pi * freq * t)
        s2 = math.sin(4 * math.pi * freq * t) * 0.5
        noise = (random.random() * 2.0 - 1.0) * 0.3
        samples.append((s1 + s2 + noise) * env * 0.7)
    save_wav("assets/sounds/special.wav", samples)

# 8. PICKUP / ITEM CHIME
def make_pickup():
    duration = 0.28
    n = int(SAMPLE_RATE * duration)
    samples = []
    notes = [523.25, 659.25, 1046.50] # C5, E5, C6
    for i in range(n):
        t = i / SAMPLE_RATE
        note_idx = min(2, int(t / (duration / 3.0)))
        note_t = t - note_idx * (duration / 3.0)
        env = (1.0 - note_t / (duration / 3.0)) ** 1.5
        freq = notes[note_idx]
        tone = math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)
        samples.append(tone * env * 0.6)
    save_wav("assets/sounds/pickup.wav", samples)

# 9. GO ALERT (Classic Streets of Rage 2-tone chime)
def make_go():
    duration = 0.35
    n = int(SAMPLE_RATE * duration)
    samples = []
    notes = [660.0, 880.0]
    for i in range(n):
        t = i / SAMPLE_RATE
        note_idx = 0 if t < 0.15 else 1
        note_t = t if note_idx == 0 else (t - 0.15)
        env = (1.0 - note_t / 0.2) ** 1.3
        freq = notes[note_idx]
        tone = math.sin(2 * math.pi * freq * t) + 0.2 * math.sin(3 * math.pi * freq * t)
        samples.append(tone * max(0.0, env) * 0.65)
    save_wav("assets/sounds/go.wav", samples)

# 10. WAVE CLEAR (Stage fanfare)
def make_clear():
    duration = 0.60
    n = int(SAMPLE_RATE * duration)
    samples = []
    notes = [440.0, 554.37, 659.25, 880.0] # A Major fanfare
    for i in range(n):
        t = i / SAMPLE_RATE
        note_idx = min(3, int(t / (duration / 4.0)))
        note_t = t - note_idx * (duration / 4.0)
        env = (1.0 - note_t / (duration / 4.0)) ** 1.3
        freq = notes[note_idx]
        tone = math.sin(2 * math.pi * freq * t) + 0.4 * math.sin(2 * math.pi * freq * 2 * t)
        samples.append(tone * env * 0.7)
    save_wav("assets/sounds/clear.wav", samples)

# 11. RETRO SYNTH BGM LOOP (Yuzo Koshiro / Streets of Rage vibe!)
def make_bgm():
    # 4 bars loop (~6 seconds)
    bpm = 124.0
    beat_dur = 60.0 / bpm
    total_beats = 16
    total_dur = total_beats * beat_dur # ~7.74s
    n = int(SAMPLE_RATE * total_dur)
    samples = [0.0] * n

    # Slap bass notes (frequencies in Hz): F# minor groove: F#2, A2, B2, C#3, E2
    bass_pattern = [
        92.5, 92.5, 110.0, 92.5,  # F#2, F#2, A2, F#2
        123.47, 92.5, 138.59, 92.5, # B2, F#2, C#3, F#2
        82.4, 82.4, 92.5, 110.0,    # E2, E2, F#2, A2
        123.47, 138.59, 110.0, 92.5 # B2, C#3, A2, F#2
    ]

    for beat in range(total_beats):
        b_start = int(beat * beat_dur * SAMPLE_RATE)
        b_len = int(beat_dur * SAMPLE_RATE)
        
        # Bass note
        freq = bass_pattern[beat % len(bass_pattern)]
        for i in range(min(b_len, n - b_start)):
            t = i / SAMPLE_RATE
            env = (1.0 - i / b_len) ** 1.8
            # Synth FM bass
            mod = math.sin(2 * math.pi * freq * 2 * t) * 1.5
            s = math.sin(2 * math.pi * freq * t + mod)
            samples[b_start + i] += s * env * 0.35

        # Drum kick on beats 0, 2, 4, 6, 8, 10, 12, 14
        if beat % 2 == 0:
            k_len = int(0.15 * SAMPLE_RATE)
            for i in range(min(k_len, n - b_start)):
                t = i / SAMPLE_RATE
                k_env = (1.0 - i / k_len) ** 3.0
                k_freq = 130.0 - (t / 0.15) * 90.0
                samples[b_start + i] += math.sin(2 * math.pi * k_freq * t) * k_env * 0.55

        # Snare / clap on beats 1, 3, 5, 7, 9, 11, 13, 15
        if beat % 2 == 1:
            sn_len = int(0.18 * SAMPLE_RATE)
            for i in range(min(sn_len, n - b_start)):
                t = i / SAMPLE_RATE
                sn_env = (1.0 - i / sn_len) ** 2.2
                noise = (random.random() * 2.0 - 1.0) * 0.4
                tone = math.sin(2 * math.pi * 180.0 * t) * 0.3
                samples[b_start + i] += (noise + tone) * sn_env * 0.45

        # Hi-hat on every 8th note
        for sub in [0, 0.5]:
            hh_start = b_start + int(sub * beat_dur * SAMPLE_RATE)
            hh_len = int(0.04 * SAMPLE_RATE)
            for i in range(min(hh_len, n - hh_start)):
                hh_env = (1.0 - i / hh_len) ** 2.0
                noise = (random.random() * 2.0 - 1.0) * 0.2
                samples[hh_start + i] += noise * hh_env

    save_wav("assets/sounds/bgm.wav", samples)

print("Synthesizing retro sound pack...")
make_punch()
make_heavy()
make_whoosh()
make_jump()
make_hurt()
make_knockdown()
make_special()
make_pickup()
make_go()
make_clear()
make_bgm()
print("All audio files generated successfully!")
