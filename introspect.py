import requests, json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API = "https://api.newlxp.ru/graphql"

# Introspect ALL types to find theme/topic related types
q = """
{
    __schema {
        types {
            name
            fields {
                name
                type { name kind }
            }
        }
    }
}
"""
r = requests.post(API, json={"query": q}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=30)
data = r.json()
if data.get("errors"):
    print("ERROR:", json.dumps(data["errors"], ensure_ascii=False, indent=2))
else:
    types = data["data"]["__schema"]["types"]
    # Find types related to theme/topic/discipline
    keywords = ["theme", "topic", "discipline", "plan", "lesson", "module", "section"]
    for t in types:
        name = t["name"]
        if name == "Query" and t.get("fields"):
            print(f"\n=== Query fields ===")
            for f in t["fields"]:
                fname = f["name"]
                ftype = f["type"]
                if any(k in fname.lower() for k in keywords):
                    print(f"  {fname}: {ftype['name']} ({ftype['kind']})")
