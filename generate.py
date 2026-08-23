import os
import base64
import urllib.request

SOURCE_URL = os.environ["SOURCE_URL"]
OUTPUT_FILE = "sub.txt"
NEW_NAME = "USA 🇺🇸"

# دریافت Subscription اصلی
req = urllib.request.Request(
    SOURCE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as response:
    data = response.read().decode("utf-8", errors="ignore").strip()

# Decode Base64
try:
    # اگر Base64 بدون padding باشد
    data += "=" * (-len(data) % 4)
    decoded = base64.b64decode(data).decode("utf-8", errors="ignore")
except Exception:
    decoded = data

# تغییر اسم کانفیگ‌ها
result = []

for line in decoded.splitlines():
    line = line.strip()

    if line.startswith(("vless://", "vmess://", "trojan://", "ss://")):
        # حذف اسم قبلی بعد از #
        if "#" in line:
            line = line.split("#", 1)[0]

        line += "#" + NEW_NAME

    result.append(line)

new_subscription = "\n".join(result) + "\n"

# Encode دوباره Base64
encoded = base64.b64encode(
    new_subscription.encode("utf-8")
).decode("utf-8")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(encoded)

print("Subscription generated successfully.")
print("Config name: " + NEW_NAME)
