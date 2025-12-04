import streamlit as st
import requests
import openai
import pandas as pd
import re
import os
from datetime import datetime

st.write("DEBUG: App is running!")  # This should appear on EVERY successful load!

# ---- CONFIGURATION ----
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"] if "GITHUB_TOKEN" in st.secrets else "your_github_token"
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your_openai_api_key"
EXCEL_FILE = "customer_requests.xlsx"

# Map of tag to username
FINANCE_TAGS = {
    "@anakarlarg": "anakarlarg",
    "@richpaik": "richpaik",
    "@meganwins": "meganwins"
}
FINANCE_TAG_LIST = list(FINANCE_TAGS.keys())

# ---- UTILITY ----

def parse_github_issue_url(issue_url):
    """
    Accepts a URL with or without #issuecomment-...
    Returns (owner, repo, number) if valid, else None.
    """
    # Remove anchor if present
    url = issue_url.split('#')[0]
    pattern = r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/issues/(?P<number>\d+)"
    match = re.match(pattern, url)
    if not match:
        return None
    return match.group("owner"), match.group("repo"), match.group("number")

def get_issue_data(issue_url):
    parsed = parse_github_issue_url(issue_url)
    if not parsed:
        st.error("Invalid GitHub issue URL format. Please paste a full issue URL, e.g. https://github.com/org/repo/issues/123")
        return None, None
    owner, repo, number = parsed

    base_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{number}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    issue_resp = requests.get(base_url, headers=headers)
    if issue_resp.status_code != 200:
        st.error(f"Could not fetch the issue from GitHub. Error {issue_resp.status_code}: {issue_resp.text}")
        return None, None
    issue = issue_resp.json()

    comments_url = issue['comments_url']
    comments_resp = requests.get(comments_url, headers=headers)
    comments = comments_resp.json() if comments_resp.status_code == 200 else []

    return issue, comments

def extract_finance_date(issue, comments):
    # Scan issue body first
    if issue and issue.get("body"):
        for tag in FINANCE_TAG_LIST:
            if tag.lower() in issue["body"].lower():
                return datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
    # Scan comments for tags
    for comment in comments:
        text = comment.get("body", "").lower()
        for tag in FINANCE_TAG_LIST:
            if tag.lower() in text:
                return datetime.strptime(comment["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
    return None  # Editable by user

def summarize_and_extract(issue):
    prompt = f"""
    You are helping fill out an enterprise request tracking spreadsheet.
    Issue Title: {issue['title']}
    Issue Body: {issue.get('body','')}
    Labels: {', '.join([l['name'] for l in issue.get('labels',[])])}
    
    Please extract or infer, in JSON, the following fields:
    - Customer Name (company or org referenced)
    - Status (must be one of: Approved, Rejected, Under Review)
    - Type of request (discount, move to metered, both, etc.)
    - Description / Summary (1-2 sentence summary)
    
    Use what you find, don't invent facts. Leave blank any field if not clear.
    """
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response['choices'][0]['message']['content']
        content = re.sub(r"^```json|```$", "", content).strip()
        data = {}
        try:
            import json
            data = json.loads(content)
        except Exception:
            try:
                data = eval(content)
            except Exception:
                data = {}
        return data
    except Exception as e:
        st.warning(f"OpenAI extraction failed: {e}")
        return {}

def extract_status_by_finance(issue, comments):
    # Same as original
    author_login = issue.get('user', {}).get('login', '').lower()
    body = issue.get('body', '').lower() if issue.get('body') else ""
    status = None

    if author_login in FINANCE_TAGS.values():
        if "approved" in body:
            status = "Approved"
        elif "rejected" in body:
            status = "Rejected"

    if not status:
        for comment in comments:
            commenter_login = comment.get('user', {}).get('login', '').lower()
            text = comment.get('body', '').lower()
            if commenter_login in FINANCE_TAGS.values():
                if "approved" in text:
                    status = "Approved"
                    break
                elif "rejected" in text:
                    status = "Rejected"
                    break
    if not status:
        status = "Under Review"
    return status

def append_to_excel(row, excel_file):
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
    else:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(excel_file, index=False)

# ---- UI ----
st.title("Enterprise Finance Request Extractor")

issue_url = st.text_input("Paste GitHub Issue URL (e.g. https://github.com/org/repo/issues/123):")

if issue_url:
    if st.button("Process and Extract"):
        issue, comments = get_issue_data(issue_url)
        if issue:
            extracted = summarize_and_extract(issue)
            finance_date = extract_finance_date(issue, comments)

            # NEW: Use status based on finance involvement
            status = extract_status_by_finance(issue, comments)
            st.subheader("Review and Edit Extracted Data")

            with st.form("edit_form"):
                customer_name = st.text_input("Customer Name*", extracted.get("Customer Name",""))
                if finance_date:
                    date_finance = st.date_input("Date (request to finance)*", value=finance_date)
                else:
                    date_finance = st.date_input("Date (request to finance)*")
                status_options = ["Approved", "Rejected", "Under Review"]
                status_index = status_options.index(status) if status in status_options else 2
                status = st.selectbox("Status*", status_options, index=status_index)
                link_to_issue = st.text_input("Link to Issue*", issue_url)
                request_type = st.text_input("Type of request*", extracted.get("Type of request",""))
                description = st.text_area("Description / Summary*", extracted.get("Description / Summary",""))

                # Optional fields
                macc = st.text_input("MACC")
                date_move = st.text_input("Date move takes place")
                length_deal = st.text_input("Length of Original Deal")
                year_transition = st.text_input("Year of deal transition")
                years_remaining = st.text_input("Years remaining in deal")
                arr_ghe_metered = st.text_input("ARR of GHE metered")
                arr_ghe_license = st.text_input("ARR of GHE License")
                arr_ghas_metered = st.text_input("ARR of GHAS metered")
                arr_ghas_license = st.text_input("ARR of GHAS License")

                submitted = st.form_submit_button("Save to Excel")

                required_fields = [customer_name, date_finance, status, link_to_issue, request_type, description]
                if submitted:
                    if all(required_fields) and date_finance is not None:
                        row = {
                            "Customer Name": customer_name,
                            "Date (request to finance)": date_finance,
                            "Status": status,
                            "Link to Issue": link_to_issue,
                            "Type of request": request_type,
                            "Description / Summary": description,
                            "MACC": macc,
                            "Date move takes place": date_move,
                            "Length of Original Deal": length_deal,
                            "Year of deal transition": year_transition,
                            "Years remaining in deal": years_remaining,
                            "ARR of GHE metered": arr_ghe_metered,
                            "ARR of GHE License": arr_ghe_license,
                            "ARR of GHAS metered": arr_ghas_metered,
                            "ARR of GHAS License": arr_ghas_license,
                        }
                        append_to_excel(row, EXCEL_FILE)
                        st.success("Row added to Excel!")
                    else:
                        st.error("Please fill in all required fields (marked with *).")

def append_to_excel(row, excel_file):
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
    else:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(excel_file, index=False)

# ---- UI ----
st.title("Enterprise Finance Request Extractor")

issue_url = st.text_input("Paste GitHub Issue URL (e.g. https://github.com/org/repo/issues/123):")

if issue_url:
    if st.button("Process and Extract"):
        issue, comments = get_issue_data(issue_url)
        if issue:
            extracted = summarize_and_extract(issue)
            finance_date = extract_finance_date(issue, comments)

            # NEW: Use status based on finance involvement
            status = extract_status_by_finance(issue, comments)
            st.subheader("Review and Edit Extracted Data")

            with st.form("edit_form"):
                customer_name = st.text_input("Customer Name*", extracted.get("Customer Name",""))
                if finance_date:
                    date_finance = st.date_input("Date (request to finance)*", value=finance_date)
                else:
                    date_finance = st.date_input("Date (request to finance)*")
                status_options = ["Approved", "Rejected", "Under Review"]
                status_index = status_options.index(status) if status in status_options else 2
                status = st.selectbox("Status*", status_options, index=status_index)
                link_to_issue = st.text_input("Link to Issue*", issue_url)
                request_type = st.text_input("Type of request*", extracted.get("Type of request",""))
                description = st.text_area("Description / Summary*", extracted.get("Description / Summary",""))

                # Optional fields
                macc = st.text_input("MACC")
                date_move = st.text_input("Date move takes place")
                length_deal = st.text_input("Length of Original Deal")
                year_transition = st.text_input("Year of deal transition")
                years_remaining = st.text_input("Years remaining in deal")
                arr_ghe_metered = st.text_input("ARR of GHE metered")
                arr_ghe_license = st.text_input("ARR of GHE License")
                arr_ghas_metered = st.text_input("ARR of GHAS metered")
                arr_ghas_license = st.text_input("ARR of GHAS License")

                submitted = st.form_submit_button("Save to Excel")

                required_fields = [customer_name, date_finance, status, link_to_issue, request_type, description]
                if submitted:
                    # Extra check: date must be selected by user if not auto-filled
                    if all(required_fields) and date_finance is not None:
                        row = {
                            "Customer Name": customer_name,
                            "Date (request to finance)": date_finance,
                            "Status": status,
                            "Link to Issue": link_to_issue,
                            "Type of request": request_type,
                            "Description / Summary": description,
                            "MACC": macc,
                            "Date move takes place": date_move,
                            "Length of Original Deal": length_deal,
                            "Year of deal transition": year_transition,
                            "Years remaining in deal": years_remaining,
                            "ARR of GHE metered": arr_ghe_metered,
                            "ARR of GHE License": arr_ghe_license,
                            "ARR of GHAS metered": arr_ghas_metered,
                            "ARR of GHAS License": arr_ghas_license,
                        }
                        append_to_excel(row, EXCEL_FILE)
                        st.success("Row added to Excel!")
                    else:
                        st.error("Please fill in all required fields (marked with *).")
                        