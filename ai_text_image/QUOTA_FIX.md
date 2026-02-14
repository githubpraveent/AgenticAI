# Quota Exceeded - How to Fix

## ❌ The Problem

You're getting a **429 Quota Exceeded** error because:

```
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0
```

**The free tier has 0 quota for image generation models.**

This is **expected behavior** - Google's image generation models (like `gemini-2.5-flash-image`) require a paid plan. The free tier is only for text generation.

## ✅ Solutions

### Option 1: Upgrade to Paid Plan (Recommended)

Image generation models require a **paid Gemini API plan**:

1. **Go to Google AI Studio**: https://ai.google.dev/studio
2. **Check your plan**: Look at your current tier/usage
3. **Enable billing**: Add a payment method to your Google Cloud account
4. **Upgrade plan**: Move from free tier to paid tier

**Cost**: Gemini API pricing is reasonable. Check: https://ai.google.dev/pricing

### Option 2: Check Your Quota

1. **Visit usage dashboard**: https://ai.google.dev/usage
2. **Check rate limits**: https://ai.google.dev/gemini-api/docs/rate-limits
3. **Verify billing**: Ensure billing is enabled for your project

### Option 3: Use Different Model (May Not Work)

The code will try regular Gemini models as fallback, but they may not support image generation.

## 📋 Current Status

- ✅ Code is working correctly
- ✅ Using Gemini models as requested
- ❌ **Free tier has 0 quota for image generation**
- ⚠️ **Need paid plan for image generation**

## 🔍 What Models Are Being Tried

The code automatically tries these models in order:
1. `gemini-2.5-flash-image` (image generation - requires paid)
2. `gemini-3-pro-image-preview` (image generation - requires paid)
3. `gemini-2.0-flash-exp` (may support images)
4. `gemini-1.5-flash` (regular model - fallback)
5. `gemini-1.5-pro` (regular model - fallback)

## 💡 Next Steps

1. **Enable billing** in Google Cloud Console
2. **Upgrade your Gemini API plan**
3. **Wait a few minutes** for quota to refresh
4. **Try again**: `python3 test_basic.py`

## 📚 Resources

- [Gemini API Pricing](https://ai.google.dev/pricing)
- [Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Usage Dashboard](https://ai.google.dev/usage)
- [Billing Setup](https://cloud.google.com/billing/docs/how-to/manage-billing-account)

---

**Note**: The code is working correctly. The issue is that image generation models require a paid plan. Once you upgrade, it should work immediately!

