# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  python-apollo
# FileName:     client.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/19
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
import json
import traceback
import threading
from apollo_proxy.helper import *

__all__ = ['ApolloClient']


class FactoryClient(object):

    def __init__(self, domain: str, app_id: str, cluster: str, secret: str = None, start_hot_update=True,
                 change_listener=None):

        # 核心路由参数
        self.cluster = cluster
        self.app_id = app_id
        self.secret = secret if secret else ''
        self.domain = domain

        # 非核心参数
        self.__ip = init_ip()

        # 私有控制变量
        self.__cycle_time = 2
        self.__stopping = False
        self.__cache = {}
        self.__no_key = {}
        self.__hash = {}
        self.__pull_timeout = 75
        self.__cache_file_path = get_project_path()
        self.__long_poll_thread = None
        self.__change_listener = change_listener  # "add" "delete" "update"
        self.__notification_map = {'application': -1}
        self.__last_release_key = None

        # 私有启动方法
        self.__path_checker()
        if start_hot_update:
            self.__start_hot_update()

        # 启动心跳线程
        heartbeat = threading.Thread(target=self.__heart_beat)
        # heartbeat.setDaemon(True)
        heartbeat.daemon = True
        heartbeat.start()

    def get_all_values(self, namespace='application'):
        namespace_data = self.__get_namespace_data(namespace)
        all_keys = namespace_data.get('configurations')
        return all_keys

    def get_value(self, key, default_val=None, namespace='application'):
        try:
            # 读取内存配置
            namespace_cache = self.__cache.get(namespace)
            val = get_value_from_dict(namespace_cache, key)
            if val is not None:
                return val

            no_key = no_key_cache_key(namespace, key)
            if no_key in self.__no_key:
                return default_val

            # 读取网络配置
            namespace_data = self.__get_json_from_net(namespace)
            val = get_value_from_dict(namespace_data, key)
            if val is not None:
                self.__update_cache_and_file(namespace_data, namespace)
                return val

            # 读取文件配置
            namespace_cache = self.__get_local_cache(namespace)
            val = get_value_from_dict(namespace_cache, key)
            if val is not None:
                self.__update_cache_and_file(namespace_cache, namespace)
                return val

            # 如果全部没有获取，则把默认值返回，设置本地缓存为None
            self.__set_local_cache_none(namespace, key)
            return default_val
        except Exception as e:
            logger.error("get_value has error, [key is %s], [namespace is %s], [error is %s], ", key, namespace, e)
            return default_val

        # 设置某个namespace的key为none，这里不设置default_val，是为了保证函数调用实时的正确性。
        # 假设用户2次default_val不一样，然而这里却用default_val填充，则可能会有问题。

    def __get_namespace_data(self, namespace):
        namespace_data = self.__cache.get(namespace)
        if not namespace_data:
            namespace_data = self.__get_local_cache(namespace)
        if not namespace_data:
            namespace_data = self.__get_json_from_net(namespace)
        if not namespace_data:
            namespace_data = None
        return namespace_data

    def __get_json_from_net(self, namespace='application'):
        url = '{}/configs/{}/{}/{}?releaseKey={}&ip={}'.format(self.domain, self.app_id, self.cluster, namespace,
                                                               "", self.__ip)
        try:
            code, body = http_request(url, timeout=3, headers=self.__sign_headers(url))
            if code == 200:
                data = json.loads(body)
                data = data["configurations"]
                return_data = {CONFIGURATIONS: data}
                return return_data
            else:
                logger.error(f"apollo接口<{url}>调用失败，原本：<code={code}, body={body}>")
                return None
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(str(e))
            return None

    def __set_local_cache_none(self, namespace, key):
        no_key = no_key_cache_key(namespace, key)
        self.__no_key[no_key] = key

    def __start_hot_update(self):
        self.__long_poll_thread = threading.Thread(target=self.__listener)
        # 启动异步线程为守护线程，主线程推出的时候，守护线程会自动退出。
        # self.__long_poll_thread.setDaemon(True)
        self.__long_poll_thread.daemon = True
        self.__long_poll_thread.start()

    def __call_listener(self, namespace, old_kv, new_kv):
        if self.__change_listener is None:
            return
        if old_kv is None:
            old_kv = {}
        if new_kv is None:
            new_kv = {}
        try:
            for key in old_kv:
                new_value = new_kv.get(key)
                old_value = old_kv.get(key)
                if new_value is None:
                    # 如果newValue 是空，则表示key，value被删除了。
                    self.__change_listener("delete", namespace, key, old_value)
                    continue
                if new_value != old_value:
                    self.__change_listener("update", namespace, key, new_value)
                    continue
            for key in new_kv:
                new_value = new_kv.get(key)
                old_value = old_kv.get(key)
                if old_value is None:
                    self.__change_listener("add", namespace, key, new_value)
        except BaseException as e:
            logger.warning(str(e))

    def __path_checker(self):
        if not os.path.isdir(self.__cache_file_path):
            if sys.version_info.major == 3:
                os.makedirs(self.__cache_file_path, exist_ok=True)
            else:
                os.makedirs(self.__cache_file_path)

        # 更新本地缓存和文件缓存

    def __update_cache_and_file(self, namespace_data, namespace='application'):
        # 更新本地缓存
        self.__cache[namespace] = namespace_data
        # 更新文件缓存
        new_string = json.dumps(namespace_data)
        new_hash = hashlib.md5(new_string.encode('utf-8')).hexdigest()
        if self.__hash.get(namespace) == new_hash:
            pass
        else:
            with open(os.path.join(self.__cache_file_path, '%s_configuration_%s.txt' % (self.app_id, namespace)),
                      'w') as f:
                f.write(new_string)
            self.__hash[namespace] = new_hash

        # 从本地文件获取配置

    def __get_local_cache(self, namespace='application'):
        cache_file_path = os.path.join(self.__cache_file_path, '%s_configuration_%s.txt' % (self.app_id, namespace))
        if os.path.isfile(cache_file_path):
            with open(cache_file_path, 'r') as f:
                result = json.loads(f.readline())
            return result
        return {}

    def __long_poll(self):
        notifications = []
        for key in self.__cache:
            namespace_data = self.__cache[key]
            notification_id = -1
            if NOTIFICATION_ID in namespace_data:
                notification_id = self.__cache[key][NOTIFICATION_ID]
            notifications.append({
                NAMESPACE_NAME: key,
                NOTIFICATION_ID: notification_id
            })
        try:
            # 如果长度为0直接返回
            if len(notifications) == 0:
                return
            url = '{}/notifications/v2'.format(self.domain)
            params = {
                'appId': self.app_id,
                'cluster': self.cluster,
                'notifications': json.dumps(notifications, ensure_ascii=False)
            }
            param_str = url_encode_wrapper(params)
            url = url + '?' + param_str
            code, body = http_request(url, self.__pull_timeout, headers=self.__sign_headers(url))
            http_code = code
            if http_code == 304:
                logger.error('No change, loop...')
                return
            if http_code == 200:
                data = json.loads(body)
                for entry in data:
                    namespace = entry[NAMESPACE_NAME]
                    n_id = entry[NOTIFICATION_ID]
                    logger.info("%s has changes: notificationId=%d", namespace, n_id)
                    self.__get_net_and_set_local(namespace, n_id, call_change=True)
                    return
            else:
                logger.warning('Sleep...')
        except Exception as e:
            logger.warning(str(e))

    def __get_net_and_set_local(self, namespace, n_id, call_change=False):
        namespace_data = self.__get_json_from_net(namespace)
        namespace_data[NOTIFICATION_ID] = n_id
        old_namespace = self.__cache.get(namespace)
        self.__update_cache_and_file(namespace_data, namespace)
        if self.__change_listener is not None and call_change:
            old_kv = old_namespace.get(CONFIGURATIONS)
            new_kv = namespace_data.get(CONFIGURATIONS)
            self.__call_listener(namespace, old_kv, new_kv)

    def __listener(self):
        logger.info('start long_poll')
        while not self.__stopping:
            self.__long_poll()
            time.sleep(self.__cycle_time)
        logger.info("stopped, long_poll")

        # 给header增加加签需求

    def __sign_headers(self, url):
        headers = {}
        if self.secret == '':
            return headers
        uri = url[len(self.domain):len(url)]
        time_unix_now = str(int(round(time.time() * 1000)))
        headers['Authorization'] = 'Apollo ' + self.app_id + ':' + signature(time_unix_now, uri, self.secret)
        headers['Timestamp'] = time_unix_now
        return headers

    def __heart_beat(self):
        while not self.__stopping:
            time.sleep(60 * 10)  # 10分钟
            for namespace in self.__notification_map:
                self.__do_heart_beat(namespace)

    def __do_heart_beat(self, namespace):
        url = '{}/configs/{}/{}/{}?ip={}'.format(self.domain, self.app_id, self.cluster, namespace,
                                                 self.__ip)
        try:
            code, body = http_request(url, timeout=3, headers=self.__sign_headers(url))
            if code == 200:
                data = json.loads(body)
                if self.__last_release_key == data["releaseKey"]:
                    return None
                self.__last_release_key = data["releaseKey"]
                data = data["configurations"]
                self.__update_cache_and_file(data, namespace)
            else:
                return None
        except Exception as e:
            logger.error(str(e))
            return None


class ApolloClient(object):
    __instance = None
    __lock = threading.Lock()
    __apollo_client = None

    # 单例模式
    def __new__(cls, *args, **kwargs):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super(ApolloClient, cls).__new__(cls)
        return cls.__instance

    def __init__(self, domain: str, app_id: str, secret: str, cluster: str = "default", namespace: str = "application"):
        self.__domain = domain
        self.__app_id = app_id
        self.__secret = secret
        self.__cluster = cluster
        self.__namespace = namespace
        self.__init_client()

    def __init_client(self):
        self.__apollo_client = FactoryClient(
            app_id=self.__app_id, secret=self.__secret, cluster=self.__cluster, domain=self.__domain
        )
        setattr(self.__apollo_client, "namespace", self.__namespace)

    @property
    def app_id(self) -> str:
        return self.__app_id

    @property
    def secret(self) -> str:
        return self.__secret

    @property
    def domain(self) -> str:
        return self.__domain

    @property
    def namespace(self) -> str:
        return self.__namespace

    @namespace.setter
    def namespace(self, namespace: str):
        self.__namespace = namespace
        setattr(self.__apollo_client, "namespace", self.__namespace)

    def get_value(self, key: str) -> t.Any:
        value = self.__apollo_client.get_value(key, namespace=self.__namespace)
        return ast.literal_eval(value) if is_json(value) is True else value

    def get_all_values(self) -> t.Any:
        value = self.__apollo_client.get_all_values(namespace=self.__namespace)
        return ast.literal_eval(value) if is_json(value) is True else value
