from tb_wrapper.handle_exception import *
from tb_wrapper.MainController import *


@handle_tb_wrapper_exception
class AssetController(MainController):

    def __init__(self, tb_url=None, userfile=None, passwordfile=None, connection=None, token=None, refresh_token=None):
        super().__init__(tb_url, userfile, passwordfile, connection, token, refresh_token)

    def get_default_asset_profile_info(self):
        return self.tb_client.get_default_asset_profile_info()

    def create_asset(self, asset_profile_id: AssetProfileId, asset_name: str, customer_obj_id: CustomerId, asset_id: AssetId = None) -> Asset:
        if asset_id is None:
            asset = Asset(
                name=asset_name, asset_profile_id=asset_profile_id, customer_id=customer_obj_id)
        else:
            asset = Asset(id=asset_id, name=asset_name,
                          asset_profile_id=asset_profile_id, customer_id=customer_obj_id)
        asset = self.tb_client.save_asset(asset)
        return asset

    def create_asset_profile(self, profile_name: str) -> AssetProfile:
        tenant_id = self.tb_client.get_user().tenant_id
        asset_profile = AssetProfile(
            name=profile_name, description=profile_name, tenant_id=tenant_id)
        return self.tb_client.save_asset_profile(asset_profile)

    def check_asset_exists_by_name(self, asset_name: str) -> bool:
        found = False
        info_asset = self.tb_client.get_tenant_asset_infos(
            page_size=10000, page=0)
        for info in info_asset.data:
            if info.name == asset_name:
                found = True
                break
        return found

    def check_asset_profile_exists_by_name(self, profile_name: str) -> bool:
        found = False
        profiles = self.tb_client.get_asset_profiles(page=0, page_size=1000)
        for profile in profiles.data:
            if profile.name == profile_name:
                found = True
                break
        return found

    def get_asset_profile_by_name(self, profile_name: str) -> AssetProfile | None:
        profiles = self.tb_client.get_asset_profiles(page=0, page_size=1000)
        profile = None
        for profile in profiles.data:
            if profile.name == profile_name:
                return profile
        return profile

    def save_asset_attributes(self, asset_id: EntityId, scope: str, body: Dict):
        return self.tb_client.save_entity_attributes_v2(asset_id, scope, body)

    def get_tenant_asset(self, asset_name: str) -> Asset:
        return self.tb_client.get_tenant_asset(asset_name)

    def create_relation(self, from_id: EntityId, to_id: EntityId, relation_type: str) -> None | Any:
        relation = EntityRelation(_from=from_id, to=to_id, type=relation_type)
        relation = self.tb_client.save_relation(relation)
        return relation

    def delete_asset(self, asset_id: AssetId) -> None:
        return self.tb_client.delete_asset(asset_id)

    def get_asset_infoById(self, asset_id: AssetId) -> AssetInfo:
        return self.tb_client.get_asset_info_by_id(asset_id)