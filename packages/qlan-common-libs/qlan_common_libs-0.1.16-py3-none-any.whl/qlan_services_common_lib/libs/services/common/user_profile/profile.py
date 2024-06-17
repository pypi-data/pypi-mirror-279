"""
UserProfileUtils
 provides helper functions to fetch user profile data

"""
from qlan_services_common_lib.libs.services.cache.user_profile.user_profile_type import UserProfileTypeCache
from qlan_services_common_lib.libs.services.cache.user_profile.user_accounts import UserAccountsCache
from qlan_services_common_lib.libs.services.solr.userprofile import UserProfileSolrUtils

import logging
import json
import random
import phonenumbers

logger = logging.getLogger(__name__)

class UserProfileUtils:
    def __init__(
                self, dbsession, 
                 redis_url=None,
                 read_db = None, 
                 write_db=None, 
                 solr_client=None,
                 UserModel=None, 
                 UserProfileModel=None, 
                 ProfileTypeModel=None,
                 TeamModel=None,
                 OrganizationModel=None,
                 TeamMemberModel=None,
                 OrgMemberModel=None,
                 UserReferralModel=None
                 ) -> None:
        """
        param: dbsession :sqlalchemy.orm.session.Session (user profile db session)
        param: redis_url :str (redis connection url)
        param: read_db :sqlalchemy.orm.session.Session (read db session)
        param: write_db :sqlalchemy.orm.session.Session (write db session)
        """
        self.session = dbsession
        self.user_profile_type_cache = UserProfileTypeCache(redis_url)
        self.user_accounts_cache = UserAccountsCache(redis_url)
        self.user_profile_solr_utils = UserProfileSolrUtils(client=solr_client)
        self.solr_client = solr_client
        self.UserModel = UserModel 
        self.UserProfileModel = UserProfileModel 
        self.read_db = read_db
        self.write_db = write_db
        self.ProfileTypeModel= ProfileTypeModel 
        self.TeamModel = TeamModel
        self.OrganizationModel = OrganizationModel
        self.TeamMemberModel = TeamMemberModel
        self.OrgMemberModel = OrgMemberModel
        self.UserReferralModel = UserReferralModel
        super().__init__()

    def get_profile_type_id(self, profile_id, profile_type):
        """
            Cached: Get Profile type id
            returns: (int) profile_type_id 
        """
        if self.user_profile_type_cache.get_profile_type_id_cache(profile_id, profile_type) is None:
            logger.info(f"Profile type id not found in cache for {profile_id} with type {profile_type}")
            if not profile_id:
                raise ValueError("User profile id cannot be empty!")

            if profile_type not in ["org", "user", "team"]:
                profile_type = "user"

            logger.info(f"Fetching profile type id for {profile_id} with type {profile_type}: from DB")
            user_profile = self.session.query(self.ProfileTypeModel.id).filter(
                self.ProfileTypeModel.profile_id == profile_id,
                self.ProfileTypeModel.profile_type == profile_type,
            ).first()

            if not profile_type:
                raise ValueError("User not Found!")

            # Set Profile info in redis
            self.user_profile_type_cache.set_profile_type_id_cache(
                profile_id, profile_type, user_profile.id)
            logger.info(
                f"Adding profile type id for {profile_id} with type {profile_type}: Redis")

        # Return profile type id
        return int(self.user_profile_type_cache.get_profile_type_id_cache(profile_id, profile_type))

    def get_profile_type_info(self, profile_id, profile_type):
        """
        param: profile_id :int
        param: profile_type :String
        returns: dict (profile type info)
        """
        if profile_type == "org":
            ProfileModel = self.OrganizationModel
        elif profile_type == "team":
            ProfileModel = self.TeamModel
        else:
            ProfileModel = self.UserModel
            profile_type = "user"

        logger.info(f"Fetching profile type info for {profile_id} with type {profile_type}: from DB")
        return {
            "profile_id": profile_id,
            "profile_type": profile_type,
            "profile_type_id": self.get_profile_type_id(profile_id, profile_type),
            "profile_model": ProfileModel,
        }

    def get_user_details(self, profile_id, profile_type):
        """
        Fetches User info from Db or Redis 
        param: profile_id :int
        param: profile_type :String
        returns: user_info :(dict)
        """
        user_info = self.user_profile_type_cache.get_user_info_cache(profile_id, profile_type)
        if user_info is None:
            if profile_type in 'team':
                # RUN query here
                user_detail = self.session.query(
                    self.TeamModel.id,
                    self.TeamModel.user_name,
                    self.TeamModel.token,
                    self.TeamModel.mobile_number,
                    self.TeamModel.email,
                    self.TeamModel.redeemed_token,
                    self.TeamModel.available_token,
                    self.TeamModel.profile_image,
                    self.TeamModel.social_profile,
                    self.TeamModel.social_profile,
                    self.TeamModel.location,
                    self.TeamModel.giftable_section,
                ).filter(self.TeamModel.id == profile_id).first()
            elif profile_type == 'org':
                # RUN query here
                user_detail = self.session.query(
                    self.OrganizationModel.id,
                    self.OrganizationModel.user_name,
                    self.OrganizationModel.token,
                    self.OrganizationModel.mobile_number,
                    self.OrganizationModel.email,
                    self.OrganizationModel.redeemed_token,
                    self.OrganizationModel.available_token,
                    self.OrganizationModel.profile_image,
                    self.OrganizationModel.social_profile,
                    self.OrganizationModel.social_profile,
                    self.OrganizationModel.location,
                    self.OrganizationModel.giftable_section,
                ).filter(self.OrganizationModel.id == profile_id).first()

            else:
                # RUN query here
                user_detail = self.session.query(
                    self.UserModel.id,
                    self.UserModel.user_name,
                    self.UserModel.token,
                    self.UserModel.mobile_number,
                    self.UserModel.email,
                    self.UserModel.redeemed_token,
                    self.UserModel.available_token,
                    self.UserModel.giftable_section,
                    self.UserProfileModel.profile_image,
                    self.UserProfileModel.social_profile,
                    self.UserProfileModel.gender,
                    self.UserProfileModel.location,
                ).filter(self.UserModel.id == profile_id).join(self.UserProfileModel, 
                                                                 self.UserProfileModel.user_id == self.UserModel.id).first()

            if not user_detail:
                ValueError("User not Found!")

            user_info = {
                'id': user_detail[0],
                'user_name': user_detail[1],
                'token': user_detail[2],
                'mobile_number': user_detail[3],
                'email': user_detail[4],
                'redeemed_token': user_detail[5],
                'available_token': user_detail[6],
                'profile_image': user_detail[7],
                'social_profile': user_detail[8],
                'gender': user_detail[9],
                'location': user_detail[10]
            }
            logger.info(f"Setting User Details Cache for {profile_id} :: {profile_type}")
            self.user_profile_type_cache.set_user_info_cache(profile_id, profile_type, user_info)
        return user_info

    # Helper to Return Device tokens
    def get_device_tokens_for_user_types(self, user_lst):
        indiv_users = []
        squad_membrs = []
        org_membrs = []

        for user in user_lst:
            if user.profile_type == 'user':
                indiv_users.append(user.profile_id)
            elif user.profile_type == 'team':
                squad_membrs.append(user.profile_id)
            else:
                org_membrs.append(user.profile_id)

        # Individuals
        device_ids = []
        for device in self.session.query(self.UserModel.id, self.UserModel.device_id).filter(self.UserModel.id.in_(indiv_users)).all():
            if device.device_id:
                device_ids.extend(device.device_id)

        # Team Admins
        team_admins = self.session.query(self.TeamMemberModel.member_id).filter(
            self.TeamMemberModel.team_id.in_(squad_membrs)).all()

        users = self.session.query(self.UserModel).with_entities(
            self.UserModel.device_id, self.UserModel.id).filter(self.UserModel.id.in_(team_admins)).all()

        for device in users:
            if device.device_id and device.id not in indiv_users:
                device_ids.extend(device.device_id)

        # Org Admins
        org_admins = self.session.query(self.OrgMemberModel.member_id).filter(
            self.OrgMemberModel.org_id.in_(org_membrs)).all()

        users = self.session.query(self.UserModel).with_entities(self.UserModel.device_id, self.UserModel.id
                                                                            ).filter(self.UserModel.id.in_(org_admins))

        for device in users:
            if device.device_id and device.id not in indiv_users:
                device_ids.extend(device.device_id)

        return device_ids
    
    def get_user_following_data(self, profile_id: int, profile_type: str):
        """
        Fetchs User 'Following' Data
        param: profile_id (int)
        param: profile_type (string)
        returns: dict (following data)
        """
        user_data = self.solr_client.search(q=f'id:{profile_id}_{profile_type}', fl='following_count,followers_count')
        user_data = list(user_data)
        following_data = {}
        if user_data:
            following_data = user_data[0]
        else:
            following_data['following_count'] = 0
            following_data['followers_count'] = 0

        return following_data
    

    def get_user_orgs(self,profile_id:int):
        """
        Returns User 'Organizations'
        param: profile_id (Integer)
        """
        usr_org_accounts = self.user_accounts_cache.get_org_accounts_cache(profile_id)
        if usr_org_accounts is None:
            org_accounts_data = self.read_db.engine.execute("select org.id,org.name,org.user_name,org.profile_image from db_organizations as org left join db_org_members as org_members on org_members.org_id=org.id where org_members.is_admin=true and org_members.member_id=%s", [profile_id])
            org_accounts_data = [{'id': account.id,'name': account.name,'user_name': account.user_name,'profile_image': account.profile_image} for account in org_accounts_data]
            self.user_accounts_cache.set_org_accounts_cache(profile_id, json.dumps(org_accounts_data))
        return json.loads(self.user_accounts_cache.get_org_accounts_cache(profile_id))
    
    def get_user_teams(self,profile_id:int):
        """
        Returns User 'Teams'
        param: profile_id (Integer)
        """
        usr_team_accounts = self.user_accounts_cache.get_team_accounts_cache(profile_id)
        if usr_team_accounts is None:
            team_accounts_data = self.read_db.engine.execute("select team.id,team.org_id,team.name,team.user_name,team.profile_image from db_teams as team left join db_team_members as team_members on team_members.team_id=team.id where team_members.is_admin=true and team_members.member_id=%s", [profile_id])
            team_accounts_data = [{'id': account.id,'org_id': account.org_id,'name': account.name,'user_name': account.user_name,'profile_image': account.profile_image} for account in team_accounts_data]
            self.user_accounts_cache.set_team_accounts_cache(profile_id, json.dumps(team_accounts_data))
        return json.loads(self.user_accounts_cache.get_team_accounts_cache(profile_id))
    
    def get_random_user(self,user_names):
        if len(user_names) > 0:
            random_name = random.choice(user_names) 
        else:
            random_name = None 
        return random_name
    
    def get_segregated_mob_numbers_and_codes(self,mobile_numbs):
        mobnumb_data = {}
        mobnumb_data['user_mobile_numbs'] = [] 
        mobnumb_data['codes_with_plus'] = []
        mobnumb_data['codes_without_plus'] = []

        for mobile_no in mobile_numbs:
            mobile_number = mobile_no["mobile_number"]
            phone = phonenumbers.parse(mobile_number)
            code = phone.country_code
            mobile = str(phone.national_number)
            mobnumb_data['user_mobile_numbs'].append(mobile)

            if mobile_number.startswith('+'):
                code_with_plus = '+' + str(code) 
                mobnumb_data['codes_with_plus'].append(code_with_plus)
            else:
                code_without_plus = str(code) 
                mobnumb_data['codes_without_plus'].append(code_without_plus)
        return mobnumb_data

    def get_user_referrals(self,profile_id:int):
        """
        Fetch User 'Referrals'  
        param: profile_id (Integer)
        returns: List of (Referrals) dicts
        
        """
        user_referrals = self.user_accounts_cache.get_user_referrals_cache(profile_id)
        if user_referrals is None:
            users = self.read_db.session.query(self.UserReferralModel.user_id).filter_by(referred_by = profile_id).subquery()
            user_info = self.read_db.session.query(users,self.UserModel.name, self.UserProfileModel.profile_image, self.UserProfileModel.created_at)\
                                .join( self.UserModel,self.UserModel.id == users.c.user_id)\
                                .join(self.UserProfileModel, self.UserProfileModel.user_id == users.c.user_id)\
                                .all()
            user_referrals = [{
                    'user_id': user.user_id,
                    'name':user.name,
                    'profile_image': user.profile_image,
                    'created_at': user.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
                }for user in user_info]
            print(user_referrals)
            self.user_accounts_cache.set_user_referrals_cache(profile_id, json.dumps(user_referrals))
        return json.loads(self.user_accounts_cache.get_user_referrals_cache(profile_id))

    def get_user_identities(self,user_id:int):
        return self.user_profile_solr_utils.get_user_identities(user_id)
    
    def get_user_skills(self,user_id:int):
        return self.user_profile_solr_utils.get_user_skills(user_id)
    
    def get_user_langs(self,user_id:int):
        return self.user_profile_solr_utils.get_user_langs(user_id)
    
    def get_user_work_experience(self,user_id:int):
        return self.user_profile_solr_utils.get_user_work_experience(user_id)

    # Helper to Return Profile Type Id
    def get_profile_type_id_for_user_types(self, user_lst):
        indiv_users = []
        squad_membrs = []
        org_membrs = []

        for user in user_lst:
            if user.profile_type == 'user':
                indiv_users.append(user.profile_id)
            elif user.profile_type == 'team':
                squad_membrs.append(user.profile_id)
            else:
                org_membrs.append(user.profile_id)

        # Individuals
        profile_type_Ids = []
        for profile_type_id in self.session.query(self.ProfileTypeModel.id).filter(self.ProfileTypeModel.profile_id.in_(indiv_users)).all():
            if profile_type_id.id:
                profile_type_Ids.append(str(profile_type_id.id))

        # Team Admins
        team_admins = self.session.query(self.TeamMemberModel.member_id).filter(
            self.TeamMemberModel.team_id.in_(squad_membrs)).all()

        for profile_type_id in self.session.query(self.ProfileTypeModel.id).filter(self.ProfileTypeModel.profile_id.in_(team_admins),self.ProfileTypeModel.profile_type == "user").all():
            if profile_type_id.id:
                profile_type_Ids.append(str(profile_type_id.id))

        # Org Admins
        org_admins = self.session.query(self.OrgMemberModel.member_id).filter(
            self.OrgMemberModel.org_id.in_(org_membrs)).all()

        for profile_type_id in self.session.query(self.ProfileTypeModel.id).filter(self.ProfileTypeModel.profile_id.in_(org_admins),self.ProfileTypeModel.profile_type == "user").all():
            if profile_type_id.id:
                profile_type_Ids.append(str(profile_type_id.id))

        return profile_type_Ids

    def get_user_name_by_id(self,user_id,user_type):
        user_data = {}
        if  user_type == 'USER':
            user_info = self.UserModel.query.filter_by(id=user_id).first()
            user_data["user_type"] = user_type
            user_data["user_id"]  = str(user_info.id)
            user_data["user_name"] = user_info.user_name if user_info.user_name else "na"
        if user_type == "TEAM":
            user_info = self.TeamModel.query.filter_by(id=user_id).first()
            user_data['user_type'] = user_type
            user_data['user_id'] = str(user_info.id)
            user_data['user_name'] = user_info.user_name if user_info.user_name else "na"
        if  user_type == "ORG":
            user_info = self.OrganizationModel.query.filter_by(id=user_id).first()
            user_data['user_type'] = user_type
            user_data['user_id'] = str(user_info.id)
            user_data['user_name'] = user_info.user_name if user_info.user_name else "na"

        return user_data
