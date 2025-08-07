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