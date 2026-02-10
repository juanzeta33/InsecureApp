import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://urchin-app-i8iuq.ondigitalocean.app/debug/eval?expression=aswdf"
TOTAL_REQUESTS = 1000000   # total de peticiones a realizar
BATCH_SIZE = 1000          # peticiones concurrentes por lote
TIMEOUT = 5                # timeout por request (segundos)
SLEEP_BETWEEN_BATCHES = 0.0  # pausa entre lotes (segundos)

session = requests.Session()


def make_request(i: int):
    try:
        r = session.get(URL, timeout=TIMEOUT)
        return i, r.status_code
    except requests.exceptions.RequestException as e:
        return i, f"ERROR: {e}"  # mantener visible el error


completed = 0
batch = 0

while completed < TOTAL_REQUESTS:
    batch += 1
    remaining = TOTAL_REQUESTS - completed
    current_batch_size = min(BATCH_SIZE, remaining)

    print(f"\n=== Batch {batch} | Launching {current_batch_size} concurrent requests ===")

    with ThreadPoolExecutor(max_workers=current_batch_size) as executor:
        futures = [executor.submit(make_request, completed + i + 1) for i in range(current_batch_size)]
        for future in as_completed(futures):
            idx, result = future.result()
            print(f"[{idx}] {result}")

    completed += current_batch_size

print("\nDone.")