import os
import json
import csv

import boto3


def save_to_dynamodb(db_table, item):
	db_table.put_item(
		Item=item
	)


def lambda_handler(event, context):
	# extract info from event
	bucket = event['Records'][0]['s3']['bucket']['name']
	s3_object = event['Records'][0]['s3']['object']['key']

	# temprorary file to store csv downloaded from s3
	tmp_csv_file = '/tmp/' + s3_object

	# Download object from S3
	s3 = boto3.client('s3')
	s3.download_file(bucket, s3_object, tmp_csv_file)

	# creating dynamodb instance
	dynamodb_table = os.environ['dynamodb_table_name']
	db_table = boto3.resource('dynamodb').Table(dynamodb_table)

	# iterate through csv and add all rows
	# csv can have distinct columns only first 2 columns need to be PK and SK resp
	with open(tmp_csv_file, 'r', encoding='utf8') as csv_file:
		reader = csv.DictReader(csv_file)
		for row in reader:
			save_to_dynamodb(db_table, row)

	return {
		'statusCode': 200,
		'body': json.dumps('CSV data successfully added to DynamoDB!!!')
	}
