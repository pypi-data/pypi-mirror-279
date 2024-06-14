#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/20 19:35
# @Author  : HEXU
# @File    : connect.py
# @Description :
import os
from redis.client import Redis
from redis.sentinel import Sentinel
from redis.cluster import RedisCluster, ClusterNode
from intelliw.utils.logger import _get_framework_logger
from intelliw.utils.redis import common

logger = _get_framework_logger()


class RedisConnect:
    def __init__(self, client_type, url, password, sentinel_password, mater_name, db, pool_size):
        try:
            self.redis_client = None
            self.type = client_type
            self.url = url
            self.password = password
            self.sentinel_password = sentinel_password
            self.mater_name = mater_name
            self.db = db
            self.pool_size = pool_size

            if not common.check_mode(self.type):
                logger.error("mode is not supported")
                return

            if self.type == "single":
                self.host, self.port = self.url.split(':')
                self.redis_client = Redis(host=self.host, port=self.port, db=self.db,
                                          password=self.password,
                                          decode_responses=False)
            elif self.type == "cluster":
                self.nodes = [
                    ClusterNode(host=x.split(':')[0], port=int(x.split(':')[1]))
                    for x in self.url.split(',')
                ]
                self.redis_client = RedisCluster(startup_nodes=self.nodes, decode_responses=False,
                                                 password=self.password)
            elif self.type == "sentinel":
                self.nodes = [(x.split(':')[0], int(x.split(':')[1])) for x in self.url.split(',')]
                self.redis_sentinel = Sentinel(self.nodes, sentinel_kwargs={'password': self.sentinel_password},
                                               socket_timeout=0.5)
                self.redis_client = self.redis_sentinel.master_for(self.mater_name, socket_timeout=0.5,
                                                                   password=self.password, db=self.db,
                                                                   decode_responses=False)

            self.redis_client.ping()
        except Exception as e:
            self.redis_client = None
            logger.error(e)

    def __del__(self):
        pass

