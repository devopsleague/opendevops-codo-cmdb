# -*- coding: utf-8 -*-
# @Author: Dongdong Liu
# @Date: 2024/9/23
# @Description: 区服环境
from sqlalchemy import Column, String, Integer, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

from models.base import TimeBaseModel

Base = declarative_base()


class EnvModels(TimeBaseModel):
    __tablename__ = 't_env_list'  # 环境列表
    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='自增ID')
    env_name = Column('env_name', String(100), comment='环境名称')
    env_no = Column("env_no", String(50), unique=True, index=True, comment='环境编号')
    env_tags = Column("env_tags", JSON, comment='环境标签', default=[])
    is_test = Column("is_test", Boolean, default=False, comment='是否测试环境')
    idip = Column("idip", String(50), comment='IDIP地址')
    app_id = Column("app_id", String(100), comment='应用ID')
    app_secret = Column("app_secret", String(500), comment='应用密钥')
    ext_info = Column('ext_info', String(1000), nullable=True, comment='扩展字段存String')
