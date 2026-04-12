import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('student_table')


# Fix Decimal issue (for GET)
def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    return obj


def lambda_handler(event, context):
    method = event['httpMethod']

    # ================== CREATE (POST) ==================
    if method == 'POST':
        body = json.loads(event['body'])

        student_id = str(uuid.uuid4())

        table.put_item(
            Item={
                "studentID": student_id,
                "name": body.get("name"),
                "age": body.get("age"),
                "phone": body.get("phone")
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Student added",
                "studentID": student_id
            })
        }

    # ================== READ (GET) ==================
    elif method == 'GET':
        params = event.get("queryStringParameters")

        # 🔹 Get by ID
        if params and params.get("studentID"):
            response = table.get_item(
                Key={"studentID": params.get("studentID")}
            )

            return {
                "statusCode": 200,
                "body": json.dumps(response.get("Item", {}), default=convert_decimal)
            }

        # 🔹 Get all
        response = table.scan()

        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", []), default=convert_decimal)
        }

    # ================== UPDATE (PUT) ==================
    elif method == 'PUT':
        body = json.loads(event['body'])

        student_id = body.get("studentID")

        table.update_item(
            Key={"studentID": student_id},
            UpdateExpression="set #n=:n, age=:a, phone=:p",
            ExpressionAttributeNames={
                "#n": "name"
            },
            ExpressionAttributeValues={
                ":n": body.get("name"),
                ":a": body.get("age"),
                ":p": body.get("phone")
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps("Student updated")
        }

    # ================== DELETE ==================
    elif method == 'DELETE':
        params = event.get("queryStringParameters")

        student_id = params.get("studentID")

        table.delete_item(
            Key={"studentID": student_id}
        )
        return {
            "statusCode": 200,
            "body": json.dumps("Student deleted")
        }

    # ================== ERROR ==================
    else:
            "statusCode": 400,
            "body": json.dumps("Invalid method")
        }        return {

