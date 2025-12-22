from sqlalchemy.orm import Session
from app.models.query import Query
from app.schemas.query import QueryCreate

class CRUDQuery:
    def get_query(self, db: Session, query_id: int):
        return db.query(Query).filter(Query.id == query_id).first()

    def create_query(self, db: Session, *, query_in: QueryCreate, user_id: int):
        db_query = Query(**query_in.dict(), user_id=user_id)
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
        return db_query

query = CRUDQuery()
