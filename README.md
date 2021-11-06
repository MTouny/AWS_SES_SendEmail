# sendEmail pipeline in DashyDash

# Feature of sendEmail Lambda Function
	1- Send Email
	2- Send Email with Attachment
	3- Send Email using Template
	4- You can now set AWS Region for SES you are working with
	5- You can set specific Character set
	6- Attach specific SES ConfigurataionSet

## Sample Message

# Send Normal Email
```
message = {
	"source": "a@test.com",
	"destination": ["b@test.com"],
	"subject": "",
	"body": "" // Can be text or HTML
}
```

# Send Templated Email
```
message = {
	"source": "a@test.com",
	"destination": ["b@test.com"],
	"Template": "Template_Name",
	"ConfigurationSetName": "ConfigSet",
	"TemplateData": "{ }" // 
}
```

# Send Email with Attachment
```
message = {
	"source": "a@test.com",
	"destination": ["b@test.com"],
	"subject": "test",
	"ConfigurationSetName": "ConfigSet",
	"BODY_TEXT": "test text",
	"BODY_HTML": """\
					<html>
					<head></head>
					<body>
					<h1>Hello!</h1>
					<p>test html block</p>
					</body>
					</html>
					""",
	"ATTACHMENT": "S3 URI"
}
```

## Code snippet to send event for Email on sendEmail Topic
```
import json
import boto3

def lambda_handler(event, context):
	sns = boto3.client('sns')
	
	message = {}

	sns.publish(
		TopicArn="arn:aws:sns:::sendEmail",
		Message=json.dumps(message)
		)
```
