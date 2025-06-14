import os
import json
import csv

UPLOADS_DIR = "uploads"
DATA_DIR = "data"


def ensure_dirs():
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)


def parse_tiktok_csv(filepath):
    # Example: expects columns like username, followers, likes, engagement_rate
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def analyze_influencer(data):
    # Simple logic: can be replaced with AI/ML or more advanced rules
    if not data:
        return "No data found."
    stats = data[0]
    followers = int(stats.get("followers", 0))
    engagement = float(stats.get("engagement_rate", 0))
    if followers < 1000:
        return "You need at least 1000 followers for a full analysis."
    # Example strategy
    strategy = [
        f"Your follower count: {followers}",
        f"Engagement rate: {engagement}%",
        "Post more consistently to boost engagement.",
        "Collaborate with similar creators for cross-promotion.",
        "Leverage trending sounds and hashtags.",
    ]
    return "\n".join(strategy)


def save_analysis(username, analysis):
    outpath = os.path.join(DATA_DIR, f"{username}_analysis.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump({"strategy": analysis}, f, indent=2)
    return outpath


def upload_and_analyze():
    ensure_dirs()
    print(
        "Upload your TikTok stats CSV (with columns: username, followers, engagement_rate):"
    )
    filepath = input("Enter file path: ").strip()
    if not os.path.exists(filepath):
        print("File not found.")
        return
    data = parse_tiktok_csv(filepath)
    if not data:
        print("No data found in file.")
        return
    username = data[0].get("username", "unknown")
    analysis = analyze_influencer(data)
    outpath = save_analysis(username, analysis)
    print(f"\nStrategy for {username}:\n{analysis}")
    print(f"Analysis saved to {outpath}")


if __name__ == "__main__":
    upload_and_analyze()
