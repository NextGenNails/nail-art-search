-- Create client reviews table in Supabase
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS client_reviews (
  id SERIAL PRIMARY KEY,
  artist_id TEXT NOT NULL,
  client_name TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  review_text TEXT NOT NULL,
  service_date DATE,
  review_photo_url TEXT,
  review_photo_filename TEXT,
  submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  status TEXT DEFAULT 'approved' CHECK (status IN ('pending', 'approved', 'rejected')),
  source TEXT DEFAULT 'client_submission',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_client_reviews_artist_id ON client_reviews(artist_id);
CREATE INDEX IF NOT EXISTS idx_client_reviews_status ON client_reviews(status);
CREATE INDEX IF NOT EXISTS idx_client_reviews_rating ON client_reviews(rating);
CREATE INDEX IF NOT EXISTS idx_client_reviews_submitted_at ON client_reviews(submitted_at);

-- Enable Row Level Security
ALTER TABLE client_reviews ENABLE ROW LEVEL SECURITY;

-- Create policies for reviews
CREATE POLICY "Allow review inserts" ON client_reviews
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow approved review reads" ON client_reviews
  FOR SELECT USING (status = 'approved');

-- Insert some test reviews (optional)
INSERT INTO client_reviews (artist_id, client_name, rating, review_text, service_date, status) VALUES
('ariadna', 'Sarah M.', 5, 'Absolutely amazing work! The attention to detail is incredible. My nails looked exactly like the inspiration photo I brought in. Will definitely be coming back!', '2024-01-15', 'approved'),
('ariadna', 'Jessica L.', 5, 'Professional, clean, and so talented! The nail art was flawless and lasted weeks. The salon is beautiful and the service was top-notch.', '2024-01-10', 'approved'),
('mia', 'Taylor R.', 4, 'Great service and beautiful results! Mia was very thorough and took her time to make sure everything was perfect. The dip powder manicure looks amazing and feels strong.', '2024-01-08', 'approved')
ON CONFLICT DO NOTHING;

-- Verify table creation
SELECT 'Client reviews table created successfully!' as status;
SELECT COUNT(*) as sample_reviews_count FROM client_reviews;
