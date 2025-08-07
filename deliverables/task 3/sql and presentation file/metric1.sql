SELECT
  
    (COUNT(DISTINCT CASE WHEN gs.submited_date IS NOT NULL THEN clips_df.user_id END)::FLOAT * 100)
    / COUNT(DISTINCT clips_df.user_id)::FLOAT AS activation_rate_percentage
FROM
    clips_df -- Using 'clips' as the main source of all users
LEFT JOIN
    gamesession_df gs ON clips_df.user_id = gs.user_id; -- Join to see their session activity
