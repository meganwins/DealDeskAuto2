# Quick Setup Checklist

Follow these steps to activate the automated agent:

## ✅ Setup Steps

### Step 1: Get GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a name (e.g., "Finance Request Agent")
4. **No scopes need to be selected** (Models API doesn't require special scopes)
5. Click **"Generate token"**
6. **Copy the token** (starts with `ghp_`)

### Step 2: Add Secret to Repository

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **"New repository secret"**
5. Name: `GITHUB_MODELS_TOKEN`
6. Value: Paste your token from Step 1
7. Click **"Add secret"**

### Step 3: Test the Agent

1. Create a new issue in your repository
2. In the issue body, mention a finance team member:
   - `@anakarlarg` or
   - `@richpaik` or
   - `@meganwins`
3. Wait 20-40 seconds
4. Check the **Actions** tab - you should see the workflow running
5. Check the issue - the bot should comment with extracted data
6. Check the repository - `customer_requests.csv` should be updated

## ✅ Verification

After setup, you should see:

- ✅ Secret `GITHUB_MODELS_TOKEN` in repository settings
- ✅ Workflow file `.github/workflows/process-finance-request.yml` in repository
- ✅ Script file `.github/scripts/process_finance_request.py` in repository
- ✅ When you create an issue with finance mention:
  - ✅ Workflow runs in Actions tab
  - ✅ Bot comments on issue
  - ✅ CSV file is updated and committed

## 🚀 You're Done!

The agent will now automatically process all finance requests when issues are created or when finance team members are mentioned.

## 📚 Additional Resources

- **AGENT_README.md** - Full documentation
- **AGENT_GUIDE.md** - Visual walkthrough
- **ARCHITECTURE_AGENT.md** - Technical details
- **README.md** - Overview

## ❓ Troubleshooting

### Agent doesn't run
- Check that secret `GITHUB_MODELS_TOKEN` is added correctly
- Verify GitHub Actions are enabled (Settings → Actions → General)
- Make sure you mentioned finance team with @ symbol

### AI extraction fails
- Verify your token hasn't expired
- Check you haven't exceeded rate limit (50-150 requests/day)
- Check Actions logs for error details

### CSV not updating
- Check Actions tab for workflow status
- Verify workflow has write permissions
- Look for error messages in workflow logs

## 💡 Tips

- Finance team can approve/reject by commenting "approved" or "rejected"
- All processing is visible in issue comments
- CSV file is version-controlled - view history with `git log customer_requests.csv`
- Each issue is only processed once (unless finance team comments)

---

**Ready to go?** Just add the `GITHUB_MODELS_TOKEN` secret and you're all set! 🎉
