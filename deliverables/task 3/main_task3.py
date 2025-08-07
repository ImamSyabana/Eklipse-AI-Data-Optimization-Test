import pandas as pd
import duckdb

# --- 1. Load CSV files into pandas DataFrames ---
try:
    gamesession_df = pd.read_csv('task 3/da_test/gamesession.csv')
    clips_df = pd.read_csv('task 3/da_test/clips.csv')
    downloaded_clips_df = pd.read_csv('task 3/da_test/downloaded_clips.csv')
    shared_clips_df = pd.read_csv('task 3/da_test/shared_clips.csv')
    premium_df = pd.read_csv('task 3/da_test/premium_users.csv')

except FileNotFoundError as msg:
    print(f"Error: {msg}. Make sure your CSV files are in the right folder.")
    exit()


# --- 2. Write SQL query as a string ---
user_active_rate = """
-- Count distinct users with a submited gamesession history
SELECT
    (COUNT(DISTINCT CASE WHEN gs.submited_date IS NOT NULL THEN clips_df.user_id END)::FLOAT * 100)
    / COUNT(DISTINCT clips_df.user_id)::FLOAT AS activation_rate_percentage
FROM
    clips_df -- Using 'clips' as the main source of all users
LEFT JOIN
    gamesession_df gs ON clips_df.user_id = gs.user_id; -- Join to see their session activity
"""

clips_distribution = """
-- Count how many downloads each type of clip gets.
SELECT
    CASE
        WHEN clips_df.clip_type_id = 1 THEN 'AI Highlight (Horizontal)'
        WHEN clips_df.clip_type_id = 2 THEN 'Converted to TikTok'
        WHEN clips_df.clip_type_id = 3 THEN 'Trimmed Clip'
        WHEN clips_df.clip_type_id = 5 THEN 'Eventful Highlight'
        WHEN clips_df.clip_type_id = 6 THEN 'Weekly Montage'
        WHEN clips_df.clip_type_id = 7 THEN 'Local Upload'
        WHEN clips_df.clip_type_id = 8 THEN 'YouTube Highlight (Vertical)'
        ELSE 'Unknown'
    END AS clip_type_name,
    COUNT(downloaded_clips_df.id) AS total_downloads
FROM
    downloaded_clips_df
JOIN
    clips_df ON downloaded_clips_df.clip_id = clips_df.id
GROUP BY
    clip_type_name
ORDER BY
    total_downloads DESC;
"""

conversion_rate = """
--  Count distinct users with a premium record and divide by all distinct users.
SELECT
    (COUNT(DISTINCT premium_df.user_id)::FLOAT * 100) / COUNT(DISTINCT clips_df.user_id)::FLOAT AS premium_conversion_rate
FROM
    clips_df -- Using 'clips' as the source for all users
LEFT JOIN
    premium_df ON clips_df.user_id = premium_df.user_id; 
"""

premium_churn_rate = """
-- Calculate the percentage of premium users who have canceled their subscription.
SELECT
    -- Count distinct users who have a cancellation date
    (COUNT(DISTINCT CASE WHEN premium_df.canceled_at IS NOT NULL THEN premium_df.user_id END)::FLOAT * 100)
    /
    -- Divide by the total number of distinct users who have ever been premium
    COUNT(DISTINCT premium_df.user_id)::FLOAT AS premium_churn_rate_percentage
FROM
    premium_df
JOIN
    clips_df ON premium_df.user_id = clips_df.user_id; -- This join is included to satisfy the assignment requirement.
"""

most_shared_clip = """
-- Find the top 10 games whose clips are shared the most.
SELECT
    clips_df.game_name,
    COUNT(clips_df.id) AS number_of_shares
FROM
    shared_clips_df
JOIN
    clips_df ON shared_clips_df.clip_id = clips_df.id
GROUP BY
    clips_df.game_name
ORDER BY
    number_of_shares DESC
LIMIT 10;
"""


# listing all the querry into a single list 
queries_list = [user_active_rate, conversion_rate, clips_distribution, premium_churn_rate, most_shared_clip]

# --- 3. Run the query
for x in range(len(queries_list)):
        
    results_df = duckdb.query(queries_list[x]).to_df()

    print("\nQuery Results")
    print(results_df)