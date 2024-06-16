from database_infrastructure_local.number_generator import NumberGenerator
from logger_local.LoggerComponentEnum import LoggerComponentEnum

USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 171
USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "user_local/src/user.py"
USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME_TEST = 'user_local/tests/user_test.py'

user_local_python_code_logger_object = {
    'component_id': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'sahar.g@circ.zone'
}

user_local_python_test_logger_object = {
    'component_id': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'sahar.g@circ.zone'
}

# Update profile_id and location_id for more tests
# TODO Let's use Profile.get_test_profile_id() Location,get_test_location_id() ... to get those test values.
TEST_PROFILE_ID = 5000014
TEST_LOCATION_ID1 = 36081
TEST_LOCATION_ID2 = 36082

number = NumberGenerator.get_random_number("user", "user_table", "user_id")
TEST_USERNAME1 = "test_username" + str(number)
TEST_MAIN_EMAIL1 = "test_email@address" + str(number)
TEST_FIRST_NAME1 = "test_first_name" + str(number)
TEST_LAST_NAME1 = "test_last_name" + str(number)

TEST_USERNAME2 = "test_username" + str(number)
TEST_MAIN_EMAIL2 = "test_email@address" + str(number)
TEST_FIRST_NAME2 = "test_first_name" + str(number)
TEST_LAST_NAME2 = "test_last_name" + str(number)
