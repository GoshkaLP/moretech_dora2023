from pyflink.datastream import StreamExecutionEnvironment

from pyflink.table import StreamTableEnvironment

import os

from dotenv import load_dotenv
load_dotenv()


env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
EVENTS_TABLE = os.getenv('EVENTS_TABLE')

KAFKA_BROKER = os.getenv('KAFKA_BROKER')
KAFKA_GROUP = os.getenv('KAFKA_GROUP')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')


# Настройка источника данных из Kafka
source_ddl = f"""
    CREATE TABLE events (
        branch_id INT,
        status STRING,
        service_id INT,
        event_time TIMESTAMP(3),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = '{KAFKA_TOPIC}',
        'properties.bootstrap.servers' = '{KAFKA_BROKER}',
        'properties.group.id' = '{KAFKA_GROUP}',
        'format' = 'json',
        'scan.startup.mode' = 'earliest-offset',
        'json.timestamp-format.standard' = 'ISO-8601'
    )
"""

t_env.execute_sql(source_ddl)

# Выполнение SQL-запроса для агрегации загруженности в 5-минутном окне
result = t_env.sql_query("""
    SELECT
            service_id,
            branch_id,
            TUMBLE_START(event_time, INTERVAL '5' MINUTE) AS w_start,
            TUMBLE_END(event_time, INTERVAL '5' MINUTE) AS w_end,
            SUM(
                CASE
                    WHEN status = 'added' THEN 1
                    WHEN status = 'processing' THEN 2
                    ELSE 0
                END
            ) AS total_load
        FROM events
        GROUP BY
            service_id, branch_id, TUMBLE(event_time, INTERVAL '5' MINUTE)
""")

# Настройка слива данных в PostgreSQL
sink_ddl = f"""
            CREATE TABLE postgres_sink (
                `service_id` INT,
                `branch_id` INT,
                `w_start` TIMESTAMP,
                `w_end` TIMESTAMP,
                `total_load` INT
            ) WITH (
              'connector' = 'jdbc',
              'url' = 'jdbc:postgresql://{POSTGRES_HOST}:5432/{POSTGRES_DB}',
              'username' = '{POSTGRES_USER}',
              'password' = '{POSTGRES_PASSWORD}',
              'table-name' = '{EVENTS_TABLE}'
            )
            """

t_env.execute_sql(sink_ddl)

result.execute_insert('postgres_sink')
