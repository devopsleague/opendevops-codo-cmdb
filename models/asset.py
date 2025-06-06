#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2023/2/15 14:59
Desc    : 基础资产Models
"""
from sqlalchemy import Column, String, Integer, Boolean, JSON, TEXT, UniqueConstraint, Date, Enum
from sqlalchemy.ext.declarative import declarative_base

from libs.utils import human_date
from models.base import TimeBaseModel

Base = declarative_base()


# 内网交换机角色枚举
class SwitchRole(Enum):
    CORE_SWITCH = 1  # 核心交换机
    AGG_SWITCH = 2  # 汇聚交换机
    ACCESS_SWITCH = 3  # 接入交换机
    POE_SWITCH = 4  # POE交换机
    WLC = 5  # 无线控制器


# 内网交换机状态枚举
class SwitchStatus(Enum):
    ONLINE = 1  # 在线
    OFFLINE = 2  # 离线
    REPAIRING = 3  # 维修中
    RETIRED = 4  # 下架

class AgentBindStatus:
    """Agent绑定状态"""
    NOT_BIND = 0 # 未绑定
    AUTO_BIND = 1 # 自动绑定
    MANUAL_BIND = 2 # 手动绑定


class AssetBaseModel(TimeBaseModel, Base):
    """资产模型基类"""
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True, info={'order': 'DESC'})
    cloud_name = Column('cloud_name', String(120), nullable=False, comment='云厂商名称', index=True)  # 云厂商信息
    account_id = Column('account_id', String(120), nullable=False, index=True, comment='AccountID')  # 账号信息
    instance_id = Column('instance_id', String(120), unique=True, nullable=False, comment='实例ID,唯一ID')
    region = Column('region', String(120), comment='地域')  # 位置信息
    zone = Column('zone', String(120), comment='可用区id')  # 位置信息
    is_expired = Column('is_expired', Boolean(), default=False, comment='True表示已过期')
    ext_info = Column('ext_info', JSON(), comment='扩展字段存JSON')


class AssetServerModels(AssetBaseModel):
    """"基础主机"""
    __tablename__ = 't_asset_server'  # server 基础主机
    name = Column('name', String(250), comment='实例名称', index=True)
    # hostname = Column('hostname', String(180), nullable=False, comment='主机名')
    inner_ip = Column('inner_ip', String(120), comment='内网IP', index=True)
    outer_ip = Column('outer_ip', String(120), comment='外网IP')
    outer_biz_addr = Column('outer_biz_addr', String(255), comment='业务出口地址')
    state = Column('state', String(30), comment='主机状态', index=True)
    agent_id = Column('agent_id', String(160), index=True, comment='AgentID')
    agent_status = Column('agent_status', String(20), index=True, default='1', comment='Agent状态')  # 1在线 2离线
    agent_info = Column('agent_info', JSON(), comment='agent上报信息字段存JSON', default={})
    is_product = Column("is_product", Integer, default=0, comment="标记是否上线", index=True)
    ownership = Column('ownership', String(120), default="内部", nullable=False, comment='归属')
    vpc_id = Column('vpc_id', String(120), comment='VPC ID')
    tags = Column('tags', JSON(), comment='标签')
    agent_bind_status = Column('agent_bind_status', Integer, default=AgentBindStatus.NOT_BIND, comment='绑定状态')
    has_main_agent = Column('has_main_agent', Boolean(), default=False, comment="是否有主Agent")
    # 联合键约束 2023年5月23日 添加关机支持
    # __table_args__ = (
    #     UniqueConstraint('region', 'inner_ip', 'state', 'is_expired', name='host_key'),
    # )


class AssetImagesModels(AssetBaseModel):
    """"基础镜像"""
    __tablename__ = 't_asset_image'  # image 基础系统镜像
    name = Column('name', String(250), comment='名称', index=True)
    image_type = Column('image_type', String(120), comment='系统类型', index=True)
    image_size = Column('image_size', String(120), comment='镜像硬盘')
    os_platform = Column('os_platform', String(255), comment='系统平台')
    os_name = Column('os_name', String(255), comment='系统名称')
    arch = Column('arch', String(30), comment='架构', index=True)
    state = Column('state', String(30), comment='镜像状态', index=True)
    description = Column('description', String(250), nullable=False, comment='备注')


class AssetMySQLModels(AssetBaseModel):
    """"基础数据库"""
    __tablename__ = 't_asset_mysql'  # MySQL 数据库
    name = Column('name', String(180), nullable=False, comment='名称', index=True)
    state = Column('state', String(50), comment='状态', index=True)
    db_class = Column('db_class', String(120), comment='类型/规格')
    db_engine = Column('db_engine', String(120), comment='引擎mysql/polardb')
    db_version = Column('db_version', String(120), comment='MySQL版本')
    db_address = Column('db_address', JSON(), comment='json地址')


class AssetRedisModels(AssetBaseModel):
    """基础Redis"""
    __tablename__ = 't_asset_redis'
    name = Column('name', String(180), nullable=False, comment='实例名称')
    state = Column('state', String(50), index=True, comment='状态')
    instance_class = Column('instance_class', String(120), comment='类型/规格')
    instance_arch = Column('instance_arch', String(120), comment='Arch 集群/标准')
    instance_type = Column('instance_type', String(120), comment='Redis/Memcache')
    instance_version = Column('instance_version', String(120), comment='版本')
    instance_address = Column('instance_address', JSON(), comment='json地址')


class AssetLBModels(AssetBaseModel):
    __tablename__ = 't_asset_lb'  # 负载均衡
    name = Column('name', String(255), nullable=False, comment='实例名称')
    type = Column('type', String(120), comment='LB类型, SLB/ALB/NLB')
    state = Column('state', String(120), comment='状态')
    dns_name = Column('dns_name', String(255), comment='DNS解析记录 7层有')
    lb_vip = Column('lb_vip', String(255), comment='vip')
    endpoint_type = Column('endpoint_type', String(255), comment='标记内网/外网')


class AssetEIPModels(AssetBaseModel):
    """弹性公网"""
    __tablename__ = 't_asset_eip'

    name = Column('name', String(128), nullable=True, index=True, comment='实例名称')
    address = Column('address', String(80), index=True, nullable=True, comment='IP地址')
    state = Column('state', String(80), index=True, nullable=True, comment='实例状态')
    bandwidth = Column('bandwidth', Integer, comment='带宽值')
    charge_type = Column('charge_type', String(20), default='Other', comment='实例计费方式')
    internet_charge_type = Column('internet_charge_type', String(20), index=True, default='Other',
                                  comment='网络计费方式')

    binding_instance_id = Column('binding_instance_id', String(80), comment='绑定实例ID')
    binding_instance_type = Column('binding_instance_type', String(80), comment='绑定实例类型')


class AssetUserFieldModels(TimeBaseModel):
    """基础Redis"""
    __tablename__ = 't_user_fields'  # server 基础主机
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column('user_name', String(120), nullable=False, comment='用户名')
    user_type = Column('user_type', String(120), comment='资产类型')
    user_fields = Column('user_fields', TEXT(), comment='收藏字段')
    # 联合键约束
    __table_args__ = (
        UniqueConstraint('user_name', 'user_type', name='user_field_key'),
    )


class AssetVPCModels(AssetBaseModel):
    """VPC"""
    __tablename__ = 't_asset_vpc'  # VPC
    id = Column(Integer, primary_key=True, autoincrement=True)
    vpc_name = Column('vpc_name', String(120), nullable=False, comment='VPC名称')
    cidr_block_v4 = Column('cidr_block_v4', String(255), index=True, comment='网段V4')
    cidr_block_v6 = Column('cidr_block_v6', String(255), index=True, comment='网段V6')
    vpc_router = Column('vpc_router', String(255), comment='路由表')
    vpc_switch = Column('vpc_switch', String(1000), comment='交换机')
    is_default = Column('is_default', Boolean(), default=False, comment='是否是默认')
    state = Column('state', String(80), index=True, default='运行中', comment='实例状态')


class AssetVSwitchModels(AssetBaseModel):
    """交换机"""
    __tablename__ = 't_asset_vswitch'  # VSwitch
    id = Column(Integer, primary_key=True, autoincrement=True)
    vpc_id = Column('vpc_id', String(120), index=True, nullable=False, comment='VPC ID')
    vpc_name = Column('vpc_name', String(120), nullable=False, comment='VPC名称')

    name = Column('name', String(120), nullable=False, comment='虚拟交换机的名称')
    cidr_block_v4 = Column('cidr_block_v4', String(255), index=True, comment='网段V4')
    cidr_block_v6 = Column('cidr_block_v6', String(255), index=True, comment='网段V6')
    address_count = Column('address_count', String(80), comment='可用的IP地址数量')
    route = Column('route', String(255), comment='网关')
    route_id = Column('route_id', String(255), comment='路由表')
    description = Column('description', String(255), comment='交换机的描述信息')
    cloud_region_id = Column('cloud_region_id', String(50), comment='云区域ID，后置变更')
    is_default = Column('is_default', Boolean(), default=False, comment='是否是默认')
    state = Column('state', String(80), index=True, default='运行中', comment='实例状态')


class AssetSwitchModels(TimeBaseModel, Base):
    """内网交换机"""
    __tablename__ = "t_asset_switch"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(64), comment="设备名称", default="")
    manage_ip = Column("manage_ip", String(39), unique=True, comment="管理IP", default="")
    sn = Column("sn", String(64),  unique=True, comment="序列号")
    mac_address = Column("mac_address", String(17), unique=True, comment="MAC地址", default="")
    vendor = Column("vendor", String(64), comment="厂商", default="")
    model = Column("model", String(255), comment="型号", default="")
    idc = Column("idc", String(64), index=True, comment="机房", default="")
    rack = Column("rack", String(64), comment="机柜", default="")
    position = Column("position", String(64), comment="U位", default="")
    role = Column("role", String(64), index=True, comment="角色", default="")
    status = Column("status", String(64), index=True,comment='状态', default="")
    description = Column("description", String(64), comment="备注", default="")
    

class SecurityGroupModels(AssetBaseModel):
    """安全组"""
    __tablename__ = 't_asset_security_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vpc_id = Column('vpc_id', String(120), index=True, default='', comment='VPC ID')
    security_group_name = Column('security_group_name', String(120), nullable=False, comment='安全组名')
    security_group_type = Column('security_group_type', String(120), default='normal', comment='安全组类型')
    security_info = Column('security_info', JSON(), comment='安全组规则存JSON')
    ref_info = Column('ref_info', JSON(), comment='安全组关联存JSON')
    description = Column('description', String(255), default='', comment='详情简介')
    state = Column('state', String(80), index=True, default='运行中', comment='实例状态')


class AssetBackupModels(TimeBaseModel):
    """资产备份"""
    __tablename__ = 't_asset_backup'
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column('asset_id', Integer, comment='资产ID')
    name = Column('name', String(128), default='', comment='名称')
    inner_ip = Column('inner_ip', String(64), default='', comment="IP")
    instance_id = Column('instance_id', String(128), default='', comment="实例ID")
    data = Column('data', JSON(), comment='数据')
    asset_type = Column('asset_type', String(32), default='', comment="资产类型")
    created_day = Column(Date, default=human_date(), comment="日期")


class AssetNatModels(AssetBaseModel):
    """NAT网关"""
    __tablename__ = 't_asset_nat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(128), nullable=False, comment='名称')
    state = Column('state', String(50), index=True, comment='状态')
    network_type = Column('network_type', String(50), comment='网络类型')
    outer_ip = Column('outer_ip', JSON(), comment='外网IP', default=[])
    network_type = Column('network_type', String(50), comment='网络类型')
    charge_type = Column('charge_type', String(50), comment='计费类型')
    subnet_id = Column('subnet_id', String(50), comment='子网ID')
    project_name = Column('project_name', String(50), comment='项目名称')
    vpc_id = Column('vpc_id', String(50), comment='VPC ID')
    description = Column('description', String(255), comment='描述信息')
    spec = Column('spec', String(50), comment='规格')
    network_interface_id = Column('network_interface_id', String(50), comment='网络接口ID')


class AssetClusterModels(AssetBaseModel):
    """集群"""
    __tablename__ = 't_asset_cluster'
    name = Column('name', String(120), nullable=False, comment='集群名称')
    state = Column('state', String(50), comment='状态')
    version = Column('version', String(50), comment='版本')
    vpc_id = Column('vpc_id', String(50), comment='VPC ID')
    inner_ip =  Column('inner_ip', String(50), comment='APIServer内网IP')
    outer_ip =  Column('outer_ip', String(50), comment='APIServer内网IP外网IP')
    description = Column('description', String(255), comment='描述信息')
    cluster_type = Column('cluster_type', String(50), comment='集群类型')
    total_node = Column('total_node', Integer, comment='节点总数')
    total_running_node = Column('total_running_node', Integer, comment='运行节点数')
    tags = Column('tags', JSON(), comment='标签')
    cidr_block_v4 = Column('cidr_block_v4', JSON(), comment='服务网段')
    ext_info = Column('ext_info', JSON(), comment='扩展字段存JSON')


class AssetMongoModels(AssetBaseModel):
    """Mongo"""
    __tablename__ = 't_asset_mongo'
    name = Column('name', String(120), nullable=False, comment='实例名称')
    state = Column('state', String(50), index=True, comment='状态')
    db_class = Column('db_class', String(120), comment='类型/规格')
    db_version = Column('db_version', String(120), comment='MongoDB版本')
    db_address = Column('db_address', JSON(), comment='连接地址')
    project_name = Column('project_name', String(50), comment='项目名称')
    vpc_id = Column('vpc_id', String(50), comment='VPC ID')
    subnet_id = Column('subnet_id', String(50), comment='子网ID')
    tags = Column('tags', JSON(), comment='标签')
    storage_type = Column('storage_type', String(50), comment='存储类型')
