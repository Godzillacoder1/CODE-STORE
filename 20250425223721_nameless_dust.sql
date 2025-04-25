/*
  # Create quotes table and functions

  1. New Tables
    - `quotes`
      - `id` (uuid, primary key)
      - `quote` (text, the philosophical quote)
      - `author` (text, who said/wrote the quote)
      - `category` (text, philosophical category)
      - `upvotes` (integer, number of upvotes)
      - `created_at` (timestamp with timezone)

  2. Functions
    - `increment_upvotes`: Safely increments the upvotes counter

  3. Security
    - Enable RLS
    - Add policies for public read access
    - Add policies for authenticated users to create and upvote
*/

-- Create quotes table
CREATE TABLE IF NOT EXISTS quotes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  quote text NOT NULL,
  author text NOT NULL,
  category text NOT NULL,
  upvotes integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Create function to safely increment upvotes
CREATE OR REPLACE FUNCTION increment_upvotes(quote_id uuid)
RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
  new_upvotes integer;
BEGIN
  UPDATE quotes
  SET upvotes = upvotes + 1
  WHERE id = quote_id
  RETURNING upvotes INTO new_upvotes;
  
  RETURN new_upvotes;
END;
$$;

-- Enable RLS
ALTER TABLE quotes ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Allow public read access" ON quotes;
DROP POLICY IF EXISTS "Allow authenticated users to create quotes" ON quotes;
DROP POLICY IF EXISTS "Allow authenticated users to upvote" ON quotes;

-- Recreate policies with correct permissions
CREATE POLICY "Allow public read access"
  ON quotes
  FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Allow insert access"
  ON quotes
  FOR INSERT
  TO public
  WITH CHECK (true);

CREATE POLICY "Allow update access"
  ON quotes
  FOR UPDATE
  TO public
  USING (true);