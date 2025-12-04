# Finance Request Auto-Processor Agent

This repository contains an automated GitHub Action that processes finance requests from issues.

## How It Works

The agent automatically triggers when:
- A new issue is created and contains mentions of finance team members (@anakarlarg, @richpaik, @meganwins)
- An issue is edited to add finance team mentions
- A comment is added to an issue that mentions finance team members
- A finance team member comments on an issue

When triggered, the agent:
1. **Extracts data** using GitHub Models AI to analyze the issue content
2. **Determines status** based on finance team responses (Approved/Rejected/Under Review)
3. **Saves data** to `customer_requests.csv` in the repository
4. **Comments** on the issue with the extracted information

## Setup

### 1. Configure GitHub Secrets

Add the following secret to your repository (Settings → Secrets and variables → Actions):

- **`GITHUB_MODELS_TOKEN`**: Your GitHub Personal Access Token
  - Get from: https://github.com/settings/tokens
  - Select "Generate new token (classic)"
  - No special scopes required for GitHub Models API
  - The default `GITHUB_TOKEN` is used for issue commenting and repository access

### 2. Enable GitHub Actions

Ensure GitHub Actions are enabled in your repository settings.

### 3. That's It!

The agent will automatically process issues when finance team members are mentioned.

## Data Fields Extracted

### Required Fields (AI-extracted)
- **Customer Name**: Company or organization referenced in the issue
- **Date**: When finance team was first mentioned
- **Status**: Approved, Rejected, or Under Review
- **Link to Issue**: URL to the GitHub issue
- **Type of request**: Discount, move to metered, both, etc.
- **Description**: 1-2 sentence summary

### Optional Fields (Available for manual update)
- MACC
- Date move takes place
- Length of Original Deal
- Year of deal transition
- Years remaining in deal
- ARR of GHE metered
- ARR of GHE License
- ARR of GHAS metered
- ARR of GHAS License

## Finance Team

The agent recognizes these finance team members:
- @anakarlarg
- @richpaik
- @meganwins

## Status Detection

The agent automatically determines status based on finance team activity:
- **Approved**: Finance team member comments "approved" on the issue
- **Rejected**: Finance team member comments "rejected" on the issue  
- **Under Review**: Default status when no approval/rejection is found

## Output

All processed requests are saved to:
- **`customer_requests.csv`**: CSV file in the repository root
- **Issue comment**: Summary posted back to the original issue

## Example Workflow

1. User creates an issue with title "Request for Acme Corp discount"
2. User mentions @anakarlarg in the issue body
3. Agent automatically triggers
4. AI extracts:
   - Customer Name: "Acme Corp"
   - Type: "discount"
   - Description: "Request for discount pricing"
5. Agent saves to CSV and comments on issue
6. Finance team reviews and comments "approved"
7. Agent updates status to "Approved" in CSV

## Benefits

- ✅ **Fully automated** - No manual data entry required
- ✅ **Free AI processing** - Uses GitHub Models API (free tier)
- ✅ **Instant processing** - Triggers within seconds of issue activity
- ✅ **Audit trail** - All data linked to original GitHub issues
- ✅ **Version controlled** - CSV data tracked in git history

## Technical Details

- **Workflow**: `.github/workflows/process-finance-request.yml`
- **Script**: `.github/scripts/process_finance_request.py`
- **Triggers**: Issue creation, editing, and commenting
- **AI Model**: GPT-4o via GitHub Models API
- **Output Format**: CSV file committed to repository

## Troubleshooting

### Agent doesn't trigger
- Ensure finance team member is mentioned with @ symbol
- Check that GitHub Actions are enabled
- Verify `GITHUB_MODELS_TOKEN` secret is set

### AI extraction fails
- Check that `GITHUB_MODELS_TOKEN` is valid
- Verify you haven't exceeded daily rate limit (50-150 requests/day)
- Check Actions logs for detailed error messages

### Status not updating
- Finance team must comment with exact words "approved" or "rejected"
- Comments must come from recognized finance team accounts

## Migration from Web App

This automated agent replaces the previous Streamlit web application. Key differences:

| Feature | Web App | Automated Agent |
|---------|---------|-----------------|
| **Trigger** | Manual button click | Automatic on issue activity |
| **Access** | Need to open app | Works in background |
| **Data Entry** | Manual review/edit | Automatic extraction |
| **Output** | Excel file | CSV in repository |
| **Cost** | Free (GitHub Models) | Free (GitHub Models) |

## License

This project is provided as-is for internal use.
