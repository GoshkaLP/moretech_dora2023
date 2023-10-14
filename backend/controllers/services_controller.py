from asyncpg.connection import Connection


class ServicesController:
    def __init__(self, db_conn: Connection):
        self.db_conn = db_conn

    async def get_branch_services(self, branch_id: int):
        rows = await self.db_conn.fetch(f'''SELECT service_id, name, juridical FROM services s 
                                        JOIN branches_services bs ON s.id=bs.service_id
                                        WHERE bs.branch_id = {branch_id}''')
        branch_services = [
            {
                'id': row['service_id'],
                'name': row['name'],
                'service_type': 'Юридическому лицу' if row['juridical'] else 'Физическому лицу'
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
