import { useState, useRef } from 'react'
import Head from 'next/head'

export default function TestPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setError(null)
      setResult(null)
      
      // Create preview URL
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const handleTest = async (event: React.FormEvent) => {
    event.preventDefault()
    
    if (!selectedFile) {
      setError('Please select an image file')
      return
    }

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      console.log('🧪 Testing with file:', selectedFile.name, 'Size:', selectedFile.size, 'Type:', selectedFile.type)

      const response = await fetch('/api/test', {
        method: 'POST',
        body: formData,
      })

      console.log('📡 Response status:', response.status)

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(`HTTP ${response.status}: ${errorData.error || 'Unknown error'}`)
      }

      const data = await response.json()
      console.log('✅ Test result:', data)
      setResult(data)
    } catch (err) {
      console.error('❌ Test failed:', err)
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Image Processing Test - Nail Art Search</title>
        <meta name="description" content="Test image processing functionality" />
      </Head>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              🧪 Image Processing Test
            </h1>
            <p className="text-lg text-gray-600">
              Test the image processing functionality to debug the 500 error
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <form onSubmit={handleTest} className="space-y-6">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                
                {previewUrl ? (
                  <div className="space-y-4">
                    <img
                      src={previewUrl}
                      alt="Preview"
                      className="max-w-xs mx-auto rounded-lg shadow-md"
                    />
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="text-blue-600 hover:text-blue-700 font-medium"
                    >
                      Choose a different image
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="text-6xl text-gray-400">📸</div>
                    <div>
                      <p className="text-lg font-medium text-gray-900">
                        Drop your test image here
                      </p>
                      <p className="text-gray-500">or click to browse</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Choose File
                    </button>
                  </div>
                )}
              </div>

              {selectedFile && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-medium text-blue-900 mb-2">Selected File:</h3>
                  <p className="text-sm text-blue-700">
                    <strong>Name:</strong> {selectedFile.name}<br/>
                    <strong>Size:</strong> {(selectedFile.size / 1024).toFixed(2)} KB<br/>
                    <strong>Type:</strong> {selectedFile.type}
                  </p>
                </div>
              )}

              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              <button
                type="submit"
                disabled={!selectedFile || isLoading}
                className="w-full bg-green-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Testing...' : 'Run Image Processing Test'}
              </button>
            </form>
          </div>

          {result && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                ✅ Test Results
              </h2>
              
              <div className="space-y-4">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="font-medium text-green-900 mb-2">Success!</h3>
                  <p className="text-green-700">{result.message}</p>
                </div>

                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <h3 className="font-medium text-gray-900 mb-2">File Information:</h3>
                  <pre className="text-sm text-gray-700 bg-white p-3 rounded border overflow-x-auto">
                    {JSON.stringify(result.fileInfo, null, 2)}
                  </pre>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-medium text-blue-900 mb-2">Tests Passed:</h3>
                  <ul className="text-blue-700 space-y-1">
                    {result.tests.map((test: string, index: number) => (
                      <li key={index} className="flex items-center">
                        <span className="text-green-600 mr-2">✓</span>
                        {test}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
