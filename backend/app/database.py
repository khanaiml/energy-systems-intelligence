from __future__ import annotations
import json
from datetime import datetime, timezone
from sqlalchemy import DateTime, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from .core import DATABASE_URL
class Base(DeclarativeBase): pass
class Run(Base):
    __tablename__="runs"
    id: Mapped[str]=mapped_column(String,primary_key=True)
    strategy: Mapped[str]=mapped_column(String)
    payload: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False}); Session=sessionmaker(engine); Base.metadata.create_all(engine)
def save(result):
    with Session() as db: db.add(Run(id=result["run_id"],strategy=result["strategy"],payload=json.dumps(result))); db.commit()
def list_runs():
    with Session() as db: return [{"run_id":r.id,"strategy":r.strategy,"created_at":r.created_at.isoformat()} for r in db.query(Run).order_by(Run.created_at.desc()).all()]
def get_run(run_id):
    with Session() as db:
        row=db.get(Run,run_id); return json.loads(row.payload) if row else None
def delete_run(run_id):
    with Session() as db:
        row=db.get(Run,run_id)
        if row: db.delete(row); db.commit(); return True
        return False
