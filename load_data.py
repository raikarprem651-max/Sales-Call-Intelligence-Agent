import json
import time
from datetime import datetime
from hindsight_client import Hindsight
from config import HINDSIGHT_KEY, HINDSIGHT_URL, BANK

client = Hindsight(base_url=HINDSIGHT_URL, api_key=HINDSIGHT_KEY)

# Create the memory bank (fine if it already exists)
try:
    client.create_bank(bank_id=BANK, name="Deal Intelligence")
except Exception as e:
    print("Bank note:", e)

with open("data.json") as f:
    calls = json.load(f)

for i, call in enumerate(calls, start=1):
    client.retain(
        bank_id=BANK,
        content=call["notes"],
        context=f"Sales call with {call['prospect']} of {call['company']}",
        timestamp=datetime.strptime(call["date"], "%Y-%m-%d"),
        document_id=f"{call['prospect']}-{call['date']}",
    )
    print(f"Saved {i}/{len(calls)}: {call['prospect']} on {call['date']}")

print("All calls saved. Waiting 30 seconds for Hindsight to process them...")
time.sleep(30)

# Quick check: ask a question and see what memory returns
results = client.recall(bank_id=BANK, query="What did we promise Priya Nair?")
print(f"Check: found {len(results.results)} memories")
for r in results.results[:5]:
    print("RECALLED:", r.text)