from asyncpg.connection import Connection


class RoutesController:
    def __init__(self, db_conn: Connection):
        self.db_conn = db_conn

    async def get_branches(self):
        rows = await self.db_conn.fetch('SELECT * FROM branches')
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

    async def search_nearest(self, form):
        pass
