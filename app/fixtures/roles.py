from fastapi_async_sqlalchemy import db

from crud.role import RoleCRUD


initial_roles = ["Admin", "Manager", "Worker"]

async def init_roles():
    async with db():
        roles = await RoleCRUD.filter()
        existing_roles = {role_name.name for role_name in roles}

        roles_to_add = set(initial_roles) - existing_roles

        if roles_to_add:
            print(f"Adding new roles: {roles_to_add}")
            for role_name in roles_to_add:
                await RoleCRUD.create({"name": role_name})

        else:
            print("All roles already exist in the database.")
