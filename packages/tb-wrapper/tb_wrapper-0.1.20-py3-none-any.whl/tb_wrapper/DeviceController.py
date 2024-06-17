from tb_wrapper.handle_exception import *
from tb_wrapper.MainController import *
from typing import Dict, List


@handle_tb_wrapper_exception
class DeviceController(MainController):

    def __init__(self, tb_url=None, userfile=None, passwordfile=None, connection=None, token=None, refresh_token=None):
        super().__init__(tb_url, userfile, passwordfile, connection, token, refresh_token)

    def get_tenant_device(self, device_name):
        return self.tb_client.get_tenant_device(device_name)

    def check_device_exists_by_name(self, device_name):
        info_device = self.tb_client.get_tenant_device_infos(
            page_size=10000, page=0)
        found = False
        for info in info_device.data:
            if info.name == device_name:
                found = True
        return found

    def create_device_with_customer(self, device_profile_id, device_name, customer_obj_id):
        device = Device(
            name=device_name, device_profile_id=device_profile_id, customer_id=customer_obj_id)
        device = self.tb_client.save_device(device)
        return device

    def create_device_without_customer(self, device_profile_id, device_name):
        device = Device(name=device_name, device_profile_id=device_profile_id)
        device = self.tb_client.save_device(device)
        return device

    def save_device_attributes(self, device_id: DeviceId, scope: str, body: Dict):
        return self.tb_client.save_device_attributes(device_id, scope, body)

    def get_default_device_profile_info(self):
        return self.tb_client.get_default_device_profile_info()

    def save_device_telemetry(self, token, body):
        return self.tb_client.post_telemetry(token, body)

    def check_device_profile_exists_by_name(self, device_profile_name):
        info_device = self.tb_client.get_tenant_profile_infos(
            page_size=10000, page=0)
        found = False
        for info in info_device.data:
            if info.name == device_profile_name:
                found = True
        return found

    def create_device_with_credentials(self, body: Dict) -> Device:
        return self.tb_client.save_device_with_credentials(
            body)

    def get_device_profile_id(self, device_profile_name: str):
        device_profile = self.tb_client.get_device_profile_infos(
            page=0, page_size=10000, text_search=device_profile_name)

        return device_profile.data[0].id

    def create_device_profile(self, device_profile_name: str, transport_configuration: Dict, rulechain_id: RuleChainId, transport_type: str, profile_type: str, device_profile_id: DeviceProfileId = None) -> DeviceProfile:
        tenant_id = self.tb_client.get_user().tenant_id

        config = DeviceProfileData(**transport_configuration)
        if device_profile_id is None:
            device_profile = DeviceProfile(
                name=device_profile_name, tenant_id=tenant_id, description=device_profile_name, default_rule_chain_id=rulechain_id, profile_data=config, type=profile_type, transport_type=transport_type)
        else:
            device_profile = DeviceProfile(id=device_profile_id,
                                           name=device_profile_name, tenant_id=tenant_id, description=device_profile_name, default_rule_chain_id=rulechain_id, profile_data=config, type=profile_type, transport_type=transport_type)
        return self.tb_client.save_device_profile(device_profile)

    def delete_device_profile(self, device_profile_id: DeviceProfileId):
        return self.tb_client.delete_device_profile(device_profile_id)

    def delete_device(self, device_id: DeviceId):
        return self.tb_client.delete_device(device_id=device_id)

    def get_tenant_devices(self, page: int, page_size: int, active: bool = None, name: str = None, sort_by: str = None, sort_order: str = None) -> PageDataDeviceInfo:
        devices = self.tb_client.get_tenant_device_infos(
            page=page, page_size=page_size, active=active, sort_property=sort_by, sort_order=sort_order, text_search=name)
        return devices

    def get_customer_devices(self, customer_id: CustomerId, page: int, page_size: int, active: bool = None, name: str = None, sort_by: str = None, sort_order: str = None) -> PageDataDeviceInfo:

        devices = self.tb_client.get_customer_device_infos(
            customer_id=customer_id, page=page, page_size=page_size, active=active, sort_property=sort_by, sort_order=sort_order, text_search=name)
        return devices

    def get_device_profile_infobyId(self, device_profile_id: DeviceProfileId) -> DeviceProfileInfo:
        return self.tb_client.get_device_profile_info_by_id(device_profile_id)

    def get_device_profile_infoByName(self, device_profile_name: str) -> DeviceProfile:
        device_profile = None
        device_profiles = self.tb_client.get_device_profiles(
            page=0, page_size=1, text_search=device_profile_name)
        if len(device_profiles.data) == 0:
            device_profile = None
        else:
            device_profile = device_profiles.data[0]
        return device_profile

    def get_device_rulechainById(self, rulechain_id: RuleChainId) -> RuleChain:
        return self.tb_client.get_rule_chain_by_id(rulechain_id)

    def get_device_rulechain_infoByName(self, rulechain_name: str) -> RuleChain:
        rule_chain = None
        rule_chains = self.tb_client.get_rule_chains(
            page=0, page_size=1, text_search=rulechain_name)
        if len(rule_chains.data) == 0:
            rule_chain = None
        else:
            rule_chain = rule_chains.data[0]
        return rule_chain

    def get_device_credentials(self, device_id: DeviceId) -> DeviceCredentials:
        return self.tb_client.get_device_credentials_by_device_id(device_id)

    def get_device_info_byId(self, device_id: DeviceId) -> Device:
        return self.tb_client.get_device_by_id(device_id)

    def get_attributes_byScope(self, device_name: str, scope: str, keys: Optional[str] = None) -> Any:
        user = self.tb_client.get_user()
        user_type = user.authority
        if user_type == "TENANT_ADMIN":
            deviceId = self.get_tenant_device(device_name=device_name).id
        else:
            deviceId = self.get_customer_devices(
                user.customer_id.id, page=0, page_size=1, name=device_name).data[0].id
        return self.tb_client.get_attributes_by_scope(
            deviceId, scope=scope, keys=keys)
