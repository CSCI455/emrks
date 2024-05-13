'''
CSCI 455 EMRKS Project - Optomet.me Optometry Clinic
Copyright (C) 2024  Julia Dewhurst, Joseph Melancon, Anna Wille, Maya Wyganowska

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import mysql.connector
import uvicorn
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64

from datetime import datetime, date
from decimal import Decimal

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import json
from jwkest import long_to_base64
import bcrypt

cnx = mysql.connector.connect(
    host=os.environ['DBHOST'],
    user=os.environ['DBUSER'],
    password=os.environ['DBPASS'],
    database="Optometry Clinic"
)

cursor = cnx.cursor()

app = FastAPI(root_path="/api")

origins = [
        "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("serverPrivKey.pem"):
    with open("serverPrivKey.pem", "rb") as f:
        data = f.read()
        pwd = os.environ["PRIVKEYPASS"].encode()
        serverKeys = RSA.import_key(data, pwd)
else:
    serverKeys = RSA.generate(4096)
    pwd = os.environ["PRIVKEYPASS"].encode()
    with open("serverPrivKey.pem", "wb") as f:
        data = serverKeys.export_key(passphrase=pwd,
                                    pkcs=8,
                                    protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
                                    prot_params={'iteration_count':131072})
        f.write(data)

print("Server PubKey: ", serverKeys.publickey().export_key())
print("\nServer PrivKey:", serverKeys.export_key())
serverCipher = PKCS1_OAEP.new(serverKeys)

@app.get("/auth/requestpubkey")
def read_pubkey():
    return {
        "kty": "RSA",
        "e": long_to_base64(serverKeys.publickey().e),
        "ext": False,
        "key_ops": ["encrypt"],
        "alg": "RSA-OAEP",
        "n": long_to_base64(serverKeys.publickey().n)
    }


class Echo(BaseModel):
    sentinel: str
    content: list

class Message(BaseModel):
    timestamp: str
    user: str
    content: list

@app.post("/auth/echoobsc")
def write_echoClear(ec: Message):
    """
    API endpoint for validating server connectivity
    """
    recMsg = decodeMessage(ec.content)
    pubkey = json.loads(recMsg.decode("utf-8").replace("\0", ""))["pubkey"]
    # Now echo it back encrypted
    return encodeMessage(recMsg, pubkey)

def verifyCredentials(user: int, password: str) -> bool:
    """
    Internal function to validate user password
    Resistant to SQL injection
    """
    # Update database
    cnx.commit()
    
    # Attempt to pull password
    cursor.execute(f"SELECT PasswordHash from PASSWORD_PATIENT WHERE PatientSSN={user}")
    
    # Isolate any returned pw entries
    res = [x[0] for x in cursor.fetchall()]
    
    # Fail if there isn't just one
    if len(res) != 1:
        return False
    
    # Get the proper PyBytes from MySQL returned hash
    pwHash = res[0][2:-1].encode()

    # See if password matches hash
    return pwHash == bcrypt.hashpw(password.encode(), pwHash)


@app.post("/auth/verifyAuth")
def verifyAuthenticationPass(ec: Message):
    """
    API endpoint to check if credentials are valid
    Verified resistant against SQL injection
    """
    # Decode message
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))

    # Strip any SSN delimeters if present and cast to int
    user = int(ec.user.replace("-", ""))

    # Verify with credential matching fn
    passwordMatches = verifyCredentials(user, recMsg["password"])

    # Return status
    if passwordMatches:
        return encodeMessage(json.dumps({
                "passed": True
            }).encode("utf-8"), recMsg["pubkey"])
    else:
        return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])


@app.post("/billing/confirmCancellable")
def verifyCaseMutable(ec: Message):
    """
    API endpoint to confirm a case is cancellable
    Validated resistant against SQL injection
    """
    # Decode message
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))

    # Strip any SSN delimeters if present and cast to int
    user = int(ec.user.replace("-", ""))

    # Verify with credential matching fn
    passwordMatches = verifyCredentials(user, recMsg["password"])

    # Return status
    if passwordMatches:
        # Pull case by ID
        cursor.execute(f"SELECT PatientSSN, Status, DateTime from APPOINTMENT where CaseID={int(recMsg["message"]["caseid"])};")
        res = cursor.fetchall()

        # Ensure only 1 case is returned and that the user
        # owns the case
        if len(res) == 1 and res[0][0] == user:
            # Check that the case meets cancellation criteria
            # (Scheduled and two days notice)
            if res[0][1] == "Scheduled" and res[0][2].timestamp() > datetime.now().timestamp() + 172800:
                # Return affirmative
                return encodeMessage(json.dumps({
                        "passed": True,
                        "date": res[0][2].strftime("%B %d %Y @ %-I:%M %p")
                    }).encode("utf-8"), recMsg["pubkey"])
            else: 
                return encodeMessage(json.dumps({
                    "passed": False
                }).encode("utf-8"), recMsg["pubkey"])
        else:
            return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])
    else:
        return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])


@app.post("/billing/confirmPayable")
def verifyBillMutable(ec: Message):
    """
    API endpoint to confirm a bill is payable
    Validated resistant against SQL injection
    """
    # Decode message
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))

    print(recMsg)

    # Strip any SSN delimeters if present and cast to int
    user = int(ec.user.replace("-", ""))

    # Verify with credential matching fn
    passwordMatches = verifyCredentials(user, recMsg["password"])

    # Return status
    if passwordMatches:
        # Pull bill details
        cursor.execute(f"SELECT A.PatientSSN, BillTotal, P.CredCardNo from BILLS INNER JOIN `Optometry Clinic`.APPOINTMENT A on BILLS.CaseID = A.CaseID INNER JOIN `Optometry Clinic`.PATIENT P on A.PatientSSN = P.SSN where BillID={int(recMsg["message"]["billid"])} and Details=\"Unpaid\";")
        res = cursor.fetchall()
        
        # Verify only one bill is returned and that the
        # user owns the bill
        if len(res) == 1 and res[0][0] == user:
            # Return affirmative plus some info for
            # populating the cancellation screen
            return encodeMessage(json.dumps({
                    "passed": True,
                    "cost": f"${res[0][1]}",
                    "cardno": str(res[0][2])[-4:]
                }).encode("utf-8"), recMsg["pubkey"])
        else:
            return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])
    else:
        return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])


@app.post("/confirmUpdatable")
def verifyFileUpdatable(ec: Message):
    """
    API endpoint to confirm a user's file is updatable
    Returns some extra data so the JS can prepopulate fields
    Validated resistant against SQL injection
    """
    # Decode message
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))

    print(recMsg)

    # Strip any SSN delimeters if present and cast to int
    user = int(ec.user.replace("-", ""))

    # Verify with credential matching fn
    passwordMatches = verifyCredentials(user, recMsg["password"])

    # Return status
    if passwordMatches:
        # Pull user file details
        cursor.execute(f"SELECT FName, LName, Email, PhoneNo, CredCardNo FROM PATIENT WHERE SSN={user};")
        res = cursor.fetchall()
        
        # Ensure only one file was returned
        if len(res) == 1:
            return encodeMessage(json.dumps({
                    "passed": True,
                    "first": res[0][0],
                    "last": res[0][1],
                    "email": res[0][2],
                    "phone": res[0][3],
                    "lastfourcc": str(res[0][4])[-4:]
                }).encode("utf-8"), recMsg["pubkey"])
        else:
            return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])
    else:
        return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])


@app.post("/updateContact")
def updateContact(ec: Message):
    """
    API endpoint to update contact info
    Validated resistant against SQL injection
    """
    # Decode message
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))

    print(recMsg)

    # Strip any SSN delimeters if present and cast to int
    user = int(ec.user.replace("-", ""))

    # Verify with credential matching fn
    passwordMatches = verifyCredentials(user, recMsg["password"])

    # Return status
    if passwordMatches:
        content = recMsg["message"]

        # Pull some bools
        updPass = content["passupd"]
        updCC = content["ccupd"]

        if updCC:
            # Validate expiration date
            expMonth = int(content["ccexp"].replace("/", "-").split("-")[0])
            if not 0 < expMonth < 13:
                return encodeMessage(json.dumps({
                        "passed": False,
                        "reason": "Not a month: " + str(expMonth)
                    }).encode("utf-8"), recMsg["pubkey"])
            expYear = int(content["ccexp"].replace("/", "-").split("-")[1])
            if expYear < 100:
                expYear += 2000
        
            # Concatenate for MySQL
            expiration = f"{expYear}-{expMonth}-01"
            
            # Potential SQL injection on credit card name, so this is
            # handled outside the f-string.
            cursor.execute(f"UPDATE PATIENT SET CredCardNo={int(content["ccnum"].replace("-", ""))}, CVV={int(content["cccvv"])}, ExpDate=CAST('{expiration}' AS DATE), CredCardName=%s WHERE Ssn={user};", (content["ccname"],))

        # Read in other vars
        fname = content["fname"]
        lname = content["lname"]
        email = content["email"]
        phone = int(content["phone"].replace("-", ""))

        # Write to database
        # This statement is vulnerable to SQL injection so more precautions
        # are taken surrounding the f-string
        cursor.execute(f"UPDATE PATIENT SET Fname=%s, Lname=%s, Email=%s, PhoneNo={phone} WHERE Ssn={user};", (fname, lname, email,))

        if updPass:
            # Password
            storageSalt = bcrypt.gensalt()
            storageHash = bcrypt.hashpw(content["pw"].encode(), storageSalt)

            cursor.execute(f"UPDATE PASSWORD_PATIENT SET PasswordHash=\"{storageHash}\" WHERE PatientSSN={user};")

        # Perform commit
        cnx.commit()

        return encodeMessage(json.dumps({
                "passed": True
            }).encode("utf-8"), recMsg["pubkey"])
    else:
        return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])

@app.post("/cancelAppt")
def cancelAppt(ec: Message):
    """
    API endpoint to cancel a case
    Validated resistant against SQL injection
    """
    # Decode message
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))

    # Strip any SSN delimeters if present and cast to int
    user = int(ec.user.replace("-", ""))

    # Verify with credential matching fn
    passwordMatches = verifyCredentials(user, recMsg["password"])

    if passwordMatches:
        # Grab some details that need to be returned if we cancel
        cursor.execute(f"SELECT PatientSSN, Status, DateTime from APPOINTMENT where CaseID={int(recMsg["message"]["caseid"])};")
        res = cursor.fetchall()
        
        # Double check that everything lines up, including ensuring
        # that the user cancelling the appointment owns it
        if len(res) == 1 and res[0][0] == user:

            # Check that the appointment is scheduled and more than two days out
            if res[0][1] == "Scheduled" and res[0][2].timestamp() > datetime.now().timestamp() + 172800:

                # Cancel Appt
                cursor.execute(f"UPDATE APPOINTMENT SET Status=\"Cancelled\" WHERE CaseID = {int(recMsg["message"]["caseid"])};")
                cnx.commit()

                # Return status
                return encodeMessage(json.dumps({
                        "passed": True,
                        "date": res[0][2].strftime("%B %d %Y @ %-I:%M %p")
                    }).encode("utf-8"), recMsg["pubkey"])
            else: 
                return encodeMessage(json.dumps({
                    "passed": False
                }).encode("utf-8"), recMsg["pubkey"])
        else:
            return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])
    else:
        return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])


@app.post("/billing/authorizeBill")
def verifyBillMutable(ec: Message):
    """
    API endpoint to authorize bill payment.
    Validated resistant against SQL injection.
    """
    # Decode message
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))

    print(recMsg)

    # Strip any SSN delimeters if present and cast to int
    user = int(ec.user.replace("-", ""))

    # Verify with credential matching fn
    passwordMatches = verifyCredentials(user, recMsg["password"])

    # Return status
    if passwordMatches:
        # Grab bill details as well as info needed for receipt printing
        cursor.execute(f"SELECT A.PatientSSN, BillTotal, P.CredCardNo, A.DateTime from BILLS INNER JOIN `Optometry Clinic`.APPOINTMENT A on BILLS.CaseID = A.CaseID INNER JOIN `Optometry Clinic`.PATIENT P on A.PatientSSN = P.SSN where BillID={int(recMsg["message"]["billid"])} and Details=\"Unpaid\";")
        res = cursor.fetchall()
        
        # Verify only one bill was returned and that the user owns the bill
        if len(res) == 1 and res[0][0] == user:
            # Approve the bill
            cursor.execute(f"UPDATE BILLS SET PaymentType=\"Credit Card\", Details=\"Paid\" WHERE BillID = {int(recMsg["message"]["billid"])};")
            cnx.commit()

            # Return a confirmation containing bill details. The 
            # application will then generate a receipt locally.
            return encodeMessage(json.dumps({
                    "passed": True,
                    "date": res[0][3].strftime("%B %d %Y @ %-I:%M %p"),
                    "cost": f"${res[0][1]}"

                }).encode("utf-8"), recMsg["pubkey"])
        else:
            return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])
    else:
        return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])


@app.post("/homedata")
def requestHomeData(ec: Message):
    """
    API endpoint to retreive data to populate home screen
    Verified that no SQL injection can occur.
    """
    # Decode message
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))

    print(recMsg)

    # Strip any SSN delimeters if present and cast to int
    user = int(ec.user.replace("-", ""))

    # Verify with credential matching fn
    passwordMatches = verifyCredentials(user, recMsg["password"])

    # Return status
    if passwordMatches:

        # Create a dict that gets returned to the user
        # for home screen population
        returnPackage = {
            "bio":{
                "fname": "",
                "phone": "",
                "email": "",
                "credcard": ""
            },
            "upcoming": [],
            "bills": [],
            "prescriptions":[]
        }

        # Pull first name
        cursor.execute(f"SELECT Fname from PATIENT WHERE SSN={user};")
        returnPackage["bio"]["name"] = cursor.fetchall()[0][0]

        # Pull phone
        cursor.execute(f"SELECT PhoneNo from PATIENT WHERE SSN={user};")
        returnPackage["bio"]["phone"] = str(cursor.fetchall()[0][0])
        
        # If the phone can be formatted as (000)-000-0000, do it
        if len(returnPackage["bio"]["phone"]) == 10:
            ph = returnPackage["bio"]["phone"]
            returnPackage["bio"]["phone"] = f"({ph[:3]})-{ph[3:6]}-{ph[6:]}"

        # Pull email
        cursor.execute(f"SELECT Email from PATIENT WHERE SSN={user};")
        returnPackage["bio"]["email"] = cursor.fetchall()[0][0]

        # Pull last four of the credit card number
        cursor.execute(f"SELECT CredCardNo from PATIENT WHERE SSN={user};")
        returnPackage["bio"]["credcard"] = str(cursor.fetchall()[0][0])[-4:]

        # Pull future cases
        cursor.execute(f"SELECT Status, CaseID, DateTime from APPOINTMENT WHERE PatientSSN={user} AND DateTime > now();")
        
        # Scrub through each row
        for line in cursor.fetchall():

            # Step through each column
            output = []
            for item in line:
                # We want to return formatted dates so look out for
                # those. If the date is more than 2 days out, 
                # leave a bool notifying the frontend that
                # things can be cancelled.
                if isinstance(item, datetime):
                    output.append(item.strftime("%B %d %Y @ %-I:%M %p"))

                    nowTimestamp = datetime.now().timestamp()
                    apptTimestamp = item.timestamp()

                    if apptTimestamp - nowTimestamp < 172800:
                        canCancel = False
                    else:
                        canCancel = True
                else:
                    output.append(item)
            returnPackage["upcoming"].append(output + [canCancel])
        
        # Grab past cases
        cursor.execute(f"SELECT B.BillID, APPOINTMENT.CaseID, DateTime, B.BillTotal, B.PaymentType from APPOINTMENT INNER JOIN `Optometry Clinic`.BILLS B on APPOINTMENT.CaseID = B.CaseID WHERE PatientSSN={user} AND DateTime < now() AND Status!=\"Cancelled\";")
        for line in cursor.fetchall():
            # Same deal with ensuring time formatting
            output = []
            for item in line:
                if isinstance(item, datetime):
                    output.append(item.strftime("%B %d %Y @ %-I:%M %p"))
                elif isinstance(item, Decimal):
                    output.append(f"${item}")
                else:
                    output.append(item)
            returnPackage["bills"].append(output)
        
        # Select prescriptions
        cursor.execute(f"SELECT PrescriptionID, CaseID, StartDate, ExpDate, Details from PRESCRIPTION where PatientSSN = {user};")
        for line in cursor.fetchall():
            # Return a string for if a prescription is Expired/Active/Future
            # This is done serverside since this sounded awful to do in JS
            output = []
            isActive = "Expired"
            if line[2] <= date.today() <= line[3]:
                isActive = "Active"
            elif line[2] >= date.today():
                isActive = "Future"
            
            # More time formatting
            for item in line:
                if isinstance(item, date):
                    output.append(item.strftime("%B %d %Y"))
                elif isinstance(item, Decimal):
                    output.append(f"${item}")
                else:
                    output.append(item)
            returnPackage["prescriptions"].append([isActive] + output)

        # Return the homescreen data object
        return encodeMessage(json.dumps({
                "passed": True,
                "content": returnPackage
            }).encode("utf-8"), recMsg["pubkey"])
    else:
        return encodeMessage(json.dumps({
                "passed": False
            }).encode("utf-8"), recMsg["pubkey"])

@app.post("/register")
def registerPatient(ec: Message):
    """
    API endpoint for user registration.
    Validated resistant against SQL injection.
    """
    recMsg = json.loads(decodeMessage(ec.content).decode("utf-8").replace("\0", ""))
    content = recMsg["message"]

    # Validate SSN isn't registered
    ssn = int(content["SSN"].replace("-", ""))
    cursor.execute(f"SELECT Fname from PATIENT WHERE Ssn={ssn};")
    res = cursor.fetchall()
    
    # Check length of returned values. If it's non-zero,
    # the SSN is already in the system
    if len(res) != 0:
        return encodeMessage(json.dumps({
                "registered": False,
                "reason": "SSN already registered in system"
            }).encode("utf-8"), recMsg["pubkey"])
    
    # Validate expiration date
    expMonth = int(content["ExpDate"].replace("/", "-").split("-")[0])
    if not 0 < expMonth < 13:
        return encodeMessage(json.dumps({
                "registered": False,
                "reason": "Not a month: " + str(expMonth)
            }).encode("utf-8"), recMsg["pubkey"])
    expYear = int(content["ExpDate"].replace("/", "-").split("-")[1])
    if expYear < 100:
        expYear += 2000
    
    # Concatenate for MySQL
    expiration = f"{expYear}-{expMonth}-01"
    print(expiration)

    # Read in other vars
    fname = content["FName"]
    lname = content["LName"]
    email = content["Email"]
    phone = int(content["PhoneNo"].replace("-", ""))
    ccnum = int(content["CredCardNo"].replace("-", ""))
    ccname = content["CredCardName"]
    cvv = int(content["CVV"])

    # Write to database
    # This statement may be vulneralble to SQL injection as
    # strings are handled, so f-strings are not used for string data.
    # The execption to this is the string expiration, but this is
    # parsed locally before execution and will not be of issue.
    cursor.execute(f"INSERT INTO PATIENT VALUES(%s, %s, %s, {phone}, {ccnum}, {cvv}, DATE '{expiration}', {ssn}, %s)",
                   (fname, lname, email, ccname,))

    # Password
    storageSalt = bcrypt.gensalt()
    storageHash = bcrypt.hashpw(content["Password"].encode(), storageSalt)

    cursor.execute(f"INSERT INTO PASSWORD_PATIENT VALUES({ssn}, \"{storageHash}\");")

    # Perform commit
    cnx.commit()

    # Now echo it back encrypted
    return encodeMessage(json.dumps({
            "registered": True,
            "reason": "Good job buckaroo"
        }).encode("utf-8"), recMsg["pubkey"])

def decodeMessage(cipherBlocks):
    # Decrypt message
    clearText = b''

    # For each block, unencode the base64 data
    # then use the server's privkey to decrypt.
    for block in cipherBlocks:
        base64_bytes = (block).encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        clearText += serverCipher.decrypt(message_bytes)

    # Return the plaintext
    return clearText

def encodeMessage(plainText, pubKey):
    # Import the pubkey for encryption
    clientKey = RSA.importKey(pubKey)
    clientCipher = PKCS1_OAEP.new(clientKey)

    # Make a list and determine how many blocks are needed
    msgBlocks = []
    completeBlockCount = len(plainText) // 216

    # Encrypt in 216-bit blocks and encode to base64
    for i in range(completeBlockCount):
        msgBlocks.append(
            base64.b64encode(clientCipher.encrypt(plainText[i * 216:(i + 1) * 216])).decode("ascii")
        )

    # Encrypt final block
    msgBlocks.append(
        base64.b64encode(clientCipher.encrypt(plainText[(completeBlockCount) * 216:])).decode("ascii")
    )

    # Return the blocks
    return msgBlocks

if __name__ == '__main__':
    uvicorn.run("main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
    )
