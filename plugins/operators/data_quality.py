from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    ui_color = '#89DA59'
    '''
    Operator overview: Perform Data Quality.
    '''

    '''
    Mapped params: table, connection id, sql instruction
    '''

    @apply_defaults
    def __init__(self,
                 table,
                 redshift_conn_id='',
                 dq_checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.c = dq_checks
        self.dq_checks = dq_checks


    '''
    Execution: 
    1) Define the redshift hook
    2) Define table names as per DAG's instruction
    3) Check if there is any empty table 
    '''
    def execute(self, context):
        redshift_hook = PostgresHook('redshift')
        self.log.info(f'Checking Staging tables...')
        for c in self.dq_checks:
            sql = c["check_sql"]
            exp = c["expected_result"]
            records = redshift_hook.get_records(sql)
            num_records = records[0][0]
            if num_records != exp:
                raise ValueError(f"Exception noticed, got: {num_records} while expected: {exp}")
            else:
                self.log.info(f"No errors noticed.")
        
        self.log.info('Quality Check Complete.')
