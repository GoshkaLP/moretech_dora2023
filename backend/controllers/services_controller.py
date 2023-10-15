from asyncpg.connection import Connection


class ServicesController:
    def __init__(self, db_conn: Connection):
        self.db_conn = db_conn
        self.branch_services_query = '''
            WITH LatestLoads AS (
                SELECT
                    branch_id,
                    service_id,
                    AVG(total_load) AS avg_load_last_5min
                FROM
                    agg_events
                WHERE
                    w_end > NOW() - INTERVAL '5 minutes'
                GROUP BY
                    branch_id, service_id
            )
            
            SELECT
                s.id AS service_id,
                s.name AS name,
                s.juridical AS juridical,
                COALESCE(ll.avg_load_last_5min, 0) AS load
            FROM services s
            JOIN branches_services bs ON s.id = bs.service_id
            LEFT JOIN LatestLoads ll ON bs.service_id = ll.service_id AND bs.branch_id = ll.branch_id
            WHERE bs.branch_id = {branch_id};
            '''

    async def get_branch_services(self, branch_id: int):
        query = self.branch_services_query.format(branch_id=branch_id)
        rows = await self.db_conn.fetch(query)
        branch_services = [
            {
                'id': row['service_id'],
                'name': row['name'],
                'service_type': 'Юридическому лицу' if row['juridical'] else 'Физическому лицу',
                'load': row['load']
            }
            for row in rows
        ]
        return branch_services

    async def get_services_juridical(self):
        rows = await self.db_conn.fetch('SELECT * FROM services WHERE juridical = false')
        services = [
            {
                'id': row['id'],
                'name': row['name'],
                'service_type': 'Юридическому лицу'
            }
            for row in rows
        ]
        return services

    async def get_services_physical(self):
        rows = await self.db_conn.fetch('SELECT * FROM services WHERE juridical = true')
        services = [
            {
                'id': row['id'],
                'name': row['name'],
                'service_type': 'Физическому лицу'
            }
            for row in rows
        ]
        return services
