import boto3
import json
import os
import sys
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def lambda_handler(event, context):
    # logging configuration
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format=f'%(asctime)s %(levelname)s %(message)s'
    # )
    # logger = logging.getLogger()

    # msgdict = {}
    # charset = ''
    # aws_region = ''

    for record in event['Records']:

        msgdict = json.loads(record['Sns']['Message'])

        if msgdict.get("AWS_REGION") is None:
            aws_region = "us-east-2"
        else:
            aws_region = msgdict["AWS_REGION"]

        if msgdict.get("CHARSET") is None:
            charset = "UTF-8"
        else:
            charset = msgdict["CHARSET"]

        client = boto3.client('ses', region_name=aws_region)

        try:
            if 'Template' in msgdict:

                print("Process Template")

                source = msgdict["source"]
                destinations = [a for a in msgdict["destination"].split(',')]
                template = msgdict["Template"]
                templatedata = msgdict["TemplateData"]
                configurationset = msgdict["ConfigurationSetName"]

                # send the email
                response = client.send_templated_email(
                    Destination={'ToAddresses': destinations},
                    Template=template,
                    TemplateData=templatedata,
                    ConfigurationSetName=configurationset,
                    Source=source, )

                return {'statusCode': 200, 'body': json.dumps("email sent")}

            elif 'ATTACHMENT' in msgdict:
                
                print("Process Email with Attachment")

                source = msgdict["source"]
                destinations = [a for a in msgdict["destination"].split(',')]
                subject = msgdict["subject"]
                attachment = msgdict["ATTACHMENT"]
                configurationset = msgdict["ConfigurationSetName"]
                body_text = msgdict["BODY_TEXT"]
                body_html = msgdict["BODY_HTML"]

                msg = MIMEMultipart('mixed')
                msg['Subject'] = subject
                msg['From'] = source
                msg['To'] = destinations

                msg_body = MIMEMultipart('alternative')

                textpart = MIMEText(body_text.encode(charset), 'plain', charset)
                htmlpart = MIMEText(body_html.encode(charset), 'html', charset)

                msg_body.attach(textpart)
                msg_body.attach(htmlpart)
                att = MIMEApplication(open(attachment, 'rb').read())
                att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))

                msg.attach(msg_body)
                msg.attach(att)

                # send the email
                response = client.send_raw_email(
                    Destination=[destinations],
                    RawMessage={
                        'Data': msg.as_string(),
                    },
                    Source=source,
                    ConfigurationSetName=configurationset, )

                return {'statusCode': 200, 'body': json.dumps("email sent")}

            else:
                
                print("Process Email")

                source = msgdict["source"]
                destinations = [a for a in msgdict["destination"].split(',')]
                subject = msgdict["subject"]
                message = msgdict["body"]

                # send the email
                response = client.send_email(
                    Destination={'ToAddresses': destinations},
                    Message={
                        'Body': {'Text': {'Charset': charset, 'Data': message, }, },
                        'Subject': {'Charset': charset, 'Data': subject, },
                    },
                    Source=source)

                return {'statusCode': 200, 'body': json.dumps("email sent")}

        except:
            print('Error')
            print(msgdict)

            # To catch the exception and error messages
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append(
                    "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" % ex_value)
            print("Stack trace : %s" % stack_trace)

            return {'statusCode': 501, 'body': json.dumps("Failed ")}
