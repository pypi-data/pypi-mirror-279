from enum import Enum

from logger_local.LoggerComponentEnum import LoggerComponentEnum
from python_sdk_remote.utilities import our_get_env


# File-Type according to storage.file_type_ml_table
# TODO Sql2Code
class FileTypeEnum(Enum):
    PROFILE_IMAGE = 1
    COVERAGE_IMAGE = 2
    PERSONAL_INTODUCTION_VIDEO = 3
    SCANNED_DRIVING_LICENSE = 4
    PDF = 5
    SCANNED_PASSPORT = 6
    GOOGLE_CONTACTS_CSV = 7
    LINKEDIN_CONTACTS_CSV = 8
    OUTLOOK_CONTACTS_CSV = 9
    ORGANIZATION_PROFILE_LOGO = 10
    PROFILE_HTML = 11


USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 207  # 13?
USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "storage-main-local-python-package"

LOGGER_CODE_OBJECT = {
    'component_id': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circ.zone'
}

LOGGER_TEST_OBJECT = {
    'component_id': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'tal.g@circ.zone'
}

# TODO Should we change this to TEST_STORAGE_FILE_TYPE_ID?
STORAGE_TYPE_ID = 1
FILE_TYPE_ID = 1

# TODO Add all values from storage.file_extension_table
# TODO Change this to TEST_EXTENSION_ID
EXTENSION_ID = 1

AWS_DEFAULT_REGION = our_get_env("AWS_DEFAULT_REGION")
AWS_DEFAULT_STORAGE_BUCKET_NAME = our_get_env("AWS_DEFAULT_STORAGE_BUCKET_NAME")