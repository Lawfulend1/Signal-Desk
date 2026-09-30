"""Database retention excerpt; not a deletion-event integration."""
import json

def purge_community(db, before):
    # Snapshots retain market data and metadata, never raw post text after purge.
    with db:
        db.execute("DELETE FROM mentions WHERE created<?", (before,))
        for row in db.execute("SELECT id,payload FROM snapshots").fetchall():
            payload = json.loads(row["payload"])
            payload["posts"] = [p for p in payload.get("posts", []) if p["created_at"] >= before]
            db.execute("UPDATE snapshots SET payload=? WHERE id=?", (json.dumps(payload), row["id"]))
