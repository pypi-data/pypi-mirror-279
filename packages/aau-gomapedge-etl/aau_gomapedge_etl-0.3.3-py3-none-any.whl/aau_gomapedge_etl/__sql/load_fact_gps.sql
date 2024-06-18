SELECT DISTINCT trajectory.trip_id                 AS trip_id,
                trajectory.img_seq_id              AS img_seq_id,
                user                               AS user_id,
                strftime(timestamp, '%Y%m%d')::INT AS date_no,
                strftime(timestamp, '%H%M%S')::INT AS time_no,
                accuracy                           AS gps_accuracy,
                altitude                           AS alt,
                altitude_accuracy                  AS alt_accuracy,
                heading,
                speed * 3.6                        AS speed,
                ST_AsWKB(point)                    AS raw_point,
                match.trip_split_id                AS trip_split_id,
                distance_to_road,
                ST_AsWKB(match_point) AS match_point,
                country,
                country_code,
                region,
                state,
                state_district,
                county,
                municipality,
                city,
                town,
                village,
                suburb,
                house_number,
                road,
                postcode,
                user_view.*,
                trip_view.*
FROM trajectory
    INNER JOIN user_view      ON user = user_id
    INNER JOIN match     USING (trip_id, img_seq_id)
    INNER JOIN trip_view USING (trip_id, trip_split_id)
    LEFT JOIN address   USING (trip_id, img_seq_id)
WHERE match_distance >= 500;