import sqlite3, json
db = sqlite3.connect("buffer.db")
cur = db.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS kv (
    k TEXT PRIMARY KEY,
    v BLOB           -- keep raw; or TEXT and store JSON
);

CREATE TABLE IF NOT EXISTS nodes (
    id   INTEGER PRIMARY KEY,
    data TEXT         -- JSON blob with arbitrary attrs
);

CREATE TABLE IF NOT EXISTS edges (
    src INTEGER,
    dst INTEGER,
    data TEXT,        -- edge attributes
    PRIMARY KEY (src, dst),
    FOREIGN KEY (src) REFERENCES nodes(id),
    FOREIGN KEY (dst) REFERENCES nodes(id)
);
""")
db.commit()

# put / get simple key‑value
cur.execute("REPLACE INTO kv(k,v) VALUES(?,?)", ("threshold", json.dumps(0.85)))
db.commit()
threshold = json.loads(cur.execute("SELECT v FROM kv WHERE k=?", ("threshold",)).fetchone()[0])

# add two nodes & an edge with attributes
n1 = cur.execute("INSERT INTO nodes(data) VALUES(?)", (json.dumps({"name":"A"}),)).lastrowid
n2 = cur.execute("INSERT INTO nodes(data) VALUES(?)", (json.dumps({"name":"B"}),)).lastrowid
cur.execute("INSERT INTO edges(src,dst,data) VALUES(?,?,?)",
            (n1, n2, json.dumps({"weight": 3.14})))
db.commit()

'''
Need traversal? For small/medium graphs, selecting edges recursively with SQLite recursive CTEs is fine:

WITH RECURSIVE walk(n) AS (
  SELECT :start_id
  UNION
  SELECT dst FROM edges, walk WHERE src = walk.n
)
SELECT n FROM walk;

'''