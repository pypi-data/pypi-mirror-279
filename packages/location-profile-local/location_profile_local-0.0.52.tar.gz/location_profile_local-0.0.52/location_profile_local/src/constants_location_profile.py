from logger_local.LoggerComponentEnum import LoggerComponentEnum


class LocationProfileLocalConstants:
    LOCATION_PROFILE_LOCAL_PYTHON_COMPONENT_ID = 167
    LOCATION_PROFILE_COMPONENT_NAME = 'location_profile_local/location_profile.py'
    LOCATION_PROFILE_TESTS_COMPONENT_NAME = 'tests/test_location_profile.py'

    OBJECT_FOR_LOGGER_CODE = {
        'component_id': LOCATION_PROFILE_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': LOCATION_PROFILE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': 'sahar.g@circ.zone'
    }

    OBJECT_FOR_LOGGER_TEST = {
        'component_id': LOCATION_PROFILE_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': LOCATION_PROFILE_TESTS_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': 'sahar.g@circ.zone'
    }
