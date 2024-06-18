import time
from threading import Thread
from typing import List

import click
import yaml
from kubernetes import client, config, utils, watch
from kubernetes.client import ApiTypeError
from pkg_resources import resource_filename

from tensorkube.constants import NAMESPACE, REGION, PodStatus


def create_namespace(namespace_name):
    config.load_kube_config()
    namespace = client.V1Namespace()
    namespace.metadata = client.V1ObjectMeta(name=namespace_name)
    v1 = client.CoreV1Api()
    v1.create_namespace(body=namespace)


def create_docker_registry_secret(secret_name: str, namespace: str, base64_encoded_dockerconfigjson: str):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    secret = client.V1Secret()
    secret.api_version = "v1"
    secret.kind = "Secret"
    secret.metadata = client.V1ObjectMeta(name=secret_name, namespace=namespace)
    secret.type = "kubernetes.io/dockerconfigjson"
    secret.data = {".dockerconfigjson": base64_encoded_dockerconfigjson}

    v1.create_namespaced_secret(namespace=namespace, body=secret)


def create_aws_secret(credentials, namespace: str = NAMESPACE):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    secret = client.V1Secret()
    secret.metadata = client.V1ObjectMeta(name="aws-secret")
    secret.string_data = {"AWS_ACCESS_KEY_ID": credentials.access_key, "AWS_SECRET_ACCESS_KEY": credentials.secret_key,
                          "AWS_SESSION_TOKEN": credentials.token}

    v1.create_namespaced_secret(namespace=namespace, body=secret)


def delete_aws_secret(namespace: str = NAMESPACE):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        v1.read_namespaced_secret(name="aws-secret", namespace=namespace)
    except client.ApiException as e:
        if e.status == 404:
            return
        else:
            raise
    v1.delete_namespaced_secret(name="aws-secret", namespace=namespace)


def create_kaniko_pv_and_pvc(bucket_name: str, namespace: str = NAMESPACE, region: str = REGION):
    config.load_kube_config()

    pv_config_file_path = resource_filename('tensorkube', 'configurations/kaniko_build_configs/pv.yaml')
    pvc_config_file_path = resource_filename('tensorkube', 'configurations/kaniko_build_configs/pvc.yaml')
    with open(pv_config_file_path) as f:
        pv = yaml.safe_load(f)
    with open(pvc_config_file_path) as f:
        pvc = yaml.safe_load(f)

    pv['spec']['mountOptions'] = ["allow-delete", "region {}".format(region)]
    pv['spec']['csi']['volumeAttributes']['bucketName'] = bucket_name
    pv['metadata']['namespace'] = namespace

    pvc['metadata']['namespace'] = namespace

    k8s_client = client.ApiClient()
    utils.create_from_dict(k8s_client, pv)
    utils.create_from_dict(k8s_client, pvc)


def apply_k8s_kaniko_configs(sanitised_project_name: str, serviceaccount_name: str, container_args: List[str],
                             namespace: str = NAMESPACE, region: str = REGION):
    config.load_kube_config()

    kaniko_deployment_file_path = resource_filename('tensorkube',
                                                    'configurations/kaniko_build_configs/kaniko_deployment_ecr.yaml')
    with open(kaniko_deployment_file_path) as f:
        kaniko_dep = yaml.safe_load(f)
    kaniko_dep['metadata']['namespace'] = namespace
    # NOTE: created unique kaniko deployment name for each project to avoid conflicts
    kaniko_dep['metadata']['name'] = 'kaniko-{}'.format(sanitised_project_name)
    kaniko_dep['spec']['serviceAccountName'] = serviceaccount_name
    kaniko_dep['spec']['containers'][0]['args'] = container_args
    # kaniko_dep['spec']['containers'][0]['args'].append('--verbosity=debug')
    kaniko_dep['spec']['containers'][0]['env'][0]['value'] = region

    k8s_client = client.ApiClient()
    utils.create_from_dict(k8s_client, kaniko_dep)
    click.echo('Deployed a build image')


def check_pod_status(pod_name, namespace):
    # Load kube config
    config.load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # Get the status of the pod
    pod_status = v1.read_namespaced_pod_status(name=pod_name, namespace=namespace)

    # Return the status of the pod
    return pod_status.status.phase


def find_and_delete_old_kaniko_pod(project_name: str, namespace: str = NAMESPACE):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace=namespace)
    for pod in pods.items:
        if pod.metadata.name == "kaniko-{}".format(project_name):
            if pod.status.container_statuses[0].state.terminated:
                v1.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace)
                return True
            else:
                return False

    return True


def start_streaming_pod(pod_name, namespace, status=None, container_name=None):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    # Create a stream to the pod
    # Initialize the Watch class
    watch_client = watch.Watch()
    # Stream events until the pod is ready
    print(f"Streaming events for pod {pod_name} in namespace {namespace}")
    for event in watch_client.stream(v1.list_namespaced_event, namespace=namespace):
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        if event['object'].involved_object.kind == 'Pod' and event['object'].involved_object.name == pod_name:
            print("Event: %s %s" % (event['type'], event['object'].message))
        if pod.status.phase != 'Pending':
            break

    print(f"Streaming logs for pod {pod_name} in namespace {namespace}")

    try:
        for event in watch_client.stream(v1.read_namespaced_pod_log, name=pod_name, namespace=namespace, follow=True,
                                         container=container_name):
            click.echo(event)
            pod = v1.read_namespaced_pod_status(name=pod_name, namespace=namespace)
            if status and status.value == pod.status.phase:
                print(f"Pod {pod_name} has reached {status.value} state")
                return
    except client.ApiException as e:
        if e.status == 404:
            print(f"Pod {pod_name} not found in namespace {namespace}")
        else:
            raise
    except KeyboardInterrupt:
        print("Log streaming stopped by user")
        return
    except ApiTypeError as e:
        print(f"An error occurred while streaming logs for pod {pod_name} in namespace {namespace}")
        print(e)
        return
    except Exception as e:
        print(f"An unexpected error occurred for pod {pod_name} in namespace {namespace}")
        print(e)
        raise


def start_streaming_service(service_name, namespace):
    # Load kube config
    config.load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # Stream the service status
    try:
        while True:
            pods = v1.list_namespaced_pod(namespace, label_selector=f'serving.knative.dev/service={service_name}')
            if pods.items:
                print(f"Pods scheduled for service {service_name}: {[pod.metadata.name for pod in pods.items]}")
                break
            time.sleep(5)
        # Start streaming the logs from the pod
        for pod in pods.items:
            thread = Thread(target=start_streaming_pod,
                            args=(pod.metadata.name, namespace, PodStatus.RUNNING, 'user-container'))
            thread.start()
    except client.ApiException as e:
        if e.status == 404:
            print(f"Service {service_name} not found in namespace {namespace}")
        else:
            raise
    except KeyboardInterrupt:
        print("Service status streaming stopped by user")
        return
    except Exception as e:
        print("An unexpected error occurred for service status streaming")
        raise
