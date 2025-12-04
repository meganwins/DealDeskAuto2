# How the Automated Agent Works - Visual Guide

## 🎯 Overview

This document provides a visual walkthrough of how the automated finance request processor works.

## 📋 Step-by-Step Process

### Step 1: User Creates Issue

A user creates a new GitHub issue requesting finance approval:

```
Title: Request for Acme Corp Discount

Body:
We need approval for a 20% discount for Acme Corp on their annual contract.

They're a strategic customer looking to expand their GitHub Enterprise usage.

@anakarlarg - can you review this request?
```

### Step 2: Agent Triggers Automatically

Within seconds, the GitHub Action detects the mention of `@anakarlarg` and triggers:

```
GitHub Actions Workflow: process-finance-request.yml
Status: Running
Trigger: Issue #123 mentioned finance team member
```

### Step 3: AI Extraction

The agent uses GitHub Models API to extract structured data:

```python
# AI analyzes the issue and extracts:
{
  "Customer Name": "Acme Corp",
  "Type of request": "discount (20% on annual contract)",
  "Description / Summary": "Strategic customer requesting 20% discount for GitHub Enterprise expansion"
}
```

### Step 4: Data Saved to CSV

The agent appends a new row to `customer_requests.csv`:

```csv
Customer Name,Date (request to finance),Status,Link to Issue,Type of request,Description / Summary,...
Acme Corp,2025-12-04,Under Review,https://github.com/.../issues/123,discount (20%),"Strategic customer requesting...",,,,,,,,,
```

### Step 5: Bot Comments on Issue

The agent posts a comment back to the issue:

```markdown
## 🤖 Finance Request Processed

The following data has been automatically extracted and saved:

- **Customer Name:** Acme Corp
- **Date:** 2025-12-04
- **Status:** Under Review
- **Type of Request:** discount (20% on annual contract)
- **Description:** Strategic customer requesting 20% discount for GitHub Enterprise expansion

Data has been saved to `customer_requests.csv` in the repository.

_This is an automated message from the Finance Request Processor agent._
```

### Step 6: Finance Team Reviews and Approves

Finance team member @anakarlarg reviews and comments:

```
Looks good. Approved for Q1 2025.
```

### Step 7: Agent Updates Status

The agent detects the word "approved" from a finance team member and:
1. Re-triggers the workflow
2. Updates the CSV row to change status from "Under Review" → "Approved"
3. Comments with the status update

## 🔄 Trigger Conditions

The agent runs when:

| Event | Condition | Result |
|-------|-----------|--------|
| **New Issue** | Contains @anakarlarg, @richpaik, or @meganwins | ✅ Process and extract |
| **Issue Edited** | Finance team member added to body | ✅ Process and extract |
| **New Comment** | Contains finance team mention | ✅ Process and extract |
| **Finance Comment** | Finance team member comments | ✅ Update status |

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Issue                              │
│  Title: "Request for Acme Corp Discount"                        │
│  Body: "@anakarlarg - can you review?"                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GitHub Actions Trigger                         │
│  Event: issues.opened / issue_comment.created                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Check: Should Process?                              │
│  • Finance team mentioned? ✓                                     │
│  • Finance team commented? ✓                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            GitHub Models API (GPT-4o)                            │
│  Prompt: "Extract customer name, type, description..."          │
│  Response: {Customer: "Acme Corp", Type: "discount", ...}       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Determine Status                                    │
│  • Check for "approved" in finance comments → Approved          │
│  • Check for "rejected" in finance comments → Rejected          │
│  • Default → Under Review                                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Save to CSV                                         │
│  Append row to customer_requests.csv                             │
│  Commit and push to repository                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Comment on Issue                                    │
│  Post formatted comment with extracted data                      │
└─────────────────────────────────────────────────────────────────┘
```

## 🎬 Example Scenarios

### Scenario A: New Request

1. User creates issue: "Discount request for TechCorp - @meganwins"
2. Agent extracts: Customer = "TechCorp", Type = "discount"
3. Agent saves to CSV with status "Under Review"
4. Agent comments with extracted data
5. User sees instant feedback

### Scenario B: Finance Approval

1. Issue already exists with "Under Review" status
2. @richpaik comments: "Approved for 15% discount"
3. Agent detects "approved" from finance team member
4. Agent updates CSV status to "Approved"
5. CSV now reflects the decision

### Scenario C: Finance Rejection

1. Issue exists for a request
2. @anakarlarg comments: "Rejected - outside policy limits"
3. Agent updates status to "Rejected"
4. Requester sees clear decision in issue

## ⚙️ Configuration

### Required Secret

```yaml
Repository Settings → Secrets and variables → Actions

Name: GITHUB_MODELS_TOKEN
Value: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Workflow File Location

```
.github/
  workflows/
    process-finance-request.yml    ← GitHub Actions workflow
  scripts/
    process_finance_request.py     ← Python extraction script
```

### Output File

```
customer_requests.csv              ← Version-controlled data
```

## 🔍 Monitoring

### View Workflow Runs

1. Go to repository **Actions** tab
2. Click on "Process Finance Request" workflow
3. See all runs, their status, and logs

### Debug Workflow

Click on any workflow run to see:
- Which issue triggered it
- AI extraction results
- CSV update confirmation
- Comment posting status
- Any errors that occurred

## 🚀 Benefits

| Feature | Manual Web App | Automated Agent |
|---------|---------------|-----------------|
| **Trigger** | Click button | Automatic |
| **Speed** | Minutes | Seconds |
| **Accuracy** | Manual review | AI extraction |
| **History** | Local file | Git history |
| **Visibility** | Private | Public (in issues) |
| **Effort** | High | Zero |

## 📝 Notes

- Agent runs on GitHub's infrastructure (no cost)
- Uses free GitHub Models API for AI
- CSV file tracked in git for full audit trail
- Issue comments provide transparency
- Finance team can approve/reject with simple comments

---

_For detailed setup instructions, see `AGENT_README.md`_
