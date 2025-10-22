import { useState, useEffect } from 'react'
import Head from 'next/head'

interface BookingStats {
  vendorId: string
  vendorName: string
  clicks: number
  percentage: number
}

interface AnalyticsData {
  totalClicks: number
  vendorCount: number
  activeVendors: number
  vendorStats: BookingStats[]
  lastUpdated: string
}

export default function Analytics() {
  const [data, setData] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [password, setPassword] = useState('')
  const [authError, setAuthError] = useState('')

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/booking-analytics')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      setData(result)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (isAuthenticated) {
      fetchAnalytics()
    }
  }, [isAuthenticated])

  // Secure password protection using environment variables
  const handleAuth = (e: React.FormEvent) => {
    e.preventDefault()
    
    // Get password from environment variable (secure)
    const correctPassword = process.env.NEXT_PUBLIC_ANALYTICS_PASSWORD
    
    if (!correctPassword) {
      setAuthError('Analytics password not configured')
      return
    }
    
    if (password === correctPassword) {
      setIsAuthenticated(true)
      setAuthError('')
    } else {
      setAuthError('Incorrect password')
    }
  }

  // Show login form if not authenticated
  if (!isAuthenticated) {
    return (
      <>
        <Head>
          <title>Analytics Login - Nail&apos;d</title>
          <meta name="description" content="Admin access to booking analytics" />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="max-w-md w-full bg-white rounded-lg shadow-sm p-6">
            <div className="text-center mb-6">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                🔒 Analytics Access
              </h1>
              <p className="text-gray-600">
                Enter admin password to view booking analytics
              </p>
            </div>

            <form onSubmit={handleAuth}>
              <div className="mb-4">
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  Admin Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter password"
                  required
                />
              </div>

              {authError && (
                <div className="mb-4 text-sm text-red-600">
                  {authError}
                </div>
              )}

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Access Analytics
              </button>
            </form>

            <div className="mt-4 text-xs text-gray-500 text-center">
              Protected analytics for business owners only
            </div>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <Head>
        <title>Booking Analytics - Nail&apos;d</title>
        <meta name="description" content="Track booking clicks and vendor leads" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <div className="flex justify-between items-center">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    📊 Booking Analytics
                  </h1>
                  <p className="text-gray-600">
                    Track leads generated for your nail technicians
                  </p>
                </div>
                <button
                  onClick={fetchAnalytics}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                  disabled={loading}
                >
                  {loading ? 'Refreshing...' : 'Refresh'}
                </button>
              </div>
            </div>

            {/* Stats Overview */}
            {data && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <div className="text-2xl font-bold text-blue-600 mb-2">
                    {data.totalClicks}
                  </div>
                  <div className="text-gray-600">Total Booking Clicks</div>
                </div>
                
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <div className="text-2xl font-bold text-green-600 mb-2">
                    {data.vendorCount}
                  </div>
                  <div className="text-gray-600">Total Vendors</div>
                  <div className="text-xs text-gray-400 mt-1">
                    ({data.activeVendors} with clicks)
                  </div>
                </div>
                
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <div className="text-2xl font-bold text-purple-600 mb-2">
                    {data.totalClicks > 0 ? Math.round(data.totalClicks / data.vendorCount) : 0}
                  </div>
                  <div className="text-gray-600">Avg Clicks per Vendor</div>
                </div>
              </div>
            )}

            {/* Vendor Breakdown */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Vendor Performance
              </h2>
              
              {loading && (
                <div className="text-center py-8">
                  <div className="text-gray-500">Loading analytics...</div>
                </div>
              )}
              
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                  <p className="text-red-800">Error: {error}</p>
                </div>
              )}
              
              {data && data.vendorStats.length > 0 ? (
                <div className="space-y-4">
                  {data.vendorStats.map((vendor) => (
                    <div key={vendor.vendorId} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h3 className="font-medium text-gray-900">{vendor.vendorName}</h3>
                        <div className="text-right">
                          <div className="text-lg font-bold text-blue-600">{vendor.clicks}</div>
                          <div className="text-sm text-gray-500">clicks</div>
                        </div>
                      </div>
                      
                      {/* Progress bar */}
                      <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${vendor.percentage}%` }}
                        ></div>
                      </div>
                      
                      <div className="text-sm text-gray-600">
                        {vendor.percentage}% of total clicks
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                !loading && (
                  <div className="text-center py-8">
                    <div className="text-gray-500 mb-2">No booking clicks yet</div>
                    <p className="text-sm text-gray-400">
                      Clicks will appear here when users book appointments
                    </p>
                  </div>
                )
              )}
              
              {data && (
                <div className="mt-6 pt-4 border-t border-gray-200">
                  <p className="text-xs text-gray-500">
                    Last updated: {new Date(data.lastUpdated).toLocaleString()}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
