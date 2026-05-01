"""SQLAlchemy database models for PequeLectores."""

from .database import Base

# Models will be defined here as the project grows
# Example:
# class Book(Base):
#     __tablename__ = "books"
#     
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     author = Column(String)
#     isbn = Column(String, unique=True, index=True)
#     cover_url = Column(String)
#     description = Column(Text)
#     genres = Column(JSON)  # Store genres as JSON array
#     created_at = Column(DateTime, default=datetime.utcnow)