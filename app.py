import streamlit as st
import fitz
import pandas as pd

from llm_service import analyze_resume
from database import (
    create_table,
    save_candidate,
    get_all_candidates,
    clear_candidates
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Resume Screener",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# APPLICATION SETTINGS
# =========================================================

SHORTLIST_THRESHOLD = 70


# =========================================================
# DATABASE SETUP
# =========================================================

create_table()


# =========================================================
# TEMPORARY DATABASE RESET
# =========================================================
# To clear the existing candidates on Streamlit Cloud,
# open the deployed app once with:
#
# https://YOUR-APP-URL.streamlit.app/?reset=true
#
# After clearing, the URL parameter is removed automatically.

if st.query_params.get("reset") == "true":

    clear_candidates()

    st.query_params.clear()

    st.rerun()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(uploaded_file):

    pdf_bytes = uploaded_file.read()

    pdf_document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    return text


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🤖 Smart Resume Screener'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered candidate screening and job matching system'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# CANDIDATE DATABASE DASHBOARD
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📊 Candidate Dashboard'
    '</div>',
    unsafe_allow_html=True
)

database_candidates = get_all_candidates()


if database_candidates:

    total_candidates = len(database_candidates)

    shortlisted_candidates = [
        candidate
        for candidate in database_candidates
        if candidate[3] >= SHORTLIST_THRESHOLD
    ]

    average_score = (
        sum(candidate[3] for candidate in database_candidates)
        / total_candidates
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👥 Total Candidates",
            total_candidates
        )

    with col2:

        st.metric(
            "🏆 Shortlisted",
            len(shortlisted_candidates)
        )

    with col3:

        st.metric(
            "📈 Average Match",
            f"{average_score:.1f}%"
        )

    st.write("")

    # -----------------------------------------------------
    # STORED RANKINGS
    # -----------------------------------------------------

    st.markdown(
        "### 🏆 Stored Candidate Rankings"
    )

    stored_table = []

    for candidate in database_candidates:

        candidate_name = candidate[1]
        filename = candidate[2]
        score = candidate[3]

        status = (
            "✅ Shortlisted"
            if score >= SHORTLIST_THRESHOLD
            else "❌ Not shortlisted"
        )

        stored_table.append(
            {
                "Candidate": candidate_name,
                "Resume": filename,
                "Match Score": f"{score}%",
                "Status": status
            }
        )

    st.dataframe(
        stored_table,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # RECRUITER FILTERS
    # =====================================================

    st.markdown(
        "### 🔎 Recruiter Filters"
    )

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        search_name = st.text_input(
            "Search candidate",
            placeholder="Enter candidate name..."
        )

    with filter_col2:

        minimum_score = st.slider(
            "Minimum match score",
            min_value=0,
            max_value=100,
            value=0,
            step=5
        )

    with filter_col3:

        shortlisted_only = st.checkbox(
            "🏆 Show shortlisted only"
        )

    # -----------------------------------------------------
    # APPLY SEARCH FILTER
    # -----------------------------------------------------

    filtered_candidates = database_candidates

    if search_name.strip():

        filtered_candidates = [
            candidate
            for candidate in filtered_candidates
            if search_name.lower()
            in candidate[1].lower()
        ]

    # -----------------------------------------------------
    # APPLY SCORE FILTER
    # -----------------------------------------------------

    filtered_candidates = [
        candidate
        for candidate in filtered_candidates
        if candidate[3] >= minimum_score
    ]

    # -----------------------------------------------------
    # APPLY SHORTLIST FILTER
    # -----------------------------------------------------

    if shortlisted_only:

        filtered_candidates = [
            candidate
            for candidate in filtered_candidates
            if candidate[3] >= SHORTLIST_THRESHOLD
        ]

    # -----------------------------------------------------
    # DISPLAY FILTERED RESULTS
    # -----------------------------------------------------

    st.markdown(
        "### 🔍 Filtered Candidates"
    )

    if filtered_candidates:

        filtered_table = []

        for candidate in filtered_candidates:

            score = candidate[3]

            filtered_table.append(
                {
                    "Candidate": candidate[1],
                    "Resume": candidate[2],
                    "Match Score": f"{score}%",
                    "Status": (
                        "✅ Shortlisted"
                        if score >= SHORTLIST_THRESHOLD
                        else "❌ Not shortlisted"
                    )
                }
            )

        st.dataframe(
            filtered_table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No candidates match the selected filters."
        )

    # =====================================================
    # CSV EXPORT
    # =====================================================

    st.markdown(
        "### 📥 Export Results"
    )

    export_data = []

    for candidate in filtered_candidates:

        score = candidate[3]

        export_data.append(
            {
                "Candidate Name": candidate[1],
                "Resume": candidate[2],
                "Match Score": score,
                "Status": (
                    "Shortlisted"
                    if score >= SHORTLIST_THRESHOLD
                    else "Not shortlisted"
                )
            }
        )

    if export_data:

        export_df = pd.DataFrame(
            export_data
        )

        csv_data = export_df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Candidate Results",
            data=csv_data,
            file_name="candidate_results.csv",
            mime="text/csv"
        )

else:

    st.info(
        "No candidates have been analyzed yet."
    )


st.divider()


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📄 Job Description'
    '</div>',
    unsafe_allow_html=True
)

job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder=(
        "Example: We are looking for a Junior Software "
        "Engineer with strong skills in Python, Java, "
        "React, Git, Data Structures and Algorithms."
    )
)


# =========================================================
# RESUME UPLOAD
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📁 Upload Resumes'
    '</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)


# =========================================================
# DISPLAY UPLOADED FILES
# =========================================================

if uploaded_files:

    st.success(
        f"{len(uploaded_files)} resume(s) uploaded successfully!"
    )

    for file in uploaded_files:

        st.write(
            f"📄 {file.name}"
        )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.divider()

if st.button(
    "🤖 Analyze & Rank Candidates",
    type="primary",
    use_container_width=True
):

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not job_description.strip():

        st.warning(
            "⚠️ Please enter a job description."
        )

    elif not uploaded_files:

        st.warning(
            "⚠️ Please upload at least one resume."
        )

    else:

        results = []

        # -------------------------------------------------
        # ANALYSIS HEADER
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🔍 Analyzing Candidates'
            '</div>',
            unsafe_allow_html=True
        )

        progress = st.progress(0)

        total_files = len(uploaded_files)

        # -------------------------------------------------
        # PROCESS EACH RESUME
        # -------------------------------------------------

        for index, file in enumerate(uploaded_files):

            try:

                # -----------------------------------------
                # EXTRACT PDF TEXT
                # -----------------------------------------

                resume_text = extract_text_from_pdf(
                    file
                )

                if not resume_text.strip():

                    st.warning(
                        f"⚠️ No text could be extracted "
                        f"from {file.name}."
                    )

                    continue

                # -----------------------------------------
                # GEMINI ANALYSIS
                # -----------------------------------------

                with st.spinner(
                    f"🤖 Gemini is analyzing {file.name}..."
                ):

                    result = analyze_resume(
                        resume_text,
                        job_description
                    )

                # -----------------------------------------
                # ADD FILE NAME
                # -----------------------------------------

                result["filename"] = file.name

                # -----------------------------------------
                # SAVE TO DATABASE
                # -----------------------------------------

                save_candidate(
                    result
                )

                # -----------------------------------------
                # ADD TO RESULTS
                # -----------------------------------------

                results.append(
                    result
                )

                # -----------------------------------------
                # UPDATE PROGRESS
                # -----------------------------------------

                progress.progress(
                    (index + 1) / total_files
                )

            except Exception as e:

                st.error(
                    f"❌ Error processing "
                    f"{file.name}: {e}"
                )

        # =================================================
        # SORT RESULTS
        # =================================================

        results.sort(
            key=lambda x: x.get(
                "match_score",
                0
            ),
            reverse=True
        )

        # =================================================
        # DISPLAY RESULTS
        # =================================================

        if results:

            st.divider()

            # =================================================
            # SHORTLISTED CANDIDATES
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '🏆 Shortlisted Candidates'
                '</div>',
                unsafe_allow_html=True
            )

            shortlisted = [
                candidate
                for candidate in results
                if candidate.get(
                    "match_score",
                    0
                ) >= SHORTLIST_THRESHOLD
            ]

            if shortlisted:

                for rank, candidate in enumerate(
                    shortlisted,
                    start=1
                ):

                    score = candidate.get(
                        "match_score",
                        0
                    )

                    candidate_name = candidate.get(
                        "candidate_name",
                        "Unknown Candidate"
                    )

                    st.markdown(
                        f"### 🥇 {rank}. "
                        f"{candidate_name}"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "🎯 Match Score",
                            f"{score}%"
                        )

                    with col2:

                        st.success(
                            "✅ SHORTLISTED"
                        )

                    with col3:

                        st.write(
                            "📄 Resume"
                        )

                        st.caption(
                            candidate.get(
                                "filename",
                                "Unknown"
                            )
                        )

                    st.progress(
                        min(score / 100, 1.0)
                    )

                    st.markdown(
                        "**🧠 AI Justification**"
                    )

                    st.info(
                        candidate.get(
                            "justification",
                            "No justification available."
                        )
                    )

                    st.divider()

            else:

                st.warning(
                    "No candidates reached the "
                    f"{SHORTLIST_THRESHOLD}% "
                    "shortlist threshold."
                )

            # =================================================
            # CANDIDATE RANKING
            # =================================================

            st.markdown(
                '<div class="section-title">'
                '📊 Candidate Ranking'
                '</div>',
                unsafe_allow_html=True
            )

            for rank, candidate in enumerate(
                results,
                start=1
            ):

                score = candidate.get(
                    "match_score",
                    0
                )

                candidate_name = candidate.get(
                    "candidate_name",
                    "Unknown Candidate"
                )

                status = (
                    "✅ Shortlisted"
                    if score >= SHORTLIST_THRESHOLD
                    else "❌ Not shortlisted"
                )

                st.write(
                    f"**{rank}. {candidate_name}** "
                    f"— **{score}%** "
                    f"— {status}"
                )

                st.progress(
                    min(score / 100, 1.0)
                )

            # =================================================
            # DETAILED ANALYSIS
            # =================================================

            st.divider()

            st.markdown(
                '<div class="section-title">'
                '📋 Detailed Candidate Analysis'
                '</div>',
                unsafe_allow_html=True
            )

            for candidate in results:

                candidate_name = candidate.get(
                    "candidate_name",
                    "Unknown Candidate"
                )

                score = candidate.get(
                    "match_score",
                    0
                )

                with st.expander(
                    f"📄 {candidate_name} — {score}%"
                ):

                    # -------------------------------------
                    # SUMMARY
                    # -------------------------------------

                    st.markdown(
                        "### 📝 Candidate Summary"
                    )

                    st.write(
                        candidate.get(
                            "candidate_summary",
                            "Not available."
                        )
                    )

                    # -------------------------------------
                    # SKILLS
                    # -------------------------------------

                    col1, col2 = st.columns(2)

                    with col1:

                        st.markdown(
                            "### ✅ Matching Skills"
                        )

                        matching_skills = candidate.get(
                            "matching_skills",
                            []
                        )

                        if matching_skills:

                            for skill in matching_skills:

                                st.write(
                                    f"• {skill}"
                                )

                        else:

                            st.write(
                                "No matching skills identified."
                            )

                    with col2:

                        st.markdown(
                            "### ⚠️ Missing Skills"
                        )

                        missing_skills = candidate.get(
                            "missing_skills",
                            []
                        )

                        if missing_skills:

                            for skill in missing_skills:

                                st.write(
                                    f"• {skill}"
                                )

                        else:

                            st.write(
                                "No major missing skills identified."
                            )

                    # -------------------------------------
                    # EDUCATION
                    # -------------------------------------

                    st.markdown(
                        "### 🎓 Education"
                    )

                    education = candidate.get(
                        "education",
                        []
                    )

                    if education:

                        for item in education:

                            st.write(
                                f"• {item}"
                            )

                    else:

                        st.write(
                            "Education information not available."
                        )

                    # -------------------------------------
                    # EXPERIENCE
                    # -------------------------------------

                    st.markdown(
                        "### 💼 Experience"
                    )

                    experience = candidate.get(
                        "experience",
                        []
                    )

                    if experience:

                        for item in experience:

                            st.write(
                                f"• {item}"
                            )

                    else:

                        st.write(
                            "No experience information identified."
                        )

                    # -------------------------------------
                    # STRENGTHS
                    # -------------------------------------

                    st.markdown(
                        "### 💪 Strengths"
                    )

                    strengths = candidate.get(
                        "strengths",
                        []
                    )

                    if strengths:

                        for item in strengths:

                            st.write(
                                f"• {item}"
                            )

                    else:

                        st.write(
                            "No strengths identified."
                        )

                    # -------------------------------------
                    # RECOMMENDATIONS
                    # -------------------------------------

                    st.markdown(
                        "### 📈 Recommendations"
                    )

                    recommendations = candidate.get(
                        "recommendations",
                        []
                    )

                    if recommendations:

                        for item in recommendations:

                            st.write(
                                f"• {item}"
                            )

                    else:

                        st.write(
                            "No recommendations available."
                        )

                    # -------------------------------------
                    # AI JUSTIFICATION
                    # -------------------------------------

                    st.markdown(
                        "### 🧠 AI Justification"
                    )

                    st.info(
                        candidate.get(
                            "justification",
                            "No justification available."
                        )
                    )


# =========================================================
# CANDIDATE COMPARISON
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '⚖️ Compare Candidates'
    '</div>',
    unsafe_allow_html=True
)

comparison_candidates = get_all_candidates()


if len(comparison_candidates) >= 2:

    # -----------------------------------------------------
    # CREATE CANDIDATE OPTIONS
    # -----------------------------------------------------

    candidate_options = {}

    for candidate in comparison_candidates:

        candidate_id = candidate[0]

        candidate_name = candidate[1]

        score = candidate[3]

        candidate_options[
            f"{candidate_name} — {score}%"
        ] = candidate_id

    # -----------------------------------------------------
    # SELECT CANDIDATES
    # -----------------------------------------------------

    selected_candidates = st.multiselect(
        "Select candidates to compare",
        options=list(
            candidate_options.keys()
        ),
        default=list(
            candidate_options.keys()
        )[:2]
    )

    if len(selected_candidates) >= 2:

        selected_ids = [
            candidate_options[name]
            for name in selected_candidates
        ]

        selected_records = [
            candidate
            for candidate in comparison_candidates
            if candidate[0] in selected_ids
        ]

        # -------------------------------------------------
        # COMPARISON TABLE
        # -------------------------------------------------

        st.markdown(
            "### 📊 Candidate Comparison"
        )

        comparison_data = []

        for candidate in selected_records:

            score = candidate[3]

            status = (
                "✅ Shortlisted"
                if score >= SHORTLIST_THRESHOLD
                else "❌ Not shortlisted"
            )

            comparison_data.append(
                {
                    "Candidate": candidate[1],
                    "Match Score": f"{score}%",
                    "Resume": candidate[2],
                    "Status": status
                }
            )

        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # SCORE COMPARISON
        # -------------------------------------------------

        st.markdown(
            "### 📈 Score Comparison"
        )

        for candidate in selected_records:

            st.write(
                f"**{candidate[1]}** — "
                f"{candidate[3]}%"
            )

            st.progress(
                min(
                    candidate[3] / 100,
                    1.0
                )
            )

        # -------------------------------------------------
        # BEST CANDIDATE
        # -------------------------------------------------

        best_candidate = max(
            selected_records,
            key=lambda x: x[3]
        )

        st.success(
            f"🏆 Best Match: **{best_candidate[1]}** "
            f"with a match score of "
            f"**{best_candidate[3]}%**"
        )

    else:

        st.info(
            "Select at least two candidates to compare."
        )

else:

    st.info(
        "At least two candidates are required "
        "for comparison."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🤖 Smart Resume Screener • "
    "Powered by Gemini AI • "
    "Built with Python, Streamlit, PyMuPDF and SQLite"
)
