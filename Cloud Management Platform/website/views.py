from datetime import datetime
import boto3
from flask import Blueprint, redirect, render_template, request, url_for
# from CostExplorer import describe_cost
from dateutil.relativedelta import relativedelta


views = Blueprint("views", __name__)
client = boto3.client('ce')


# @views.route('/')
# def home():
#     items = describe_cost()
#     total_cost = sum([float(group['Metrics']['UnblendedCost']['Amount']) for item in items['ResultsByTime'] for group in item['Groups']])
#     return render_template("home2.html", items=items, total_cost=total_cost)

# @views.route('/')
# @views.route('/<string:month>')
# def home(month=None):
#     if month:
#         start = datetime.datetime.strptime(month, '%Y-%m')
#         end = start + relativedelta(months=1, days=-1)
#     else:
#         start = datetime.datetime.today().replace(day=1)
#         end = start + relativedelta(months=1, days=-1)

#     result = client.get_cost_and_usage(
#         TimePeriod={
#             'Start': start.strftime('%Y-%m-%d'),
#             'End': end.strftime('%Y-%m-%d')
#         },
#         Granularity='MONTHLY',
#         Metrics=['UnblendedCost'],
#         GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
#     )

#     items = result
#     total_cost = sum([float(group['Metrics']['UnblendedCost']['Amount']) for item in items['ResultsByTime'] for group in item['Groups']])
#     return render_template("home.html", items=items, total_cost=total_cost)

# @views.route('/')
# @views.route('/<string:month>')
# def home(month=None):
#     if month:
#         start = datetime.strptime(month, '%Y-%m')
#         end = start + relativedelta(months=1, days=-1)
#     else:
#         start = datetime.today().replace(day=1)
#         end = start + relativedelta(months=1, days=-1)

#     result = client.get_cost_and_usage(
#         TimePeriod={
#             'Start': start.strftime('%Y-%m-%d'),
#             'End': end.strftime('%Y-%m-%d')
#         },
#         Granularity='MONTHLY',
#         Metrics=['UnblendedCost'],
#         GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
#     )

#     items = result
#     total_cost = sum([float(group['Metrics']['UnblendedCost']['Amount']) for item in items['ResultsByTime'] for group in item['Groups']])
    
#     # create a list of month options to be included in the dropdown
#     month_options = []
#     current_month = datetime.today().replace(day=1)
#     for i in range(6):
#         month_options.append(current_month.strftime('%Y-%m'))
#         current_month -= relativedelta(months=1)

#     return render_template("home.html", items=items, total_cost=total_cost, month_options=month_options)

# @views.route('/', methods=['GET', 'POST'])
# @views.route('/<string:month>', methods=['GET', 'POST'])
# def home(month=None):
#     if request.method == 'POST':
#         if month:
#             start = datetime.strptime(month, '%Y-%m')
#             end = start + relativedelta(months=1, days=-1)
#         else:
#             start = datetime.today().replace(day=1)
#             end = start + relativedelta(months=1, days=-1)

#         if request.method == 'POST':
#             start_date_str = request.form['start-date']
#             end_date_str = request.form['end-date']
#             start = datetime.strptime(start_date_str, '%Y-%m-%d')
#             end = datetime.strptime(end_date_str, '%Y-%m-%d')

#         result = client.get_cost_and_usage(
#             TimePeriod={
#                 'Start': start.strftime('%Y-%m-%d'),
#                 'End': end.strftime('%Y-%m-%d')
#             },
#             Granularity='MONTHLY',
#             Metrics=['UnblendedCost'],
#             GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
#         )

#         items = result
#         total_cost = sum([float(group['Metrics']['UnblendedCost']['Amount']) for item in items['ResultsByTime'] for group in item['Groups']])
        
#         # create a default start and end date
#         default_start = datetime.today().replace(day=1)
#         default_end = default_start + relativedelta(months=1, days=-1)

#     return render_template("home.html", items=items, total_cost=total_cost, default_start=default_start, default_end=default_end)
#     return items



@views.route('/', methods=['GET', 'POST'])
@views.route('/<string:month>', methods=['GET', 'POST'])
def home(month=None):
    if request.method == 'POST':
        start_date = request.form.get('start-date')
        end_date = request.form.get('end-date')
        time_period = {
            'Start': start_date,
            'End': end_date
        }
    else:
        time_period = {
            'Start': '2023-03-01',
            'End': '2023-03-31'
        }
        
    response = client.get_cost_and_usage(
        TimePeriod=time_period,
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    items = response['ResultsByTime']
    total_cost = sum([float(group['Metrics']['UnblendedCost']['Amount']) for item in items for group in item['Groups']])
    default_start = datetime.strptime(time_period['Start'], '%Y-%m-%d')
    default_end = datetime.strptime(time_period['End'], '%Y-%m-%d')
    
    return render_template('home.html', items=items, total_cost=total_cost, default_start=default_start, default_end=default_end)

