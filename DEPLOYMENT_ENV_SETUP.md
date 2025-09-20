# Environment Variables for Deployment

## Required Environment Variables

When deploying to Vercel, you MUST add these environment variables in your Vercel dashboard:

### Supabase Configuration
```
NEXT_PUBLIC_SUPABASE_URL=https://yejyxznoddkegbqzpuex.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inllanl4em5vZGRrZWdicXpwdWV4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3MzM1ODUsImV4cCI6MjA3MTMwOTU4NX0.NvZYKHzFRHuGCw37NTwFrP_CxABiBLka01IPFwuWLQY
```

## How to Add Environment Variables in Vercel:

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable:
   - Name: `NEXT_PUBLIC_SUPABASE_URL`
   - Value: `https://yejyxznoddkegbqzpuex.supabase.co`
   - Environment: Production, Preview, Development

   - Name: `NEXT_PUBLIC_SUPABASE_ANON_KEY` 
   - Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inllanl4em5vZGRrZWdicXpwdWV4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3MzM1ODUsImV4cCI6MjA3MTMwOTU4NX0.NvZYKHzFRHuGCw37NTwFrP_CxABiBLka01IPFwuWLQY`
   - Environment: Production, Preview, Development

5. Redeploy your project

## Security Notes:

- ✅ **SAFE**: The anon key is public-facing and designed to be exposed in frontend code
- ✅ **SECURE**: No sensitive credentials are hardcoded in the repository
- ✅ **PROPER**: Using environment variables for deployment
- ⚠️ **IMPORTANT**: Never commit your service role key to the repository

## Local Development:

Create a `.env.local` file in the frontend directory with the same variables for local testing.
