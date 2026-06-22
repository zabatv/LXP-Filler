import requests, json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMGZmZjNhZi1lZmJhLTRhYTItYTViZS1mMzU1ODc1OWZmYWEiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzgxNjA3MzIzLCJleHAiOjE3ODE2OTM3MjN9.KVA-sYdGY5cFZw1y38xMJHIPP3smf1WoQei4DioGpJc"
API = "https://api.newlxp.ru/graphql"

# Get a student first
q1 = """
query {
    searchStudentsInLearningGroup(input: {
        filters: { learningGroupId: "fbd3bb8f-1442-453e-b710-43fe8b28eca0", isExpelled: false }
    }) {
        items { id user { lastName firstName } }
    }
}
"""
r = requests.post(API, json={"query": q1}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
data = r.json()
students = data.get("data", {}).get("searchStudentsInLearningGroup", {}).get("items", [])
if students:
    sid = students[0]["id"]
    print(f"Student: {sid}")
    
    # Try searchStudentDisciplines with more fields
    q2 = """
    query {
        searchStudentDisciplines(input: { studentId: "%s" }) {
            disciplineId
            disciplineGrade
            hasRetake
            retakeDisciplineGrade
            retakeScore
            topic
            topics
            theme
            themes
            semester
            controlType
        }
    }
    """ % sid
    r2 = requests.post(API, json={"query": q2}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
    data2 = r2.json()
    print(json.dumps(data2, ensure_ascii=False, indent=2)[:2000])
