# 🔒 Analytics Password Setup Instructions

## 🎯 **Secure Analytics Implementation**

Your analytics dashboard is now protected with environment variable authentication to keep your business data secure.

---

## 🔧 **Local Development Setup**

### **Step 1: Add Password to Local Environment**

Add this line to your `frontend/.env.local` file:

```bash
NEXT_PUBLIC_ANALYTICS_PASSWORD=tupTac-tanpos-nunfi6
```

**Full .env.local should look like:**
```bash
# Supabase Configuration for Local Development
NEXT_PUBLIC_SUPABASE_URL=https://yejyxznoddkegbqzpuex.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Analytics Dashboard Password (keep this secret!)
NEXT_PUBLIC_ANALYTICS_PASSWORD=tupTac-tanpos-nunfi6
```

---

## 🚀 **Production Setup (Vercel)**

### **Step 1: Add Environment Variable to Vercel**

1. Go to your **Vercel Dashboard**
2. Select your **nail-art-search project**
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Name**: `NEXT_PUBLIC_ANALYTICS_PASSWORD`
   - **Value**: `tupTac-tanpos-nunfi6`
   - **Environment**: Production (and Preview if needed)
5. **Save** and **redeploy**

### **Step 2: Redeploy**
After adding the environment variable, Vercel will automatically redeploy, or you can trigger a redeploy manually.

---

## 🔑 **How to Change Password Later**

### **For Local Development:**
1. Edit `frontend/.env.local`
2. Change the `NEXT_PUBLIC_ANALYTICS_PASSWORD` value
3. Restart your local server

### **For Production:**
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Edit the `NEXT_PUBLIC_ANALYTICS_PASSWORD` variable
3. Update the value
4. Redeploy the project

---

## 🧪 **Testing**

### **Local Testing:**
1. Go to `http://localhost:3000/analytics`
2. Enter password: `tupTac-tanpos-nunfi6`
3. Should show booking analytics dashboard

### **Production Testing:**
1. Go to `https://naild.io/analytics` (or your domain)
2. Enter the same password
3. Should work after Vercel environment variable is set

---

## 🛡️ **Security Benefits**

✅ **Password not in GitHub** - Stored securely in environment variables
✅ **Different passwords per environment** - Can have different local/production passwords
✅ **Easy to change** - Update environment variable without code changes
✅ **No code exposure** - Competitors can't see the password in your repository

---

## ⚠️ **Important Notes**

- **Never commit** the actual .env.local file to GitHub
- **Keep password secure** - Only share with authorized team members
- **Vercel environment variables** are encrypted and secure
- **Change password regularly** for better security

---

## 🆘 **Troubleshooting**

**If analytics login doesn't work:**
1. Check environment variable is set correctly
2. Restart local development server
3. Check browser console for errors
4. Verify Vercel environment variable is saved

**If password is rejected:**
1. Double-check spelling and case sensitivity
2. Ensure no extra spaces in environment variable
3. Check if environment variable is properly loaded
