"""
Stores Shopify subscriber emails using GraphQL queries.
"""
import csv
import datetime
import json
import os
from pathlib import Path
import pytz
import shopify
from order_followup.helpers import order_followup_query
from order_followup.helpers import get_shopify_api_credentials

MONKEE = Path(os.getenv('MONKEE'))
CSV_OUTPUT_PATH = MONKEE.joinpath("order_follow_up/accepts_marketing/accepts_marketing.csv")
LAST_DATES_PATH = MONKEE.joinpath("order_follow_up/shopify/outreach report dates.txt")


def construct_date_range_string(start_date: str, before_date: str):
    """"
    Returns a string used with the start and end dates (UTC time) used as the 'query' parameter. It's used to filter orders by dates.
    @param start_date: earliest order date (inclusive)
    @param before_date: cutoff date (exclusive)
    Example: created_at:>='2023-02-17T06:00:00Z' AND created_at:<'2023-02-18T06:00:00Z'\"
    """
    return """"created_at:>='{0}T06:00:00Z' AND created_at:<'{1}'\"""".format(start_date, before_date)


def construct_graphql_query(date_range_string: str):
    """
    Returns a string to be used with a GraphQL request with an embedded date range query.
    @param date_range_string: string used for the start and end dates (UTC time)
    """
    return order_followup_query.format(date_range_string)


def execute_grapql_query(graphql_query: str):
    """Return the result of a Shopify GraphQL query."""
    session = get_session(api_version = '2023-01')
    shopify.ShopifyResource.activate_session(session)    
    return json.loads(shopify.GraphQL().execute(query=graphql_query))


def get_before_date_as_string(date_string: str, days: int):
    """
    Returns a UTC date string in the format of 2023-02-17T06:00:00Z
    @param date_string: a date string in the format of '2023-02-17'
    @param days: the number of days to add or subtract from date_string
    """
    no_tz = datetime.datetime.strptime(date_string, "%Y-%m-%d") + datetime.timedelta(days=days)
    next_date_utc = no_tz.astimezone(pytz.timezone('UTC'))
    return datetime.datetime.strftime(next_date_utc, "%Y-%m-%dT%H:%M:%SZ")


def get_session(api_version = '2023-01')-> shopify.Session:
    """Returns a shopify.Session object"""
    creds = get_shopify_api_credentials()
    store_url = "groove-monkee.myshopify.com"    
    session = shopify.Session(store_url, api_version, creds.get('SHOPIFY_ADMIN_API_ACCESS_TOKEN'))
    shopify.ShopifyResource.activate_session(session)
    return session


def parse_query_results(data: dict):
    """
    Yields email addresses for subscribers.
    @param data: a dictionary of query results.
    """
    results = set()
    for node in data['data']['orders']['edges']:     
        status = node['node']['customer']['emailMarketingConsent']['marketingState']
        if status == 'SUBSCRIBED':
            results.add(node['node']['customer']['email'])
    return [[e] for e in results]


def main():
    """
    Manager function that runs the whole process.
    """
    start_date = input("Enter the start date as YYYY-MM-DD: ")
    last_date  = input("Enter the end date (inclusive) as YYYY-MM-DD: ")
    output_filepath = input("Enter the compete path to the csv file to write or hit Enter: ")
    if not output_filepath:
        output_filepath = CSV_OUTPUT_PATH
    before_date = get_before_date_as_string(last_date, days=1)
    date_range_string = construct_date_range_string(start_date, before_date=before_date)
    graphql_query = construct_graphql_query(date_range_string)
    results = execute_grapql_query(graphql_query)    
    emails = parse_query_results(results)
    write_to_file(emails, output_filepath)
    write_to_file([[f"Start date: {start_date}"], [f"Ending date: {last_date}"]], LAST_DATES_PATH)
    print(f"\nStart date: {start_date} End date: {last_date}")
    print(f"Wrote {len(emails)} email addresses to: {output_filepath}\n")


def write_to_file(data, filepath:str):
    """Writes data to a file."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)        


if __name__ == '__main__':  
    main()
    