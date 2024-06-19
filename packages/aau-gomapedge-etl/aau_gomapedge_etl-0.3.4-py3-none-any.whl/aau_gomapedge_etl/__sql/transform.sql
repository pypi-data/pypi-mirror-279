CREATE TEMP VIEW trip_view AS
    SELECT trip_id,
           trip_split_id,
           first(timestamp ORDER BY timestamp ASC)                                                        AS start_time,
           last(timestamp ORDER BY timestamp ASC)                                                         AS end_time,
           duration                                                                                       AS match_duration,
           epoch(last(timestamp ORDER BY timestamp ASC)) - epoch(first(timestamp ORDER BY timestamp ASC)) AS raw_duration,
           distance                                                                                       AS match_distance,
           count(point)                                                                                   AS point_cnt,
           max(speed) * 3.6                                                                               AS max_speed,
           min(speed) * 3.6                                                                               AS min_speed,
           avg(speed) * 3.6                                                                               AS avg_speed,
           max(accuracy)                                                                                  AS max_accuracy,
           min(accuracy)                                                                                  AS min_accuracy,
           avg(accuracy)                                                                                  AS avg_accuracy,
           max(altitude)                                                                                  AS max_altitude,
           min(altitude)                                                                                  AS min_altitude,
           avg(altitude)                                                                                  AS avg_altitude,
           ST_AsWKB(ST_StartPoint(geom))                                                                  AS match_start_point,
           ST_AsWKB(ST_EndPoint(geom))                                                                    AS match_end_point,
           first(ST_AsWKB(point) ORDER BY timestamp ASC)                                                  AS raw_start_point,
           last(ST_AsWKB(point) ORDER BY timestamp ASC)                                                   AS raw_end_point,
           ST_AsWKB(ST_MakeLine(LIST(point ORDER BY timestamp ASC)))                                      AS raw_trajectory,
           ST_AsWKB(geom)                                                                                 AS match_trajectory,
    FROM match
        INNER JOIN trip       USING (trip_id, trip_split_id)
        INNER JOIN trajectory USING (trip_id, img_seq_id)
    GROUP BY trip_id, trip_split_id, duration, distance, geom
    ORDER BY trip_id, trip_split_id;


CREATE TEMP VIEW user_view AS
    SELECT id AS user_id,
           creation_time,
           UNNEST(parse_user_agent(user_agent)),
           user_agent
    FROM user;
