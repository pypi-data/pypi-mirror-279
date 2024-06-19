SELECT start_time,
       end_time,
       img_seq_id,
       x,
       y,
       width,
       height,
       img_width,
       img_height,
       device_cls,
       device_score,
       cls.cls                            AS etl_cls,
       cls.score                          AS etl_score,
       strftime(timestamp, '%Y%m%d')::INT AS date_no,
       strftime(timestamp, '%H%M%S')::INT AS time_no,
       model.name                         AS model_id,
       model.version                      AS model_version,
       model.size                         AS model_size,
       img                                AS crop,
       md5(hex(img))::UUID                AS crop_hash,
       user_view.*,
       trip_view.*
FROM detection
    INNER JOIN user_view                         ON user = user_id
    INNER JOIN match                             USING (trip_id, img_seq_id)
    INNER JOIN trip_view                         USING (trip_id, trip_split_id)
    INNER JOIN model                             USING (model_id)
    LEFT JOIN classification              AS cls USING (trip_id, img_seq_id, obj_seq_id)
WHERE match_distance >= 500;
