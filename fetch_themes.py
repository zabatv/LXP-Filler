import requests
import json
import os
from pathlib import Path

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API_URL = "https://api.newlxp.ru/graphql"

# ISIP Nalchik
ISIP_SUBORG = "40f63fed-7beb-48f5-88e5-e49536897a3d"
AUTUMN_SP = "71e7d993-a53e-45a4-bf0f-0e439f51c222"  # Осенний семестр 25-26
SPRING_SP = "735916cd-2dfc-4ac4-84bd-feb7f3252e86"    # Весенний семестр 25-26

OUTPUT_DIR = Path(__file__).parent / "themes_output"

def gql(query):
    r = requests.post(API_URL, json={"query": query}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=30)
    data = r.json()
    if data.get("errors"):
        print("GQL ERROR:", json.dumps(data["errors"], ensure_ascii=False)[:200])
        return None
    return data["data"]

def save_txt(rel_path, content):
    path = OUTPUT_DIR / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def semester_label(sp_id):
    return "Осенний 25-26" if sp_id == AUTUMN_SP else "Весенний 25-26"

# Get all groups for ISIP Nalchik for both semesters
all_data = {}  # group_name -> semester -> [discipline_info]

for sp_id in [AUTUMN_SP, SPRING_SP]:
    sp_label = semester_label(sp_id)
    q = 'query { learningGroupsByStudyPeriodIdAndSuborganizationId(input: { studyPeriodId: "%s" suborganizationId: "%s" }) { id name } }' % (sp_id, ISIP_SUBORG)
    data = gql(q)
    if not data:
        continue
    groups = data["learningGroupsByStudyPeriodIdAndSuborganizationId"]
    print(f"\n=== {sp_label}: {len(groups)} groups ===")
    
    for g in groups:
        gid = g["id"]
        gname = g["name"]
        print(f"  Group: {gname}")
        
        # Get disciplines with sections
        q2 = '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code sections { id name description } } }' % gid
        ddata = gql(q2)
        if not ddata:
            continue
        discs = ddata["disciplinesByGroups"]
        print(f"    Disciplines: {len(discs)}")
        
        for d in discs:
            did = d["id"]
            dname = d["name"]
            dcode = d.get("code", "")
            
            # Get section topics/themes
            sections = d.get("sections", [])
            themes = []
            for s in sections:
                sname = s.get("name", "")
                sdesc = s.get("description", "")
                themes.append(sname)
                if sdesc:
                    themes.append(f"  Описание: {sdesc}")
            
            # Save to txt: <group>/<semester>/<discipline>.txt
            themes_text = "\n".join(f"  - {t}" for t in themes) if themes else "  (нет разделов)"
            content = f"""Дисциплина: {dname}
Код: {dcode}
Семестр: {sp_label}

Разделы / Темы:
{themes_text}
"""
            safe_gname = gname.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_")
            safe_dname = dname.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_")
            sp_dir = "Осенний_25-26" if sp_id == AUTUMN_SP else "Весенний_25-26"
            rel = Path("ИСиП_Нальчик") / safe_gname / sp_dir / f"{safe_dname}.txt"
            save_txt(rel, content)
            print(f"      {dname} -> {rel}")

print("\nDone!")
