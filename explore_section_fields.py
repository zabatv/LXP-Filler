import requests, json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API = "https://api.newlxp.ru/graphql"
GID = "fbd3bb8f-1442-453e-b710-43fe8b28eca0"

# More section sub-fields
fields = ["description", "content", "hours", "weeks", "number", "order", "index", "fullName", "title",
          "academicHours", "controlType", "attestationType", "lessonPlan", "lessonsCount",
          "topicCount", "totalHours", "lectureHours", "practiceHours", "labHours",
          "independentHours", "certification"]

for field in fields:
    q = '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code sections { id name %s } } }' % (GID, field)
    try:
        r = requests.post(API, json={"query": q}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
        data = r.json()
        err = data.get("errors")
        if err:
            msg = err[0]["message"]
            if "Cannot query field" in msg:
                pass  # skip, too many
            else:
                print(f"  {field}: ERROR - {msg[:100]}")
        else:
            print(f"  {field}: OK - {json.dumps(data['data'], ensure_ascii=False)[:300]}")
    except Exception as e:
        print(f"  {field}: Exception - {e}")
