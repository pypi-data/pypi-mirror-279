import random
from datetime import date, datetime

from fastapi_react_toolkit import ADMIN_ROLE, Role, User, UserCreate, UserDatabase, g
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Application, Asset, Unit


async def add_base_data(session: AsyncSession):
    # Get user admin
    stmt = select(User).where(User.username == "admin")
    result = await session.execute(stmt)
    user = result.scalars().first()

    # Get the admin role
    stmt = select(Role).where(Role.name == ADMIN_ROLE)
    result = await session.execute(stmt)
    role = result.scalars().first()

    if not user:
        async for um in g.get_user_manager(UserDatabase(session, User)):
            user = await um.create(
                UserCreate(
                    email="admin@test.com",
                    username="admin",
                    password="admin",
                    first_name="Admin",
                    last_name="Admin",
                    active=True,
                )
            )
            user.roles.append(role)
            await session.commit()

    for i in range(100):
        asset = Asset(name=f"asset&{i}", date_time=datetime.now(), date=date.today())
        if i % 10 == 0:
            unit = Unit(name=f"unit&{int(i / 10)}")
            session.add(unit)
        asset.owner = unit
        session.add(asset)
    await session.commit()

    for i in range(20):
        application = Application(name=f"application_{i}", description=f"info_{i}")
        session.add(application)
    await session.commit()

    stmt = select(Asset).options(selectinload(Asset.applications))
    result = await session.execute(stmt)
    assets = result.scalars().all()
    stmt = select(Application)
    result = await session.execute(stmt)
    applications = result.scalars().all()

    for i, asset in enumerate(assets):
        for j in range(
            1, len(assets) // len(applications) + 1
        ):  # Associate each asset with 5 applications
            application = applications[random.randint(1, len(applications) - 1)]
            asset.applications.append(application)

    await session.commit()
