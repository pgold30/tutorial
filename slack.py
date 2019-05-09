from airflow.hooks.base_hook import BaseHook
from airflow.operators.slack_operator import SlackAPIPostOperator
SLACK_CONN_ID = 'slack'

def task_fail_slack_alert(context):
    """
    Sends message to a slack channel.
    If you want to send it to a "user" -> use "@user",
        if "public channel" -> use "#channel",
        if "private channel" -> use "channel"
    """
    slack_channel = BaseHook.get_connection(SLACK_CONN_ID).login
    slack_token = BaseHook.get_connection(SLACK_CONN_ID).password
    failed_alert = SlackAPIPostOperator(
        task_id='slack_failed',
        channel=slack_channel,
        token=slack_token,
        text="""
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
        )
    )
    return failed_alert.execute(context=context)
