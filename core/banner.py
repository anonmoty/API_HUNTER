import random
import time
import sys
import os
from datetime import datetime
from core.colors import C

# Dark Green + Red color palette
DG = '\033[38;5;22m'   # Dark Green
MG = '\033[38;5;34m'   # Medium Green
LG = '\033[38;5;46m'   # Light Green (Neon)
DR = '\033[38;5;124m'  # Dark Red
MR = '\033[38;5;196m'  # Medium Red (Neon)
LR = '\033[38;5;203m'  # Light Red
DIM = '\033[2m'
BOLD = '\033[1m'
RESET = '\033[0m'
CY = '\033[96m'
Y = '\033[93m'
W = '\033[97m'

LOGO = r"""
 █████╗ ██████╗ ██╗    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██╔══██╗██╔══██╗██║    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
███████║██████╔╝██║    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██╔══██║██╔═══╝ ██║    ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║██║     ██║    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝"""

TAGLINE = "Ultimate Web App API Endpoint Discovery Framework"

def matrix_rain(lines=2, width=68):
    """Matrix-style falling characters"""
    chars = "01アイウエオカキクケコサシスセソ{}[]<>/\\|=+-*&^%$#@!"
    for _ in range(lines):
        line = ""
        for _ in range(width):
            r = random.random()
            if r < 0.25:
                line += DG + random.choice(chars) + RESET
            elif r < 0.35:
                line += LG + random.choice(chars) + RESET
            else:
                line += " "
        print("  " + line)

def glitch_frame(text, intensity=3):
    """Create a glitched version of text safely"""
    if not text or len(text) <= 1:
        return text
    glitch_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`━━❖❖♥𝄞⋆⃝🌻ATTACKING♀️❖❖━━"
    result = list(text)
    safe_intensity = min(intensity, len(result))
    for _ in range(safe_intensity):
        pos = random.randint(0, len(result) - 1)
        if result[pos] != ' ':
            result[pos] = random.choice(glitch_chars)
    return "".join(result)

def typing_effect(text, color="", delay=0.015):
    """Typewriter animation"""
    for char in text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_bar(label, duration=0.4, width=32):
    """Animated loading bar"""
    steps = 15
    for i in range(steps + 1):
        filled = int(width * i / steps)
        bar = LG + "█" * filled + RESET + DG + "░" * (width - filled) + RESET
        pct = int(100 * i / steps)
        sys.stdout.write("\r  " + MR + "[" + RESET + bar + MR + "]" + RESET + " " + LG + str(pct).rjust(3) + "%" + RESET + " " + DIM + label + RESET)
        sys.stdout.flush()
        time.sleep(duration / steps)
    print()

def show_banner():
    os.system("clear" if os.name != "nt" else "cls")

    # Phase 1: Matrix Rain
    print()
    matrix_rain(2)

    # Phase 2: Logo with Glitch Effect
    raw_lines = [l for l in LOGO.split("\n") if l.strip()]

    # Quick glitch pass
    for frame in range(2):
        for line in raw_lines:
            glitched = glitch_frame(line, 4 - frame)
            sys.stdout.write("\r" + DR + glitched + RESET)
            sys.stdout.flush()
        time.sleep(0.04)
        sys.stdout.write("\r" + " " * 80 + "\r")

    # Final Logo with Red -> Green Gradient
    print()
    for i, line in enumerate(raw_lines):
        if i < 2:
            color = MR
        elif i < 4:
            color = LG
        else:
            color = MG
        print(color + BOLD + line + RESET)
        time.sleep(0.03)

    # Phase 3: Box Header with Animated Border
    sep = "═" * 70
    print()
    sys.stdout.write("  " + DR + "╔" + sep + "╗" + RESET + "\n")

    # Tagline with typing effect
    sys.stdout.write("  " + DR + "║" + RESET + "  ")
    typing_effect(TAGLINE, LG, 0.01)

    info_lines = [
        ("Version", "2.0 Ultimate", LG),
        ("Modules", "12 Extraction Engines", LG),
        ("Threads", "40 Concurrent Workers", LG),
        ("Developer", "Maxod anonmoty " + chr(9670), MR),
        ("Warning", "Authorized Bug Bounty Testing Only", Y),
        ("Session", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), DIM),
    ]

    for label, value, color in info_lines:
        line_content = "    " + DIM + label.ljust(12) + RESET + color + BOLD + value + RESET
        # 70 is the inner width
        pad_len = 70 - (len(label) + 4 + len(value) + 4)
        if pad_len < 0:
            pad_len = 0
        print("  " + DR + "║" + RESET + line_content + (" " * pad_len) + DR + "║" + RESET)
        time.sleep(0.02)

    sys.stdout.write("  " + DR + "╚" + sep + "╝" + RESET + "\n")

    # Phase 4: Fast Loading Indicators
    print()
    loading_bar("Initializing extraction engines...", 0.3)
    loading_bar("Loading API endpoint heuristics...", 0.2)
    loading_bar("Multi-thread worker pool ready...", 0.2)

    # Phase 5: Ready Signal
    print()
    print("  " + LG + BOLD + "[✓]" + RESET + " " + W + "APIHunter v2.0 " + DIM + "ready. Select an extraction module." + RESET)
    print()
