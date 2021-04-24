CREATE TABLE events (
	event_id INTEGER NOT NULL,
	event_type VARCHAR(32),
	event_data TEXT,
	origin VARCHAR(32),
	time_fired DATETIME,
	created DATETIME,
	context_id VARCHAR(36),
	context_user_id VARCHAR(36), context_parent_id CHARACTER(36),
	PRIMARY KEY (event_id)
)
CREATE TABLE recorder_runs (
	run_id INTEGER NOT NULL,
	start DATETIME,
	"end" DATETIME,
	closed_incorrect BOOLEAN,
	created DATETIME,
	PRIMARY KEY (run_id),
	CHECK (closed_incorrect IN (0, 1))
)
CREATE TABLE schema_changes (
	change_id INTEGER NOT NULL,
	schema_version INTEGER,
	changed DATETIME,
	PRIMARY KEY (change_id)
)
CREATE TABLE states (
	state_id INTEGER NOT NULL,
	domain VARCHAR(64),
	entity_id VARCHAR(255),
	state VARCHAR(255),
	attributes TEXT,
	event_id INTEGER,
	last_changed DATETIME,
	last_updated DATETIME,
	created DATETIME,
	context_id VARCHAR(36),
	context_user_id VARCHAR(36), context_parent_id CHARACTER(36), old_state_id INTEGER,
	PRIMARY KEY (state_id),
	FOREIGN KEY(event_id) REFERENCES events (event_id)
)
CREATE TABLE sqlite_stat1(tbl,idx,stat)
CREATE INDEX ix_events_context_user_id ON events (context_user_id)
CREATE INDEX ix_events_event_type ON events (event_type)
CREATE INDEX ix_events_context_id ON events (context_id)
CREATE INDEX ix_events_time_fired ON events (time_fired)
CREATE INDEX ix_recorder_runs_start_end ON recorder_runs (start, "end")
CREATE INDEX ix_states_entity_id ON states (entity_id)
CREATE INDEX ix_states_context_user_id ON states (context_user_id)
CREATE INDEX ix_states_last_updated ON states (last_updated)
CREATE INDEX ix_states_event_id ON states (event_id)
CREATE INDEX ix_states_entity_id_last_updated ON states (entity_id, last_updated)
CREATE INDEX ix_states_context_id ON states (context_id)
CREATE INDEX ix_states_context_parent_id ON states (context_parent_id)
CREATE INDEX ix_events_context_parent_id ON events (context_parent_id)
