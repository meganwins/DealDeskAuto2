# Architecture Comparison

## Before: Using OpenAI API (Paid)

```
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit App (app.py)                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  User pastes GitHub Issue URL                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  GitHub App Authentication                                │   │
│  │  (Uses: GITHUB_APP_ID, GITHUB_INSTALLATION_ID,           │   │
│  │         GITHUB_PRIVATE_KEY)                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Fetch Issue Data from GitHub                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  OpenAI API Call ❌ (PAID)                                │   │
│  │  • API: api.openai.com                                    │   │
│  │  • Key: OPENAI_API_KEY                                    │   │
│  │  • Model: gpt-4                                            │   │
│  │  • Cost: $$ (requires credits)                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Extract & Display Data → Save to Excel                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## After: Using GitHub Models API (FREE)

```
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit App (app.py)                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  User pastes GitHub Issue URL                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  GitHub App Authentication                                │   │
│  │  (Uses: GITHUB_APP_ID, GITHUB_INSTALLATION_ID,           │   │
│  │         GITHUB_PRIVATE_KEY)                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Fetch Issue Data from GitHub                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  GitHub Models API Call ✅ (FREE)                         │   │
│  │  • API: models.inference.ai.azure.com                     │   │
│  │  • Key: GITHUB_TOKEN (GitHub PAT)                         │   │
│  │  • Model: gpt-4o                                           │   │
│  │  • Cost: FREE (50-150 requests/day)                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Extract & Display Data → Save to Excel                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Key Differences

| Aspect | Before (OpenAI) | After (GitHub Models) |
|--------|-----------------|----------------------|
| **Cost** | Paid (requires credits) | **FREE** |
| **API Endpoint** | `api.openai.com` | `models.inference.ai.azure.com` |
| **Authentication** | OpenAI API Key | GitHub Personal Access Token |
| **Model** | `gpt-4` | `gpt-4o` |
| **Rate Limit** | Based on paid tier | 50-150 requests/day |
| **Setup Complexity** | Requires OpenAI account & billing | Just need GitHub account |
| **Code Changes** | N/A | **Minimal** (3 lines changed) |

## What Stayed the Same

✅ GitHub App authentication (unchanged)  
✅ Issue data fetching (unchanged)  
✅ Data extraction logic (unchanged)  
✅ Excel export functionality (unchanged)  
✅ UI/UX (unchanged)  
✅ All features work identically  

## Code Change Summary

Only **3 key changes** in `app.py`:

1. **Line 17:** `OPENAI_API_KEY` → `GITHUB_TOKEN`
2. **Lines 136-139:** Added `base_url="https://models.inference.ai.azure.com"`
3. **Line 142:** `model="gpt-4"` → `model="gpt-4o"`

Everything else remains the same!
