import python_sdk_remote.utilities as utilities
import requests
from language_remote.lang_code import LangCode
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from url_remote.action_name_enum import ActionName
from url_remote.component_name_enum import ComponentName
from url_remote.entity_name_enum import EntityName
from url_remote.our_url import OurUrl
from user_context_remote.user_context import UserContext

# TODO Let's use enum const and array from Components Package
GROUP_REMOTE_COMPONENT_ID = 213
GROUP_PROFILE_COMPONENT_NAME = "Group Remote Python"
DEVELOPER_EMAIL = "yarden.d@circ.zone"

GROUP_REMOTE_PYTHON_LOGGER_CODE_OBJECT = {
    'component_id': GROUP_REMOTE_COMPONENT_ID,
    'component_name': GROUP_PROFILE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'component_type': LoggerComponentEnum.ComponentType.Remote.value,
    "developer_email": DEVELOPER_EMAIL
}

# TODO Please use the array per environment in Url Remote Package
GROUP_REMOTE_API_VERSION = 1


# Server GroupDto:
#     id: string="0";
#     number: string="0";
#     itemType?:string="0";
#     title: string;
#     titleLangCode: string="en";
#     parentGroupId: string=null;
#     sequence: number;
#     isInterest: boolean=null;
#     image?: string;
#     childrenGroups?: GroupDto[];
#     isTestData?:boolean;

# TODO: refactor - reuse the same code for all the methods
class GroupsRemote(metaclass=MetaLogger, object=GROUP_REMOTE_PYTHON_LOGGER_CODE_OBJECT):

    def __init__(self, is_test_data: bool = False) -> None:
        self.our_url = OurUrl()
        self.user_context = UserContext()
        self.is_test_data = is_test_data

    def get_all_groups(self, lang_code: LangCode = None):  # GET

        query_params = {"langCode": self._get_lang_code_str(lang_code)}

        try:
            get_all_group_url = self.our_url.endpoint_url(
                brand_name=utilities.get_brand_name(),
                environment_name=utilities.get_environment_name(),
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.GET_ALL_GROUPS.value,  # "getAllGroups",
                query_parameters=query_params
            )

            self.logger.info("Endpoint group remote - getAllGroups action", object={
                'get_all_group_url': get_all_group_url, 'query_params': query_params})
            user_jwt = self.user_context.get_user_jwt()
            header = utilities.create_authorization_http_headers(user_jwt)
            get_all_groups_response = requests.get(get_all_group_url, headers=header)
            # TODO Call a function to process the response, if response status = 500 display the url and raise exception
            self.logger.end(
                "group-main-remote-restapi-python-package get_all_groups()",
                object={'get_all_groups_response': get_all_groups_response})
            return get_all_groups_response

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise exception
        except requests.Timeout as exception:
            self.logger.exception(
                "Timeout Exception- Request timed out", object={'exception': exception})
            raise exception
        except requests.RequestException as exception:
            self.logger.exception((
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise exception
        except Exception as exception:
            self.logger.exception((
                f"An unexpected error occurred: {str(exception)}", exception))
            raise exception

    # TODO I wish we can change groupName: GroupName (so group name will no be from type str but from GroupName type/class)
    def get_group_by_group_name(self, group_name: str, lang_code: LangCode = None):  # GET
        query_params = {"langCode": self._get_lang_code_str(lang_code),
                        "name": group_name, "isTestData": self.is_test_data}
        try:
            url = self.our_url.endpoint_url(
                brand_name=utilities.get_brand_name(),
                environment_name=utilities.get_environment_name(),
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.GET_GROUP_BY_NAME.value,  # "getGroupByName",
                query_parameters=query_params
            )

            self.logger.info(
                "Endpoint group remote - getGroupByName action: " + url)
            user_jwt = self.user_context.get_user_jwt()
            header = utilities.create_authorization_http_headers(user_jwt)
            get_group_by_name_response = requests.get(url, headers=header)
            # TODO Call a function to process the response, if response status = 500 display the url and raise exception

            return get_group_by_name_response

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise exception
        except requests.Timeout as exception:
            self.logger.exception(
                "Timeout Exception- Request timed out", object={'exception': exception})
            raise exception
        except requests.RequestException as exception:
            self.logger.exception((
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise exception
        except Exception as exception:
            self.logger.exception((
                f"An unexpected error occurred: {str(exception)}", exception))
            raise exception

    def get_group_by_profile_id(self, profile_id: int = None, lang_code: LangCode = None):  # GET

        profile_id = profile_id or self.user_context.get_effective_profile_id()
        query_params = {"langCode": self._get_lang_code_str(lang_code), "profileId": profile_id}

        try:
            url = self.our_url.endpoint_url(
                brand_name=utilities.get_brand_name(),
                environment_name=utilities.get_environment_name(),
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name="getGroupsByProfileId",  # TODO: use ActionName.GET_GROUPS_BY_PROFILE_ID.value once ready
                query_parameters=query_params,
            )

            self.logger.info(
                "Endpoint group remote - getGroupByName action: ", object={"url": url, "query_params": query_params})
            user_jwt = self.user_context.get_user_jwt()
            header = utilities.create_authorization_http_headers(user_jwt)
            get_group_by_name_response = requests.get(url, headers=header)
            # TODO Call a function to process the response, if response status = 500, display the url and raise exception
            # Example: of response.json() :
            # {"message": "", "success": true, "data": [
            #     {"groupId": "24", "number": "24", "title": "פעילות מתיחות", "sequence": null, "isInterest": 1,
            #      "image": "GroupImage", "childrenGroups": []},
            #     {"groupId": "21", "number": "21", "title": "טי אר אקס 2", "sequence": null, "isInterest": 1,
            #      "image": "GroupImage", "childrenGroups": []},
            #      ...]}
            return get_group_by_name_response

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise exception
        except requests.Timeout as exception:
            self.logger.exception(
                "Timeout Exception- Request timed out", object={'exception': exception})
            raise exception
        except requests.RequestException as exception:
            self.logger.exception((
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise exception
        except Exception as exception:
            self.logger.exception((
                f"An unexpected error occurred: {str(exception)}", exception))
            raise exception

    def get_group_by_group_id(self, group_id: int, lang_code: LangCode = None):  # GET
        try:
            url = self.our_url.endpoint_url(
                brand_name=utilities.get_brand_name(),
                environment_name=utilities.get_environment_name(),
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.GET_GROUP_BY_ID.value,
                path_parameters={'groupId': str(group_id)},
                query_parameters={"langCode": self._get_lang_code_str(lang_code),
                                  "isTestData": self.is_test_data}
            )
            # https://ly0jegwkib.execute-api.us-east-1.amazonaws.com/play1/api/v1/group/getGroupById/123456789998?langCode=en

            self.logger.info("Endpoint group remote - getGroupById action: ", object={"url": url})
            user_jwt = self.user_context.get_user_jwt()
            headers = utilities.create_authorization_http_headers(user_jwt)
            response = requests.get(url, headers=headers)
            # {"groupId":"50003460","number":"50003460","title":"Test Group 1717057844453","titleLangCode":"en",
            # "parentGroupId":1,"sequence":null,"isInterest":1,"image":"GroupImage","childrenGroups":[]}}
            # TODO Call a function to process the response, if response status = 500 display the url and raise exception
            self.logger.end(
                f"End get_group_by_id group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise exception
        except requests.Timeout as exception:
            self.logger.exception(
                "Timeout Exception- Request timed out", object={'exception': exception})
            raise exception
        except requests.RequestException as exception:
            self.logger.exception((
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise exception
        except Exception as exception:
            self.logger.exception((
                f"An unexpected error occurred: {str(exception)}", exception))
            raise exception

    def create_group(self, title: str, lang_code: LangCode = None, parent_group_id: str = None,
                     is_interest: bool = None, image: str = None, non_members_visibility_id: int = 1,
                     members_visibility_id: int = 1):  # POST

        try:
            url = self.our_url.endpoint_url(
                brand_name=utilities.get_brand_name(),
                environment_name=utilities.get_environment_name(),
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.CREATE_GROUP.value,  # "createGroup",
            )

            # class CreateGroupDto {
            #     title: string = "";
            #     langCode?: languageCode;
            #     parentGroupId?: string;
            #     isInterest?: boolean;
            #     image?: string;
            #
            # }
            payload = {"title": title, "isTestData": self.is_test_data, "langCode": self._get_lang_code_str(lang_code)}

            if parent_group_id is not None:
                payload["parentGroupId"] = parent_group_id
            if is_interest is not None:
                payload["isInterest"] = is_interest
            if image is not None:
                payload["image"] = image

            user_jwt = self.user_context.get_user_jwt()
            header = utilities.create_authorization_http_headers(user_jwt)
            self.logger.info("creatGroup", object={"url": url, "payload": payload})
            response = requests.post(url, json=payload, headers=header)
            # TODO Call a function to process the response, if response status = 500 display the url and raise exception
            self.logger.end(
                f"End create group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise exception
        except requests.Timeout as exception:
            self.logger.exception(
                "Timeout Exception- Request timed out", object={'exception': exception})
            raise exception
        except requests.RequestException as exception:
            self.logger.exception((
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise exception
        except Exception as exception:
            self.logger.exception((
                f"An unexpected error occurred: {str(exception)}", exception))
            raise exception

    def insert_update_group(self, *, title: str, lang_code: LangCode = None, parent_group_id: str = None,
                            is_interest: bool = None,
                            ## TODO Replace all Magic Numbers such as 1 with cost enum from Visibility Package
                            image: str = None, non_members_visibility_id: int = 1, members_visibility_id: int = 1):
        # TODO: why are we inserting and updating with the same data?

        try:
            # Try to get the group by name
            response = self.get_group_by_group_name(title, lang_code)
            # TODO Call a function to process the response, if response status = 500 display the url and raise exception

            # If the group does not exist, create it
            if response.status_code == requests.codes.no_content:
                response = self.create_group(title, lang_code, parent_group_id, is_interest, image,
                                             non_members_visibility_id, members_visibility_id)
            # If the group exists, update it
            elif response.status_code == requests.codes.ok:
                create_group_response_dict = response.json()
                self.logger.info(f"create_group_response_dict: {create_group_response_dict}")
                try:
                    group_id = int(create_group_response_dict['data'][0]['groupId'])
                except Exception as exception:
                    raise Exception(
                        f"Unexpected response from get_group_response_by_group_name: {create_group_response_dict}, exception={exception}")

                response = self.update_group(group_id, title, lang_code, parent_group_id, is_interest, image,
                                             non_members_visibility_id, members_visibility_id)
                # TODO Error handing of the reponse i.e. response.status_code
            # TODO Call a function to process the response, if response status = 500 display the url and raise exception
            else:
                self.logger.error(
                    f"group-main-remote-restapi-python-package create_group() Unexpected status code: {response.status_code}")

            return response

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise exception
        except requests.Timeout as exception:
            self.logger.exception("Timeout Exception- Request timed out", object={'exception': exception})
            raise exception
        except requests.RequestException as exception:
            self.logger.exception(
                (f"RequestException Exception- General error: {str(exception)}", exception))
            raise exception
        except Exception as exception:
            self.logger.exception((f"An unexpected error occurred: {str(exception)}", exception))
            raise exception

    def update_group(self, group_id: int, title: str = None, lang_code: LangCode = None, parent_group_id: int = None,
                     is_interest: bool = None, image: str = None, non_members_visibility_id: int = 1,
                     members_visibility_id: int = 1):  # PATCH
        # TODO Not implemented yet on server side
        try:
            url = self.our_url.endpoint_url(
                brand_name=utilities.get_brand_name(),
                environment_name=utilities.get_environment_name(),
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.UPDATE_GROUP.value,  # "updateGroup",
                path_parameters={'groupId': group_id},

            )

            self.logger.info(
                "Endpoint group remote - updateGroup action: " + url)

            payload = {
                "title": title,
                # "non_members_visibility_id": non_members_visibility_id,
                # "members_visibility_id": members_visibility_id
            }

            if lang_code is not None:
                payload["langCode"] = self._get_lang_code_str(lang_code)
            if parent_group_id is not None:
                payload["parentGroupId"] = str(parent_group_id)
            if is_interest is not None:
                payload["isInterest"] = is_interest
            if image is not None:
                payload["image"] = image

            user_jwt = self.user_context.get_user_jwt()
            header = utilities.create_authorization_http_headers(user_jwt)
            # TODO logger.info() with all parameters calling to requests.patch() incase we will have Exception, we can see the url, payload and header
            update_group_response = requests.patch(url, json=payload, headers=header)
            # TODO Call a function to process the response, if response status = 500 display the url and raise exception
            # TODO Call one genreic Error Handing function (existing/new from python SDK) after all requests.* with update_group_response_json, if status_code not OK, logger.error all parameters (i.e. url, payload and header)
            self.logger.end(
                f"End update group-remote, update_group_response: {str(update_group_response)}")
            return update_group_response

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise exception
        except requests.Timeout as exception:
            self.logger.exception(
                "Timeout Exception- Request timed out", object={'exception': exception})
            raise exception
        except requests.RequestException as exception:
            self.logger.exception((
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise exception
        except Exception as exception:
            self.logger.exception((
                f"An unexpected error occurred: {str(exception)}", exception))
            raise exception

    def delete_group_by_group_id(self, group_id: int):  # DELETE
        try:
            url = self.our_url.endpoint_url(
                brand_name=utilities.get_brand_name(),
                environment_name=utilities.get_environment_name(),
                component_name=ComponentName.GROUP.value,
                entity_name=EntityName.GROUP.value,
                version=GROUP_REMOTE_API_VERSION,
                action_name=ActionName.DELETE_GROUP.value,  # "deleteGroup",
                path_parameters={'groupId': group_id}
            )

            self.logger.info(
                "Endpoint group remote - deleteGroup action: " + url)
            user_jwt = self.user_context.get_user_jwt()
            header = utilities.create_authorization_http_headers(user_jwt)
            response = requests.delete(url, headers=header)
            # TODO Call a function to process the response, if response status = 500 display the url and raise exception
            # TODO Call one genreic Error Handing function (from python SDK) after all requests.*
            self.logger.end(
                f"End delete group-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)",
                                  object={'exception': exception})
            raise exception
        except requests.Timeout as exception:
            self.logger.exception(
                "Timeout Exception- Request timed out", object={'exception': exception})
            raise exception
        except requests.RequestException as exception:
            self.logger.exception((
                f"RequestException Exception- General error: {str(exception)}", exception))
            raise exception
        except Exception as exception:
            self.logger.exception((
                f"An unexpected error occurred: {str(exception)}", exception))
            raise exception

        # TODO Develop merge_groups( main_group_id_a, identical_group_id) # We should link everything from identical_group
        # to main_group, main_group should have new alias names, we should be logically delete identical_group, we
        # should be able to unmerge_groups
        # TODO Develop unmerge_groups( main_group_id_a, identical_group_id ) # Low priority
        # TODO Develop link_group_to_a_parent_group( group_id, parent_group_id) # We should support multiple parents
        # TODO Develop unlink_group_to_a_parent_group( group_id, parent_group_id) # We should support multiple parents

    def _get_lang_code_str(self, lang_code: LangCode = None):
        if lang_code is None:
            lang_code = self.user_context.get_effective_profile_preferred_lang_code()
        return lang_code.value
