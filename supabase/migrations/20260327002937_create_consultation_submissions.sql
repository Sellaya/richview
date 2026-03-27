/*
  # Create consultation submissions table

  1. New Tables
    - `consultation_submissions`
      - `id` (uuid, primary key) - Unique identifier for each submission
      - `first_name` (text) - Contact's first name
      - `last_name` (text) - Contact's last name
      - `email` (text) - Contact's email address
      - `phone` (text) - Contact's phone number
      - `interest` (text) - What they're interested in (borrowing, investing, brokering)
      - `message` (text) - Their message or inquiry details
      - `consultation_date` (date) - Preferred date for consultation
      - `consultation_time` (text) - Preferred time for consultation
      - `status` (text, default: 'pending') - Status of the submission (pending, contacted, completed, cancelled)
      - `source` (text, default: 'website') - Source of the submission
      - `user_agent` (text) - Browser/device information
      - `ip_address` (inet) - IP address of submitter (for security/analytics)
      - `created_at` (timestamptz, default: now()) - When submission was created
      - `updated_at` (timestamptz, default: now()) - When submission was last updated
      - `notes` (text) - Internal notes about the submission

  2. Security
    - Enable RLS on `consultation_submissions` table
    - Add policy for public to insert their own submissions
    - Add policy for authenticated staff to view all submissions
    - Add policy for authenticated staff to update submissions

  3. Indexes
    - Index on email for quick lookups
    - Index on created_at for sorting
    - Index on status for filtering

  4. Functions
    - Add function to automatically update updated_at timestamp
*/

-- Create consultation_submissions table
CREATE TABLE IF NOT EXISTS consultation_submissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name text NOT NULL,
  last_name text NOT NULL,
  email text NOT NULL,
  phone text NOT NULL,
  interest text NOT NULL CHECK (interest IN ('borrowing', 'investing', 'brokering')),
  message text NOT NULL,
  consultation_date date NOT NULL,
  consultation_time text NOT NULL,
  status text DEFAULT 'pending' CHECK (status IN ('pending', 'contacted', 'completed', 'cancelled')),
  source text DEFAULT 'website',
  user_agent text,
  ip_address inet,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  notes text
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_consultation_submissions_email ON consultation_submissions(email);
CREATE INDEX IF NOT EXISTS idx_consultation_submissions_created_at ON consultation_submissions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_consultation_submissions_status ON consultation_submissions(status);
CREATE INDEX IF NOT EXISTS idx_consultation_submissions_consultation_date ON consultation_submissions(consultation_date);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_consultation_submissions_updated_at ON consultation_submissions;
CREATE TRIGGER update_consultation_submissions_updated_at
  BEFORE UPDATE ON consultation_submissions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Enable RLS
ALTER TABLE consultation_submissions ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can insert a consultation submission (public form)
CREATE POLICY "Anyone can insert consultation submission"
  ON consultation_submissions
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- Policy: Authenticated users (staff) can view all submissions
CREATE POLICY "Authenticated users can view all submissions"
  ON consultation_submissions
  FOR SELECT
  TO authenticated
  USING (true);

-- Policy: Authenticated users (staff) can update submissions
CREATE POLICY "Authenticated users can update submissions"
  ON consultation_submissions
  FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Policy: Authenticated users (staff) can delete submissions
CREATE POLICY "Authenticated users can delete submissions"
  ON consultation_submissions
  FOR DELETE
  TO authenticated
  USING (true);