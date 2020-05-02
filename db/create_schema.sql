CREATE TABLE cash_entity
(
  ce_code INTEGER NOT NULL PRIMARY KEY,
  ce_name TEXT NOT NULL,
  ce_type TEXT NOT NULL,
  parent_code INTEGER REFERENCES cash_entity (ce_code),
  x_coord TEXT NOT NULL,
  y_coord TEXT NOT NULL
);

COMMENT ON TABLE cash_entity IS 'Cash Entity';

CREATE TABLE shipments
(
    id INTEGER NOT NULL PRIMARY KEY,
    date date NOT NULL,
    point INTEGER[],
    length DECIMAL NOT NULL,
    cost DECIMAL NOT NULL
);

COMMENT ON TABLE shipments IS 'Shipments';

CREATE TABLE balance
(
    date date NOT NULL,
    code INTEGER NOT NULL REFERENCES cash_entity (ce_code),
    percent DECIMAL NOT NULL,
    PRIMARY KEY (date, code)
);

COMMENT ON TABLE balance IS 'Balance';


DROP TABLE cash_entity CASCADE;
DROP TABLE shipments;
DROP TABLE balance;
