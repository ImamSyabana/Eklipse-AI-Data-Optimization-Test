import pandas as pd
import duckdb

# --- 1. Load your CSV files into pandas DataFrames ---
try:
    gamesession_df = pd.read_csv('task 3/da_test/gamesession.csv')
    clips_df = pd.read_csv('task 3/da_test/clips.csv')
    downloaded_clips_df = pd.read_csv('task 3/da_test/downloaded_clips.csv')
    shared_clips_df = pd.read_csv('task 3/da_test/shared_clips.csv')
    premium_df = pd.read_csv('task 3/da_test/premium_users.csv')

    print("✅ All CSV files loaded successfully!")

except FileNotFoundError as e:
    print(f"❌ Error: {e}. Make sure your CSV files are in the same folder as the script.")
    exit()


# --- NEW: Data Cleaning and Standardization Section ---
all_dfs = [gamesession_df, clips_df, downloaded_clips_df, shared_clips_df, premium_df]

for df in all_dfs:
    # Convert all column names to lowercase to fix inconsistencies like 'gamesession_Id'
    df.columns = df.columns.str.lower()
    
    # Drop the 'unnamed: 0' column if it exists
    if 'unnamed: 0' in df.columns:
        df.drop(columns=['unnamed: 0'], inplace=True)
        
    # Specifically fix the 'user_ld' typo if it exists after lowering case
    if 'user_ld' in df.columns:
        df.rename(columns={'user_ld': 'user_id'}, inplace=True)

print("✅ All column names have been standardized to lowercase.")


# --- 2. SQL Queries Section ---
# Now that all column names are standardized, these queries will work correctly.

print("\n" + "="*50)
print("--- Running Query 1: User Activation Rate ---")
query_1_activation = """
SELECT
    (COUNT(DISTINCT CASE WHEN gs.submited_date IS NOT NULL THEN c.user_id END)::FLOAT * 100)
    / COUNT(DISTINCT c.user_id)::FLOAT AS activation_rate_percentage
FROM
    clips_df c
LEFT JOIN
    gamesession_df gs ON c.user_id = gs.user_id;
"""
result_1 = duckdb.query(query_1_activation).to_df()
print(result_1)


print("\n" + "="*50)
print("--- Running Query 2: Clip Engagement Rate ---")
query_2_engagement = """
SELECT
    COUNT(DISTINCT c.id)::FLOAT * 100 / (SELECT COUNT(*) FROM clips_df WHERE gamesession_id IS NOT NULL) AS clip_engagement_rate
FROM
    clips_df c
LEFT JOIN
    downloaded_clips_df dc ON c.id = dc.clip_id
LEFT JOIN
    shared_clips_df sc ON c.id = sc.clip_id
WHERE
    c.gamesession_id IS NOT NULL
    AND (dc.clip_id IS NOT NULL OR sc.clip_id IS NOT NULL OR c.clip_type_id = 2);
"""
result_2 = duckdb.query(query_2_engagement).to_df()
print(result_2)


print("\n" + "="*50)
print("--- Running Query 3: Free-to-Premium Conversion Rate ---")
query_3_conversion = """
SELECT
    (COUNT(DISTINCT p.user_id)::FLOAT * 100) / COUNT(DISTINCT c.user_id)::FLOAT AS premium_conversion_rate
FROM
    clips_df c
LEFT JOIN
    premium_df p ON c.user_id = p.user_id;
"""
result_3 = duckdb.query(query_3_conversion).to_df()
print(result_3)


print("\n" + "="*50)
print("--- Running Query 4: Average Clips Generated Per Premium User ---")
query_4_avg_clips = """
SELECT
    COUNT(c.id)::FLOAT / COUNT(DISTINCT p.user_id)::FLOAT AS avg_clips_per_premium_user
FROM
    premium_df p
JOIN
    clips_df c ON p.user_id = c.user_id
WHERE
    CAST(p.ends_at AS DATE) >= CURRENT_DATE
    AND c.gamesession_id IS NOT NULL;
"""
result_4 = duckdb.query(query_4_avg_clips).to_df()
print(result_4)


print("\n" + "="*50)
print("--- Running Query 5: Most Engaging Games ---")
query_5_top_games = """
SELECT
    game_name,
    COUNT(*) AS total_engagement_actions
FROM (
    SELECT c.game_name
    FROM downloaded_clips_df dc
    JOIN clips_df c ON dc.clip_id = c.id
    UNION ALL
    SELECT c.game_name
    FROM shared_clips_df sc
    JOIN clips_df c ON sc.clip_id = c.id
) AS all_interactions
WHERE game_name IS NOT NULL
GROUP BY game_name
ORDER BY total_engagement_actions DESC
LIMIT 5;
"""
result_5 = duckdb.query(query_5_top_games).to_df()
print(result_5)
print("\n" + "="*50)