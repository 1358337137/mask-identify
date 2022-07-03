from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  # 预配置范围的会话(session),代替connect执行数据库操作

# 创建数据库引擎
engine = create_engine("mysql+pymysql://root:Key1999...@43.138.26.63:3306/flask_db",
                       isolation_level="READ UNCOMMITTED", pool_size=200, pool_pre_ping=True)
# 创建一个基类来继承
Base = declarative_base(engine)
session = sessionmaker(engine)()


# 1. 创建一个ORM模型，这个ORM模型必须继承自sqlalchemy给我们提供好的基类
class User(Base):
    # 表名
    __tablename__ = 'user'
    # 2. 在这个ORM模型中创建一些属性，来跟表中的字段进行一一映射，这些属性必须是sqlalchemy提供好的数据类型
    # 设定id为Int，主键， 自增长
    id = Column(Integer, primary_key=True, autoincrement=True)
    # String类型需要指定长度
    username = Column(String(50))
    password = Column(String(50))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Student(Base):
    # 表名
    __tablename__ = 'student'
    # 2. 在这个ORM模型中创建一些属性，来跟表中的字段进行一一映射，这些属性必须是sqlalchemy提供好的数据类型
    # 设定id为Int，主键， 自增长
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    # String类型需要指定长度
    student_number = Column(String(20))
    name = Column(String(20))
    student_phone = Column(String(20))
    teacher = Column(String(20))
    teacher_phone = Column(String(20))

    major_id = Column(Integer)
    institute_id = Column(Integer)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    # #  __repr__方法用于输出该类的对象被print()时输出的字符串
    # def __repr__(self):
    #     return "<Student(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)
    #     return "<Student>{}:{}".format(self.student_id,self.student_number,self.name,self.student_phone,self.teacher,self.teacher_phone)


# 违规记录
class Record(Base):
    # 表名
    __tablename__ = 'record'
    # 2. 在这个ORM模型中创建一些属性，来跟表中的字段进行一一映射，这些属性必须是sqlalchemy提供好的数据类型
    # 设定id为Int，主键， 自增长
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    # String类型需要指定长度
    student_number = Column(String(20))
    name = Column(String(20))
    student_id = Column(Integer)
    image_url = Column(String(255))
    create_time = Column(String(40))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 学院
class Institute(Base):
    __tablename__ = 'institute'
    institute_id = Column(Integer, primary_key=True, autoincrement=True)
    institute_name = Column(String(20))
    major_num = Column(Integer)
    profile = Column(String(200))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 专业，类似于班级
class Major(Base):
    __tablename__ = 'major'
    major_id = Column(Integer, primary_key=True, autoincrement=True)
    institute_id = Column(Integer)
    major_name = Column(String(20))
    student_num = Column(Integer)
    profile = Column(String(200))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 3.将创建好的ORM模型映射到数据库中

Base.metadata.create_all()
