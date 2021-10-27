# Airflow Pipeline processing

## Pre requisites:

In order to run this solution properly you will need to install Airflow, and configure an AWS Redshift cluster. 

* Airflow installation (instructions for MacOS):
1) Set up the environment variable for airflow

    >export AIRFLOW_HOME=~/airflow 
    
2) Install Airflow Python Package (ideally in an environment)

    >pip3 install apache-airflow
    >pip3 install typing_extensions
    >pip3 install 'apache-airflow[postgres]'
    >pip3 install apache-airflow-providers-amazon
    
3) [OPTIONAL] Edit airflow.cfg line 111 so airflow doesn’t load the examples:

    >load_examples = False
    
4) Start Airflow
    
    >airflow db init
    
5) Create initial user (substitute USR, PWD and other information with your choice of Admin user and Password)
    
    >airflow users  create --role Admin --username USR --email EMAIL --firstname FIRSTNAME --lastname LASTNAME --password PWD
    
6) Start airflow
    
    >airflow webserver -p 8080
    
7) Start Airflow scheduler (in another terminal window)
    
    >Airflow scheduler
    
8) Open the airflow in the browser by accessing the following address: http://localhost:8080/


* Redshift setup:
1) Initiate a new Redshift cluster
2) Release public acces to the cluster by clickin in Actions >> Modify publicly accessible setting
3) Create inbound rules in the security group attached to the VPC for this cluster to enable remote access

* Create tables in Redshift
Using the Redshift Query Editor, run the SQL queries in the Create Tables.sql file

## Purpose of this database 

Sparify is a streaming startup that is growing its user base and database and wish to move their database to the cloud. They used to store their data in JSON files in their on-prem servers. The data was made available in S3 buckets in order to be transitioned into a Parquet Database.

This project is composed of an Airflow managed ETL pipeline that extracts data from S3, stages them in AWS Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. 

## How to run this solution

1) Open Airflow user interface by accessing http://localhost:8080/
2) Click in the dag icon
2) Turn on the on/off toggle 
3) Monitor the DAG running
4) When finished, turn the DAG off
