-- Schema for the points table

CREATE TABLE IF NOT EXISTS points (
	track_id VARCHAR(255) NOT NULL,
	n INTEGER NOT NULL,
	lat REAL NOT NULL,
	lng REAL NOT NULL,
	height REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS points_track_id_idx ON points(track_id);

