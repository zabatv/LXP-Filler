import json, os

# Read suborgs
with open("D:/Desktop/LXP/lxp-web/themes_output/00_suborganizations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data["getMe"]["assignedSuborganizations"]
seen = {}
for s in items:
    sid = s["suborganizationId"]
    if sid not in seen:
        seen[sid] = s["suborganization"]["name"]

print("SUBORGANIZATIONS:")
for sid, name in seen.items():
    print(f"  {sid} | {name}")

# Read study periods
with open("D:/Desktop/LXP/lxp-web/themes_output/00_study_periods.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("\nSTUDY PERIODS:")
for sp in data["studyPeriods"]:
    print(f"  {sp['id']} | {sp['name']} | {sp['startDate']} | {sp['endDate']}")
