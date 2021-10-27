from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    '''
    Operator overview: Load data into staging tables.
    '''

    '''
    COPY SQL: Copy instruction for AWS to gather information from the JSON files
    '''
    
    template_fields = ("s3_key",)
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION '{}'
        {}       
    """


    '''
    Mapped params: connection id, aws credentials, table name, S3 bucket and key, 
    json format, region and other parameters passed by the DAG
    '''

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 json_format="",
                 region="",
                 param="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.param = param
        self.region = region
        self.aws_credentials_id = aws_credentials_id
        self.json_format = json_format


    '''
    Execution: 
    1) define the redshift hook and credentials
    2) Delete previous informatio in staging table
    3) Insert information according to SQL string passed from DAG 
    '''
    def execute(self, context):

        aws_hook = AwsHook(self.aws_credentials_id, client_type="redshift")
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.param

        )
        redshift.run(formatted_sql)





