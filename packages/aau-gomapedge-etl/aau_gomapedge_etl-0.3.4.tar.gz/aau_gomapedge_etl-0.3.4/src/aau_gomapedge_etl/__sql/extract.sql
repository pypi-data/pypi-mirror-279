CREATE SEQUENCE seq_model_id;


CREATE TABLE user (
    id            UUID PRIMARY KEY,
    creation_time TIMESTAMP,
    user_agent    TEXT
);

CREATE TABLE trajectory (
    trip_id           INT,
    img_seq_id        INT,
    user              UUID,
    timestamp         TIMESTAMP     CHECK (epoch(age(timestamp)) > 0),
    point             GEOMETRY,
    accuracy          REAL,
    altitude          REAL          CHECK (altitude >= -420 AND altitude <= 2900),
    altitude_accuracy REAL,
    heading           DECIMAL(5, 2) CHECK (heading <= 360 AND heading >= 0),
    speed             DECIMAL(5, 2) CHECK (speed < 500 AND speed >= 0),
    PRIMARY KEY (img_seq_id, trip_id)
);

CREATE TABLE address (
    trip_id        INT          NOT NULL,
    img_seq_id     INT          NOT NULL,
    country        VARCHAR(56),
    country_code   VARCHAR(3),
    region         VARCHAR(30),
    state          VARCHAR(30),
    state_district VARCHAR(30),
    county         VARCHAR(30),
    municipality   VARCHAR(30),
    city           VARCHAR(30),
    town           VARCHAR(30),
    village        VARCHAR(30),
    suburb         VARCHAR(30),
    house_number   VARCHAR(10),
    road           VARCHAR(50),
    postcode       VARCHAR(30),
    PRIMARY KEY (img_seq_id, trip_id)
);


CREATE TABLE model (
    model_id INT PRIMARY KEY DEFAULT nextval('seq_model_id'),
    name     VARCHAR(50),
    version  VARCHAR(20),
    size     VARCHAR(20),
    UNIQUE (name, version, size)
);


CREATE TABLE detection (
    trip_id      INT,
    img_seq_id   INT,
    obj_seq_id   INT,
    model_id     INT NOT NULL,
    user         UUID,
    timestamp    TIMESTAMP,
    x            INT,
    y            INT,
    width        INT,
    height       INT,
    img_width    INT,
    img_height   INT,
    device_cls   VARCHAR(50),
    device_score REAL,
    img          BLOB,
    PRIMARY KEY (trip_id, img_seq_id, obj_seq_id),
    FOREIGN KEY (model_id) REFERENCES model(model_id)
);


CREATE TABLE classification (
    trip_id    INT,
    img_seq_id INT,
    obj_seq_id INT,
    cls        VARCHAR(50),
    score      REAL,
    PRIMARY KEY (trip_id, img_seq_id, obj_seq_id)
);

CREATE TABLE trip (
    trip_id       INT,
    trip_split_id INT,
    confidence    REAL,
    distance      REAL,
    duration      REAL,
    geom          GEOMETRY,
    PRIMARY KEY (trip_id, trip_split_id)
);

CREATE TABLE match (
    trip_id          INT,
    img_seq_id       INT,
    trip_split_id    INT,
    distance_to_road REAL,
    match_point      GEOMETRY,
    PRIMARY KEY (trip_id, img_seq_id)
);