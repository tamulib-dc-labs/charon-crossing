import pandas as pd
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_FILE = "Fedora Collections.csv"
LOG_FILE = "ferry_log.txt"
MAX_WORKERS = 6

df = pd.read_csv(INPUT_FILE)

downloaded = 0
skipped = 0
failed = 0


def get_filename_from_url(url):
    return url.rstrip("/").split("/")[-1]


def run_ferry(url):

    global downloaded, skipped, failed

    filename = get_filename_from_url(url)
    expected_csv = f"{filename}.csv"

    if os.path.exists(expected_csv):
        print(f"Skipping {filename}")
        skipped += 1
        return

    print(f"Processing {filename}")

    result = subprocess.run(
        ["ferry", "ferry", url],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{filename},{url},ERROR\n")
            log.write(result.stderr + "\n")

        print(f"ERROR {filename}")
        failed += 1
        return

    if os.path.exists(expected_csv):
        print(f"Done {filename}")
        downloaded += 1
    else:
        failed += 1


urls = df["URI"].dropna().tolist()

try:
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(run_ferry, url) for url in urls]

        for future in as_completed(futures):
            future.result()

except KeyboardInterrupt:
    print("\nInterrupted by user")

finally:
    print("Downloaded:", downloaded)
    print("Skipped:", skipped)
    print("Failed:", failed)