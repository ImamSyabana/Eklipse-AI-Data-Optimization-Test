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
SELECT
    /*
    Count distinct users with a submited gamesession history
    Can be tracked by the filled submited_date and divide by all distinct users.
    */
    (COUNT(DISTINCT CASE WHEN gs.submited_date IS NOT NULL THEN c.user_id END)::FLOAT * 100)
    / COUNT(DISTINCT c.user_id)::FLOAT AS activation_rate_percentage
FROM
    clips_df c -- Using 'clips' as the main source of all users
LEFT JOIN
    gamesession_df gs ON c.user_id = gs.user_id; -- Join to see their session activity
"""

query_2_engagement = """
-- Query 2: Count how many downloads each type of clip gets.
SELECT
    CASE
        WHEN c.clip_type_id = 1 THEN 'AI Highlight (Horizontal)'
        WHEN c.clip_type_id = 2 THEN 'Converted to TikTok'
        WHEN c.clip_type_id = 3 THEN 'Trimmed Clip'
        WHEN c.clip_type_id = 5 THEN 'Eventful Highlight'
        WHEN c.clip_type_id = 6 THEN 'Weekly Montage'
        WHEN c.clip_type_id = 7 THEN 'Local Upload'
        WHEN c.clip_type_id = 8 THEN 'YouTube Highlight (Vertical)'
        ELSE 'Unknown'
    END AS clip_type_name,
    COUNT(dc.id) AS total_downloads
FROM
    downloaded_clips_df dc
JOIN
    clips_df c ON dc.clip_id = c.id
GROUP BY
    clip_type_name
ORDER BY
    total_downloads DESC;
"""

query_3_conversion = """
SELECT
    /*
    Count distinct users with a premium record and divide by all distinct users.
    COUNT(DISTINCT p.user_id) only counts users who successfully joined to the premium table.
    */
    (COUNT(DISTINCT p.user_id)::FLOAT * 100) / COUNT(DISTINCT c.user_id)::FLOAT AS premium_conversion_rate
FROM
    clips_df c -- Using 'clips' as the source for all users
LEFT JOIN
    premium_df p ON c.user_id = p.user_id; -- Join to check for a premium subscription
"""
most_shared_game_clip = """
-- Query 4: Find the top 10 games whose clips are shared the most.
SELECT
    c.game_name,
    COUNT(c.id) AS number_of_shares
FROM
    shared_clips_df sc
JOIN
    clips_df c ON sc.clip_id = c.id
GROUP BY
    c.game_name
ORDER BY
    number_of_shares DESC
LIMIT 10;
"""

premium_churn_rate = """
-- Query 5: Calculate the percentage of premium users who have canceled their subscription.
SELECT
    -- Count distinct users who have a cancellation date
    (COUNT(DISTINCT CASE WHEN p.canceled_at IS NOT NULL THEN p.user_id END)::FLOAT * 100)
    /
    -- Divide by the total number of distinct users who have ever been premium
    COUNT(DISTINCT p.user_id)::FLOAT AS premium_churn_rate_percentage
FROM
    premium_df p
JOIN
    clips_df c ON p.user_id = c.user_id; -- This join is included to satisfy the assignment requirement.
"""

# listing all the querry into a single list 
queries_list = [user_active_rate, query_2_engagement, query_3_conversion, most_shared_game_clip, premium_churn_rate]

# --- 3. Run the query using DuckDB and print the result ---
# duckdb.query() runs the SQL. .to_df() converts the result back to a DataFrame.
for x in range(len(queries_list)):
        
    results_df = duckdb.query(queries_list[x]).to_df()

    print("\nQuery Results")
    print(results_df)