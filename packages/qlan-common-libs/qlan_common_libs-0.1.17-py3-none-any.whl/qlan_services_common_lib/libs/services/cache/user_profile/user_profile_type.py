
import logging
from qlan_services_common_lib.libs.services.cache.base import get_redis_client
import json
from datetime import timedelta

logger = logging.getLogger(__name__)
class UserProfileTypeCache:
    _PROFILE_TYPE = "profile_type_id_{}_{}"
    _USER_INFO = "user_info_{}_{}"

    def __init__(self, redis_url) -> None:
        self.client = get_redis_client(redis_url)
        super().__init__()

    def set_profile_type_id_cache(self, profile_id: int, profile_type: str, profile_type_id: int):
        logger.info(f"Adding cache for {self._PROFILE_TYPE.format(profile_id, profile_type)} :: {profile_type_id}")
        self.client.set(self._PROFILE_TYPE.format(profile_id, profile_type), profile_type_id)
        self.client.expire(self._PROFILE_TYPE.format(profile_id, profile_type), timedelta(days=1))
        
    def get_profile_type_id_cache(self,profile_id: int, profile_type: str) -> bytes:
        logger.info(f"Querying cache for {self._PROFILE_TYPE.format(profile_id, profile_type)}")
        return self.client.get(self._PROFILE_TYPE.format(profile_id, profile_type))
    
    def reset_profile_type_id_cache(self,profile_id: int, profile_type: str):
        self.client.unlink(self._PROFILE_TYPE.format(profile_id, profile_type))
     
    def set_user_info_cache(self, profile_id: int, profile_type: str, user_info: dict):
        logger.info(f"Adding cache for User Info{self._USER_INFO.format(profile_id, profile_type)}")
        self.client.set(self._USER_INFO.format(profile_id, profile_type), json.dumps(user_info))
        self.client.expire(self._USER_INFO.format(profile_id, profile_type), timedelta(days=1))
        
    def get_user_info_cache(self,profile_id: int, profile_type: str) -> dict:
        logger.info(f"Querying cache for {self._USER_INFO.format(profile_id, profile_type)}")
        user_cache = self.client.get(self._USER_INFO.format(profile_id, profile_type))
        user_info = None
        if  user_cache:
            user_info = json.loads(user_cache)
        return user_info
    
    def reset_user_info_cache(self,profile_id: int, profile_type: str):
        self.client.unlink(self._USER_INFO.format(profile_id, profile_type))