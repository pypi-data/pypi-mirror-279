import concurrent.futures
from panoramaTool import APICall, PostRulesManager, ServiceManager
from panoramaTool.panorama_api.address_groups_manager import AddressGroupsManager
from panoramaTool.panorama_api.address_manager import AddressManager
from panoramaTool.panorama_api.service_groups_manager import ServiceGroupsManager


class BusinessLogic:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    @staticmethod
    def check_for_valid_session(request) -> bool:
        url = request.cookies.get('panorama_url')
        api_key = request.cookies.get('api_key')
        if url is None or api_key is None:
            return False
        valid = APICall.check_valid_key(panorama_url=url, api_key=api_key)
        return valid

    @staticmethod
    def make_concurrent_calls(request, function, csv):
        url = request.cookies.get('panorama_url')
        api_key = request.cookies.get('api_key')
        device_group = request.form.get('device-group') or 'shared'
        response = []
        faulty_response = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            data = []
            for csv_data in csv:
                futures.append(executor.submit(function, url, api_key, csv_data, device_group))
                data.append(csv_data)

            concurrent.futures.wait(futures)

            for counter, future in enumerate(futures):
                if "success" in str(future.result()):
                    response.append(future.result())
                else:
                    print((data[counter], future.result()))
                    faulty_response.append((data[counter], future.result()))
        return faulty_response

    @staticmethod
    def create_address(url, api_key, csv_data, device_group):
        address_manager = AddressManager(panorama_url=url, api_key=api_key, verify=False)
        return address_manager.create_address(
            name=csv_data.get('NAME').replace(" ", ""),
            ip=csv_data.get('IP ADDRESS').replace(" ", ""),
            cidr=csv_data.get('CIDR').replace(" ", "") or '32',
            description=csv_data.get('DESCRIPTION').replace(" ", "") or ''
        )

    @staticmethod
    def create_services(url, api_key, csv_data, device_group):
        service_manager = ServiceManager(panorama_url=url, api_key=api_key, verify=False)
        return service_manager.create_service(
            protocol=csv_data.get('PROTOCOL').replace(" ", ""),
            port=csv_data.get('DESTINATION PORT').replace(" ", ""),
            name=csv_data.get('NAME').replace(" ", "")
        )

    @staticmethod
    def create_address_groups(url, api_key, csv_data, device_group):
        address_groups_manager = AddressGroupsManager(panorama_url=url, api_key=api_key, verify=False)
        return address_groups_manager.create_address_group(
            name=csv_data.get('NAME').replace(" ", ""),
            members=csv_data.get('MEMBERS').replace(" ", ""),
            description=csv_data.get('DESCRIPTION').replace(" ", "")
        )

    @staticmethod
    def create_service_groups(url, api_key, csv_data, device_group):
        service_groups_manager = ServiceGroupsManager(panorama_url=url, api_key=api_key, verify=False)
        return service_groups_manager.create_service_group(
            device_group=device_group,
            name=csv_data.get('NAME').replace(" ", ""),
            members=csv_data.get('MEMBERS').replace(" ", "")
        )

    @staticmethod
    def create_security_post_rules(url, api_key, csv_data, device_group):
        security_post_rules_manager = PostRulesManager(panorama_url=url, api_key=api_key, verify=False)
        return security_post_rules_manager.create_post_rules(
            device_group=device_group,
            name=csv_data.get('NAME').lstrip(),
            action=csv_data.get('ACTION') or 'allow',
            description=csv_data.get('DESCRIPTION') or '',
            from_zone=csv_data.get('FROM') or 'any',
            source_group=csv_data.get('SOURCE') or 'any',
            to_zone=csv_data.get('TO').lstrip() or 'any',
            destination_group=csv_data.get('DESTINATION') or 'any',
            service=csv_data.get('SERVICE') or 'application-default',
            profile_type=csv_data.get('PROFILE TYPE') or 'group',
            profile=csv_data.get('PROFILE') or 'Alert-Only'
        )
