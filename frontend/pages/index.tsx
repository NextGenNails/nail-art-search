import { useEffect } from 'react'
import { useRouter } from 'next/router'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    router.push('/upload')
  }, [router])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Nail Art Visual Similarity Search</h1>
        <p className="text-gray-600">Redirecting to upload page...</p>
      </div>
    </div>
  )
} 