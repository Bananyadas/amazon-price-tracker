# -*- coding: utf-8 -*-
"""alerter_and_mailer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HCPQ3uFFzqTf9QL3jXjmivI6U66b61PD
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendmail(prod , email_cred):
  self = email_cred[0]
  pswd = email_cred[1]
  fromaddr = email_cred[2]
  toaddr = email_cred[3]

  message = MIMEMultipart()
  message['From'] = fromaddr
  message['To'] = toaddr
  message['Subject'] = "Product Price Alert" + prod

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(self, pswd)
  text = message.as_string()
  server.sendmail(fromaddr, toaddr, text)
  server.quit()

from amazonapi import AmazonAPI
import csv
import time

def pricereader(csvFile):
  prices = {}
  targetdata = {}
  with open(csvFile , 'rb') as F:
    for i in F:
      row = i.strip('\n\r').split(',')
      col = row[0].split('|')
      prices[col[0]] = row[1:]
      targetdata[col[0]] = col[1]
  F.close()
  return prices , targetdata

def updatedprices(oldprice , newprice):
  for i in newprice:
    prod = i[0]
    price = i[1]
    try: oldprice[prod].append(price)
    except KeyError:
      print("product skipped.")
  return oldprice

def pricewrite(newprice, targetdata, csvFile ):
  with open(csvFile , 'wb') as F:
    writer = csv.writer(F)
    for prod in newprice:
      target = targetdata[prod]
      writer.writerow([prod + '|' + target] + newprice[prod])
  F.close()

def findprice(prodID, aws_cred):
  amazon_details = AmazonAPI(aws_cred[0], aws_cred[1], aws_cred[2]) #returns 3 details accesskeyid, secretaccesskey, associate key
  product = amazon_details.lookup(ItemId=prodID)
  return result_title, result.price_and_currency[0]

def addprod(prodID, csvFile, alertWhen, alertType, aws_cred):
  currentprice = findprice(prodID, aws_cred)[1]
  if alertType == "percentChange":
    delta = (float(alertWhen)/100)+1
    alertprice = currentprice*delta

  elif alertType == "desiredprice":
    alertprice = float(alertWhen)

  else: raise ValueError("invalid")
  with open(csvFile, 'a') as F:
    writer = csv.writer(F)
    writer.writerow([prodID + '|' + str(alertprice)] + [currentprice])
  F.close()

def dailyscan(prodIDs, csvFile, aws_cred, email_cred):
  prices, targets = pricereader(csvFile)
  alerts = []
  update = []
  for prodID in prodIDs:
    title, price = findprice(prodID, aws_cred)
    date = time.strfttime("%Y-%m-%d")
    update.append((prodID, date+ '|' + str(price)))

    try:
      if price <= float(targets[prodID]):
        alerts.append(prodID)
    except
      KeyError: pass

updated_prices = updatedprices(update, prices)
pricewrite(updatedprices, targets, csvFile)

for alert in alerts:
  sendmail(alert, email_cred)