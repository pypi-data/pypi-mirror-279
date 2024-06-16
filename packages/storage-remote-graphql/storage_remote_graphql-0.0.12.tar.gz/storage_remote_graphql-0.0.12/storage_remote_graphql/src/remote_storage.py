import requests
from python_sdk_remote.utilities import our_get_env
from url_remote.component_name_enum import ComponentName
from url_remote.entity_name_enum import EntityName
from url_remote.our_url import OurUrl

# TODO Please replace all strings and Magic Numbers such as "graphql" to const enum
version = 1
action = "graphql"
BRAND_NAME = our_get_env('BRAND_NAME')
ENVIRONMENT_NAME = our_get_env('ENVIRONMENT_NAME')

# TODO: use logger
class RemoteStorage:
    def __init__(self) -> None:
        self.url = OurUrl.endpoint_url(
            brand_name=BRAND_NAME, environment_name=ENVIRONMENT_NAME,
            component_name=ComponentName.GROUP_PROFILE.value,
            entity_name=EntityName.GROUP_PROFILE.value, version=version,
            action_name=action)

    def put(self, *, filename: str, local_path: str, created_user_id: int, entity_type_id: int, profile_id: int) -> str:
        """
        Uploads a file to the remote storage and returns the file's remote path.

        :param filename: The name of the file.
        :param local_path: The local path to the file on your system.
        :param created_user_id: The ID of the user who created the file.
        :param entity_type_id: The ID of the entity type associated with the file.
        :param profile_id: The ID of the profile associated with the file.
        :return: The remote path of the uploaded file.
        """
        put_query = f"""
        mutation {{
          put(
            filename: "{filename}",
            local_path: "{local_path}",
            created_user_id: "{created_user_id}",
            entity_type_id: "{entity_type_id}",
            profile_id: "{profile_id}"
          )
        }}"""
        response = requests.post(self.url, json={"query": put_query})

        response_data = response.json().get("data", {})
        if "errors" in response_data:
            raise Exception(response_data["errors"][0]["message"])
        elif "put" not in response_data:
            raise Exception("Unknown error while uploading file", response_data)
        else:
            return response_data["put"]

    def download(self, *, filename: str, local_path: str, entity_type_id: int, profile_id: int) -> str:
        """
        Downloads a file from the remote storage and returns the file's contents.

        :param filename: The name of the file to download.
        :param entity_type_id: The ID of the entity type associated with the file.
        :param profile_id: The ID of the profile associated with the file.
        :param local_path: The local path where the downloaded file should be saved.
        :return: The contents of the downloaded file.
        """
        download_query = f"""
        mutation {{
          download(
            filename: "{filename}",
            entity_type_id: "{entity_type_id}",
            profile_id: "{profile_id}",
            local_path: "{local_path}"
          )
        }}
        """
        response = requests.post(self.url, json={"query": download_query})

        response_data = response.json().get("data", {})
        if "errors" in response_data:
            raise Exception(response_data["errors"][0]["message"])

        return response_data["download"]
