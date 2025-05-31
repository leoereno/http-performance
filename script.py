import subprocess
import json
import sys

if len(sys.argv) < 2:
    print("missing URL argument!")
    sys.exit(1)

WEBSITE = sys.argv[1]  
OUTPUT_FILE = "httping_report.txt"

cmd = ["httping", WEBSITE, "-c", "10", "-M"]
try:
    result = subprocess.run(cmd, capture_output=True, text=True)
    #print(result.stdout.strip())
except FileNotFoundError:
    print("Error: 'httping' not found. Please install it first.")
    sys.exit(1)

if result.returncode != 0:
    print("Error running httping:", result.stderr)
    sys.exit(1)

responses = []
try:
    data = json.loads(result.stdout.strip())
    #print(data)
    for i in data:
        responses.append(i)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")

if not responses:
    print("No valid responses received.")
    sys.exit(1)

total_rtt = sum(float((r["total_ms"]).replace(",", ".")) for r in responses)
average_rtt = total_rtt / len(responses)

# Write report
with open(OUTPUT_FILE, "w") as f:
    f.write(f"HTTPing Report for {WEBSITE}\n")
    f.write("=" * 40 + "\n")
    f.write(f"Number of successful pings: {len(responses)}\n")
    f.write(f"Average response time (RTT): {average_rtt:.2f} ms\n")
    f.write("\nDetailed responses:\n")
    for i,r in enumerate(responses, 1):
        f.write(f"Ping {i}: Status {str(r['http_code'])}, RTT {float((r['total_ms']).replace(",", ".")):.2f} ms\n")

print(f"Report written to {OUTPUT_FILE}")
