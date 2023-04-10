import boto3
import datetime

client = boto3.client('ce')

def describe_cost():
    start = datetime.date(2023, 3, 1)
    end = datetime.date(2023, 4, 10)

    result = client.get_cost_and_usage(
        TimePeriod={
            'Start': start.strftime('%Y-%m-%d'),
            'End': end.strftime('%Y-%m-%d')
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[            {'Type': 'DIMENSION', 'Key': 'SERVICE'}        ]
    )
    return result