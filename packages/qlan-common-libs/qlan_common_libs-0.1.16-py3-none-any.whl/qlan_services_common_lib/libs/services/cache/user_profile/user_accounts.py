"""
user_accounts.py
This module contains the UserAccountsCache class which is responsible for caching user accounts data
"""

import logging
from datetime import timedelta
from qlan_services_common_lib.libs.services.cache.base import get_redis_client

logger = logging.getLogger(__name__)

class UserAccountsCache:
    ORG_ACCOUNTS_CACHE = "org_accounts_cache_{}"
    TEAM_ACCOUNTS_CACHE = "team_accounts_cache_{}"
    USER_REFERRALS_CACHE = "user_referrals_cache_{}"
    QLAN_CREATOR_REFERRAL_CACHE = "influencer_refuser_{}"
    QLAN_CREATOR_COINS_CACHE = "influencer_ref_coins_{}"

    def __init__(self, redis_url) -> None:
        self.client = get_redis_client(redis_url)
        super().__init__()

    def set_org_accounts_cache(self, profile_id: int, org_data:str):
        logger.info(f"Adding cache for {self.ORG_ACCOUNTS_CACHE.format(profile_id)} :: {profile_id}")
        self.client.set(self.ORG_ACCOUNTS_CACHE.format(profile_id), org_data)
        self.client.expire(self.ORG_ACCOUNTS_CACHE.format(profile_id), timedelta(hours=2))
    
    def set_team_accounts_cache(self, profile_id: int,team_data:str):
        logger.info(f"Adding cache for {self.TEAM_ACCOUNTS_CACHE.format(profile_id)}")
        self.client.set(self.TEAM_ACCOUNTS_CACHE.format(profile_id), team_data)
        self.client.expire(self.TEAM_ACCOUNTS_CACHE.format(profile_id), timedelta(hours=2))
        
    def set_user_referrals_cache(self, profile_id: int,referral_data:str):
        logger.info(f"Adding cache for {self.USER_REFERRALS_CACHE.format(profile_id)}")
        self.client.set(self.USER_REFERRALS_CACHE.format(profile_id), referral_data)
        self.client.expire(self.USER_REFERRALS_CACHE.format(profile_id), timedelta(hours=2))

    def set_qlan_creator_referrals_cache(self, profile_id: int,referral_code:str):
        logger.info(f"Adding cache for {self.QLAN_CREATOR_REFERRAL_CACHE.format(profile_id)}")
        self.client.set(self.QLAN_CREATOR_REFERRAL_CACHE.format(profile_id), referral_code)
        self.client.expire(self.QLAN_CREATOR_REFERRAL_CACHE.format(profile_id), timedelta(hours=2))

    def set_qlan_creator_coins_cache(self, profile_id: int,referral_code:str):
        logger.info(f"Adding cache for {self.QLAN_CREATOR_COINS_CACHE.format(profile_id)}")
        self.client.set(self.QLAN_CREATOR_COINS_CACHE.format(profile_id), referral_code)
        self.client.expire(self.QLAN_CREATOR_COINS_CACHE.format(profile_id), timedelta(hours=2))

    def get_user_referrals_cache(self, profile_id: int):
        logger.info(f"Querying cache for {self.USER_REFERRALS_CACHE.format(profile_id)}")
        return self.client.get(self.USER_REFERRALS_CACHE.format(profile_id))
    
    def get_qlan_creator_referrals_cache(self, profile_id: int):
        logger.info(f"Querying cache for {self.QLAN_CREATOR_REFERRAL_CACHE.format(profile_id)}")
        return self.client.get(self.QLAN_CREATOR_REFERRAL_CACHE.format(profile_id))
    
    def get_qlan_creator_coins_cache(self, profile_id: int):
        logger.info(f"Querying cache for {self.QLAN_CREATOR_COINS_CACHE.format(profile_id)}")
        return self.client.get(self.QLAN_CREATOR_COINS_CACHE.format(profile_id))

    def get_org_accounts_cache(self,profile_id: int) -> bytes:
        logger.info(f"Querying cache for {self.ORG_ACCOUNTS_CACHE.format(profile_id)}")
        return self.client.get(self.ORG_ACCOUNTS_CACHE.format(profile_id))
    
    def get_team_accounts_cache(self,profile_id: int) -> bytes:
        logger.info(f"Querying cache for {self.TEAM_ACCOUNTS_CACHE.format(profile_id)}")
        return self.client.get(self.TEAM_ACCOUNTS_CACHE.format(profile_id))
    
    def reset_org_accounts_cache(self,profile_id: int):
        self.client.unlink(self.ORG_ACCOUNTS_CACHE.format(profile_id))
        logger.info(f"Resetting cache for {self.ORG_ACCOUNTS_CACHE.format(profile_id)}")
    
    def reset_team_accounts_cache(self,profile_id: int):
        self.client.unlink(self.TEAM_ACCOUNTS_CACHE.format(profile_id))
        logger.info(f"Resetting cache for {self.TEAM_ACCOUNTS_CACHE.format(profile_id)}")
     
    def reset_user_referrals_cache(self,profile_id: int):
        self.client.unlink(self.USER_REFERRALS_CACHE.format(profile_id))
        logger.info(f"Resetting cache for {self.USER_REFERRALS_CACHE.format(profile_id)}")

    def empty_org_accounts_cache(self, profile_id: int):
        logger.info(f"Deleting cache for {self.ORG_ACCOUNTS_CACHE.format(profile_id)} :: {profile_id}")
        self.client.unlink(self.ORG_ACCOUNTS_CACHE.format(profile_id))
   
    def empty_team_accounts_cache(self, profile_id: int):
        logger.info(f"Deleting cache for {self.TEAM_ACCOUNTS_CACHE.format(profile_id)}")
        self.client.unlink(self.TEAM_ACCOUNTS_CACHE.format(profile_id))