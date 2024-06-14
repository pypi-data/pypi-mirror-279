import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

import boto3
import click
import pyperclip
from botocore.exceptions import ProfileNotFound, NoCredentialsError, PartialCredentialsError, ClientError
from rich.console import Console
from rich.table import Table

DYNAMODB_TABLE = "ecsclusters"
CACHE_FILE = os.path.expanduser("~/.dashcli_cache.json")
console = Console()


@click.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument('aws_profile', required=False, default='dev')
@click.argument('db_user_name', required=False)
@click.option('--region', default='us-east-1', help='AWS region to use.')
@click.option('--refresh', is_flag=True, help='Refresh cached data.')
@click.option('--psql', is_flag=True, help='Connect to PostgreSQL database using psql.')
def dashcli(aws_profile, db_user_name, region, refresh, psql):
    session = None

    try:
        session = boto3.Session(profile_name=aws_profile, region_name=region)
    except ProfileNotFound:
        click.echo(
            f"The config profile ({aws_profile}) could not be found. Please create one using the following command:")
        click.echo(f"aws configure --profile {aws_profile}")
        return
    except (NoCredentialsError, PartialCredentialsError):
        click.echo("AWS credentials not found or incomplete. Please configure your AWS credentials.")
        click.echo("Use the command: aws configure")
        return
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")
        return

    sts_client = session.client('sts')
    dynamodb = session.resource('dynamodb')
    rds_client = session.client('rds')

    if not db_user_name:
        db_user_name = get_cached_user_name(aws_profile, region, sts_client, refresh)

    sslrootcertificate = os.path.expanduser('~/us-east-1-bundle.pem')
    if not os.path.isfile(sslrootcertificate):
        click.echo("File is not present hence downloading...")
        if not download_certificate():
            click.echo("Couldn't download the file. Something's wrong with the link!! Exiting!")
            return
        else:
            click.echo("PEM file for RDS authentication downloaded successfully.")
    else:
        click.echo(f"RDS connection certificate is present in {os.path.expanduser('~')}.")

    click.echo(f"Selected Username = {db_user_name}")
    cluster_name = select_cluster(dynamodb, aws_profile, region, refresh)
    if not cluster_name:
        return

    service_name, tags = select_service(dynamodb, cluster_name, refresh)
    if not service_name:
        return

    db_host, db_port, db_name = get_db_details(tags)

    if not all([db_host, db_port, db_name]):
        click.echo("Database details not found. Displaying all tags for the selected service:")
        display_tags(service_name, tags, aws_profile)
        return

    display_tags(service_name, tags, aws_profile)

    if not check_vars(db_name=db_name, db_port=db_port, db_host=db_host, db_user_name=db_user_name):
        return

    try:
        pg_password = rds_client.generate_db_auth_token(
            DBHostname=db_host,
            Port=db_port,
            Region=region,
            DBUsername=db_user_name
        )
    except ClientError as e:
        click.echo(f"Error generating DB auth token: {e}")
        return

    # Copy the pg_password to clipboard
    pyperclip.copy(pg_password)

    click.echo("******************************************************************************************")
    click.echo(f"1. RDS Database Username    : {db_user_name}")
    click.echo(f"2. RDS Database Hostname    : {db_host}")
    click.echo(f"3. RDS Database Port        : {db_port}")
    click.echo(f"4. RDS Database Name        : {db_name}")
    click.echo("******************************************************************************************")
    click.echo(
        "##### DASH Database Password is on the next line. Make sure that you are not copying extra white spaces. #####")
    click.echo(f"\033[31m{pg_password}\033[0m")
    click.echo("The password has been copied to your clipboard.")

    if psql:
        connect_to_psql(db_host, db_port, db_name, db_user_name, sslrootcertificate, pg_password)


def get_cached_user_name(aws_profile, region, sts_client, refresh):
    cache_data = load_cache()
    cache_key = f"user_name_{aws_profile}_{region}"
    if not refresh and cache_key in cache_data:
        return cache_data[cache_key]

    with ThreadPoolExecutor() as executor:
        future = executor.submit(get_user_id, sts_client)
        click.echo("Retrieving the database username in the background...")
        db_user_name = future.result()

    if db_user_name:
        cache_data[cache_key] = db_user_name
        save_cache(cache_data)
    return db_user_name


def get_user_id(sts_client):
    try:
        caller_identity = sts_client.get_caller_identity()
        return caller_identity.get('UserId')
    except ClientError as e:
        click.echo(f"Error retrieving caller identity: {e}")
        return None


def download_certificate():
    url = 'https://truststore.pki.rds.amazonaws.com/us-east-1/us-east-1-bundle.pem'
    destination = os.path.expanduser('~/us-east-1-bundle.pem')
    try:
        subprocess.run(['curl', '-o', destination, url], check=True)
        return True
    except subprocess.CalledProcessError as e:
        click.echo(f"Error downloading certificate: {e}")
        return False


def select_cluster(dynamodb, aws_profile, region, refresh):
    cache_data = load_cache()
    cache_key = f"clusters_{aws_profile}_{region}"
    if not refresh and cache_key in cache_data:
        clusters = cache_data[cache_key]
    else:
        table = dynamodb.Table(DYNAMODB_TABLE)
        try:
            response = table.scan()
            clusters = [item['clustername'] for item in response['Items'] if 'clustername' in item]
            clusters.sort()
            cache_data[cache_key] = clusters
            save_cache(cache_data)
        except ClientError as e:
            click.echo(f"Error retrieving clusters from DynamoDB: {e}")
            return None

    if not clusters:
        click.echo("No ECS clusters found.")
        return None

    click.echo("Select a cluster:")
    for i, cluster in enumerate(clusters, 1):
        click.echo(f"{i}. {cluster}")

    try:
        cluster_index = click.prompt("Enter the cluster number", type=int)
        if 1 <= cluster_index <= len(clusters):
            selected_cluster = clusters[cluster_index - 1]
            click.echo(f"You have selected {selected_cluster}")
            return selected_cluster
        else:
            click.echo(f"{cluster_index} is not a valid cluster number. Exiting...")
            return None
    except Exception as e:
        click.echo(f"Invalid input: {e}. Exiting...")
        return None


def select_service(dynamodb, cluster_name, refresh):
    cache_data = load_cache()
    cache_key = f"services_{cluster_name}"
    if not refresh and cache_key in cache_data:
        services = cache_data[cache_key]
    else:
        table = dynamodb.Table(DYNAMODB_TABLE)
        try:
            response = table.get_item(Key={'clustername': cluster_name})
            if 'Item' in response:
                services = response['Item'].get('services', {})
                cache_data[cache_key] = services
                save_cache(cache_data)
            else:
                click.echo(f"No services found for cluster {cluster_name}.")
                return None, None
        except ClientError as e:
            click.echo(f"Error retrieving services from DynamoDB: {e}")
            return None, None

    service_names = list(services.keys())
    click.echo("Select a service:")
    for i, service in enumerate(service_names, 1):
        click.echo(f"{i}. {service}")

    try:
        service_index = click.prompt("Enter the service number", type=int)
        if 1 <= service_index <= len(service_names):
            selected_service = service_names[service_index - 1]
            click.echo(f"You have selected {selected_service}")
            return selected_service, services[selected_service].get('tags', {})
        else:
            click.echo(f"{service_index} is not a valid service number. Exiting...")
            return None, None
    except Exception as e:
        click.echo(f"Invalid input: {e}. Exiting...")
        return None, None


def get_db_details(tags):
    db_host = tags.get('DB_HOST')
    db_port = tags.get('DB_PORT')
    db_name = tags.get('DB_NAME')
    return db_host, db_port, db_name


def display_tags(service_name, tags, aws_profile):
    table = Table(title=f"Service Tags for {service_name}")
    table.add_column("Key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    # Sort the tags by key, prioritizing "Name"
    sorted_tags = sorted(tags.items(), key=lambda item: (item[0] != "Name", item[0]))

    for key, value in sorted_tags:
        if key == "LOGS":
            value = f"{value} --profile {aws_profile}"
        table.add_row(key, value)

    console.print(table)


def check_vars(**kwargs):
    for var_name, value in kwargs.items():
        if not value:
            click.echo(f"{var_name} is unset.")
            return False
    return True


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_cache(data):
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f)


def connect_to_psql(db_host, db_port, db_name, db_user_name, sslrootcertificate, pg_password):
    os.environ['PGPASSWORD'] = pg_password
    psql_command = f'psql "host={db_host} port={db_port} dbname={db_name} user={db_user_name} sslmode=verify-full sslrootcert={sslrootcertificate}"'
    subprocess.run(psql_command, shell=True)


if __name__ == '__main__':
    dashcli()
