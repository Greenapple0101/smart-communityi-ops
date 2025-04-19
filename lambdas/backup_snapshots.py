import boto3, os, datetime

EC2 = boto3.client('ec2')
RDS = boto3.client('rds')
S3  = boto3.client('s3')

def create_snapshots():
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    # EC2 인스턴스 스냅샷
    for inst in EC2.describe_instances()['Reservations']:
        for i in inst['Instances']:
            snap = EC2.create_snapshot(
                VolumeId=i['BlockDeviceMappings'][0]['Ebs']['VolumeId'],
                Description=f"{i['InstanceId']}-{today}"
            )
    # RDS 인스턴스 스냅샷
    for db in RDS.describe_db_instances()['DBInstances']:
        sid = f"{db['DBInstanceIdentifier']}-{today}"
        RDS.create_db_snapshot(DBSnapshotIdentifier=sid, DBInstanceIdentifier=db['DBInstanceIdentifier'])
    print("Snapshots created:", today)

def prune_old_snapshots(days=30):
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    # EC2 스냅샷 정리
    for snap in EC2.describe_snapshots(OwnerIds=['self'])['Snapshots']:
        if snap['StartTime'].replace(tzinfo=None) < cutoff:
            EC2.delete_snapshot(SnapshotId=snap['SnapshotId'])
    # RDS 스냅샷 정리
    for snap in RDS.describe_db_snapshots(SnapshotType='manual')['DBSnapshots']:
        if snap['SnapshotCreateTime'].replace(tzinfo=None) < cutoff:
            RDS.delete_db_snapshot(DBSnapshotIdentifier=snap['DBSnapshotIdentifier'])
    print("Snapshots pruned older than", days, "days")

def handler(event, context):
    create_snapshots()
    prune_old_snapshots()
    return {"status": "complete"}
