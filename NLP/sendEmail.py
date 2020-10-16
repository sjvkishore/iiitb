import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from wsgiref import simple_server
from flask import Flask, request
from flask import Response
import os
from flask_cors import CORS, cross_origin


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)



@app.route("/sendmail", methods=['POST'])
@cross_origin()
def sendEmail():
    try:
        if request.json['emailId'] is not None:

            toaddr = request.json['emailId']  ## email id of the user
            contact_add = "*****@gmail.com"  ## the email id of the support team
            fromaddr = "*****@gmail.com"   ## the email id from where we are going to send the mail
            mobile_number = request.json['mobile_number']
            name = request.json['name']


            # instance of MIMEMultipart
            msg = MIMEMultipart()

            # storing the senders email address
            msg['From'] = fromaddr

            # storing the receivers email address
            msg['To'] = ",".join(toaddr)
            # msg['To'] = toaddr

            # storing the subject
            msg['Subject'] = "Test bot email"

            # string to store the body of the mail
            body = "This will contain attachment"

            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))

            # open the file to be sent
            filename = "projects.txt"
            attachment = open(filename, "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # attach the instance 'p' to instance 'msg'
            msg.attach(p)

            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            s.starttls()

            # Authentication
            s.login(fromaddr,"*******") # give your password here

            # Converts the Multipart msg into a string
            text = msg.as_string()
            # sending the mail
            s.sendmail(fromaddr, toaddr, text)

            # send mail with username , mobile number and email id to concerned team

            # instance of MIMEMultipart
            msg1 = MIMEMultipart()
            # storing the subject
            msg1['Subject'] = "Query For Course Details"

            # string to store the body of the mail
            body1 = "person with name {0} have some queries regarding our course details." \
                   "Please reach to {0} at his mobile number {1} and email id {2}".format(name,mobile_number,toaddr)

            # attach the body with the msg instance
            msg1.attach(MIMEText(body1, 'plain'))

            text = msg1.as_string()
            # sending the mail
            s.sendmail(fromaddr, contact_add, text)

            # terminating the session
            s.quit()

            return Response("Course details is sent to the mail id %s" % toaddr +"\t " +
                            "and your details have been forwarded to the concerned team.")

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)

#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()