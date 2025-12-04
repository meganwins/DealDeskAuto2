# Enterprise Finance Request Auto-Processor

An automated GitHub Action agent that extracts and processes enterprise finance requests from GitHub issues using AI-powered analysis.

> 🤖 **This is now an automated agent!** Previously a Streamlit web app, this has been converted to a fully automated GitHub Action that processes issues automatically when finance team members are mentioned.

## Features

- **Fully Automated**: Automatically processes issues when finance team is mentioned
- **AI-Powered Extraction**: Uses GitHub Models API (free tier) for intelligent data extraction
- **Auto-Detection**: Detects finance team involvement and determines approval status
- **CSV Export**: Automatically saves data to version-controlled CSV file
- **Issue Comments**: Posts extracted data back to the issue for visibility

## Quick Start

### For Repository Admins

1. **Add GitHub Secret**:
   - Go to Settings → Secrets and variables → Actions
   - Add secret: `GITHUB_MODELS_TOKEN` with your GitHub Personal Access Token
   - Get token from: https://github.com/settings/tokens (no special scopes needed)

2. **That's it!** The agent will automatically activate.

### For Users (Creating Finance Requests)

1. **Create an issue** in this repository
2. **Mention a finance team member** in the issue body or comments:
   - @anakarlarg
   - @richpaik  
   - @meganwins
3. **Wait a few seconds** - The agent will automatically:
   - Extract customer name, request type, and description
   - Save data to `customer_requests.csv`
   - Comment on your issue with the extracted data

### For Finance Team (Approving/Rejecting)

1. **Comment on the issue** with:
   - "approved" to mark as Approved
   - "rejected" to mark as Rejected
2. The agent will automatically update the status in the CSV

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  User creates issue and mentions @finance-team-member       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub Action triggers automatically                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  AI extracts data using GitHub Models API (GPT-4o)          │
│  • Customer Name                                             │
│  • Request Type                                              │
│  • Description                                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Agent determines status from finance team comments         │
│  • Approved / Rejected / Under Review                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Data saved to customer_requests.csv in repository          │
│  Comment posted to issue with extracted data                │
└─────────────────────────────────────────────────────────────┘
```

## Data Fields

### Automatically Extracted by AI
- **Customer Name**: Company or organization referenced in the issue
- **Date (request to finance)**: When finance team was first mentioned
- **Status**: Approved, Rejected, or Under Review (based on finance comments)
- **Link to Issue**: URL to the GitHub issue
- **Type of request**: Discount, move to metered, both, etc.
- **Description / Summary**: AI-generated 1-2 sentence summary

### Available for Manual Update (in CSV)
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

The application recognizes the following finance team members:
- @anakarlarg
- @richpaik
- @meganwins

## Output

Data is automatically saved to **`customer_requests.csv`** in the repository root, with each issue processed as a new row. The CSV file is version-controlled so you can track all changes over time.

Additionally, the agent posts a comment on each processed issue showing the extracted data.

## Troubleshooting

### Agent doesn't run automatically

- Ensure you've added `GITHUB_MODELS_TOKEN` secret in repository settings
- Check that GitHub Actions are enabled for the repository
- Verify finance team member is mentioned with @ symbol (e.g., @meganwins)
- Check the Actions tab for workflow run logs

### "GitHub Models extraction failed"

- Verify your `GITHUB_MODELS_TOKEN` is valid and not expired
- Check that you haven't exceeded the daily rate limit (50-150 requests/day)
- Check the Actions workflow logs for detailed error messages

### Status not updating correctly

- Finance team must comment with the exact words "approved" or "rejected"
- Comments must come from recognized finance team member accounts (@anakarlarg, @richpaik, @meganwins)
- Status defaults to "Under Review" if no approval/rejection is found

### CSV file not updating

- Check the Actions tab to see if the workflow ran successfully
- Verify the workflow has write permissions to the repository
- Check for errors in the workflow logs

## Legacy Web Application

The previous Streamlit web application (`app.py`) is still available in the repository but is no longer the primary method. The automated agent is now the recommended approach.

To use the old web app:
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.streamlit/secrets.toml` (see `.streamlit/secrets.toml.template`)
3. Run: `streamlit run app.py`

## Migration to Automated Agent

**Why automated?**
- ✅ No manual intervention required
- ✅ Processes issues instantly when finance team is mentioned
- ✅ Data saved automatically to version-controlled CSV
- ✅ Transparent - all processing visible in issue comments
- ✅ Same free GitHub Models API for AI processing

## License

This project is provided as-is for internal use.
