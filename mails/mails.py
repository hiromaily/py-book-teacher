# coding:utf-8
import base64
import configs.configs as con
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib

"""mail module"""


def __create_message(from_addr, to_addr, subject, body, mime=None, attach_file=None):
    """
    [private] create message of E-mail
    @:param from_addr
    @:param to_addr
    @:param subject
    @:param body
    @:param mime : MIME
    @:param attach_file : attachment
    @:return : message
    """

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = formatdate()
    msg["Subject"] = subject
    body = MIMEText(body)
    msg.attach(body)

    # attachment
    if mime is not None and attach_file is not None:
        attachment = MIMEBase(mime['type'], mime['subtype'])
        file = open(attach_file['path'])
        attachment.set_payload(file.read())
        file.close()

        # Encoders.encode_base64(attachment)
        attachment = base64.b64encode(attachment)
        msg.attach(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])

    return msg


def __send_email(from_addr, to_addrs, msg):
    """
    [private] send E-mail
    @:param from_addr
    @:param to_addr (list)
    @:param msg
    """
    smtp = con.ConfigClass.get_conf("mail", "smtp")
    port = con.ConfigClass.get_conf("mail", "port")
    address = con.ConfigClass.get_conf("mail", "address")
    password = con.ConfigClass.get_conf("mail", "password")

    smtp_obj = smtplib.SMTP(smtp, int(port))
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.ehlo()

    try:
        print("sending mail")
        smtp_obj.login(address, password)
        smtp_obj.sendmail(from_addr, to_addrs, msg.as_string())
    # except:
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] failed to send mail!")
        smtp_obj.close()
        return

    print("finished to send mail!")
    smtp_obj.close()


def send_email(body, from_addr=None, to_addr=None, subject=None):
    """
    [public] send mail
    """
    if from_addr is None:
        from_addr = con.ConfigClass.get_conf("mail", "address")

    if to_addr is None:
        to_addr = con.ConfigClass.get_conf("mail", "toaddr")

    if subject is None:
        subject = con.ConfigClass.get_conf("mail", "subject")

    # create message
    msg = __create_message(from_addr, to_addr, subject, body)

    # send
    __send_email(from_addr, [to_addr], msg)

