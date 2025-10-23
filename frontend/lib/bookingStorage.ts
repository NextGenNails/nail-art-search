// Shared booking statistics storage
// In production, this should be replaced with a database

let bookingStats: { [vendorId: string]: number } = {}

export function incrementBookingCount(vendorId: string): number {
  if (!bookingStats[vendorId]) {
    bookingStats[vendorId] = 0
  }
  bookingStats[vendorId]++
  return bookingStats[vendorId]
}

export function getBookingStats(): { [vendorId: string]: number } {
  return { ...bookingStats }
}

export function getTotalClicks(): number {
  return Object.values(bookingStats).reduce((sum, count) => sum + count, 0)
}

export function getVendorClicks(vendorId: string): number {
  return bookingStats[vendorId] || 0
}

// Reset stats (for testing)
export function resetBookingStats(): void {
  bookingStats = {}
}

// Initialize with some test data (remove in production)
if (process.env.NODE_ENV === 'development') {
  // You can add test data here if needed
}
