import streamlit as st
from streamlit_lottie import st_lottie
import requests

def render_sidebar():
    st.sidebar.markdown(
        """
        <style>
        .stSidebar {
            background: rgba(36, 34, 62, 0.55) !important;
            border-radius: 1.5rem !important;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 1.5px 8px 0 #00000033 !important;
            backdrop-filter: blur(18px) saturate(160%) !important;
            -webkit-backdrop-filter: blur(18px) saturate(160%) !important;
            border: 1.5px solid rgba(162, 89, 247, 0.18) !important;
            position: relative;
            overflow: hidden;
        }
        .stSidebar::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 1.5rem;
            pointer-events: none;
            background: linear-gradient(120deg, rgba(162,89,247,0.12) 0%, rgba(90,49,244,0.09) 100%);
            z-index: 0;
            filter: blur(2px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.image("https://img.icons8.com/color/96/000000/briefcase.png", width=48)
    st.sidebar.markdown("<span style='font-size:1.7rem; font-weight:700; color:#FF7A00'>Resume Match Pro</span>", unsafe_allow_html=True)
    st.sidebar.info("AI-powered resume matching for professionals. All data stays private.")
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<small style='color:#C4C4C4'>🔒 <b>Privacy:</b> Data is processed in your browser and never stored.</small>",
        unsafe_allow_html=True,
    )

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_fun = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_4kx2q32n.json")  # Fun robot

def render_header():
    st.markdown(
        """
        <style>
        html, body, .stApp, .main {
            height: 100%;
        }
        body, .stApp, .main {
            background: linear-gradient(90deg, #221a38 0%, #35337a 100%) !important;
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        }
        .css-18e3th9, .css-1d391kg { background: none !important; }
        .hero-outer {
            min-height: 90vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .hero-bg-blob {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 600px;
            height: 400px;
            background: radial-gradient(circle at 60% 40%, #5A31F4 0%, #35337a 80%, transparent 100%);
            filter: blur(60px) brightness(1.1);
            opacity: 0.25;
            transform: translate(-50%, -50%);
            z-index: 0;
            pointer-events: none;
            animation: blobFade 8s ease-in-out infinite alternate;
        }
        @keyframes blobFade {
            0% { opacity: 0.18; }
            50% { opacity: 0.32; }
            100% { opacity: 0.18; }
        }
        .hero-card, .onboarding-pill, .feature-list {
            background: rgba(36, 34, 62, 0.55);
            border-radius: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 1.5px 8px 0 #00000033;
            backdrop-filter: blur(18px) saturate(160%);
            -webkit-backdrop-filter: blur(18px) saturate(160%);
            border: 1.5px solid rgba(162, 89, 247, 0.18);
            position: relative;
            overflow: hidden;
        }
        .hero-card::before, .onboarding-pill::before, .feature-list::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 1.5rem;
            pointer-events: none;
            background: linear-gradient(120deg, rgba(162,89,247,0.12) 0%, rgba(90,49,244,0.09) 100%);
            z-index: 0;
            filter: blur(2px);
        }
        .hero-card {
            max-width: 420px;
            width: 100%;
            text-align: center;
            position: relative;
            margin: 0 auto 2.2rem auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            z-index: 1;
        }
        .hero-card::after {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 1.5rem;
            pointer-events: none;
            background: linear-gradient(120deg, rgba(162,89,247,0.10) 0%, rgba(90,49,244,0.08) 100%);
            z-index: 0;
            filter: blur(2px);
        }
        .onboarding-pill, .feature-list {
            z-index: 1;
        }
        .glass-glow {
            position: absolute;
            top: -60px; left: -60px; right: -60px; bottom: -60px;
            background: radial-gradient(circle, rgba(162,89,247,0.18) 0%, rgba(90,49,244,0.09) 100%);
            filter: blur(48px);
            z-index: 0;
            pointer-events: none;
            opacity: 0.7;
            border-radius: 2rem;
            animation: glassGlowPulse 6s ease-in-out infinite alternate;
        }
        @keyframes glassGlowPulse {
            0% { opacity: 0.5; }
            50% { opacity: 0.9; }
            100% { opacity: 0.5; }
        }
        .hero-icon {
            margin-bottom: 1.1rem;
        }
        .hero-title {
            font-size: 2.1rem;
            font-weight: 900;
            color: #fff;
            margin-bottom: 0.3rem;
            letter-spacing: 1px;
            text-shadow: 0 2px 12px #5A31F4cc;
        }
        .hero-subtitle {
            font-size: 1.13rem;
            color: #C4C4C4;
            font-weight: 500;
            margin-bottom: 0.2rem;
        }
        .onboarding-pill {
            width: 100%;
            max-width: 420px;
            margin: 0 auto 0 auto;
            text-align: center;
            color: #fff;
            font-size: 1.01rem;
            font-weight: 600;
            background: linear-gradient(90deg, #5A31F4 0%, #35337a 100%);
            border-radius: 2rem;
            padding: 0.55rem 1.5rem;
            box-shadow: 0 2px 12px #5A31F433;
            border: 1.5px solid #35337a;
            display: block;
            z-index: 1;
        }
        .feature-list {
            margin: 2.2rem auto 0 auto;
            max-width: 420px;
            text-align: center;
            color: #C4C4C4;
            font-size: 1.08rem;
            font-weight: 400;
            background: rgba(53,51,122,0.18);
            border-radius: 1.2rem;
            padding: 1.1rem 1.5rem 1.1rem 1.5rem;
            box-shadow: 0 2px 12px #5A31F433;
            border: 1.5px solid #35337a;
            z-index: 1;
        }
        .scroll-arrow {
            margin: 2.2rem auto 0 auto;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1;
        }
        .scroll-arrow svg {
            animation: arrowBounce 1.5s infinite alternate;
        }
        @keyframes arrowBounce {
            0% { transform: translateY(0); opacity: 0.7; }
            100% { transform: translateY(18px); opacity: 1; }
        }
        </style>
        <div class="hero-outer">
            <div class="glass-glow"></div>
            <div class="hero-bg-blob"></div>
            <div class="hero-card">
                <div class="hero-icon">
                    <svg width="38" height="38" viewBox="0 0 54 54" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="19" cy="19" r="17" fill="none" stroke="#FF7A00" stroke-width="2.5"/>
                        <path d="M13 20.5L18 25.5L28 15.5" stroke="#FF7A00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div class="hero-title">Resume Match Pro</div>
                <div class="hero-subtitle">AI-powered resume matching for professionals.</div>
            </div>
            <div class="onboarding-pill">How it works: Upload your resume, paste a job description, see your match.</div>
            <div class="feature-list">
                <b>Features:</b> Upload your resume, compare with multiple job descriptions, get instant AI feedback, beautiful reports, and more!
            </div>
            <div class="scroll-arrow">
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M16 8V24" stroke="#5A31F4" stroke-width="3" stroke-linecap="round"/>
                    <path d="M8 16L16 24L24 16" stroke="#5A31F4" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def onboarding_tour():
    pass  # Onboarding now rendered in header for perfect alignment 