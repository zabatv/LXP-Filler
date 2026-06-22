import requests, json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API = "https://api.newlxp.ru/graphql"

# Get a group for ISIP Nalchik first
q1 = """
query {
    learningGroupsByStudyPeriodIdAndSuborganizationId(input: {
        studyPeriodId: "71e7d993-a53e-45a4-bf0f-0e439f51c222"
        suborganizationId: "40f63fed-7beb-48f5-88e5-e49536897a3d"
    }) { id name }
}
"""
r = requests.post(API, json={"query": q1}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
data = r.json()
groups = data.get("data", {}).get("learningGroupsByStudyPeriodIdAndSuborganizationId", [])
if groups:
    g = groups[0]
    print(f"Group: {g['id']} | {g['name']}")
    
    # Get disciplines
    q2 = '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code } }' % g["id"]
    r2 = requests.post(API, json={"query": q2}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
    ddata = r2.json()
    discs = ddata.get("data", {}).get("disciplinesByGroups", [])
    if discs:
        d = discs[0]
        print(f"Discipline: {d['id']} | {d['name']}")
        did = d["id"]
        
        # Try various theme-related queries
        queries_to_try = [
            ('topicPlans on Discipline', 
             '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code topicPlans { id name } } }' % g["id"]),
            ('topicPlan on Discipline',
             '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code topicPlan { id name } } }' % g["id"]),
            ('sections on Discipline',
             '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code sections { id name } } }' % g["id"]),
            ('modules on Discipline',
             '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code modules { id name } } }' % g["id"]),
            ('lessonPlans on Discipline',
             '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code lessonPlans { id name } } }' % g["id"]),
            ('calendarPlans on Discipline',
             '{ disciplinesByGroups(input: { groupIds: ["%s"] }) { id name code calendarPlans { id name } } }' % g["id"]),
            ('getDisciplineTopicPlans query',
             '{ getDisciplineTopicPlans(input: { disciplineId: "%s" }) { id name } }' % did),
            ('disciplineTopicPlans query',
             '{ disciplineTopicPlans(input: { disciplineId: "%s" }) { id name } }' % did),
            ('getTopicPlans query',
             '{ getTopicPlans(input: { disciplineId: "%s" }) { id name } }' % did),
            ('topicPlans query',
             '{ topicPlans(input: { disciplineId: "%s" }) { id name } }' % did),
        ]
        
        for label, q in queries_to_try:
            try:
                r3 = requests.post(API, json={"query": q}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
                result = r3.json()
                errors = result.get("errors")
                if errors:
                    msg = errors[0]["message"]
                    print(f"  {label}: ERROR - {msg[:80]}")
                else:
                    print(f"  {label}: OK - {json.dumps(result['data'], ensure_ascii=False)[:200]}")
            except Exception as e:
                print(f"  {label}: Exception - {e}")
else:
    print(f"No groups found. Response: {json.dumps(data, ensure_ascii=False)[:200]}")
