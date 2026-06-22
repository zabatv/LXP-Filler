import requests, json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API = "https://api.newlxp.ru/graphql"

# Try __type for Section and Discipline
for type_name in ["Section", "Discipline", "StudentDiscipline"]:
    q = """
    {
        __type(name: "%s") {
            name
            fields {
                name
                type { name kind ofType { name } }
            }
        }
    }
    """ % type_name
    r = requests.post(API, json={"query": q}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
    data = r.json()
    print(f"\n=== {type_name} ===")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:1500])
