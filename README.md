# Enterprise Finance Request Extractor

A Streamlit application that extracts and processes enterprise finance requests from GitHub issues using AI-powered analysis.

## Features

- Parses GitHub issue URLs to extract request information
- Uses GitHub Models API (free tier) for AI-powered data extraction
- Authenticates with GitHub App for issue access
- Automatically detects finance team involvement
- Exports data to Excel format

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Secrets

Create a `.streamlit/secrets.toml` file with the following configuration:

```toml
# GitHub App credentials
GITHUB_APP_ID = "your_app_id"
GITHUB_INSTALLATION_ID = "your_installation_id"
GITHUB_PRIVATE_KEY = """
-----BEGIN RSA PRIVATE KEY-----
your_private_key_content_here
-----END RSA PRIVATE KEY-----
"""

# GitHub Personal Access Token for Models API
# Get this from: https://github.com/settings/tokens
# Required scope: No special scopes needed for Models API
GITHUB_TOKEN = "ghp_your_personal_access_token"
```

### 3. Getting a GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" (classic)
3. Give it a descriptive name (e.g., "DealDesk AI Models")
4. No special scopes are required for the free GitHub Models API
5. Click "Generate token"
6. Copy the token and add it to your secrets.toml

## GitHub Models API

This application uses the **free tier** of GitHub Models API instead of OpenAI. Key features:

- **No cost**: Free tier available to all GitHub users
- **OpenAI-compatible**: Uses the same OpenAI Python SDK
- **Model**: Uses `gpt-4o` (or other available models)
- **Endpoint**: `https://models.inference.ai.azure.com`
- **Rate limits**: Typically 50-150 requests/day depending on the model

For more information, see the [GitHub Models documentation](https://docs.github.com/en/github-models/quickstart).

## Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Paste a GitHub issue URL (e.g., `https://github.com/org/repo/issues/123`)
3. Click "Process and Extract"
4. Review and edit the extracted data
5. Click "Save to Excel" to export

## How It Works

1. **GitHub Authentication**: Uses GitHub App credentials to access issue data
2. **AI Extraction**: Sends issue content to GitHub Models API to extract:
   - Customer Name
   - Request Type
   - Status (Approved/Rejected/Under Review)
   - Description/Summary
3. **Finance Detection**: Automatically detects when finance team members are involved
4. **Data Export**: Saves all information to an Excel spreadsheet

## Fields

### Required Fields
- Customer Name
- Date (request to finance)
- Status
- Link to Issue
- Type of request
- Description / Summary

### Optional Fields
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

Data is saved to `customer_requests.xlsx` in the current directory.

## Troubleshooting

### "GitHub Models extraction failed"

- Verify your `GITHUB_TOKEN` is valid and not expired
- Check that you haven't exceeded the daily rate limit
- Ensure you have internet connectivity

### "Could not authenticate with GitHub App"

- Verify your `GITHUB_APP_ID`, `GITHUB_INSTALLATION_ID`, and `GITHUB_PRIVATE_KEY` are correct
- Ensure the GitHub App has access to the repository containing the issue

### "Invalid GitHub issue URL format"

- URL must be in the format: `https://github.com/owner/repo/issues/123`
- Remove any anchor tags (e.g., `#issuecomment-...`)

## License

This project is provided as-is for internal use.
