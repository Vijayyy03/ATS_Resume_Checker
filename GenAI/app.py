import streamlit as st
import io
from PyPDF2 import PdfReader
import docx
from fuzzywuzzy import fuzz
from nlp import extract_keywords, extract_sections
from ui import render_sidebar, render_header, onboarding_tour
import matplotlib.pyplot as plt
import openai
import datetime
from streamlit_lottie import st_lottie
import requests

# --- Custom CSS for clean dark mode UI with micro-interactions ---
st.markdown(
    """
    <style>
    body, .stApp, .main {
        background: #1a1530 !important;
        color: #F3F0FF !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    }
    .header-banner {
        background: linear-gradient(90deg, #5B21B6 0%, #A259F7 100%);
        color: #F3F0FF;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 1rem;
        margin: 2rem auto 2rem auto;
        box-shadow: 0 8px 32px 0 rgba(162,89,247,0.25), 0 1.5px 8px 0 #00000033;
        text-align: center;
        max-width: 700px;
        animation: fadeInDown 1s cubic-bezier(.23,1.01,.32,1);
        perspective: 800px;
    }
    .centered-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }
    .section, .result-card, .stepper-card, .hero-card, .feature-list, .onboarding-pill {
        background: rgba(36, 28, 58, 0.85);
        border-radius: 1.5rem;
        box-shadow: 0 2px 8px 0 rgba(20, 16, 40, 0.18);
        backdrop-filter: blur(8px) saturate(120%);
        -webkit-backdrop-filter: blur(8px) saturate(120%);
        border: 1.5px solid rgba(80, 60, 120, 0.18);
        padding: 2rem 2rem 1.5rem 2rem;
        margin-bottom: 2rem;
        max-width: 650px;
        margin-left: auto;
        margin-right: auto;
        animation: fadeInUp 1s cubic-bezier(.23,1.01,.32,1);
        transition: box-shadow 0.3s, transform 0.3s, filter 0.3s;
        perspective: 800px;
        position: relative;
        overflow: hidden;
    }
    .section::before, .result-card::before, .stepper-card::before, .hero-card::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 1.5rem;
        pointer-events: none;
        background: none;
        z-index: 0;
    }
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        animation: fadeIn 1.2s cubic-bezier(.23,1.01,.32,1);
        text-shadow: 0 2px 8px #1a1530cc;
        color: #F3F0FF;
        z-index: 1;
    }
    .result-card {
        background: rgba(36, 28, 58, 0.92);
        border-radius: 1.5rem;
        box-shadow: 0 2px 8px 0 rgba(20, 16, 40, 0.18);
        border: 1.5px solid rgba(80, 60, 120, 0.22);
        padding: 1.7rem;
        margin-bottom: 1.2rem;
        animation: fadeIn 1.2s cubic-bezier(.23,1.01,.32,1);
        filter: none;
        position: relative;
        overflow: hidden;
    }
    .result-card::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 1.5rem;
        pointer-events: none;
        background: none;
        z-index: 0;
    }
    .missing-keywords {
        color: #F87171;
        font-weight: bold;
        animation: fadeIn 1.2s;
        z-index: 1;
    }
    .match-percent {
        color: #A259F7;
        font-size: 2.2rem;
        font-weight: bold;
        animation: fadeIn 1.2s;
        text-shadow: 0 2px 8px #1a1530cc;
        z-index: 1;
    }
    .fuzzy-score {
        color: #C4B5FD;
        font-size: 1.2rem;
        font-weight: bold;
        animation: fadeIn 1.2s;
        z-index: 1;
    }
    .suggestion {
        color: #A259F7;
        font-size: 1.08rem;
        font-style: italic;
        animation: fadeIn 1.2s;
        z-index: 1;
    }
    .stTextArea textarea, .stTextInput input {
        background: rgba(36, 28, 58, 0.92) !important;
        color: #F3F0FF !important;
        border-radius: 0.7rem !important;
        border: 1.5px solid #5B21B6 !important;
        font-size: 1.08rem;
        transition: box-shadow 0.3s, background 0.3s;
        box-shadow: 0 1px 4px #1a153033;
        backdrop-filter: blur(6px) saturate(120%);
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        box-shadow: 0 0 0 2px #A259F7, 0 2px 8px #a259f799;
        background: rgba(36, 28, 58, 0.98) !important;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #A259F7 0%, #5B21B6 100%);
        transition: background 0.5s;
        box-shadow: 0 1px 4px #1a153033;
        border-radius: 0.7rem;
    }
    .stButton>button {
        background: rgba(36, 28, 58, 0.92);
        color: #F3F0FF;
        border-radius: 0.7rem;
        font-weight: 700;
        font-size: 1.13rem;
        padding: 0.6rem 2.1rem;
        border: 1.5px solid #A259F7;
        transition: background 0.3s, box-shadow 0.3s, transform 0.2s, filter 0.2s;
        box-shadow: 0 1px 4px #1a153033;
        animation: fadeInUp 1.2s cubic-bezier(.23,1.01,.32,1);
        filter: none;
        backdrop-filter: blur(6px) saturate(120%);
    }
    .stButton>button:hover {
        background: rgba(80, 60, 120, 0.98);
        box-shadow: 0 2px 8px #1a153033;
        transform: scale3d(1.04,1.04,1.04);
        filter: none;
    }
    .stExpander, .stExpanderHeader {
        background: rgba(36, 28, 58, 0.92) !important;
        border-radius: 1.2rem !important;
        border: 1.5px solid #5B21B6 !important;
        color: #F3F0FF !important;
        box-shadow: 0 1px 4px #1a153033;
        margin-bottom: 1rem;
        backdrop-filter: blur(6px) saturate(120%);
    }
    .stExpanderHeader {
        font-weight: 700;
        font-size: 1.08rem;
    }
    .stDownloadButton>button {
        background: rgba(36, 28, 58, 0.92);
        color: #F3F0FF;
        border-radius: 0.7rem;
        font-weight: 700;
        font-size: 1.08rem;
        border: 1.5px solid #A259F7;
        box-shadow: 0 1px 4px #1a153033;
        margin-top: 0.7rem;
        margin-bottom: 0.7rem;
        transition: background 0.3s, box-shadow 0.3s;
        backdrop-filter: blur(6px) saturate(120%);
    }
    .stDownloadButton>button:hover {
        background: rgba(80, 60, 120, 0.98);
        box-shadow: 0 2px 8px #1a153033;
        filter: none;
    }
    .glass-glow {
        display: none;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

render_sidebar()
render_header()
onboarding_tour()

st.markdown('<div id="file-upload-section"></div>', unsafe_allow_html=True)
st.markdown('<div class="centered-container">', unsafe_allow_html=True)

# --- Resume File Upload (move out of stepper_card) ---
st.markdown("<h3 style='color:#fff; margin-bottom:1.2rem;'>Upload Your Resume</h3>", unsafe_allow_html=True)
st.markdown("<p style='color:#C4C4C4; margin-bottom:1.2rem;'>PDF or DOCX only</p>", unsafe_allow_html=True)
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
st.markdown("<hr style='border: none; border-top: 1.5px solid #35337a; margin: 2.2rem 0;' />", unsafe_allow_html=True)

def modern_card(content, max_width=500):
    st.markdown(f"""
    <div style="
        background: linear-gradient(120deg, #23213a 80%, #35337a 100%);
        border-radius: 1.3rem;
        box-shadow: 0 8px 32px 0 #23294699, 0 1.5px 8px 0 #00000044;
        border: 2px solid #35337a;
        padding: 2.1rem 2.2rem 1.7rem 2.2rem;
        max-width: {max_width}px;
        width: 100%;
        margin: 2.2rem auto 2.2rem auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    ">
    {content}
    </div>
    """, unsafe_allow_html=True)

# --- Extract resume text from uploaded file ---
resume_text = ""
if 'resume_file' in locals() and resume_file is not None:
    if resume_file.type == "application/pdf":
        try:
            pdf = PdfReader(resume_file)
            resume_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    elif resume_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"] or resume_file.name.lower().endswith(".docx"):
        try:
            doc = docx.Document(resume_file)
            resume_text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")
    else:
        st.warning("Unsupported file type. Please upload a PDF or DOCX resume.")

# --- Language Selection ---
language = st.sidebar.selectbox("Select Language", ["English"], index=0)

# --- Multiple Job Descriptions ---
if 'jd_count' not in st.session_state:
    st.session_state['jd_count'] = 1

st.sidebar.markdown("---")
if st.sidebar.button("Add Another Job Description"):
    st.session_state['jd_count'] += 1
if st.sidebar.button("Remove Last Job Description") and st.session_state['jd_count'] > 1:
    st.session_state['jd_count'] -= 1

jd_texts = []
for i in range(st.session_state['jd_count']):
    st.markdown(f'<div class="section">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">\
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="24" rx="12" fill="#A259F7"/><path d="M8 12h8M8 16h8M8 8h8" stroke="#F3F0FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Paste Job Description #{i+1}</div>', unsafe_allow_html=True)
    jd_text = st.text_area(f"Paste the job description here (#{i+1})", height=200, key=f"jd_text_{i}")
    jd_texts.append(jd_text)
    st.markdown('</div>', unsafe_allow_html=True)

resume_keywords = extract_keywords(resume_text) if resume_text else set()

# For live feedback and analysis, loop over all job descriptions
for idx, jd_text in enumerate(jd_texts):
    jd_keywords = extract_keywords(jd_text) if jd_text else set()

    # --- Live Feedback Section ---
    if resume_keywords and jd_keywords:
        matched_keywords = resume_keywords & jd_keywords
        missing_keywords = jd_keywords - resume_keywords
        match_percent = int(100 * len(matched_keywords) / len(jd_keywords)) if jd_keywords else 0
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">\
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="24" rx="12" fill="#A259F7"/><path d="M12 20v-6M12 14l-3-3m3 3l3-3" stroke="#F3F0FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="8" r="1" fill="#F3F0FF"/></svg> Live Match Feedback</div>', unsafe_allow_html=True)
        st.markdown(f"**Live Match Percentage for JD #{idx+1}:** `{match_percent}%`")
        st.progress(match_percent)
        st.caption("This updates in real time as you edit your resume or job description.")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander(f"🔍 Show Resume Keywords (JD #{idx+1})", expanded=False):
        if resume_keywords:
            st.write(", ".join(sorted(resume_keywords)))
        else:
            st.caption("No keywords extracted yet.")
    with st.expander(f"🔍 Show Job Description Keywords (JD #{idx+1})", expanded=False):
        if jd_keywords:
            st.write(", ".join(sorted(jd_keywords)))
        else:
            st.caption("No keywords extracted yet.")

    # --- Section-wise Analysis ---
    resume_sections = extract_sections(resume_text) if resume_text else {"skills": "", "experience": "", "education": ""}

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">\
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="24" rx="12" fill="#A259F7"/><path d="M12 20v-6M12 14l-3-3m3 3l3-3" stroke="#F3F0FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="8" r="1" fill="#F3F0FF"/></svg> Section-wise Resume Analysis</div>', unsafe_allow_html=True)

    st.markdown("**Skills Section:**")
    st.code(resume_sections["skills"] or "Not found", language="markdown")
    st.markdown("**Experience Section:**")
    st.code(resume_sections["experience"] or "Not found", language="markdown")
    st.markdown("**Education Section:**")
    st.code(resume_sections["education"] or "Not found", language="markdown")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Full Analysis Section ---
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">\
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="24" rx="12" fill="#A259F7"/><path d="M12 20v-6M12 14l-3-3m3 3l3-3" stroke="#F3F0FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="8" r="1" fill="#F3F0FF"/></svg> Analysis Results</div>', unsafe_allow_html=True)
    st.markdown("## :mag: Analysis Results")
    if st.button(f":bar_chart: Analyze Match for JD #{idx+1}"):
        with st.spinner("Analyzing with AI..."):
            if not resume_file or not jd_text.strip():
                st.warning("Please upload a resume and paste a job description.")
            else:
                matched_keywords = resume_keywords & jd_keywords
                missing_keywords = jd_keywords - resume_keywords
                match_percent = 0
                if jd_keywords:
                    match_percent = int(100 * len(matched_keywords) / len(jd_keywords))
                fuzzy_score = fuzz.token_set_ratio(" ".join(resume_keywords), " ".join(jd_keywords))

                st.markdown(
                    f"""
                    <div class='result-card'>
                        <span class='match-percent'>Match Percentage: {match_percent}%</span><br>
                        <span class='fuzzy-score'>FuzzyWuzzy Score: {fuzzy_score}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(match_percent)
                # Pie chart for matched vs missing keywords
                if jd_keywords:
                    labels = ['Matched', 'Missing']
                    sizes = [len(matched_keywords), len(missing_keywords)]
                    colors = ['#A259F7', '#F87171']
                    fig, ax = plt.subplots(figsize=(3,3))
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90, textprops={'color':'#F3F0FF'})
                    ax.set_aspect('equal')
                    plt.setp(ax.texts, size=12, weight='bold')
                    plt.tight_layout()
                    st.pyplot(fig)
                if missing_keywords:
                    st.markdown(
                        f"<div class='result-card missing-keywords'>Missing Keywords: {', '.join(sorted(missing_keywords))}</div>",
                        unsafe_allow_html=True)
                else:
                    st.success("Your resume covers all the main keywords from the job description!")
                st.markdown(
                    "<div class='suggestion'>Suggestions: Add the missing keywords to your resume where relevant to improve your match.</div>",
                    unsafe_allow_html=True,
                )
                # Highlight matched/missing skills
                if resume_sections["skills"]:
                    skill_tokens = set([s.strip().lower() for s in resume_sections["skills"].replace(",", "\n").splitlines() if s.strip()])
                    matched_skills = skill_tokens & jd_keywords
                    missing_skills = jd_keywords - skill_tokens
                    st.markdown(f"**Matched Skills:** <span style='color:#A259F7'>{', '.join(sorted(matched_skills)) or 'None'}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Missing Skills:** <span style='color:#F87171'>{', '.join(sorted(missing_skills)) or 'None'}</span>", unsafe_allow_html=True)
                    # GPT-powered suggestions
                    if missing_skills and st.button(f"Get AI Suggestions for Missing Skills (JD #{idx+1})"):
                        prompt = f"Suggest 1-2 example resume bullet points for each of these missing skills: {', '.join(missing_skills)}. Keep it concise and professional."
                        with st.spinner("Generating AI suggestions..."):
                            try:
                                response = openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",
                                    messages=[{"role": "system", "content": "You are a helpful resume assistant."},
                                             {"role": "user", "content": prompt}]
                                )
                                suggestion = response.choices[0].message.content
                                st.success("AI Suggestions:")
                                st.markdown(suggestion)
                            except Exception as e:
                                st.error(f"Error from OpenAI: {e}")
                # Export analysis as text
                if st.button(f"Download Analysis Report as TXT for JD #{idx+1}"):
                    report = io.StringIO()
                    report.write("Resume Analysis Report\n\n")
                    report.write(f"Match Percentage: {match_percent}%\n")
                    report.write(f"FuzzyWuzzy Score: {fuzzy_score}\n")
                    report.write(f"Matched Skills: {', '.join(sorted(matched_skills)) or 'None'}\n")
                    report.write(f"Missing Skills: {', '.join(sorted(missing_skills)) or 'None'}\n")
                    report.write("\nSection-wise Resume Analysis:\n")
                    for sec in ["skills", "experience", "education"]:
                        report.write(f"\n{sec.capitalize()} Section:\n{resume_sections[sec] or 'Not found'}\n")
                    st.download_button("Download TXT Report", report.getvalue(), file_name="resume_analysis.txt")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- User Account (Session-based) ---
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'history' not in st.session_state:
    st.session_state['history'] = []

with st.sidebar:
    st.markdown("---")
    st.markdown("#### User Account")
    username = st.text_input("Enter your username", value=st.session_state['username'])
    if username:
        st.session_state['username'] = username
        st.success(f"Welcome, {username}!")
    else:
        st.info("Enter a username to save your analysis history.")
    st.markdown("---")
    st.markdown("#### Analysis History")
    if st.session_state['history']:
        for i, h in enumerate(st.session_state['history']):
            st.markdown(f"**{h['title']}** - {h['timestamp']}")
            st.download_button(f"Download Report {i+1}", h['report'], file_name=f"resume_analysis_{i+1}.txt")
    else:
        st.caption("No analysis history yet.") 

# Helper to load Lottie animation from URL
@st.cache_data
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie animation for header
lottie_robot = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_4kx2q32n.json")
st_lottie(lottie_robot, height=120, key="header-lottie") 