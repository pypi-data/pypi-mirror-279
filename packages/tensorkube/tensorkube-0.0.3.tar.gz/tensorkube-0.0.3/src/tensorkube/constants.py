from enum import Enum

REGION = 'us-east-1'
NAMESPACE = 'kube-system'
DEFAULT_NAMESPACE = 'default'
SERVICE_ACCOUNT_NAME = 's3-csi-driver-sa'
ADDON_NAME = "aws-mountpoint-s3-csi-driver"
KNATIVE_SERVING_NAMESPACE = 'knative-serving'
CONFIG_FEATURES = 'config-features'


def get_mount_policy_name(cluster_name):
    return f'{cluster_name}-mountpoint-policy'

def get_mount_driver_role_name(cluster_name):
    return f'{cluster_name}-mountpoint-driver-role'
class Events(Enum):
    CONFIGURE_START = 'configure-start'
    CONFIGURE_END = 'configure-end'
    CONFIGURE_ERROR = 'configure-error'

    DEPLOY_START = 'deploy-start'
    DEPLOY_END = 'deploy-end'
    DEPLOY_ERROR = 'deploy-error'

    TEST_START = 'test-start'
    TEST_END = 'test-end'

class PodStatus(Enum):
    PENDING = 'Pending'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    UNKNOWN = 'Unknown'

