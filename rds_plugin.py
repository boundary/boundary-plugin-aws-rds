import boto
import boto.rds
import sys

from boundary_aws_plugin.cloudwatch_plugin import CloudwatchPlugin
from boundary_aws_plugin.cloudwatch_metrics import CloudwatchMetrics


class RdsCloudwatchMetrics(CloudwatchMetrics):
    def __init__(self, access_key_id, secret_access_key):
        super(RdsCloudwatchMetrics, self).__init__(access_key_id, secret_access_key, 'AWS/RDS')

    def get_region_list(self):
        # Some regions are returned that actually do not support RDS.  Skip those.
        return [r for r in boto.rds.regions() if r.name not in ['cn-north-1', 'us-gov-west-1']]

    def get_entities_for_region(self, region):
        rds = boto.connect_rds(self.access_key_id, self.secret_access_key, region=region)
        return rds.get_all_dbinstances()

    def get_entity_dimensions(self, region, db):
        return dict(DBInstanceIdentifier=db.id)

    def get_entity_source_name(self, db):
        return db.id

    def get_metric_list(self):
        return (
            ('BinLogDiskUsage', 'Average', 'AWS_RDS_BIN_LOG_DISK_USAGE'),
            ('CPUUtilization', 'Average', 'AWS_RDS_CPU_UTILIZATION'),
            ('DatabaseConnections', 'Average', 'AWS_RDS_DATABASE_CONNECTIONS'),
            ('DiskQueueDepth', 'Average', 'AWS_RDS_DISK_QUEUE_DEPTH'),
            ('FreeableMemory', 'Average', 'AWS_RDS_FREEABLE_MEMORY'),
            ('FreeStorageSpace', 'Average', 'AWS_RDS_FREE_STORAGE_SPACE'),
            ('ReplicaLag', 'Average', 'AWS_RDS_REPLICA_LAG'),
            ('SwapUsage', 'Average', 'AWS_RDS_SWAP_USAGE'),
            ('ReadIOPS', 'Average', 'AWS_RDS_READ_IOPS'),
            ('WriteIOPS', 'Average', 'AWS_RDS_WRITE_IOPS'),
            ('ReadLatency', 'Average', 'AWS_RDS_READ_LATENCY'),
            ('WriteLatency', 'Average', 'AWS_RDS_WRITE_LATENCY'),
            ('ReadThroughput', 'Average', 'AWS_RDS_READ_THROUGHPUT'),
            ('WriteThroughput', 'Average', 'AWS_RDS_WRITE_THROUGHPUT'),
            ('NetworkReceiveThroughput', 'Sum', 'AWS_RDS_NET_RX_TP'),
            ('NetworkTransmitThroughput', 'Sum', 'AWS_RDS_NET_TX_TP'),
        )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        import logging
        logging.basicConfig(level=logging.INFO)

    plugin = CloudwatchPlugin(RdsCloudwatchMetrics, '', 'boundary-plugin-aws-rds-python-status')
    plugin.main()
