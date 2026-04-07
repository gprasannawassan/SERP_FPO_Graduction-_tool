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
.section-card {background-color:#f0f8ff;padding:20px;border-radius:12px;text-align:center;font-size:18px;font-weight:bold;margin-bottom:10px;color:black;}
.section-title {font-size:18px;font-weight:bold;}
.section-text {font-size:20px;font-weight:bold;}
.progress-container {width:100%;background-color:#ddd;border-radius:8px;margin-top:8px;}
.progress-bar {height:10px;border-radius:8px;}
.overall-card {background-color:#f0f8ff;padding:20px;border-radius:12px;text-align:center;font-size:22px;font-weight:bold;margin-top:30px;}
</style>
""", unsafe_allow_html=True)

# ==============================
# FUNCTIONS
# ==============================
def clean_text(x):
    if pd.isna(x):
        return ""
    return str(x).strip().lower()

def normalize(val):
    val = clean_text(val)
    if val in ["yes","y"]: return "yes"
    elif val in ["no","n"]: return "no"
    elif val in ["nan","","none"]: return "missing"
    return val

def format_text(x):
    return str(x).capitalize()

def maturity_label(p):
    if p < 50: return "Nascent","red"
    elif p < 80: return "Somewhat Mature","orange"
    elif p < 100: return "Near Mature","lightgreen"
    else: return "Mature","green"

def calculate_section_percent(df, cols):
    total, correct = 0, 0
    for col in cols:
        if col in df.columns and col in mature_map:
            vals = df[col].apply(normalize)
            correct += sum(vals == mature_map[col])
            total += len(vals)
    return (correct / total) * 100 if total else 0

# ==============================
# LOAD DATA (FIXED)
# ==============================
file_path = "FPO_Dashboard.xlsx"

response_df = pd.read_excel(file_path, "Response")
mature_df = pd.read_excel(file_path, "Mature")

try:
    rules_df = pd.read_excel(file_path, "Rules")
except:
    rules_df = pd.DataFrame(columns=["section","condition","areas_of_improvements","action_plan"])

# ✅ apply instead of applymap
response_df = response_df.apply(lambda col: col.map(clean_text))
mature_df = mature_df.apply(lambda col: col.map(clean_text))
rules_df = rules_df.apply(lambda col: col.map(clean_text))

response_df.columns = response_df.columns.map(clean_text)
mature_df.columns = mature_df.columns.map(clean_text)
rules_df.columns = rules_df.columns.str.strip().str.lower().str.replace(" ", "_")

# ==============================
# MATURE MAP
# ==============================
mature_map = {
    clean_text(mature_df.iloc[i,0]): normalize(mature_df.iloc[i,1])
    for i in range(len(mature_df))
    if clean_text(mature_df.iloc[i,0]) not in ["","nan","none"]
}

# ==============================
# SESSION STATE
# ==============================
for k,v in {
    "selected_section":None,
    "view_details_section":None,
    "selected_fpo_main":""
}.items():
    if k not in st.session_state:
        st.session_state[k]=v

# ==============================
# SECTIONS
# ==============================
sections = {

    "FPO Registration":[
        "fpo_registration-registration_certificate",
        "fpo_registration-filing_regularly",
        "fpo_registration-notice_non-filing_returns",
        "fpo_registration-display_certificate",
        "fpo_registration-bylaws_copy_available"
    ],

    "Membership":[
        "fpo_membership-membership_forms_available",
        "fpo_membership-membership_receipts_available",
        "fpo_membership-membership_data_available",
        "fpo_membership-share_certificates_issued",
        "fpo_membership-share_certificates_acknowledged",
        "fpo_membership-active_shareholders_50percent"
    ],

    "Institutional Strength and Governance":[
        "strength_governanace-bod-tenure_rotation_rules",
        "strength_governanace-bod-bod_meet_once_a_month",
        "strength_governanace-bod-meeting_quorum",
        "strength_governanace-bod-meetings_documented",
        "strength_governanace-bod-financial_update_bod_meeting",
        "strength_governanace-bod-bod_sanctions_annual_budget",
        "strength_governanace-fpg-members_organized_fpgs",
        "strength_governanace-fpg-financial_update_in_fpg",
        "strength_governanace-fpg-bod_minutes_in_fpg",
        "strength_governanace-fpg-fpg_with_1_or_2_leaders",
        "strength_governanace-fpg-fpg_minutes_in_bod",
        "strength_governanace-capacity_building-member_education",
        "strength_governanace-capacity_building-bod_fpo_staff_trainings_last_2_years",
        "strength_governanace-agm_patronage_bonus-agm_every_year",
        "strength_governanace-agm_patronage_bonus-max_patronage_bonus",
        "strength_governanace-agm_patronage_bonus-annual_report"
    ],

    # ✅ NEW SECTIONS START

    "FPO Staff":[
        "fpo_staff_details-fpo_staff_status-staff_status_ceo",
        "fpo_staff_details-fpo_staff_status-staff_status_accountant",
        "fpo_staff_details-fpo_staff_status-staff_status_procurement_coordinator",
        "fpo_staff_details-fpo_staff_status-staff_status_processing_incharge",
        "fpo_staff_details-fpo_staff_status-staff_status_warehouse_charge",
        "fpo_staff_details-fpo_staff_status-staff_status_marketing_person",
        "fpo_staff_details-fpo_staff_status-others",
        "fpo_staff_details-fpo_staff_status-fpo_pay_staff_salaries"
    ],

    "Compliance":[
        "compliance-fpo_license_certificate-licences_certificates_pan",
        "compliance-fpo_license_certificate-licences_certificates_tan",
        "compliance-fpo_license_certificate-licences_certificates_gst",
        "compliance-fpo_license_certificate-licences_certificates_fssai",
        "compliance-fpo_license_certificate-licences_certificates_meteorology",
        "compliance-fpo_license_certificate-licences_certificates_amc_trade_licence",
        "compliance-fpo_license_certificate-licences_certificates_professional_tax",
        "compliance-fpo_license_certificate-licences_certificates_seed_licence",
        "compliance-fpo_license_certificate-licences_certificates_nsc",
        "compliance-fpo_license_certificate-licences_certificates_fertilizer_retail_licence",
        "compliance-fpo_license_certificate-licences_certificates_panchayat_municipal_approval"
    ],

    "Assets":[
        "fpo_assets-asset_register_maintained",
        "fpo_assets-assets_owned_fpo-assets_owned_warehouse_godown",
        "fpo_assets-assets_owned_fpo-assets_destoner",
        "fpo_assets-assets_owned_fpo-assets_grader",
        "fpo_assets-assets_owned_fpo-assets_dehuller_mill",
        "fpo_assets-assets_owned_fpo-assets_oil_expeller",
        "fpo_assets-assets_owned_fpo-assets_pulveriser",
        "fpo_assets-assets_owned_fpo-assets_packing_machine",
        "fpo_assets-assets_owned_fpo-assets_moisture_meters",
        "fpo_assets-assets_owned_fpo-assets_grading_tables",
        "fpo_assets-assets_owned_fpo-assets_pallets_crates",
        "fpo_assets-assets_owned_fpo-assets_sewing_machine",
        "fpo_assets-assets_owned_fpo-assets_commercial_vehicle",
        "fpo_assets-assets_owned_fpo-assets_office_furniture",
        "fpo_assets-assets_owned_fpo-assets_laptops",
        "fpo_assets-assets_owned_fpo-assets_others"
    ],

    "Accounts and Financial Management":[
        "fpo_accounts_financial_management-fpo_records-records_maintained_attendance_register",
        "fpo_accounts_financial_management-fpo_records-records_maintained_meeting_minutes_register",
        "fpo_accounts_financial_management-fpo_records-records_maintained_general_bod_meeting_register",
        "fpo_accounts_financial_management-fpo_records-records_maintained_wages_register",
        "fpo_accounts_financial_management-fpo_records-records_maintained_staff_salaries_register",
        "fpo_accounts_financial_management-fpo_records-records_maintained_used_tally_zoho_sap",
        "fpo_accounts_financial_management-fpo_records-records_maintained_purchase_bills",
        "fpo_accounts_financial_management-fpo_records-records_maintained_purchase_register",
        "fpo_accounts_financial_management-fpo_records-records_maintained_payment_vouchers",
        "fpo_accounts_financial_management-fpo_records-records_maintained_sales_invoices",
        "fpo_accounts_financial_management-fpo_records-records_maintained_sales_register",
        "fpo_accounts_financial_management-fpo_records-records_maintained_receipt_vouchers",
        "fpo_accounts_financial_management-fpo_records-records_maintained_stock_register",
        "fpo_accounts_financial_management-fpo_records-records_maintained_cash_book",
        "fpo_accounts_financial_management-fpo_records-records_maintained_bank_book",
        "fpo_accounts_financial_management-fpo_records-records_maintained_bank_reports",
        "fpo_accounts_financial_management-fpo_records-records_maintained_bank_statement_file",
        "fpo_accounts_financial_management-fpo_financial_compliance-financial_compliance_annual_financial_audit",
        "fpo_accounts_financial_management-fpo_financial_compliance-financial_compliance_itr_report",
        "fpo_accounts_financial_management-fpo_financial_compliance-financial_compliance_gst_filing",
        "fpo_accounts_financial_management-fpo_financial_compliance-financial_compliance_bank_reconciliation"
    ],

    "Business Lines":[
        "fpo_business_lines-business_lines_seed_sale",
        "fpo_business_lines-business_lines_tools_equipment_rental",
        "fpo_business_lines-business_lines_tools_equipment_sales",
        "fpo_business_lines-business_lines_fertilizers_sale",
        "fpo_business_lines-business_lines_farm_consumables",
        "fpo_business_lines-business_lines_bioinputs_sale",
        "fpo_business_lines-business_lines_animalfeed_sale",
        "fpo_business_lines-business_lines_other_inputs",
        "fpo_business_lines-business_lines_food_crops",
        "fpo_business_lines-business_lines_high_value_crops",
        "fpo_business_lines-business_lines_fresh_products",
        "fpo_business_lines-business_lines_value_added",
        "fpo_business_lines-business_lines_onward_lending",
        "fpo_business_lines-business_lines_others"
    ],

    "Market Linkages":[
        "market_linkages-market_channels_local_markets",
        "market_linkages-market_channels_input_outlets",
        "market_linkages-market_channels_fpo_partners",
        "market_linkages-market_channels_corporate_buyers",
        "market_linkages-market_channels_ecommerce_digital_marketing",
        "market_linkages-market_channels_own_brand"
    ],

    "Business Processes":[
        "fpo_business_processes-business_processes_planning_exercise",
        "fpo_business_processes-business_processes_farm_level_data",
        "fpo_business_processes-business_processes_annual_business_plan",
        "fpo_business_processes-business_processes_procurement_committee"
    ]
}

# ==============================
# COMMON FILTER
# ==============================
def get_df():
    if st.session_state.selected_fpo_main == "":
        return response_df
    return response_df[
        response_df["fpo_registration-fpo_name"] == st.session_state.selected_fpo_main
    ]

# ==============================
# DASHBOARD
# ==============================
if st.session_state.selected_section is None and st.session_state.view_details_section is None:

    st.markdown('<div class="main-title-card"><h1>FPO Graduation Tool</h1></div>', unsafe_allow_html=True)

    fpo_list = response_df["fpo_registration-fpo_name"].unique().tolist()
    st.selectbox("Select FPO", [""] + fpo_list, key="selected_fpo_main")

    df = get_df()

    section_scores = {}
    for section, cols in sections.items():
        section_scores[section] = round(calculate_section_percent(df, cols))

    cols_ui = st.columns(3)

    for i,(section,percent) in enumerate(section_scores.items()):
        with cols_ui[i]:
            label,color = maturity_label(percent)

            st.markdown(f"""
            <div class="section-card">
                <div class="section-title">{section}</div>
                <p class='section-text' style='color:{color};'>{percent}% - {label}</p>
                <div class="progress-container">
                    <div class="progress-bar" style="width:{percent}%; background-color:{color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1,c2 = st.columns(2)

            if c1.button("View Recommendations", key=f"rec_{section}"):
                st.session_state.selected_section = section

            if c2.button("View Details", key=f"det_{section}"):
                st.session_state.view_details_section = section

    overall = sum(section_scores.values()) / len(section_scores)

    st.markdown(f"""
    <div class="overall-card">
    Overall Performance : {round(overall)}%
    </div>
    """, unsafe_allow_html=True)

# ==============================
# RECOMMENDATIONS PAGE
# ==============================
elif st.session_state.selected_section:

    section = st.session_state.selected_section

    st.markdown(f'<div class="main-title-card"><h1>{section} - Recommendations</h1></div>', unsafe_allow_html=True)

    fpo_list = response_df["fpo_registration-fpo_name"].unique().tolist()
    st.selectbox("Select FPO", [""] + fpo_list, key="selected_fpo_main")

    if st.session_state.selected_fpo_main == "":
        st.warning("⚠️ Please select an FPO to view suggestions")
        if st.button("⬅️ Back"):
            st.session_state.selected_section = None
        st.stop()

    df = get_df()
    percent = calculate_section_percent(df, sections[section])

    section_rules = rules_df[rules_df["section"] == clean_text(section)]

    if percent == 100: cond = "100"
    elif percent > 80: cond = ">80"
    elif percent > 50: cond = ">50"
    else: cond = "<50"

    matched = section_rules[section_rules["condition"] == cond]

    tab1, tab2, tab3 = st.tabs(["Area of Improvements","Action Plan","View Details"])

    with tab1:
        for _,r in matched.iterrows():
            st.write(format_text(r["areas_of_improvements"]))

    with tab2:
        for _,r in matched.iterrows():
            st.write(format_text(r["action_plan"]))

    with tab3:
        correct_list, wrong_list = [], []

        for col in sections[section]:
            if col in df.columns and col in mature_map:
                vals = df[col].apply(normalize)
                if sum(vals == mature_map[col]) == len(vals):
                    correct_list.append(col)
                else:
                    wrong_list.append(col)

        st.subheader("Benchmarks Met")
        for q in correct_list:
            st.write(q)

        st.subheader("Actionable Improvement Areas")
        for q in wrong_list:
            st.write(q)

    if st.button("⬅️ Back"):
        st.session_state.selected_section = None

# ==============================
# DETAILS PAGE
# ==============================
elif st.session_state.view_details_section:

    section = st.session_state.view_details_section

    st.markdown(f'<div class="main-title-card"><h1>{section} - Detailed View</h1></div>', unsafe_allow_html=True)

    fpo_list = response_df["fpo_registration-fpo_name"].unique().tolist()
    st.selectbox("Select FPO", [""] + fpo_list, key="selected_fpo_main")

    if st.session_state.selected_fpo_main == "":
        st.warning("⚠️ Please select an FPO to view suggestions")
        if st.button("⬅️ Back to Dashboard"):
            st.session_state.view_details_section = None
        st.stop()

    df = get_df()

    correct_list, wrong_list = [], []

    for col in sections[section]:
        if col in df.columns and col in mature_map:
            vals = df[col].apply(normalize)
            if sum(vals == mature_map[col]) == len(vals):
                correct_list.append(col)
            else:
                wrong_list.append(col)

    tab1, tab2, tab3 = st.tabs([
        "Benchmarks Met",
        "Actionable Improvement Areas",
        "Recommendations"
    ])

    with tab1:
        for q in correct_list:
            st.write(q)

    with tab2:
        for q in wrong_list:
            st.write(q)

    with tab3:
        percent = calculate_section_percent(df, sections[section])

        section_rules = rules_df[rules_df["section"] == clean_text(section)]

        if percent == 100: cond = "100"
        elif percent > 80: cond = ">80"
        elif percent > 50: cond = ">50"
        else: cond = "<50"

        matched = section_rules[section_rules["condition"] == cond]

        st.subheader("Area of Improvements")
        for _,r in matched.iterrows():
            st.write(format_text(r["areas_of_improvements"]))

        st.subheader("Action Plan")
        for _,r in matched.iterrows():
            st.write(format_text(r["action_plan"]))

    if st.button("⬅️ Back to Dashboard"):
        st.session_state.view_details_section = None