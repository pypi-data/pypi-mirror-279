# -*- coding: utf-8 -*-
import json
import logging
from typing import List, Set, Optional, Dict
from ..client.redis_client import Redis
from ..lib import cfg
from ..model.items import AuthUser, AuthApp

logger = logging.getLogger(__name__)
rds = Redis(redis_uri=cfg.get('AUTH_REDIS_URL', None), redis_db=cfg.get('AUTH_REDIS_DB', None)).client
default_expire = 43200


def save_cached_app(access_token: str, app: AuthApp, expire: int = None):
    if app:
        _expire = expire or default_expire
        rds.set(f'share:access:{access_token}', app.json(), ex=_expire)


def get_cached_user(access_token: str) -> Optional[AuthUser]:
    rs = rds.get(f'share:access:{access_token}')
    if rs:
        js_user = json.loads(rs)
        # 容错
        if isinstance(js_user, str):
            js_user = json.loads(js_user)
        # 特征验证（user对象需要有id字段）
        if js_user and js_user.get('id', None):
            user = AuthUser(**js_user)
            user.userName = js_user.get('username', '')
            return user

    return None


def get_cached_app(access_token: str) -> Optional[AuthApp]:
    rs = rds.get(f'share:access:{access_token}')
    if rs:
        js_app = json.loads(rs)
        # 容错
        if isinstance(js_app, str):
            js_app = json.loads(js_app)
        # 特征验证（APP对象需要有appId字段）
        if js_app and js_app.get('appId', None):
            app = AuthApp(**js_app)
            return app

    return None


def get_cached_access_dict(access_token: str) -> Optional[Dict]:
    rs = rds.get(f'share:access:{access_token}')
    if rs:
        item = json.loads(rs)
        # 容错
        if isinstance(item, str):
            item = json.loads(item)
        return item

    return None


def has_access(access_token: str) -> bool:
    return rds.exists(f'share:access:{access_token}')


def save_cached_permission(access_token: str, permissions: Set[str], expire: int = None):
    if permissions:
        key = f'share:permissions:{access_token}'
        for per in permissions:
            rds.sadd(key, per)
        _expire = expire or default_expire
        rds.expire(key, _expire)


def has_permission(access_token: str, permission: str) -> bool:
    # 后者兼容Java版本异常
    _key = f'share:permissions:{access_token}'
    return rds.sismember(_key, f'{permission}') or rds.sismember(_key, f'"{permission}"')


def get_cached_permission(access_token: str) -> List[str]:
    return rds.smembers(f'share:permissions:{access_token}')


def clean_cache(access_token: str):
    rds.delete(f'share:access:{access_token}')
    rds.delete(f'share:permissions:{access_token}')
