#!/usr/bin/python3
# coding: utf-8
import json
import shutil
import sys
from pathlib import Path

import yaml

import click
from pySabaCLI import root_dir
from pySabaCLI import config
from pySabaCLI.lib.util import debug_arg, get_logger, shell_execute

logger = get_logger(__file__)
ssh_dir = Path("/root/.ssh")
config_dir = root_dir.joinpath("config")


def start_main(user, password, subscription):
    ssh_keygen()
    debug_arg(logger, "user", user)
    debug_arg(logger, "password", password)
    az_login(user, password)
    if subscription is None:
        az_show_subscription()
        print("=== Please select subscription to use ===")
        print("If you want to use default, please enter 'default'")
        subscription = click.prompt("SubscriptionId for", type=str)
        if subscription == "default":
            subscription = az_get_subscription()
        az_set_subscription(subscription)
        debug_arg(logger, "subscription", subscription)
    client_id, secret, tenant = az_get_connection_info()
    az_dump_credential_file(subscription, client_id, secret, tenant)
    print("=== How would you name resource group? ===")
    print("Default is 'RyuGoo-Saba'. If that's okay, please enter 'default'")
    resource_group = click.prompt("Resource Group for", type=str)
    generate_ansible_var_file(resource_group)
    generate_ssl_certificate()
    run_ansible()
    dump_config(user, password, subscription, resource_group)


def ssh_keygen():
    ssh_dir.mkdir(parents=True, exist_ok=True)
    l_cmd = ["ssh-keygen", "-q", "-t", "rsa", "-N",
             "''", "-f", ssh_dir.joinpath("id_rsa")]
    status, stdout, stderr = shell_execute(l_cmd)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)


def az_login(user, password):
    l_cmd = ["az", "login", "-u", user, "-p", password]
    status, stdout, stderr = shell_execute(l_cmd)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)


def az_show_subscription():
    cmd = "az account list --output table"
    status, stdout, stderr = shell_execute(cmd)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)


def az_get_subscription():
    cmd = "az account show --query '{subscription_id: id}'"
    status, stdout, stderr = shell_execute(cmd, flush=False)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)
    data = json.loads(stdout)
    subscription = data["subscription_id"]

    return subscription


def az_set_subscription(subscription):
    l_cmd = ["az", "account", "set", "--subscription", subscription]
    status, stdout, stderr = shell_execute(l_cmd)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)


def az_get_connection_info():
    cmd = "az ad sp create-for-rbac --query '{client_id: appId, secret: password, tenant: tenant}'"
    status, stdout, stderr = shell_execute(cmd, flush=False)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)
    data = json.loads(stdout)
    client_id = data["client_id"]
    secret = data["secret"]
    tenant = data["tenant"]

    return client_id, secret, tenant


def az_dump_credential_file(subscription, client_id, secret, tenant):
    credential_path = Path("/root/.azure/credentials")
    with credential_path.open(mode="w") as f:
        f.write("[default]\n")
        f.write("subscription_id={}\n".format(subscription))
        f.write("client_id={}\n".format(client_id))
        f.write("secret={}\n".format(secret))
        f.write("tenant={}\n".format(tenant))


def generate_ansible_var_file(resource_group):
    var_file_path = \
        root_dir.joinpath("ansible-master").joinpath("vars_files").joinpath("master-config.yml")
    with var_file_path.open(mode="w") as f:
        f.write("---\n")
        f.write("resource_group: {}\n".format(resource_group))
        f.write("location: {}\n".format(config.LOCATION))
        f.write("storageaccount:\n")
        f.write("  name: {}\n".format(config.STORAGEACCOUNT))
        f.write("cidr_prefix: {}\n".format(config.CIDR_PREFIX))
        f.write("vm_name: {}\n".format(config.MASTER_VM_NAME))
        f.write("vm_size: {}\n".format(config.MASTER_INSTANCE_SIZE))
        f.write("gb_size: {}\n".format(config.MASTER_DISK_SIZE))
        f.write("username: {}\n".format("ryugoo"))
        f.write("authorized_keys: ")
        with open("/root/.ssh/id_rsa.pub", "r") as f_auth:
            f.write(f_auth.read())


def generate_ssl_certificate():
    key_path = \
        root_dir.joinpath("config").joinpath("ca.key")
    csr_path = \
        root_dir.joinpath("config").joinpath("ca.csr")
    crt_path = \
        root_dir.joinpath("config").joinpath("ca.crt")

    cmd = ["openssl genrsa -out", key_path, "2048"]
    status, stdout, stderr = shell_execute(cmd, flush=True)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)

    cmd = ["openssl req -out", csr_path, "-new -newkey rsa:2048 -nodes -keyout", key_path, "-subj", '"/C=JP/ST=Foo/L=Foo/O=Foo/OU=Foo/CN=Foo"']
    status, stdout, stderr = shell_execute(cmd, flush=True)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)

    cmd = ["openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout", key_path, "-out", crt_path, "-subj", '"/C=JP/ST=Foo/L=Foo/O=Foo/OU=Foo/CN=Foo"']
    status, stdout, stderr = shell_execute(cmd, flush=True)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)


def run_ansible():
    ansible_create_vm_path = \
        root_dir.joinpath("ansible-master").joinpath("playbook-create-vm.yml")
    ansible_launch_app_path = \
        root_dir.joinpath("ansible-master").joinpath("playbook-launch-app.yml")

    cmd = ["ansible-playbook", ansible_create_vm_path]
    status, stdout, stderr = shell_execute(cmd, flush=True)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)

    cmd = ["ansible-playbook", ansible_launch_app_path,
           "-i", "ryugoo-saba-master-vm,"]
    status, stdout, stderr = shell_execute(cmd, flush=True)
    if status != 0:
        sys.stderr.write(stderr)
        sys.stderr.flush()
        sys.exit(status)


def dump_config(user, password, subscription, resource_group):
    shutil.copy("/root/.ssh/id_rsa", str(config_dir.joinpath("id_rsa")))
    shutil.copy("/root/.ssh/id_rsa.pub", str(config_dir.joinpath("id_rsa.pub")))
    shutil.copy("/root/.ssh/config", str(config_dir.joinpath("config")))
    shutil.copy("/root/.azure/credentials",
                str(config_dir.joinpath("credentials")))
    shutil.copy(str(root_dir.joinpath("pySabaCLI").joinpath("config.py")),
                str(config_dir.joinpath("config.py")))
    shutil.copy(str(root_dir.joinpath("ansible-master").joinpath("vars_files").joinpath("master-config.yml")),
                str(config_dir.joinpath("master-config.yml")))

    config_path = config_dir.joinpath("user_info.yml")
    config_path.touch(exist_ok=True)
    with config_path.open(mode="r") as f:
        data = yaml.load(f.read())
    if data is None:
        data = dict()
    data["azure_user"] = user
    data["azure_password"] = password
    data["azure_subscription"] = subscription
    data["azure_resource_group"] = resource_group
    with config_path.open(mode="w") as f:
        f.write(yaml.dump(data, default_flow_style=False))


# for DEBUG
if __name__ == "__main__":
    if len(sys.argv) <= 2 or len(sys.argv) >= 5:
        logger.debug("Please input user, password, subscription")
        sys.exit(1)
    elif len(sys.argv) == 3:
        user = sys.argv[1]
        password = sys.argv[2]
        subscription = None
    else:
        user = sys.argv[1]
        password = sys.argv[2]
        subscription = sys.argv[3]

    start_main(user, password, subscription)
