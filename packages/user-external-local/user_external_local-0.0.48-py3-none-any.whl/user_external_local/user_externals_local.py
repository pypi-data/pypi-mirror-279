from database_mysql_local.connector import Connector
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger

USER_EXTERNAL_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 115
USER_EXTERNAL_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'user_external_local_python'
DEVELOPER_EMAIL = "idan.a@circ.zone"
object_init = {
    'component_id': USER_EXTERNAL_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': USER_EXTERNAL_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL,
}
logger = Logger.create_logger(object=object_init)

DEFAULT_SCHEMA_NAME = 'user_external'
DEFAULT_TABLE_NAME = 'user_external_table'
DEFAULT_VIEW_NAME = 'user_external_view'
DEFAULT_ID_COLUMN_NAME = 'user_external_id'


class UserExternalsLocal(GenericCRUD):
    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name=DEFAULT_SCHEMA_NAME, default_table_name=DEFAULT_TABLE_NAME,
                         default_view_table_name=DEFAULT_VIEW_NAME, default_column_name=DEFAULT_ID_COLUMN_NAME,
                         is_test_data=is_test_data)

    def insert_or_update_user_external_access_token(self, *, system_id: int, username: str, access_token: str, profile_id: int,
                                                    expiry=None, refresh_token: str = None) -> None:
        object_start = {
            'username': username,
            'profile_id': profile_id,
            'system_id': system_id,
            'access_token': access_token,
            'expiry': expiry,
            'refresh_token': refresh_token
        }
        logger.start(object=object_start)
        try:
            current_token = self.get_access_token(system_id=system_id, username=username, profile_id=profile_id)
            if current_token is not None:
                self.delete_access_token(
                    system_id=system_id, username=username, profile_id=profile_id)

            connection = Connector.connect('user_external')
            if (expiry is None):
                expiry = ""
            if (refresh_token is None):
                refresh_token = ""
            query_insert_external = (
                "INSERT INTO user_external_table (system_id,username,access_token,expiry,refresh_token)"
                " VALUES (%s,%s,%s,%s,%s)"
            )
            values = (system_id, username, access_token, expiry, refresh_token)
            cursor = connection.cursor()
            cursor.execute(query_insert_external, values)
            id_new = cursor.lastrowid()
            values = (id_new, profile_id)
            connection.commit()
            connection_profile = Connector.connect('profile_user_external')
            query_insert_profile_user_external = (
                "INSERT INTO profile_user_external_table (user_external_id,profile_id) VALUES (%s,%s)"
            )
            cursor = connection_profile.cursor()
            cursor.execute(query_insert_profile_user_external, values)
            connection_profile.commit()
            object_info = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger.info("external user inserted", object=object_info)
        except Exception as error:
            logger.exception(object=error)
            logger.end()
            raise
        logger.end(object={})

    def get_access_token_by_username_and_system_id(self, *, username: str, system_id: int) -> str:
        access_token = None
        try:
            object_start = {
                'username': username,
                'system_id': system_id
            }
            logger.start(object=object_start)
            connection = Connector.connect('user_external')
            # TODO: move to generic crud
            query_get = "SELECT access_token FROM user_external.user_external_view WHERE username=%s AND system_id=%s"
            cursor = connection.cursor()
            cursor.execute(query_get, (username, system_id))
            access_token = cursor.fetchone()
        except Exception as error:
            logger.exception(object=error)
            logger.end()
            raise
        logger.end(object={'access_token': access_token})
        return access_token

    # TODO Shall we default the profile_id to profile_id from User Context?
    def get_access_token(self, *, system_id: int, username: str, profile_id: int) -> str:
        access_token = None
        try:
            object_start = {
                'username': username,
                'profile_id': profile_id,
                'system_id': system_id
            }
            logger.start(object=object_start)
            connection = Connector.connect('user_external')
            query_get = (
                "SELECT access_token FROM user_external.user_external_view as eu join "
                "profile_user_external.profile_user_external_table as eup on eu.user_external_id=eup.user_external_id WHERE"
                " eu.username=%s AND eu.system_id=%s And eup.profile_id=%s"
            )
            cursor = connection.cursor()
            cursor.execute(query_get, (username, system_id, profile_id))
            access_token = cursor.fetchone()
        except Exception as error:
            logger.exception(object=error)
            logger.end()
            raise
        logger.end(object={'access_token': access_token})
        return access_token

    # TODO username -> username_str
    def update_user_external_access_token(self, *, system_id: int, username: str, profile_id: int, access_token, expiry=None,
                                          refresh_token: str = None) -> None:
        try:
            object_start = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger.start(object=object_start)
            connection = Connector.connect('user_external')
            update_query = (
                "UPDATE user_external.user_external_table AS eu JOIN profile_user_external.profile_user_external_table AS eup"
                " ON eu.user_external_id = eup.user_external_id SET eu.access_token = %s WHERE eu.username = %s AND"
                " eu.system_id = %s AND eup.profile_id = %s;"
            )
            values = (access_token, username, system_id, profile_id)
            cursor = connection.cursor()
            cursor.execute(update_query, values)
            connection.commit()
            object_info = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger.info("external user updated", object=object_info)
        except Exception as error:
            logger.exception(object=error)
            logger.end()
            raise
        logger.end(object={})

    def delete_access_token(self, *, system_id: int, username: str, profile_id: int):
        try:
            object_start = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
            }
            logger.start(object=object_start)
            connection = Connector.connect('user_external')
            cursor = connection.cursor()
            update_query = (
                "UPDATE user_external.user_external_table AS eu JOIN profile_user_external.profile_user_external_table AS eup"
                " ON eu.user_external_id = eup.user_external_id SET eu.end_timestamp = now() WHERE eu.username = %s AND"
                " eu.system_id = %s AND eup.profile_id = %s;"
            )
            values = (username, system_id, profile_id)
            cursor.execute(update_query, values)
            connection.commit()
            object_info = {
                'username': username,
                'system_id': system_id,
                'profile_id': profile_id,
            }
            logger.info("external user updated", object=object_info)
        except Exception as error:
            logger.exception(object=error)
            logger.end()
            raise
        logger.end(object={})

    def get_auth_details_by_system_id_and_profile_id(self, *, system_id: int, profile_id: int) -> tuple:
        try:
            object_start = {
                'system_id': system_id,
                "profile_id": profile_id
            }
            logger.warning(
                log_message="This static method is deprecated, "
                            "please use the non static method",
            )
            logger.start(object=object_start)
            connection = Connector.connect('user_external')
            query_get_all = (
                "SELECT eu.user_external_id, access_token,refresh_token,expiry FROM user_external.user_external_view AS eu"
                " JOIN profile_user_external.profile_user_external_table AS eup on eu.user_external_id=eup.user_external_id"
                " WHERE eu.system_id=%s AND eup.profile_id=%s order BY eu.start_timestamp DESC LIMIT 1"
            )
            cursor = connection.cursor()
            cursor.execute(query_get_all, (system_id, profile_id))
            auth_details = cursor.fetchone()
        except Exception as error:
            logger.exception(object=error)
            logger.end()
            raise
        logger.end(object={'auth_details': auth_details})
        return auth_details

    def get_auth_details(self, *, system_id: int, username: str, profile_id: int) -> None:
        auth_details = None
        try:
            object_start = {
                "username": username,
                'system_id': system_id,
                "profile_id": profile_id,
            }
            logger.start(object=object_start)
            connection = Connector.connect('user_external')
            query_get_all = (
                "SELECT access_token,refresh_token,expiry FROM user_external.user_external_view AS eu JOIN"
                " profile_user_external.profile_user_external_view AS eup ON eu.user_external_id=eup.user_external_id WHERE"
                " eu.username=%s AND eu.system_id=%s AND eup.profile_id=%s ORDER BY eu.start_timestamp DESC LIMIT 1"
            )
            cursor = connection.cursor()
            cursor.execute(query_get_all, (username, system_id, profile_id))
            auth_details_list = cursor.fetchall()
            if auth_details_list:
                auth_details = auth_details_list[0]
            else:
                logger.error(log_message="user external not found", object={"auth_details_list": auth_details_list})
        except Exception as error:
            logger.exception(object=error)
            logger.end()
            raise
        logger.end(object={'auth_details': auth_details})
        return auth_details
