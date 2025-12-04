#!/usr/bin/env python3
"""
Automated GitHub Action to process finance requests from issues.
Extracts data using GitHub Models API and saves to CSV.
"""

import os
import sys
import json
import re
from datetime import datetime
import requests
import pandas as pd
from openai import OpenAI

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_MODELS_TOKEN = os.environ.get('GITHUB_MODELS_TOKEN', GITHUB_TOKEN)
ISSUE_NUMBER = os.environ.get('ISSUE_NUMBER')
ISSUE_TITLE = os.environ.get('ISSUE_TITLE', '')
ISSUE_BODY = os.environ.get('ISSUE_BODY', '')
ISSUE_URL = os.environ.get('ISSUE_URL', '')
ISSUE_LABELS = os.environ.get('ISSUE_LABELS', '[]')
ISSUE_CREATED_AT = os.environ.get('ISSUE_CREATED_AT', '')
COMMENT_BODY = os.environ.get('COMMENT_BODY', '')
COMMENT_CREATED_AT = os.environ.get('COMMENT_CREATED_AT', '')
COMMENT_USER = os.environ.get('COMMENT_USER', '')
REPOSITORY = os.environ.get('REPOSITORY', '')

FINANCE_TAGS = ["@anakarlarg", "@richpaik", "@meganwins"]
FINANCE_USERS = ["anakarlarg", "richpaik", "meganwins"]

CSV_FILE = "customer_requests.csv"

def should_process_issue():
    """Determine if this issue should be processed."""
    # Check if it's a new issue or if finance team is mentioned
    if COMMENT_BODY:
        # Check if finance team member was mentioned in comment
        for tag in FINANCE_TAGS:
            if tag.lower() in COMMENT_BODY.lower():
                return True
        # Check if comment is from finance team
        if COMMENT_USER.lower() in FINANCE_USERS:
            return True
        return False
    else:
        # New issue or edited issue - check if finance team is mentioned in body
        if ISSUE_BODY:
            for tag in FINANCE_TAGS:
                if tag.lower() in ISSUE_BODY.lower():
                    return True
    return False

def get_issue_comments():
    """Fetch all comments for the current issue."""
    if not REPOSITORY or not ISSUE_NUMBER:
        return []
    
    api_url = f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching comments: {e}")
    
    return []

def extract_finance_date():
    """Extract the date when finance team was first involved."""
    # Check issue body first
    if ISSUE_BODY:
        for tag in FINANCE_TAGS:
            if tag.lower() in ISSUE_BODY.lower():
                if ISSUE_CREATED_AT:
                    try:
                        return datetime.strptime(ISSUE_CREATED_AT, "%Y-%m-%dT%H:%M:%SZ").date()
                    except:
                        pass
    
    # Check comments
    comments = get_issue_comments()
    for comment in comments:
        text = comment.get("body", "").lower()
        for tag in FINANCE_TAGS:
            if tag.lower() in text:
                try:
                    return datetime.strptime(comment["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
                except:
                    pass
    
    # Default to today
    return datetime.now().date()

def extract_status_by_finance():
    """Extract status based on finance team involvement."""
    # Check issue body
    if ISSUE_BODY:
        body_lower = ISSUE_BODY.lower()
        # Check if author is finance team
        # (Note: We don't have issue author in env, so we'll check comments)
        if "approved" in body_lower:
            for user in FINANCE_USERS:
                # Simplified check - in real scenario we'd check issue author
                if "approved" in body_lower:
                    return "Approved"
        elif "rejected" in body_lower:
            for user in FINANCE_USERS:
                if "rejected" in body_lower:
                    return "Rejected"
    
    # Check comments
    comments = get_issue_comments()
    for comment in comments:
        commenter = comment.get('user', {}).get('login', '').lower()
        text = comment.get('body', '').lower()
        
        if commenter in FINANCE_USERS:
            if "approved" in text:
                return "Approved"
            elif "rejected" in text:
                return "Rejected"
    
    return "Under Review"

def summarize_and_extract():
    """Use GitHub Models API to extract structured data from issue."""
    try:
        labels = json.loads(ISSUE_LABELS)
        label_names = [l.get('name', '') for l in labels]
    except:
        label_names = []
    
    prompt = f"""
    You are helping fill out an enterprise request tracking spreadsheet. 
    Issue Title: {ISSUE_TITLE}
    Issue Body: {ISSUE_BODY}
    Labels: {', '.join(label_names)}
    
    Please extract or infer, in JSON, the following fields:
    - Customer Name (company or org referenced)
    - Status (must be one of: Approved, Rejected, Under Review)
    - Type of request (discount, move to metered, both, etc.)
    - Description / Summary (1-2 sentence summary)
    
    Use what you find, don't invent facts. Leave blank any field if not clear.
    Return ONLY valid JSON.
    """
    
    try:
        client = OpenAI(
            api_key=GITHUB_MODELS_TOKEN,
            base_url="https://models.inference.ai.azure.com"
        )
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        # Remove markdown code fences if present
        content = re.sub(r"^```json\s*|\s*```$", "", content, flags=re.MULTILINE).strip()
        
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"GitHub Models extraction failed: {e}")
        return {}

def post_comment_to_issue(message):
    """Post a comment to the issue with extracted data."""
    if not REPOSITORY or not ISSUE_NUMBER:
        return
    
    api_url = f"https://api.github.com/repos/{REPOSITORY}/issues/{ISSUE_NUMBER}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    payload = {"body": message}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 201:
            print("Comment posted successfully")
        else:
            print(f"Failed to post comment: {response.status_code}")
    except Exception as e:
        print(f"Error posting comment: {e}")

def save_to_csv(data):
    """Save extracted data to CSV file."""
    # Load existing CSV or create new
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame()
    
    # Create new row
    new_row = pd.DataFrame([data])
    
    # Append and save
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    print(f"Data saved to {CSV_FILE}")

def main():
    """Main processing logic."""
    print("=" * 60)
    print("Finance Request Auto-Processor")
    print("=" * 60)
    
    # Check if we should process this issue
    if not should_process_issue():
        print("Issue does not require processing (no finance team involvement)")
        return
    
    print(f"Processing issue #{ISSUE_NUMBER}")
    print(f"Title: {ISSUE_TITLE}")
    
    # Extract data using AI
    print("Extracting data using GitHub Models API...")
    extracted = summarize_and_extract()
    
    # Get additional data
    finance_date = extract_finance_date()
    status = extract_status_by_finance()
    
    # Build complete record
    record = {
        "Customer Name": extracted.get("Customer Name", ""),
        "Date (request to finance)": finance_date.strftime("%Y-%m-%d") if finance_date else "",
        "Status": status,
        "Link to Issue": ISSUE_URL,
        "Type of request": extracted.get("Type of request", ""),
        "Description / Summary": extracted.get("Description / Summary", ""),
        "MACC": "",
        "Date move takes place": "",
        "Length of Original Deal": "",
        "Year of deal transition": "",
        "Years remaining in deal": "",
        "ARR of GHE metered": "",
        "ARR of GHE License": "",
        "ARR of GHAS metered": "",
        "ARR of GHAS License": "",
    }
    
    # Save to CSV
    save_to_csv(record)
    
    # Post comment to issue
    comment = f"""## 🤖 Finance Request Processed

The following data has been automatically extracted and saved:

- **Customer Name:** {record['Customer Name']}
- **Date:** {record['Date (request to finance)']}
- **Status:** {record['Status']}
- **Type of Request:** {record['Type of request']}
- **Description:** {record['Description / Summary']}

Data has been saved to `customer_requests.csv` in the repository.

_This is an automated message from the Finance Request Processor agent._
"""
    
    post_comment_to_issue(comment)
    
    print("=" * 60)
    print("Processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
