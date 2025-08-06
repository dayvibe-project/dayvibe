-- Supabase Database Setup for DayVibe Apps
-- Run these commands in your Supabase SQL Editor

-- 1. Create signups table for email collection (DayVibe Landing)
CREATE TABLE IF NOT EXISTS signups (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    signup_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'landing_page',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create journal_entries table for DayVibe app (optional, for future use)
CREATE TABLE IF NOT EXISTS journal_entries (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    entry_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    audio_url TEXT,
    transcription TEXT,
    mood_score DECIMAL(3,2),
    mood_label VARCHAR(50),
    duration_seconds INTEGER,
    ai_insights JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create user_stats table for tracking user statistics
CREATE TABLE IF NOT EXISTS user_stats (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) UNIQUE,
    streak_days INTEGER DEFAULT 0,
    total_entries INTEGER DEFAULT 0,
    avg_mood DECIMAL(3,2) DEFAULT 0.0,
    last_entry_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_signups_email ON signups(email);
CREATE INDEX IF NOT EXISTS idx_signups_date ON signups(signup_date);
CREATE INDEX IF NOT EXISTS idx_journal_entries_user_date ON journal_entries(user_id, entry_date DESC);
CREATE INDEX IF NOT EXISTS idx_user_stats_user_id ON user_stats(user_id);

-- 5. Enable Row Level Security (RLS) for better security
ALTER TABLE signups ENABLE ROW LEVEL SECURITY;
ALTER TABLE journal_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;

-- 6. Create RLS policies

-- Allow anyone to insert signups (for landing page)
CREATE POLICY "Anyone can insert signups" ON signups
    FOR INSERT WITH CHECK (true);

-- Allow reading signups for admin purposes (optional - you might want to restrict this)
CREATE POLICY "Admins can read signups" ON signups
    FOR SELECT USING (false); -- Change to appropriate admin check

-- Users can only access their own journal entries
CREATE POLICY "Users can insert own journal entries" ON journal_entries
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can read own journal entries" ON journal_entries
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own journal entries" ON journal_entries
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own journal entries" ON journal_entries
    FOR DELETE USING (auth.uid() = user_id);

-- Users can manage their own stats
CREATE POLICY "Users can insert own stats" ON user_stats
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can read own stats" ON user_stats
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own stats" ON user_stats
    FOR UPDATE USING (auth.uid() = user_id);

-- 7. Create function to update timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 8. Create triggers for automatic timestamp updates
CREATE TRIGGER update_signups_updated_at BEFORE UPDATE ON signups
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_journal_entries_updated_at BEFORE UPDATE ON journal_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_stats_updated_at BEFORE UPDATE ON user_stats
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 9. Insert sample data for testing (optional)
-- Uncomment the following lines if you want sample data

/*
INSERT INTO signups (email, source) VALUES 
    ('test1@example.com', 'landing_page'),
    ('test2@example.com', 'landing_page'),
    ('test3@example.com', 'direct');
*/

-- 10. Create view for signup analytics (optional)
CREATE OR REPLACE VIEW signup_analytics AS
SELECT 
    DATE(signup_date) as signup_day,
    COUNT(*) as daily_signups,
    source,
    COUNT(*) OVER (ORDER BY DATE(signup_date)) as cumulative_signups
FROM signups
GROUP BY DATE(signup_date), source
ORDER BY signup_day DESC;

-- Success message
SELECT 'Database setup completed successfully!' as message;
SELECT 'Tables created: signups, journal_entries, user_stats' as tables_info;
SELECT 'RLS policies configured for security' as security_info;
SELECT 'Remember to update your .env file with Supabase credentials' as next_step;
