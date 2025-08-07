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