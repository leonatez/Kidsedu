-- Supabase database schema for Kidsedu vocabulary game

-- Create vocabulary_items table
CREATE TABLE IF NOT EXISTS vocabulary_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    image_url TEXT NOT NULL,
    vocabulary TEXT,
    category TEXT DEFAULT 'default',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create storage bucket for vocabulary images
INSERT INTO storage.buckets (id, name, public) 
VALUES ('vocabulary-images', 'vocabulary-images', true)
ON CONFLICT (id) DO NOTHING;

-- Allow public access to vocabulary images
CREATE POLICY "Public Access" ON storage.objects
FOR SELECT USING (bucket_id = 'vocabulary-images');

-- Allow authenticated users to insert vocabulary images
CREATE POLICY "Authenticated users can upload vocabulary images" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'vocabulary-images');

-- Allow public read access to vocabulary_items table
CREATE POLICY "Enable read access for all users" ON vocabulary_items
FOR SELECT USING (true);

-- Allow public insert and update access to vocabulary_items table
CREATE POLICY "Enable insert access for all users" ON vocabulary_items
FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update access for all users" ON vocabulary_items
FOR UPDATE USING (true);

-- Enable Row Level Security
ALTER TABLE vocabulary_items ENABLE ROW LEVEL SECURITY;

-- Migration: Add category column to existing table and set default values
-- Run this if you already have an existing vocabulary_items table
-- ALTER TABLE vocabulary_items ADD COLUMN IF NOT EXISTS category TEXT DEFAULT 'default';
-- UPDATE vocabulary_items SET category = 'default' WHERE category IS NULL;