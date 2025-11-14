from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app=Flask(__name__)
model=SentenceTransformer('all-MiniLM-L6-v2')

with open("skills.txt", "r") as f:
    skill_keywords = [line.strip().lower() for line in f.readlines()]

def extract_skills(text):
    text=text.lower()
    found=[skill for skill in skill_keywords if skill in text]
    return list(set(found))

@app.route('/match', methods=['POST'])
def match():
    data=request.json
    resume_text=data.get('resume')
    job_desc=data.get('jd')

    embeddings=model.encode([resume_text, job_desc])
    similarity=float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])

    resume_skills=extract_skills(resume_text)
    jd_skills=extract_skills(job_desc)
    common_skills=list(set(resume_skills) & set(jd_skills))

    return jsonify({
        "match_score": round(similarity * 100, 2),
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "common_skills": common_skills
    })

if __name__=='__main__':
    app.run(debug=True)
