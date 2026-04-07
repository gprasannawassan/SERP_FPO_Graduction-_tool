import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
.main-title-card {background-color:#0073e6;padding:3px;border-radius:4px;margin-bottom:8px;}
.main-title-card h1 {color:white;font-size:22px;font-weight:bold;margin:0;}

.section-card {background-color:#f0f8ff;padding:15px;border-radius:12px;text-align:center;margin-bottom:10px;}
.section-title {font-size:16px;font-weight:bold;}
.section-score {font-size:20px;font-weight:bold;}
.section-percent {font-size:18px;font-weight:bold;}

.progress-container {width:100%;background-color:#ddd;border-radius:8px;margin-top:8px;}
.progress-bar {height:10px;border-radius:8px;}

.overall-card {background-color:#f0f8ff;padding:20px;border-radius:12px;text-align:center;font-size:22px;font-weight:bold;margin-top:30px;}
</style>
""", unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
mapped_file = "final_mapped_output.xlsx"
mature_file = "FPO_Dashboard.xlsx"

df = pd.read_excel(mapped_file)
mature_df = pd.read_excel(mature_file, sheet_name="Mature")
rules_df = pd.read_excel(mature_file, sheet_name="Rules")

df.columns = df.columns.str.strip().str.lower()
mature_df.columns = mature_df.columns.str.strip().str.lower()
rules_df.columns = rules_df.columns.str.strip().str.lower()

# ==============================
# FUNCTIONS
# ==============================
def mature_to_binary(val):
    val = str(val).strip().lower()
    if val in ["yes","y","1"]: return 1
    if val in ["no","n","0"]: return 0
    return None

def maturity_label(p):
    if p < 50: return "Nascent","red"
    elif p < 80: return "Somewhat Mature","orange"
    elif p < 100: return "Near Mature","lightgreen"
    else: return "Mature","green"

# ==============================
# MATURE MAP
# ==============================
mature_map = {
    str(mature_df.iloc[i,0]).strip().lower(): mature_to_binary(mature_df.iloc[i,1])
    for i in range(len(mature_df))
}

# ==============================
# SCORE FUNCTION
# ==============================
def calculate_score(df, cols):
    total = 0
    correct = 0
    for col in cols:
        if col in df.columns and col in mature_map:
            if col == "fpo_registration-fpo_name":
                continue
            expected = mature_map[col]
            correct += (df[col] == expected).sum()
            total += len(df[col])
    percent = int((correct / total) * 100) if total else 0
    return correct, total, percent

# ==============================
# SECTIONS
# ==============================
sections = {
    "FPO Registration":[col for col in df.columns if "fpo_registration-" in col],
    "Membership":[col for col in df.columns if "fpo_membership-" in col],
    "Governance":[col for col in df.columns if "strength_governanace" in col],
    "FPO Staff":[col for col in df.columns if "fpo_staff_details" in col],
    "Compliance":[col for col in df.columns if "licences_certificates" in col],
    "Assets":[col for col in df.columns if "assets_owned" in col or "asset_register" in col],
    "Accounts":[col for col in df.columns if "records_maintained" in col or "financial_compliance" in col],
    "Business":[col for col in df.columns if "business_lines" in col],
    "Market":[col for col in df.columns if "market_linkages" in col],
    "Processes":[col for col in df.columns if "business_processes" in col]
}

# ==============================
# SESSION STATE
# ==============================
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None
if "selected_fpo" not in st.session_state:
    st.session_state.selected_fpo = ""

# ==============================
# FILTER
# ==============================
def get_df():
    if st.session_state.selected_fpo == "":
        return df
    return df[df["fpo_registration-fpo_name"] == st.session_state.selected_fpo]

# ==============================
# DASHBOARD
# ==============================
if st.session_state.selected_section is None:

    st.markdown('<div class="main-title-card"><h1>FPO Graduation Tool</h1></div>', unsafe_allow_html=True)

    fpo_list = [""] + df["fpo_registration-fpo_name"].dropna().unique().tolist()
    current_index = fpo_list.index(st.session_state.selected_fpo) if st.session_state.selected_fpo in fpo_list else 0
    st.session_state.selected_fpo = st.selectbox("SELECT FPO", fpo_list, index=current_index)

    data = get_df()
    cols_ui = st.columns(5)
    scores = []

    for i,(section,cols) in enumerate(sections.items()):
        correct,total,percent = calculate_score(data, cols)
        scores.append(percent)
        label,color = maturity_label(percent)

        with cols_ui[i % 5]:
            st.markdown(f"""
            <div class="section-card">
                <div class="section-title">{section}</div>
                <div class="section-score">{correct}/{total}</div>
                <div class="section-percent" style="color:{color};">{percent}% - {label}</div>
                <div class="progress-container">
                    <div class="progress-bar" style="width:{percent}%; background-color:{color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("View details", key=f"view_{section}"):
                st.session_state.selected_section = section

    overall = int(sum(scores)/len(scores))
    st.markdown(f"""
    <div class="overall-card">
    Overall Maturity : {overall}%
    </div>
    """, unsafe_allow_html=True)

# ==============================
# DETAIL PAGE (PER SECTION)
# ==============================
else:
    section = st.session_state.selected_section
    st.markdown(f'<div class="main-title-card"><h1>{section}</h1></div>', unsafe_allow_html=True)

    data = get_df()
    cols = sections[section]

    correct_list, wrong_list = [], []
    for col in cols:
        if col in data.columns and col in mature_map:
            expected = mature_map[col]
            if (data[col] == expected).all():
                correct_list.append(col)
            else:
                wrong_list.append(col)

    # Card-style tabs
    tab_choice = st.radio(
        "Select View",
        ["Benchmarks Met", "Areas of Improvement", "Action Plan"],
        horizontal=True,
        key="tab_choice"
    )

    if tab_choice == "Benchmarks Met":
        with st.expander("✅ Benchmarks Met", expanded=True):
            for q in correct_list:
                st.write(f"- {q}")

    elif tab_choice == "Areas of Improvement":
        with st.expander("⚠️ Areas of Improvement", expanded=True):
            for q in wrong_list:
                st.write(f"- {q}")

    elif tab_choice == "Action Plan":
        subtab1, subtab2 = st.tabs(["Action Plan","How to Do"])
        with subtab1:
            for _,row in rules_df[rules_df['section']==section].iterrows():
                st.write(row.get("action_plan","-"))
        with subtab2:
            for _,row in rules_df[rules_df['section']==section].iterrows():
                st.write(row.get("how_to_do","-"))

    if st.button("⬅️ Back"):
        st.session_state.selected_section = None
