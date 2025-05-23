# !/usr/bin/env python
# -*- coding: utf-8 -*-

from cmdb.handlers.business_handler import biz_urls
from cmdb.handlers.cloud_handler import cloud_urls
from cmdb.handlers.template_handler import template_urls
from cmdb.handlers.dynamic_group_handler import dynamic_group_urls
from cmdb.handlers.dynamic_rule_handler import dynamic_rule_urls
from cmdb.handlers.events_handler import events_urls
from cmdb.handlers.asset_search_handler import search_urls
from cmdb.handlers.server_handler import server_urls
from cmdb.handlers.img_handler import img_urls
from cmdb.handlers.redis_handler import redis_urls
from cmdb.handlers.mysql_handler import mysql_urls
from cmdb.handlers.lb_handler import lb_urls
from cmdb.handlers.vpc_handler import vpc_urls
from cmdb.handlers.security_group_handler import security_group_urls
from cmdb.handlers.tree_handler import tree_urls
from cmdb.handlers.tag_handler import tag_urls
from cmdb.handlers.cloud_region_handler import cloud_region_urls
from cmdb.handlers.consul_handler import consul_urls
from cmdb.handlers.role_handler import role_urls
from cmdb.handlers.perm_group_handler import perm_group_urls
from cmdb.handlers.jms_handler import jms_urls
from cmdb.handlers.audit_handler import audit_urls
from cmdb.handlers.interface_handler import interface_urls
from cmdb.handlers.area_handler import area_urls
from cmdb.handlers.env_handler import env_urls
from cmdb.handlers.nat_handler import nat_urls
from cmdb.handlers.asset_switch_handler import switch_urls
from cmdb.handlers.secret import secret_urls
from cmdb.handlers.agent_handler import agent_urls
from cmdb.handlers.asset_mongodb_handler import mongodb_urls
from cmdb.handlers.asset_k8s_cluster_handler import cluster_urls

urls = []
urls.extend(biz_urls)
urls.extend(template_urls)
urls.extend(dynamic_group_urls)
urls.extend(dynamic_rule_urls)
urls.extend(cloud_urls)
urls.extend(events_urls)
urls.extend(search_urls)
urls.extend(server_urls)
urls.extend(img_urls)
urls.extend(mysql_urls)
urls.extend(redis_urls)
urls.extend(lb_urls)
urls.extend(vpc_urls)
urls.extend(security_group_urls)
urls.extend(tag_urls)
urls.extend(tree_urls)
urls.extend(cloud_region_urls)
urls.extend(consul_urls)
urls.extend(role_urls)
urls.extend(perm_group_urls)
urls.extend(jms_urls)
urls.extend(audit_urls)
urls.extend(interface_urls)
urls.extend(area_urls)
urls.extend(env_urls)
urls.extend(nat_urls)
urls.extend(switch_urls)
urls.extend(secret_urls)
urls.extend(agent_urls)
urls.extend(mongodb_urls)
urls.extend(cluster_urls)