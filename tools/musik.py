"""Erzeugt eine eigene, lizenzfreie Hintergrundmusik (sanfter Corporate-Beat) als WAV.
Aufruf: python3 musik.py ziel.wav [sekunden] [seed]"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
out = sys.argv[1]; dur = float(sys.argv[2]) if len(sys.argv) > 2 else 16.0
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rng = np.random.default_rng(seed)
bpm = 104; beat = 60 / bpm; n = int(SR * dur); t = np.arange(n) / SR
mix = np.zeros(n)

def note(f): return 440 * 2 ** ((f - 69) / 12)
def env(length, a=0.01, r=0.3):
    e = np.ones(length); ai = int(a * SR); ri = int(r * SR)
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return e
def add(sig, start):
    s = int(start * SR); e = min(n, s + len(sig))
    if s < n: mix[s:e] += sig[:e - s]

# Akkorde (C – Am – F – G), warme Pads
progs = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]
bar = 4 * beat
for k in range(int(dur / bar) + 1):
    ch = progs[k % 4]; L = int(bar * SR) + int(0.4 * SR); tt = np.arange(L) / SR
    pad = sum(np.sin(2 * np.pi * note(m) * tt) + 0.3 * np.sin(2 * np.pi * note(m) * 2.005 * tt) for m in ch)
    add(0.05 * pad * env(L, 0.3, 0.6), k * bar)
    # Bass auf 1 und 3
    for b in (0, 2):
        Lb = int(beat * 1.8 * SR); tb = np.arange(Lb) / SR
        add(0.22 * np.sin(2 * np.pi * note(ch[0] - 24) * tb) * env(Lb, 0.01, 0.4), k * bar + b * beat)
    # Arpeggio Achtel
    for i in range(8):
        m = ch[[0, 1, 2, 3, 2, 1, 2, 3][i]] + 12; La = int(beat * 0.5 * SR); ta = np.arange(La) / SR
        add(0.045 * np.sin(2 * np.pi * note(m) * ta) * np.exp(-ta * 9), k * bar + i * beat / 2)

# Drums: Kick, Clap, Hi-Hat
for i in range(int(dur / beat) + 1):
    st = i * beat; Lk = int(0.25 * SR); tk = np.arange(Lk) / SR
    if i % 2 == 0: add(0.5 * np.sin(2 * np.pi * (50 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 14), st)
    else:
        Lc = int(0.15 * SR); add(0.12 * rng.standard_normal(Lc) * np.exp(-np.arange(Lc) / SR * 30), st)
    for h in (0, 0.5):
        Lh = int(0.05 * SR); add(0.035 * rng.standard_normal(Lh) * np.exp(-np.arange(Lh) / SR * 80), st + h * beat)

b, a = butter(2, 9000 / (SR / 2)); mix = lfilter(b, a, mix)
fade = int(1.2 * SR); mix[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR)); mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix / np.max(np.abs(mix)) * 0.8
wavfile.write(out, SR, np.stack([mix, mix], 1).astype(np.float32))
print("Musik ✓", out)
