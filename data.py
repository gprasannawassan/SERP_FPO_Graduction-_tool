import pandas as pd

# ==============================
# LOAD RESPONSE DATA
# ==============================
file_path = "FPO_Dashboard.xlsx"

response_df = pd.read_excel(file_path, sheet_name="Response")

# Clean column names
response_df.columns = response_df.columns.str.strip().str.lower()

# ==============================
# MASTER COLUMN LIST
# ==============================
master_columns = [
    
    "fpo_registration-fpo_name",  # TEXT COLUMN
"fpo_registration-registration_certificate",
"fpo_registration-filing_regularly",
"fpo_registration-notice_non-filing_returns",
"fpo_registration-display_certificate",
"fpo_registration-bylaws_copy_available",

"fpo_membership-membership_forms_available",
"fpo_membership-membership_receipts_available",
"fpo_membership-membership_data_available",
"fpo_membership-share_certificates_issued",
"fpo_membership-share_certificates_acknowledged",
"fpo_membership-active_shareholders_50percent",

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
"strength_governanace-agm_patronage_bonus-annual_report",

# Staff
"fpo_staff_details-fpo_staff_status-staff_status_ceo",
"fpo_staff_details-fpo_staff_status-staff_status_accountant",
"fpo_staff_details-fpo_staff_status-staff_status_procurement_coordinator",
"fpo_staff_details-fpo_staff_status-staff_status_processing_incharge",
"fpo_staff_details-fpo_staff_status-staff_status_warehouse_charge",
"fpo_staff_details-fpo_staff_status-staff_status_marketing_person",
"fpo_staff_details-fpo_staff_status-others",
"fpo_staff_details-fpo_staff_status-fpo_pay_staff_salaries",

# Certificates
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
"compliance-fpo_license_certificate-licences_certificates_panchayat_municipal_approval",

# Assets
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
"fpo_assets-assets_owned_fpo-assets_others",

# Accounts
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
"fpo_accounts_financial_management-fpo_financial_compliance-financial_compliance_bank_reconciliation",

# Business lines
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
"fpo_business_lines-business_lines_others",

# Market
"market_linkages-market_channels_local_markets",
"market_linkages-market_channels_input_outlets",
"market_linkages-market_channels_fpo_partners",
"market_linkages-market_channels_corporate_buyers",
"market_linkages-market_channels_ecommerce_digital_marketing",
"market_linkages-market_channels_own_brand",

# Process
"fpo_business_processes-business_processes_planning_exercise",
"fpo_business_processes-business_processes_farm_level_data",
"fpo_business_processes-business_processes_annual_business_plan",
"fpo_business_processes-business_processes_procurement_committee"
]


# ==============================
# CREATE MASTER DF
# ==============================
master_df = pd.DataFrame(0, index=response_df.index, columns=master_columns)

# Add respondent id if exists
if "respondent_id" in response_df.columns:
    master_df["respondent_id"] = response_df["respondent_id"]

# ==============================
# HELPER FUNCTION
# ==============================
def clean_text(x):
    if pd.isna(x):
        return ""
    return str(x).strip().lower()

# ==============================
# MAPPING FUNCTION
# ==============================
def map_responses(response_df, master_df):

    for col in response_df.columns:

        # find related columns (prefix match)
        related_cols = [c for c in master_df.columns if c.startswith(col)]

        for i in response_df.index:

            response = clean_text(response_df.loc[i, col])

            if response in ["", "nan", "none"]:
                continue

            # =========================
            # ✅ TEXT COLUMN (STORE DIRECT)
            # =========================
            if col == "fpo_registration-fpo_name":
                master_df.loc[i, col] = response_df.loc[i, col]
                continue

            # =========================
            # ✅ SPECIAL RULE (NO = 1)
            # =========================
            if col == "fpo_registration-notice_non-filing_returns":
                if response in ["no", "n"]:
                    master_df.loc[i, col] = 1
                else:
                    master_df.loc[i, col] = 0
                continue

            # =========================
            # ✅ YES / NO QUESTIONS
            # =========================
            if response in ["yes", "y"]:
                if col in master_df.columns:
                    master_df.loc[i, col] = 1

            elif response in ["no", "n"]:
                if col in master_df.columns:
                    master_df.loc[i, col] = 0

            # =========================
            # ✅ MULTI-CHOICE
            # =========================
            else:
                tokens = response.replace(",", " ").split()
                tokens = list(set(tokens))

                for token in tokens:
                    for mc in related_cols:
                        if mc.endswith("_" + token):
                            master_df.loc[i, mc] = 1

    return master_df

# ==============================
# RUN MAPPING
# ==============================
master_df = map_responses(response_df, master_df)

# ==============================
# SAVE OUTPUT
# ==============================
output_file = "final_mapped_output.xlsx"
master_df.to_excel(output_file, index=False)

print("✅ Mapping Completed Successfully!")
print(f"📁 File saved as: {output_file}")