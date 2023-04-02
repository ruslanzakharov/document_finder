from sqlalchemy import String, Integer, Column, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db import Base


association_table = Table(
    'association_table',
    Base.metadata,
    Column('document_id', ForeignKey('document.id'), primary_key=True),
    Column('rubrics_id', ForeignKey('rubrics.id'), primary_key=True)
)


class Documents(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    creation_date = Column(DateTime)

    rubrics = relationship(
        'Rubrics',
        secondary=association_table,
        back_populates='documents'
    )


class Rubrics(Base):
    __tablename__ = 'rubrics'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    documents = relationship(
        'Documents',
        secondary=association_table,
        back_populates='rubrics'
    )
