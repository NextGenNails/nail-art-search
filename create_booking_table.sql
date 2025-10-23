-- Create booking clicks tracking table in Supabase
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS booking_clicks (
  id SERIAL PRIMARY KEY,
  vendor_id TEXT NOT NULL,
  vendor_name TEXT NOT NULL,
  source TEXT DEFAULT 'unknown',
  user_ip TEXT,
  user_agent TEXT,
  clicked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_booking_clicks_vendor_id ON booking_clicks(vendor_id);
CREATE INDEX IF NOT EXISTS idx_booking_clicks_clicked_at ON booking_clicks(clicked_at);

-- Enable Row Level Security (optional, for extra security)
ALTER TABLE booking_clicks ENABLE ROW LEVEL SECURITY;

-- Create policy to allow inserts (for tracking clicks)
CREATE POLICY "Allow booking click inserts" ON booking_clicks
  FOR INSERT WITH CHECK (true);

-- Create policy to allow reads (for analytics)
CREATE POLICY "Allow booking click reads" ON booking_clicks
  FOR SELECT USING (true);

-- Insert some test data (optional, remove in production)
-- INSERT INTO booking_clicks (vendor_id, vendor_name, source) VALUES
-- ('ariadna', 'Ariadna Palomo (Onix Beauty Center)', 'test'),
-- ('mia', 'Mia Pham (Ivy''s Nail and Lash)', 'test');

-- Verify table creation
SELECT 'Booking clicks table created successfully!' as status;
