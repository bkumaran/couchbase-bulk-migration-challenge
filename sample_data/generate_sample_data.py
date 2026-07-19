#!/usr/bin/env python3
"""
Generates a legacy-style dataset of user profile JSON documents for the
Couchbase migration interview exercise.

Usage:
    python3 generate_sample_data.py [--count 100000] [--mode files|single]

--mode files   (default) writes one JSON file per user into ./profiles/
--mode single  writes one big JSON array into ./profiles_single.json
               (useful for testing "read a large local JSON file" without
               running out of memory)
"""
import argparse
import json
import os
import random
import uuid
from datetime import datetime, timedelta

FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Riley", "Casey", "Sam",
               "Jamie", "Avery", "Quinn", "Priya", "Wei", "Fatima", "Diego", "Noor"]
LAST_NAMES = ["Smith", "Johnson", "Lee", "Garcia", "Patel", "Kim", "Chen",
              "Müller", "Silva", "Nguyen", "Khan", "Rossi", "Ivanov"]
COUNTRIES = ["US", "GB", "IN", "DE", "BR", "JP", "AU", "CA", "FR", "SG"]
PLANS = ["free", "starter", "pro", "enterprise"]


def random_date(start_year=2015, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).isoformat() + "Z"


def make_profile(i: int) -> dict:
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return {
        "id": str(uuid.uuid4()),
        "legacyId": i,
        "type": "user_profile",
        "firstName": first,
        "lastName": last,
        "email": f"{first.lower()}.{last.lower()}{i}@example.com",
        "country": random.choice(COUNTRIES),
        "plan": random.choice(PLANS),
        "createdAt": random_date(),
        "lastLoginAt": random_date(2023, 2026),
        "preferences": {
            "newsletter": random.choice([True, False]),
            "theme": random.choice(["light", "dark"]),
            "locale": random.choice(["en-US", "en-GB", "de-DE", "pt-BR", "ja-JP"]),
        },
        "tags": random.sample(
            ["beta", "vip", "trial", "churn-risk", "high-value", "newsletter-subscriber"],
            k=random.randint(0, 3),
        ),
    }


def write_individual_files(count: int, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    for i in range(count):
        profile = make_profile(i)
        path = os.path.join(out_dir, f"profile_{i:06d}.json")
        with open(path, "w") as f:
            json.dump(profile, f)
    print(f"Wrote {count} files to {out_dir}/")


def write_single_file(count: int, out_path: str):
    """
    Streams a JSON array to disk without holding all documents in memory
    at once (writes incrementally), so this itself is a mini example of
    memory-conscious file writing.
    """
    with open(out_path, "w") as f:
        f.write("[")
        for i in range(count):
            if i > 0:
                f.write(",")
            json.dump(make_profile(i), f)
        f.write("]")
    print(f"Wrote {count} documents to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100_000)
    parser.add_argument("--mode", choices=["files", "single"], default="files")
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    if args.mode == "files":
        write_individual_files(args.count, os.path.join(here, "profiles"))
    else:
        write_single_file(args.count, os.path.join(here, "profiles_single.json"))
