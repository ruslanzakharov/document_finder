from sqlalchemy import String, Integer, Column, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db import Base


association_table = Table(
    'association_table',
    Base.metadata,
    Column('document_id', ForeignKey('document.id'), primary_key=True),
    Column('rubric_id', ForeignKey('rubric.id'), primary_key=True)
)


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    creation_date = Column(DateTime)

    rubrics = relationship(
        'Rubric',
        secondary=association_table,
        back_populates='documents'
    )


class Rubric(Base):
    __tablename__ = 'rubric'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    documents = relationship(
        'Document',
        secondary=association_table,
        back_populates='rubrics'
    )
