import streamlit as st
from recommendation_engine import recommend_assessments

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

st.markdown("<h2 style='color:red;'>🔍 SHL Assessment Recommendation Engine</h2>", unsafe_allow_html=True)
st.markdown(
    "Get personalized SHL assessments based on your job description or query. "
    "Paste a JD URL or describe your role in natural language."
)

# --- User Input ---
option = st.radio("How would you like to input your query?", ("Text Query", "Job Description URL"))

if option == "Text Query":
    user_input = st.text_area("Enter your job description or role requirement:", height=150)
    is_url = False
else:
    user_input = st.text_input("Enter JD URL (must be public):")
    is_url = True

top_k = st.slider("How many recommendations do you want?", 1, 10, 5)

# --- Submit ---
if st.button("Get Recommendations") and user_input.strip():
    with st.spinner("Generating recommendations..."):
        try:
            results = recommend_assessments(user_input, is_url=is_url, top_k=top_k)

            if not results:
                st.warning("No recommendations found. Try a different query.")
            else:
                st.success(f"Top {len(results)} recommendations:")
                for i, rec in enumerate(results, 1):
                    st.markdown(f"### {i}. [{rec['Assessment Name']}]({rec['Assessment URL']})")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Remote Testing Support", rec['Remote Testing Support'])
                    col2.metric("Adaptive/IRT Support", rec['Adaptive/IRT Support'])
                    col3.metric("Duration", rec['Duration'])

                    test_types = [t.strip() for t in rec['Test Type'].split(',')]
                    st.markdown("**Test Type:**", unsafe_allow_html=True)
                    for tt in test_types:
                        st.markdown(
                            f"""
                            <span style='display:inline-block; background-color:#1f77b4; color:white; 
                            padding:6px 12px; margin:4px 4px 4px 0; border-radius:20px; font-size:13px;'>
                            {tt}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                    

                    st.markdown("---")

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Please provide a valid query or JD URL above to get started.")
