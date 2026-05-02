import psycopg2
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
conn.autocommit = True
cur = conn.cursor()


def get_or_create_player(username):
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    res = cur.fetchone()

    if res:
        return res[0]

    cur.execute(
        "INSERT INTO players (username) VALUES (%s) RETURNING id",
        (username,)
    )
    return cur.fetchone()[0]


def save_game(username, score, level):
    pid = get_or_create_player(username)
    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (pid, score, level))


def get_top():
    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)
    return cur.fetchall()


def get_best(username):
    cur.execute("""
        SELECT MAX(score)
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        WHERE p.username=%s
    """, (username,))
    res = cur.fetchone()[0]
    return res if res else 0