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