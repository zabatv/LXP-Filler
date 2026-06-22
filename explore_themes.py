import requests, json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API = "https://api.newlxp.ru/graphql"
GROUP_ID = "d3e4bdd5-58d8-4f20-b44e-12e47cd2b1c6"  # a sample group

# Try different field names for themes
field_tries = ["topics", "topicPlans", "themes", "topicPlan", "disciplineTopics"]

for field in field_tries:
    q = '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code %s } }' % (GROUP_ID, field)
    try:
        r = requests.post(API, json={"query": q}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
        data = r.json()
        print(f"=== Field: {field} ===")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:800])
        print()
    except Exception as e:
        print(f"Field {field}: Error - {e}\n")
