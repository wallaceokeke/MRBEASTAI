# Conversational AI Strategist – Hugging Face Upload Version

"""
This script is a ready-to-deploy Conversational AI Strategist designed for use on Hugging Face Spaces or locally.
It explains elite content strategies (e.g., MrBeast, Gary Vee, Khaby Lame, KSI) with structured logic,
a CLI interface, and growth mindset philosophies.

To use this script:
1. Clone or upload it to Hugging Face Spaces (Python environment).
2. Run the CLI or adapt for a web UI (Gradio/Streamlit).
3. Expand profiles or hook to external data for broader use.

Author: Okeke Wallace Brown (AI Developer)
"""

import difflib
import pyttsx3
import time
import os
import json
import threading
import random


# Load pronunciation dictionary
def load_pronunciations(filename="pronunciations.txt"):
    pronunciations = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    word, pron = line.strip().split(":", 1)
                    pronunciations[word.lower()] = pron.strip()
    except FileNotFoundError:
        pass
    return pronunciations


PRONUNCIATIONS = load_pronunciations()


# Load alias mapping
def load_aliases(filename="aliases.txt"):
    alias_map = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    alias, canonical = line.strip().split(":", 1)
                    alias_map[alias.lower()] = canonical.lower()
    except FileNotFoundError:
        pass
    return alias_map


ALIAS_MAP = load_aliases()

# Map canonical keys to (filename, display name)
creator_files = {
    "mrbeast": ("mrbeast.txt", "Mister Beast"),
    "gary_vee": ("gary_vee.txt", "Gary Vee"),
    "khaby_lame": ("khaby_lame.txt", "Khaby Lame"),
    "ksi": ("ksi.txt", "K S I"),
}


# Self-learning: Load and save influencer knowledge
def load_influencer_data(filename="influencers.json"):
    if not os.path.exists(filename):
        return {"recent_searches": [], "user_vibes": {}}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_influencer_data(data, filename="influencers.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


influencer_data = load_influencer_data()

# TTS setup: American English female, warm, slow
engine = pyttsx3.init()
voices = engine.getProperty("voices")
selected_voice = None
for voice in voices:
    if ("female" in voice.name.lower() or "zira" in voice.name.lower()) and (
        "en_us" in voice.id.lower()
        or "us" in voice.id.lower()
        or "zira" in voice.id.lower()
    ):
        selected_voice = voice.id
        break
if not selected_voice:
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            selected_voice = voice.id
            break
if selected_voice:
    engine.setProperty("voice", selected_voice)
engine.setProperty("rate", 145)

SPEAKING = True
last_influencer = None
last_section = 0
user_name = "friend"
idle_timer = None
exit_timer = None


def speak(text):
    if not SPEAKING:
        return
    words = text.split()
    spoken = []
    for word in words:
        pron = PRONUNCIATIONS.get(word.lower(), word)
        spoken.append(pron)
    say_text = " ".join(spoken)
    engine.say(say_text)
    engine.runAndWait()
    time.sleep(0.3)


def load_creator_profile(filename):
    path = os.path.join("creators", filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf8") as f:
        return f.read()


def find_canonical_key(user_input):
    aliases = list(ALIAS_MAP.keys())
    match = difflib.get_close_matches(user_input.lower(), aliases, n=1, cutoff=0.7)
    if match:
        return ALIAS_MAP[match[0]]
    return None


def idle_prompt():
    speak(
        f"Hey {user_name}, are you still there? Want to keep talking about influencers or try someone new?"
    )
    print(
        f"\nHey {user_name}, are you still there? Want to keep talking about influencers or try someone new?"
    )
    start_exit_timer()


def start_exit_timer():
    global exit_timer
    if exit_timer:
        exit_timer.cancel()
    exit_timer = threading.Timer(10.0, confirm_exit)
    exit_timer.daemon = True
    exit_timer.start()


def confirm_exit():
    speak(
        "Looks like you're away. I'll exit now, but you can always come back to learn more about your favorite creators!"
    )
    print(
        "Looks like you're away. I'll exit now, but you can always come back to learn more about your favorite creators!"
    )
    exit(0)


def reset_idle_timer():
    global idle_timer, exit_timer
    if idle_timer:
        idle_timer.cancel()
    if exit_timer:
        exit_timer.cancel()
    idle_timer = threading.Timer(90.0, idle_prompt)
    idle_timer.daemon = True
    idle_timer.start()


def explain_creator_profile(filename, display_name, start_section=0):
    global last_influencer, last_section
    profile = load_creator_profile(filename)
    if not profile:
        print(f"Sorry, I couldn't find the profile for {display_name}.")
        speak(f"Sorry, I couldn't find the profile for {display_name}.")
        return
    sections = profile.split("\n\n")
    last_influencer = filename
    for idx, section in enumerate(sections[start_section:], start=start_section):
        last_section = idx
        lines = section.strip().splitlines()
        for line in lines:
            print(line)
            speak(line)
        time.sleep(1.2)  # Pause for natural flow


def strategist_chat():
    global SPEAKING, last_influencer, last_section, user_name
    welcome = "\nWelcome to Know Your Influencer and Creators 🎯 – Powered by Hugging Face Protocol\n\nWhat's your name?"
    print(welcome)
    speak("Welcome to Know Your Influencer and Creators. What's your name?")
    user_name = input("Your name: ").strip() or "friend"
    speak(
        f"Nice to meet you, {user_name}! Who are you curious about today? For example, Mister Beast, Gary Vee, Khaby Lame, or K S I."
    )
    print(
        f"\nHi {user_name}, who are you curious about today? (e.g., Mister Beast, Gary Vee, Khaby Lame, K S I)"
    )

    reset_idle_timer()
    while True:
        query = input("\nYou: ").strip().lower()
        reset_idle_timer()
        if "exit" in query:
            goodbye = f"Goodbye {user_name}, keep scaling your influence!"
            print(goodbye)
            speak(goodbye)
            break
        if "resume" in query and last_influencer:
            # Resume from where left off
            display_name = [
                v[1] for k, v in creator_files.items() if v[0] == last_influencer
            ][0]
            speak(f"Let's continue with {display_name}.")
            explain_creator_profile(last_influencer, display_name, last_section + 1)
            continue
        canonical_key = find_canonical_key(query)
        if canonical_key and canonical_key in creator_files:
            display_name = creator_files[canonical_key][1]
            if get_confirmation(
                f"Ooh, I hope you meant {display_name}. Should I go on?"
            ):
                influencer_data["recent_searches"].append(display_name)
                save_influencer_data(influencer_data)
                explain_creator_profile(*creator_files[canonical_key])
                if canonical_key == "mrbeast":
                    share_fact_about_mrbeast()
            else:
                speak("No worries! Who else are you interested in?")
                print("No worries! Who else are you interested in?")
        else:
            aliases = list(ALIAS_MAP.keys())
            suggestion = difflib.get_close_matches(query, aliases, n=1, cutoff=0.3)
            if suggestion:
                suggested_key = ALIAS_MAP[suggestion[0]]
                if suggested_key in creator_files:
                    suggestion_name = creator_files[suggested_key][1]
                    msg = f"Ooh, did you mean {suggestion_name}? Should I go on?"
                    print(msg)
                    speak(msg)
                    confirm = input("(yes/no): ").strip().lower()
                    if confirm in ["yes", "y"]:
                        influencer_data["recent_searches"].append(suggestion_name)
                        save_influencer_data(influencer_data)
                        explain_creator_profile(*creator_files[suggested_key])
                    else:
                        speak("Alright, just let me know who you're interested in!")
                        print("Alright, just let me know who you're interested in!")
                else:
                    msg = "Sorry, I couldn't find a close match. Try: Mister Beast, Gary Vee, Khaby Lame, or K S I."
                    print(msg)
                    speak(msg)
            else:
                msg = "Sorry, I couldn't find a close match. Try: Mister Beast, Gary Vee, Khaby Lame, or K S I."
                print(msg)
                speak(msg)


def load_responses(filename="responses.txt"):
    response_map = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, values = line.strip().split(":", 1)
                    response_map[key] = [v.strip() for v in values.split(",")]
    except FileNotFoundError:
        pass
    return response_map


RESPONSES = load_responses()


def fuzzy_yes_no(user_input):
    user_input = user_input.lower().strip()
    for yes_word in RESPONSES.get("yes", []):
        if user_input.startswith(yes_word):
            return "yes"
    for no_word in RESPONSES.get("no", []):
        if user_input.startswith(no_word):
            return "no"
    return None
def get_confirmation(prompt):
    speak(prompt)
    print(prompt)
    reset_idle_timer()
    answer = input().strip().lower()
    result = fuzzy_yes_no(answer)
    if result == "yes":
        return True
    elif result == "no":
        return False
    elif answer:  # If not recognized, ask for clarification
        speak("Did you mean yes? Please say yes or no.")
        print("Did you mean yes? Please say yes or no.")
        answer2 = input().strip().lower()
        result2 = fuzzy_yes_no(answer2)
        return result2 == "yes"
    else:  # If silent, proceed as yes
        return True


MRBEAST_FACTS = [
    "Mister Beast's real name is Jimmy Donaldson.",
    "He is known for giving away millions of dollars in his videos.",
    "He started YouTube at the age of 13.",
    "He once recreated the Squid Game with real people and a huge cash prize.",
    "Mister Beast has planted over 20 million trees through Team Trees.",
    "He is one of the most-subscribed YouTubers in the world.",
]


def share_fact_about_mrbeast():
    fact = random.choice(MRBEAST_FACTS)
    speak(f"Here's a fun fact about Mister Beast: {fact}")
    print(f"Here's a fun fact about Mister Beast: {fact}")


if __name__ == "__main__":
    strategist_chat()
