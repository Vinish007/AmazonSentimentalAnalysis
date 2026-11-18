
import streamlit as st
import requests
import time

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Amazon Sentiment Analyzer",
    page_icon="🚀",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background:
        radial-gradient(ellipse at center, #14213d 0%, #080d1b 60%, #02040a 100%);
    min-height: 100vh;
    overflow-x: hidden;
}

/* ANIMATED STARFIELD */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;

    background-image:
        radial-gradient(2px 2px at 20% 30%, white 99%, transparent),
        radial-gradient(1px 1px at 70% 20%, white 99%, transparent),
        radial-gradient(2px 2px at 80% 70%, #60a5fa 99%, transparent),
        radial-gradient(1px 1px at 30% 80%, white 99%, transparent),
        radial-gradient(2px 2px at 50% 50%, #93c5fd 99%, transparent);

    background-size: 300px 300px;
    animation: starsMove 25s linear infinite;
}

/* KEEP CONTENT ABOVE BACKGROUND */
.stApp > header,
.stApp .main,
.stApp [data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 1;
}

.stApp [data-testid="stMainBlockContainer"] {
    background: transparent;
}

/* STAR MOVEMENT */
@keyframes starsMove {
    from {
        background-position: 0 0;
    }
    to {
        background-position: 300px 300px;
    }
}

/* TITLE */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 0 15px #38bdf8;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #a5c9f5;
    font-size: 16px;
    margin-bottom: 30px;
}

/* INPUT AREA */
.stTextArea textarea {
    background: rgba(10, 20, 40, 0.85) !important;
    color: white !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 12px !important;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    border: 1px solid #38bdf8;
    background: linear-gradient(90deg, #075985, #2563eb);
    color: white;
    font-size: 18px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 25px #38bdf8;
    border: 1px solid white;
}

/* RESULT CARDS */
.result-card {
    padding: 25px;
    margin-top: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 24px;
    font-weight: bold;
    animation: resultAppear 0.7s ease;
}

.positive {
    background: linear-gradient(135deg, #064e3b, #059669);
    border: 1px solid #34d399;
    box-shadow: 0 0 25px rgba(52, 211, 153, 0.4);
}

.negative {
    background: linear-gradient(135deg, #7f1d1d, #dc2626);
    border: 1px solid #f87171;
    box-shadow: 0 0 25px rgba(248, 113, 113, 0.4);
}

@keyframes resultAppear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}


/* ==========================================
   COLORFUL FULL-SCREEN HYPERSPACE EFFECT
   ========================================== */

.stApp:has(.warp-trigger)::after {
    content: "";
    position: fixed;
    inset: -20%;
    width: 140vw;
    height: 140vh;
    z-index: 9999;
    pointer-events: none;

    background:
        /* Pink and purple light beams */
        repeating-conic-gradient(
            from 0deg at 50% 50%,
            transparent 0deg 2deg,
            rgba(255, 0, 230, 0.95) 2.05deg 2.16deg,
            transparent 2.3deg 4deg
        ),

        /* Electric blue beams */
        repeating-conic-gradient(
            from 1deg at 50% 50%,
            transparent 0deg 4deg,
            rgba(0, 180, 255, 0.9) 4.05deg 4.13deg,
            transparent 4.3deg 7deg
        ),

        /* Cyan energy */
        repeating-conic-gradient(
            from 2deg at 50% 50%,
            transparent 0deg 8deg,
            rgba(0, 255, 255, 0.7) 8.05deg 8.12deg,
            transparent 8.3deg 11deg
        ),

        /* Bright central energy */
        radial-gradient(
            circle at center,
            rgba(255, 255, 255, 0.95) 0%,
            rgba(180, 80, 255, 0.55) 3%,
            rgba(30, 80, 255, 0.25) 12%,
            transparent 35%
        ),

        /* Purple and blue atmosphere */
        radial-gradient(
            ellipse at center,
            rgba(100, 0, 255, 0.3),
            rgba(10, 10, 60, 0.1) 60%,
            transparent 85%
        );

    mask-image: radial-gradient(
        ellipse at center,
        black 0%,
        black 70%,
        transparent 100%
    );

    filter: blur(1px) brightness(1.4);

    animation: colorfulHyperspace 2.2s ease-in-out forwards;
}

/* Background acceleration */
.stApp:has(.warp-trigger)::before {
    animation:
        starsMove 25s linear infinite,
        warpBackground 2.2s ease-in-out forwards;
}

/* HYPERSPACE MOVEMENT */
@keyframes colorfulHyperspace {

    0% {
        opacity: 0;
        transform: scale(0.12) rotate(0deg);
        filter: blur(3px) brightness(1);
    }

    20% {
        opacity: 1;
        transform: scale(0.8) rotate(3deg);
        filter: blur(1px) brightness(1.8);
    }

    55% {
        opacity: 1;
        transform: scale(1.8) rotate(8deg);
        filter: blur(1.5px) brightness(2.5);
    }

    85% {
        opacity: 0.9;
        transform: scale(3.2) rotate(15deg);
        filter: blur(3px) brightness(2);
    }

    100% {
        opacity: 0;
        transform: scale(5) rotate(22deg);
        filter: blur(5px) brightness(1);
    }
}

/* Screen brightness and acceleration */
@keyframes warpBackground {

    0% {
        filter: brightness(1);
        transform: scale(1);
    }

    40% {
        filter: brightness(1.8) saturate(2);
        transform: scale(1.08);
    }

    75% {
        filter: brightness(2.2) saturate(2.5);
        transform: scale(1.15);
    }

    100% {
        filter: brightness(1);
        transform: scale(1);
    }
}

/* FOOTER */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🚀 Amazon Sentiment Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered product review sentiment detection</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# REVIEW INPUT
# --------------------------------------------------

review = st.text_area(
    "📝 Enter your Amazon product review",
    height=150,
    placeholder="Example: This product is amazing. The quality is excellent!"
)


# --------------------------------------------------
# HYPERSPACE ANIMATION PLACEHOLDER
# --------------------------------------------------

animation_placeholder = st.empty()


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button("🚀 Analyze Sentiment"):

    if not review.strip():
        st.warning("Please enter a review before analyzing.")

    else:
        # Trigger full-screen animation
        animation_placeholder.markdown(
            '<div class="warp-trigger"></div>',
            unsafe_allow_html=True
        )

        time.sleep(2)

        animation_placeholder.empty()

        # Connect to Flask API
        try:
            with st.spinner("Analyzing your review..."):

                response = requests.post(
                    "http://127.0.0.1:5000/predict",
                    json={"reviews": review},
                    timeout=30
                )

            if response.status_code == 200:

                result = response.json()
                sentiment = result.get("prediction", "").lower()

                if sentiment == "positive":

                    st.markdown("""
                    <div class="result-card positive">
                        😊 POSITIVE REVIEW
                        <div style="font-size:16px; margin-top:10px;">
                            This customer has expressed a positive opinion!
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                elif sentiment == "negative":

                    st.markdown("""
                    <div class="result-card negative">
                        😞 NEGATIVE REVIEW
                        <div style="font-size:16px; margin-top:10px;">
                            This customer has expressed a negative opinion.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.info(f"Prediction: {sentiment}")

            else:
                st.error(
                    f"API Error: {response.status_code} - {response.text}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Flask API. "
                "Please start your Flask backend first."
            )

        except requests.exceptions.Timeout:
            st.error("The prediction request timed out.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    Built with Python, Streamlit, Flask and Machine Learning
    <br>
    ✨ Powered by AI
</div>
""", unsafe_allow_html=True)
