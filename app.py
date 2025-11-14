import streamlit as st
import PyPDF2
import requests

st.set_page_config(page_title="Job-Resume Matcher",page_icon="🧠")

st.title("Job–Resume Matching System")
st.write("Upload your resume and paste a job description to check how well they Match!")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

uploaded_file=st.file_uploader("Upload Resume (PDF)",type=["pdf"])
job_desc=st.text_area("Paste Job Description")
if st.button("Check Match"):
    if not uploaded_file:
        st.warning("⚠️ Please upload your resume first!")
    elif not job_desc.strip():
        st.warning("⚠️ Please enter a job description.")
    else:
        resume_text=extract_text_from_pdf(uploaded_file)
        try:
            response=requests.post(
                "http://127.0.0.1:5000/match",
                json={"resume": resume_text,"jd": job_desc}
            )
            if response.status_code==200:
                data=response.json()
                match_score=data["match_score"]
                common_skills=data["common_skills"]

                st.subheader("✅ Match Results:")
                st.write(f"**Match Score:** {match_score}%")
                if match_score>=70:
                    st.success("🎯 Excellent match! Your resume fits this job well.")
                elif match_score>=40:
                    st.info("🟡 Decent match. Try improving or adding relevant skills.")
                else:
                    st.warning("🔴 Low match. Customize your resume for better alignment.")

                st.write(f"**Common Skills:** {', '.join(common_skills) if common_skills else 'None found'}")
                with st.expander("View Skill Details"):
                    st.write(f"**Skills in Resume:** {', '.join(data['resume_skills'])}")
                    st.write(f"**Skills in Job Description:** {', '.join(data['jd_skills'])}")
            else:
                st.error("❌ Backend error. Please ensure Flask server is running.")
        except Exception as e:
            st.error(f"⚠️ Connection error: {e}")

st.write("💡 Improvement Tips:")
st.markdown("""
        - Add skills mentioned in the job description to your resume where applicable.  
        - Highlight technical projects or experiences that match the JD.  
        - Use similar keywords recruiters use in job postings.  
        """)