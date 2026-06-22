import requests, json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API = "https://api.newlxp.ru/graphql"

# Try various fields on sections
q = """
{
    disciplinesByGroups(input: { groupIds: ["fbd3bb8f-1442-453e-b710-43fe8b28eca0"] }) {
        id name code
        sections {
            id name
            topics { id name }
            lessons { id name }
            classes { id name }
            subSections { id name }
            childSections { id name }
        }
    }
}
"""
r = requests.post(API, json={"query": q}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
data = r.json()
print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
