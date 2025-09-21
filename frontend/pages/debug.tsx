import { useState, useEffect } from 'react'
import Head from 'next/head'

export default function DebugPage() {
  const [envStatus, setEnvStatus] = useState<any>(null)
  const [supabaseTest, setSupabaseTest] = useState<any>(null)

  useEffect(() => {
    // Test environment variables
    setEnvStatus({
      hasSupabaseUrl: !!process.env.NEXT_PUBLIC_SUPABASE_URL,
      hasSupabaseKey: !!process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
      supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL?.substring(0, 30) + '...',
      keyLength: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY?.length || 0
    })

    // Test Supabase connection
    testSupabase()
  }, [])

  const testSupabase = async () => {
    try {
      console.log('🧪 Testing Supabase connection...')
      const response = await fetch('/api/supabase-images?limit=5')
      const data = await response.json()
      
      setSupabaseTest({
        success: response.ok,
        status: response.status,
        data: data,
        error: response.ok ? null : data.error
      })
    } catch (error) {
      setSupabaseTest({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      })
    }
  }

  const testUpload = async () => {
    try {
      // Create a small test file
      const canvas = document.createElement('canvas')
      canvas.width = 100
      canvas.height = 100
      const ctx = canvas.getContext('2d')!
      ctx.fillStyle = '#ff0000'
      ctx.fillRect(0, 0, 100, 100)
      
      canvas.toBlob(async (blob) => {
        if (!blob) return
        
        const formData = new FormData()
        formData.append('file', blob, 'test.png')
        formData.append('artistId', 'ariadna')

        console.log('🧪 Testing upload...')
        const response = await fetch('/api/vendor/upload-photo', {
          method: 'POST',
          body: formData
        })

        const result = await response.json()
        console.log('Upload test result:', result)
        alert(`Upload test: ${response.ok ? 'SUCCESS' : 'FAILED'}\n${JSON.stringify(result, null, 2)}`)
      })
    } catch (error) {
      console.error('Upload test error:', error)
      alert(`Upload test error: ${error}`)
    }
  }

  return (
    <>
      <Head>
        <title>Debug - Nail&apos;d</title>
      </Head>

      <div className="min-h-screen p-8" style={{ backgroundColor: '#FEFAE0' }}>
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-black mb-8">🔍 Deployment Debug</h1>

          {/* Environment Variables */}
          <div className="bg-white rounded-lg p-6 mb-6 shadow-sm">
            <h2 className="text-xl font-semibold text-black mb-4">Environment Variables</h2>
            {envStatus ? (
              <div className="space-y-2 font-mono text-sm">
                <div>NEXT_PUBLIC_SUPABASE_URL: {envStatus.hasSupabaseUrl ? '✅' : '❌'}</div>
                <div>NEXT_PUBLIC_SUPABASE_ANON_KEY: {envStatus.hasSupabaseKey ? '✅' : '❌'}</div>
                <div>URL Preview: {envStatus.supabaseUrl}</div>
                <div>Key Length: {envStatus.keyLength} chars</div>
              </div>
            ) : (
              <div>Loading...</div>
            )}
          </div>

          {/* Supabase Connection Test */}
          <div className="bg-white rounded-lg p-6 mb-6 shadow-sm">
            <h2 className="text-xl font-semibold text-black mb-4">Supabase Connection</h2>
            {supabaseTest ? (
              <div className="space-y-2">
                <div className="font-mono text-sm">
                  Status: {supabaseTest.success ? '✅ Connected' : '❌ Failed'}
                </div>
                <div className="font-mono text-sm">
                  HTTP Status: {supabaseTest.status}
                </div>
                {supabaseTest.success ? (
                  <div className="font-mono text-sm">
                    Images Found: {supabaseTest.data?.total_count || 0}
                  </div>
                ) : (
                  <div className="font-mono text-sm text-red-600">
                    Error: {supabaseTest.error}
                  </div>
                )}
              </div>
            ) : (
              <div>Testing connection...</div>
            )}
          </div>

          {/* Upload Test */}
          <div className="bg-white rounded-lg p-6 mb-6 shadow-sm">
            <h2 className="text-xl font-semibold text-black mb-4">Upload Test</h2>
            <button
              onClick={testUpload}
              className="bg-black text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors"
            >
              🧪 Test Photo Upload
            </button>
            <p className="text-sm text-gray-600 mt-2">
              This will create a small test image and try to upload it
            </p>
          </div>

          {/* Quick Links */}
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-black mb-4">Quick Links</h2>
            <div className="space-y-2">
              <a href="/" className="block text-blue-600 hover:underline">← Back to Main App</a>
              <a href="/vendor/ariadna/manage" className="block text-blue-600 hover:underline">Ariadna Management</a>
              <a href="/vendor/mia/manage" className="block text-blue-600 hover:underline">Mia Management</a>
              <a href="/artist/ariadna" className="block text-blue-600 hover:underline">Ariadna Profile</a>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
