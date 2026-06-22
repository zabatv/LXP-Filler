import json, os, requests

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API = "https://api.newlxp.ru/graphql"

# Read saved groups from JSON
path = r"D:\Desktop\LXP\lxp-web\themes_output"
for f in os.listdir(path):
    if f.endswith(".json") and "groups" in f:
        with open(os.path.join(path, f), "r", encoding="utf-8") as fp:
            data = json.load(fp)
        groups = data.get("learningGroupsByStudyPeriodIdAndSuborganizationId", [])
        if groups:
            g = groups[0]
            print(f"Group: {g['id']} | {g['name']}")
            
            # Now explore what fields are available on this discipline
            q = '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code } }' % g["id"]
            r = requests.post(API, json={"query": q}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
            data = r.json()
            discs = data.get("data", {}).get("disciplinesByGroups", [])
            if discs:
                d = discs[0]
                print(f"  Discipline: {d['id']} | {d['name']}")
                
                # Now try introspection to find what fields exist on Discipline type
                intro_q = """
                query {
                    __type(name: "Discipline") {
                        name
                        fields {
                            name
                            type {
                                name
                                kind
                            }
                        }
                    }
                }
                """
                r2 = requests.post(API, json={"query": intro_q}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
                intro_data = r2.json()
                fields = intro_data.get("data", {}).get("__type", {}).get("fields", [])
                print("\n  Discipline fields:")
                for field in fields:
                    print(f"    {field['name']}: {field['type']['name']} ({field['type']['kind']})")
                break
