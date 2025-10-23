import { useState, useEffect, useCallback } from 'react'

interface Review {
  id: string
  client_name: string
  rating: number
  review_text: string
  service_date: string
  review_photo_url?: string
}

interface ReviewsSectionProps {
  artistId: string
}

export default function ReviewsSection({ artistId }: ReviewsSectionProps) {
  const [reviews, setReviews] = useState<Review[]>([])
  const [showReviewForm, setShowReviewForm] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [selectedRating, setSelectedRating] = useState<number>(0)
  const [hoveredRating, setHoveredRating] = useState<number>(0)

  // No fake reviews - only show real client reviews from database

  const loadReviews = useCallback(async () => {
    try {
      const response = await fetch(`/api/vendor/${artistId}/reviews`)
      const data = await response.json()
      // Only show real reviews from database
      const apiReviews = data.reviews || []
      setReviews(apiReviews)
    } catch (error) {
      console.error('Failed to load reviews:', error)
      // If API fails, show no reviews (empty array)
      setReviews([])
    }
  }, [artistId])

  useEffect(() => {
    loadReviews()
  }, [loadReviews])

  const submitReview = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    
    // Validate rating is selected (silent validation)
    if (selectedRating === 0) {
      // Silent validation - just don't submit if no rating
      setIsSubmitting(false)
      return
    }
    
    setIsSubmitting(true)

    try {
      const formData = new FormData(e.currentTarget)
      formData.append('artistId', artistId)

      // Debug: Log form data being sent
      console.log('🔍 Submitting review with data:', {
        artistId,
        clientName: formData.get('clientName'),
        rating: formData.get('rating'),
        reviewText: formData.get('reviewText'),
        serviceDate: formData.get('serviceDate'),
        selectedRating
      })

      const response = await fetch('/api/vendor/add-review', {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const result = await response.json()
        console.log('✅ Review submission successful:', result)
        
        // Clean refresh of the page after successful submission
        window.location.reload()
        
      } else {
        const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
        console.error('❌ Review submission failed:', errorData)
        // Silent failure - no user alerts
      }
    } catch (error) {
      console.error('Review submission error:', error)
      // Silent failure - no user alerts
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="bg-transparent border-2 border-black rounded-2xl p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-2xl font-medium text-black pp-eiko">Client Reviews</h3>
        <button
          onClick={() => setShowReviewForm(!showReviewForm)}
          className="bg-black text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors"
        >
          {showReviewForm ? 'Cancel' : '+ Add Review'}
        </button>
      </div>

      {/* Review Form */}
      {showReviewForm && (
        <div className="mb-8 p-6 bg-gray-50 rounded-xl border border-gray-200">
          <h4 className="text-lg font-bold text-black mb-4 pp-eiko">Leave a Review</h4>
          
          <form onSubmit={submitReview} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-bold text-black mb-2">Your Name</label>
                <input
                  type="text"
                  name="clientName"
                  placeholder="Enter your name"
                  className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-black text-black bg-white"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-bold text-black mb-2">Service Date</label>
                <input
                  type="date"
                  name="serviceDate"
                  className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-black text-black bg-white"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-black mb-2">Rating</label>
              <div className="flex space-x-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setSelectedRating(star)}
                    onMouseEnter={() => setHoveredRating(star)}
                    onMouseLeave={() => setHoveredRating(0)}
                    className="text-3xl transition-colors cursor-pointer focus:outline-none"
                  >
                    <span className={
                      star <= (hoveredRating || selectedRating) 
                        ? 'text-yellow-400' 
                        : 'text-gray-300'
                    }>
                      ⭐
                    </span>
                  </button>
                ))}
                {/* Hidden input for form submission */}
                <input
                  type="hidden"
                  name="rating"
                  value={selectedRating || 5}
                  required
                />
                {/* Debug: Show current rating */}
                <p className="text-xs text-gray-500 mt-1">
                  Selected rating: {selectedRating || 'None'} stars
                </p>
              </div>
              {selectedRating > 0 && (
                <p className="text-sm text-gray-600 mt-1">
                  {selectedRating} out of 5 stars
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-bold text-black mb-2">Review</label>
              <textarea
                name="reviewText"
                placeholder="Share your experience..."
                rows={4}
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-black text-black bg-white"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-black mb-2">Photo (Optional)</label>
              <input
                type="file"
                name="reviewPhoto"
                accept="image/*"
                className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-black text-black bg-white"
              />
              <p className="text-xs text-gray-600 mt-1">Upload a photo of your nails (max 5MB)</p>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="bg-black text-white px-6 py-3 rounded-full font-bold hover:bg-gray-800 transition-colors disabled:opacity-50"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Review'}
            </button>
          </form>
        </div>
      )}

      {/* Reviews List */}
      {reviews.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-black font-medium">No reviews yet</p>
          <p className="text-sm text-gray-600 mt-1">Be the first to leave a review!</p>
        </div>
      ) : (
        <div className="space-y-6">
          {reviews.map((review) => (
            <div key={review.id} className="border-b border-gray-300 pb-6 last:border-b-0 bg-transparent">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h5 className="font-bold text-black text-lg">{review.client_name}</h5>
                  <div className="flex items-center space-x-2 mt-1">
                    <div className="flex">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <span
                          key={star}
                          className={star <= review.rating ? 'text-yellow-400' : 'text-gray-300'}
                        >
                          ⭐
                        </span>
                      ))}
                    </div>
                    <span className="text-sm text-gray-600 font-medium">
                      {new Date(review.service_date).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
              
              {/* BULLETPROOF BLACK TEXT */}
              <p 
                className="text-black font-medium leading-relaxed mb-3"
                style={{ 
                  color: '#000000 !important',
                  fontWeight: '500',
                  fontSize: '16px',
                  lineHeight: '1.5'
                }}
              >
                {review.review_text}
              </p>
              
              {review.review_photo_url && (
                <div className="mt-3">
                  <img
                    src={review.review_photo_url}
                    alt="Client's nail art"
                    className="w-32 h-32 object-cover rounded-lg border-2 border-gray-200"
                    onError={(e) => {
                      e.currentTarget.style.display = 'none'
                    }}
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
