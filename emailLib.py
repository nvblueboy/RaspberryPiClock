##Email Parser

import configuration, logger

import sys, imaplib, email, datetime, time

def getNewMail():
    config = configuration.Config()
    M = imaplib.IMAP4_SSL(config.imap)
    try:
        rv, data = M.login(config.email, config.password)
    except imaplib.IMAP4.error:
        logger.log("IMAP login failed.")
        return False
    rv, mailboxes = M.list()
    if rv!="OK":
        logger.log("Could not read mailboxes.")
        return False
    rv, data = M.select("INBOX")
    if rv!="OK":
        logger.log("Could not read mailboxes.")
        return False
    
    rv, data = M.search(None, "UnSeen")
    output= []
    if len(data[0].split()) == 0:
        return "No emails"
    for num in data[0].split():
        rv, data = M.fetch(num, "(RFC822)")
        msg = email.message_from_string(data[0][1].decode("utf-8"))
        t = time.mktime(email.utils.parsedate_tz(msg.get('date'))[:9])
        if msg.is_multipart():
            for payload in msg.get_payload():
                output.append((payload.get_payload(),t))
        else:
            output.append((t,msg.get_payload()))
    return output

        
if __name__ == "__main__":
    for i in getNewMail():
        print(i)
