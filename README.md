# CSCI 455 Spring 2024 Project

*Julia Dewhurst ([@juliaDewhurst](https://github.com/juliaDewhurst)), Joseph Melancon ([@jmelancon](https://github.com/jmelancon)), Anna Wille ([@annawille](https://github.com/annawille)), Maya Wyganowska ([@mayawyganowska](https://github.com/mayawyganowska))*

## Project Description

From the project definition (Prof. Hassan Reza, UND):

>Electronic Medical Record Keeping Systems, known as EMRKS, allow physicians, nurses, and lab technicians to read medical records from a computer rather than have to chase down paper files when time is critical. 
In simple form, EMRKS is used to automate the paper medical record-keeping system. In EMRKS all the patient-related tasks are performed electronically instead of manually. Not only can electronic records be misplaced as paper records can, but the information in the record is more accurate as well as legible.
A portable medical record comprises a plurality of processors connected by a network to the database including a medical record, a plurality of folders for storing messages in the medical record, a means for controlling access to each of the folders, and a means for sorting each message into at least one folder.

In our report, we summarized our work as such:

>The Electronic Medical Record Keeping System that was created for an optometry clinic supports all the actions and actors that should be present in an optometry clinic. This system holds patient information related to appointments, prescriptions, medical history, and bills. This system is a centralized platform that securely holds this data. The major actions that occur within the system include creating, modifying and retrieving appointments, appointment notes, bills, and other sensitive patient information. These actions allow for a more streamlined version of data storage. 

## Running the Project

To run the project, simply clone this repo and use `docker compose up`
to deploy a prepopulated MySQL database and to deploy all Patient
interface components. The Employee interface may be accessed by 
running [employee-frontend/frontend.py](employee-frontend/frontend.py)
on a local computer that has Python3 installed with TK. TK usually
ships with Python by default. The `mysql-connector-python` library
is also needed for the Employee frontend. This can be installed with
`pip install mysql-connector-python`.

The Employee frontend must be given a server IP or URL on login to function. Be sure
that you know the IP address of your server before running. If you are
running the Compose script locally, you may use `localhost` as the 
server address.

## Account Credentials

To access the database, there's a few default credentials set.

### MySQL Database

The only default user created intentionally for direct database
acceess is `root`. The password (as defined in the compose file)
is `toortoor`.

### Patient Frontend

Any patient can log in on the web interface. All passwords are
`changeme` by default. Usually, Jane Doe, SSN `123-12-3123`, is 
the account we used for debugging.

### Employee Frontend

There's a few default employees created, one for each actor
in our use case model. See the table below.

| Account Type        | Account ID | Password       |
|---------------------|------------|----------------|
| Receptionist        | `1001`     | `receptionist` |
| Administrator       | `2001`     | `admin`        |
| Optometrist         | `3001`     | `opt`          |
| Optometry Assistant | `4001`     | `optass`       |
