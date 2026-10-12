-- Problem rate per line, worst first
SELECT
    s.mode,
    s.line_id,
    s.line_name,
    COUNT(*) AS snapshots,
    SUM(CASE WHEN s.status <> 'Good Service' THEN 1 ELSE 0 END) AS problems,
    ROUND(100.0 * SUM(CASE WHEN s.status <> 'Good Service' THEN 1 ELSE 0 END) / COUNT(*), 1) AS problem_rate,
    l.colour
FROM line_status AS s
LEFT JOIN lines AS l ON s.line_id = l.line_id
GROUP BY s.mode, s.line_id, s.line_name, l.colour
ORDER BY problem_rate DESC, s.line_name;