"""Run all silver scripts in dependency order. Stops at the first error."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = [
    "s01_geolocation.py", "s02_customers.py", "s03_sellers.py", "s04_products.py",
    "s05_orders.py", "s06_order_items.py", "s07_payments.py", "s08_reviews.py",
]

for script in ORDER:
    print(f"\n===== {script} =====")
    subprocess.run([sys.executable, str(HERE / script)], check=True)

print("\nSilver layer finished.")
