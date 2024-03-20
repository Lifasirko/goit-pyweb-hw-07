from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from datetime import datetime as dt
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimeBaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(DateTime(True),
                        default=func.now(),
                        onupdate=func.now(),
                        server_default=func.now())


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))


class Discipline(Base):
    __tablename__ = 'discipline'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    group_id = Column(Integer, ForeignKey("group.id"))


class Mark(TimeBaseModel):
    __tablename__ = 'mark'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer)
    name = Column(String(250))
    discipline_id = Column(Integer, ForeignKey("discipline.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
