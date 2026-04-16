import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(layout="wide")

# ==============================
# HEADER
# ==============================
def show_header():
    st.markdown("""
    <div style="
        background:#0073e6;
        padding:6px 15px;
        border-radius:8px;
        margin-bottom:10px;
        display:flex;
        align-items:center;
        height:50px;">
        <h3 style="color:white;margin:0;">
            SERP-AP FPO Graduation Tool
        </h3>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
mapped_file = "final_mapped_output.xlsx"
rules_file = "FPO_Dashboard.xlsx"

df = pd.read_excel(mapped_file)
rules_df = pd.read_excel(rules_file, sheet_name="Rules")
rules_dff = pd.read_excel(rules_file, sheet_name="label mapping")
mature_df = pd.read_excel(rules_file, sheet_name="Mature")

# ==============================
# CLEAN COLUMNS
# ==============================
df.columns = df.columns.str.strip().str.lower()
rules_df.columns = rules_df.columns.str.strip().str.lower()
rules_dff.columns = rules_dff.columns.str.strip().str.lower()
mature_df.columns = mature_df.columns.str.strip().str.lower()

# ==============================
# SAFE VALUE CONVERTER
# ==============================
def safe_binary(val):
    if pd.isna(val):
        return None
    try:
        return int(float(val))
    except:
        val = str(val).strip().lower()
        if val in ["yes", "y"]:
            return 1
        if val in ["no", "n"]:
            return 0
    return None

# ==============================
# MATURE MAP
# ==============================
mature_map = {
    str(mature_df.iloc[i, 0]).strip().lower(): safe_binary(mature_df.iloc[i, 1])
    for i in range(len(mature_df))
}

# ==============================
# LABEL MAP
# ==============================
rules_dff["indicator"] = rules_dff["indicator"].astype(str).str.strip().str.lower()
label_map = rules_dff.groupby("indicator").first().to_dict("index")

def get_label(col):
    return label_map.get(str(col).strip().lower(), {})

# ==============================
# MATURITY LABEL
# ==============================
def maturity_label(p):
    if p < 50:
        return "Nascent", "red"
    elif p < 80:
        return "Somewhat Mature", "orange"
    elif p < 100:
        return "Near Mature", "lightgreen"
    else:
        return "Mature", "green"

# ==============================
# SCORE CALCULATION (UPDATED FOR AGGREGATE)
# ==============================
def calculate_score(df_filtered, cols, aggregate=False):
    total = 0
    correct = 0

    if df_filtered.empty:
        return 0, 0, 0

    # 👉 OVERALL MODE
    if aggregate:
        for _, row in df_filtered.iterrows():
            for col in cols:
                if col not in df_filtered.columns or col == "fpo_registration-fpo_name":
                    continue

                actual = safe_binary(row[col])
                expected = 1 if col.startswith("fpo_registration-") else safe_binary(mature_map.get(col))

                if actual is None or expected is None:
                    continue

                total += 1
                if actual == expected:
                    correct += 1

    # 👉 SINGLE FPO MODE
    else:
        row = df_filtered.iloc[0]

        for col in cols:
            if col not in df_filtered.columns or col == "fpo_registration-fpo_name":
                continue

            actual = safe_binary(row[col])
            expected = 1 if col.startswith("fpo_registration-") else safe_binary(mature_map.get(col))

            if actual is None or expected is None:
                continue

            total += 1
            if actual == expected:
                correct += 1

    percent = int((correct / total) * 100) if total else 0
    return correct, total, percent

# ==============================
# SECTION GROUPING
# ==============================
sections = {
    "FPO Registration": [c for c in df.columns if "fpo_registration-" in c],
    "Membership": [c for c in df.columns if "fpo_membership-" in c],
    "Governance": [c for c in df.columns if "strength_governanace" in c],
    "FPO Staff": [c for c in df.columns if "fpo_staff_details" in c],
    "Compliance": [c for c in df.columns if "licences_certificates" in c],
    "Assets": [c for c in df.columns if "assets_owned" in c or "asset_register" in c],
    "Accounts": [c for c in df.columns if "records_maintained" in c or "financial_compliance" in c],
    "Business": [c for c in df.columns if "business_lines" in c],
    "Market": [c for c in df.columns if "market_linkages" in c],
    "Processes": [c for c in df.columns if "business_processes" in c]
}

# ==============================
# SESSION STATE
# ==============================
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None

if "selected_fpo" not in st.session_state:
    st.session_state.selected_fpo = ""

if "action_plan_df" not in st.session_state:
    st.session_state.action_plan_df = None

# ==============================
# FILTER DATA
# ==============================
def get_df():
    if not st.session_state.selected_fpo:
        return df.copy()
    return df[df["fpo_registration-fpo_name"].str.upper() == st.session_state.selected_fpo].copy()

# ==============================
# DASHBOARD
# ==============================
if st.session_state.selected_section is None:

    show_header()

    # 👉 UPPERCASE display
    fpo_list = [""] + df["fpo_registration-fpo_name"].dropna().str.upper().unique().tolist()

    selected = st.selectbox(
        "Select FPO",
        fpo_list,
        index=fpo_list.index(st.session_state.selected_fpo)
        if st.session_state.selected_fpo in fpo_list else 0
    )

    st.session_state.selected_fpo = selected

    data = get_df()
    scores = []

    aggregate = True if not st.session_state.selected_fpo else False

    section_items = list(sections.items())

    for i in range(0, len(section_items), 5):
        cols_ui = st.columns(5)

        for j, (section, cols) in enumerate(section_items[i:i+5]):

            correct, total, percent = calculate_score(data, cols, aggregate)
            scores.append(percent)

            label, color = maturity_label(percent)

            with cols_ui[j]:
                st.markdown(f"""
                <div style="background:white;padding:15px;border-radius:12px;
                            border:1px solid #ddd;box-shadow:2px 2px 6px #ccc;">
                    <h4 style="color:#0073e6;">{section}</h4>
                    <p>Score: <b>{correct}/{total}</b></p>
                    <p style="color:{color};">Maturity: {percent}% - {label}</p>
                    <div style="background:#eee;height:10px;border-radius:6px;">
                        <div style="width:{percent}%;background:{color};height:10px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("View details", key=section):
                    st.session_state.selected_section = section
                    st.session_state.action_plan_df = None

    overall = int(sum(scores) / len(scores)) if scores else 0

    st.markdown(f"""
    <div style="background:#0073e6;color:white;padding:15px;
                border-radius:10px;text-align:center;">
        <h3>Overall Maturity : {overall}%</h3>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# DETAIL PAGE
# ==============================
else:

    show_header()

    section = st.session_state.selected_section
    st.markdown(f"<h2 style='color:#0073e6;'>{section}</h2>", unsafe_allow_html=True)

    # 👉 NEW CONDITION
    if not st.session_state.selected_fpo:
        st.warning("Select FPO to view details")

    else:
        st.markdown(f"**Selected FPO:** {st.session_state.selected_fpo}")

        data = get_df()
        cols = sections[section]

        tab_choice = st.radio(
            "Select View",
            ["Benchmarks Met", "Areas of Improvement"],
            horizontal=True
        )

        if tab_choice == "Benchmarks Met":
            for col in cols:
                l = get_label(col)
                if col in data.columns:
                    expected = 1 if col.startswith("fpo_registration-") else safe_binary(mature_map.get(col))
                    if safe_binary(data.iloc[0][col]) == expected:
                        st.success(l.get("message", ""))

        elif tab_choice == "Areas of Improvement":
            for col in cols:
                l = get_label(col)
                if col in data.columns:
                    expected = 1 if col.startswith("fpo_registration-") else safe_binary(mature_map.get(col))
                    if safe_binary(data.iloc[0][col]) != expected:
                        st.warning(l.get("message", ""))

       
    if st.button("⬅️ Back"):
        st.session_state.selected_section = None