#!/usr/bin/python3
# coding: utf-8
import shutil
from pySabaCLI import root_dir

config_file_path = root_dir.joinpath("pySabaCLI").joinpath("config.py")
config_file_dist_path = root_dir.joinpath(
    "pySabaCLI").joinpath("config.py-dist")
if config_file_path.exists() is False:
    shutil.copy(str(config_file_dist_path), str(config_file_path))

import click
from pySabaCLI import config
from pySabaCLI.lib import start_main


@click.group(help="RyuGoo-Saba: a CWL-based execution engine utilizing cloud resources for big data analysis in life science")
def saba():
    pass


@saba.group("job", help="Subcommand to handle jobs")
def saba_job():
    pass


@saba_job.command("list", help="Display of registered job")
@click.option("-r", "--running", "running", is_flag=True, help="Display only running job")
@click.option("-s", "--simple", "simple", is_flag=True, help="Reduce items to display")
@click.option("-t", "--table", "table", is_flag=True, help="Display in table format")
def job_list(running, simple, table):
    pass


@saba_job.command("remove", help="Remove registered job")
@click.option("-f", "--force", "force", is_flag=True, help="Even if the job status is running, delete it")
@click.argument("job_id", nargs=1, type=int, envvar="JOB_ID")
def job_remove(job_id, force):
    if force is True:
        if click.confirm("Running VM is deleted and results are lost, is it OK?") is False:
            raise click.Abort()
    pass


@saba_job.command("log", help="Display log of registered job")
@click.argument("job_id", nargs=1, type=int, envvar="JOB_ID")
def job_log(job_id):
    pass


@saba_job.command("submit", help="Submit the job")
@click.option("-s", "--SRA_accession_nums", "SRA_accession_nums", multiple=True, required=True, help="Specifying multiple SRA accession numbers")
@click.option("-c", "--CWL_file_urls", "CWL_file_urls", multiple=True, required=True, help="Specifying CWL file urls")
@click.option("-i", "--instance_size", "instance_size", nargs=1, default=config.WORKER_DEFAULT_INSTANCE_SIZE, help="Azure instance size(default=Standard_D2_v3)")
@click.option("-d", "--disk_size", "disk_size", nargs=1, default=config.WORKER_DEFAULT_DISK_SIZE, help="VM disk size[GB] (default=40)")
def job_submit(SRA_accession_nums, CWL_file_urls, instance_size, disk_size):
    pass


@saba.command("start", help="Start the managed node on azure")
@click.option("-u", "--user", "user", nargs=1, prompt="Azure user name for", help="Azure user account")
@click.option("-p", "--password", "password", nargs=1, prompt="Azure user password for", help="Azure user password")
@click.option("-s", "--subscription", "subscription", nargs=1, help="Azure subscription")
def saba_start(user, password, subscription):
    start_main(user, password, subscription)


@saba.command("stop", help="Stop the managed node. Data on jobs will not disappear")
@click.option("-f", "--force", "force", is_flag=True, help="Even if a running job exists, it stops")
def saba_stop(force):
    if force is True:
        if click.confirm("Running job becomes failed and results are lost, is it OK?") is False:
            raise click.Abort()
    pass


@saba.command("log", help="Display log of master node")
def saba_log():
    pass


@saba.command("info", help="Confirm your user id and subscription")
def saba_info():
    pass


@saba.command("purge", help="Delete the managed node. Data on jobs will disappear")
@click.option("-f", "--force", "force", is_flag=True, required=True, help="Even if a running job exists, it purge")
def saba_purge(force):
    if force is True:
        if click.confirm("The VM itself of the Master node is deleted and data of all jobs is lost. Is it OK?") is False:
            raise click.Abort()
    pass


@saba.command("import", help="Import connection information on other PC")
def saba_import():
    pass


def main():
    saba()


if __name__ == "__main__":
    main()
