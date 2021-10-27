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
                 select_sql='',
                 stagingtables='',
                 dimtables='',
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.stagingtables = stagingtables
        self.dimtables = dimtables
        self.select_sql = select_sql

    '''
    Execution: 
    1) Define the redshift hook
    2) Define table names as per DAG's instruction
    3) Check if there is any empty table 
    '''
    def execute(self, context):
        redshift_hook = PostgresHook('redshift')
        stagingtables = self.stagingtables
        dimtables = self.dimtables
        self.log.info(f'Checking Staging tables...')
        for t in stagingtables:
            records=redshift_hook.get_records(f'select count(*) from {t};')
            if len(records) < 1 or len(records[0]) < 1:
                raise AssertionError(f'Data quality check failed. {t} returned no results!')
            else:
                self.log.info(f'Data quality check successful. {t} returned no errors!')

        self.log.info(f'Checking Fact and Dim tables...')
        for t in dimtables:
            records=redshift_hook.get_records(f'select count(*) from {t};')
            if len(records) < 1 or len(records[0]) < 1:
                raise AssertionError(f'Data quality check failed. {t} returned no results!')
            else:
                self.log.info(f'Data quality check successful. {t} returned no errors!')     
        self.log.info('Quality Check Complete.')