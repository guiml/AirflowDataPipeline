from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    ui_color = '#80BD9E'
    '''
    Operator overview: Load data into dim tables.
    '''

    '''
    Mapped params: table, connection id, sql instruction, truncate
    '''
    @apply_defaults
    def __init__(self,
                 table,
                 redshift_conn_id='',
                 select_sql='',
                 trunc=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql
        self.trunc = trunc


    '''
    Execution: 
    1) define the redshift hook
    2) Truncate fact table, if specified in DAG param
    3) Insert information according to SQL string passed from DAG 
    '''
    def execute(self, context):
        redshift_hook = PostgresHook('redshift')
        if self.trunc == False:
            self.log.info(f'truncating table {self.table}')
            redshift_hook.run('TRUNCATE TABLE {};'.format(self.table))
            self.log.info('Truncating complete') 

        self.log.info(f'Loading data into {self.table} fact table...')
        redshift_hook.run('INSERT INTO {} {};'.format(self.table, self.select_sql))
        self.log.info('Loading complete.')
