SELECT
    (COUNT(DISTINCT premium_df.user_id)::FLOAT * 100) / COUNT(DISTINCT clips_df.user_id)::FLOAT AS premium_conversion_rate
FROM
    clips_df -- Using 'clips' as the source for all users
LEFT JOIN
    premium_df ON clips_df.user_id = premium_df.user_id; 