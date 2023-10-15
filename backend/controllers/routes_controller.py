from asyncpg.connection import Connection


class RoutesController:
    def __init__(self, db_conn: Connection):
        self.db_conn = db_conn
        self.nearest_query = '''
        WITH RecentLoads AS (
            SELECT
                branch_id,
                service_id,
                AVG(total_load) AS avg_load_last_5min
            FROM
                agg_events
            WHERE
                w_end >= NOW() - INTERVAL '5 minutes'
            AND
                service_id IN {services_ids}
            GROUP BY
                branch_id, service_id
        )
        SELECT
            b.id,
            b.name,
            b.address,
            ST_X(b.geometry) AS longitude,
            ST_Y(b.geometry) AS latitude,
            array_agg(bs.service_id) AS services,
            COALESCE(COUNT(bs.service_id) FILTER (WHERE bs.service_id IN {services_ids}) - COALESCE(rl.avg_load_last_5min, 0), 0) AS score
        FROM
            branches b
        JOIN
            branches_services bs ON b.id = bs.branch_id
        LEFT JOIN
            RecentLoads rl ON b.id = rl.branch_id
        WHERE
            ST_Distance(
                b.geometry,
                ST_GeographyFromText('POINT({latitude} {longitude})')
            ) < {distance}
        GROUP BY
            b.id, b.name, b.address, b.geometry, rl.avg_load_last_5min
        ORDER BY
            score DESC;
                '''

    async def get_branches(self):
        rows = await self.db_conn.fetch('''SELECT id, name, address, ST_X(geometry) AS longitude,
                                        ST_Y(geometry) AS latitude FROM branches''')
        branches = [
            {
                'id': row['id'],
                'name': row['name'],
                'address': row['address'],
                'latitude': row['latitude'],
                'longitude': row['longitude']
            }
            for row in rows
        ]
        return branches

    async def get_branch_services(self, branch_id: int):
        rows = await self.db_conn.fetch(f'''SELECT service_id, name, juridical FROM services s 
                                        JOIN branches_services bs ON s.id=bs.service_id
                                        WHERE bs.branch_id = {branch_id}''')
        branch_services = [
            {
                'id': row['service_id'],
                'name': row['name'],
                'juridical': 'Юридическому лицу' if row['juridical'] else 'Физическому лицу'
            }
            for row in rows
        ]
        return branch_services

    async def search_nearest(self, services_ids, latitude, longitude):
        distance = 1
        rows = None

        while not rows:
            query = self.nearest_query.format(
                services_ids=f'({",".join(services_ids)})',
                latitude=latitude,
                longitude=longitude,
                distance=distance*1000
            )
            rows = await self.db_conn.fetch(query)
            if rows and set(rows[0]['services']).issubset(set(services_ids)):
                break
            distance += 10

        max_branches = 5 if len(rows) >= 5 else len(rows)
        branches = [
            {
                'id': row['id'],
                'name': row['name'],
                'address': row['address'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'score': row['score']
            }
            for row in rows[:max_branches]
        ]
        return branches

