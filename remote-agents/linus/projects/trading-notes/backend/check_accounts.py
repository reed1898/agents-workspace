import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.trade_account import TradeAccount
from app.core.config import settings

async def check_accounts():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        result = await session.execute(
            select(TradeAccount).where(
                TradeAccount.account_name.ilike('%moomoo%')
            )
        )
        accounts = result.scalars().all()

        if not accounts:
            print("No moomoo accounts found")
            # Try to get all accounts
            result = await session.execute(select(TradeAccount))
            all_accounts = result.scalars().all()
            print(f"\nAll accounts ({len(all_accounts)}):")
            for acc in all_accounts:
                print(f"  - ID: {acc.id}")
                print(f"    Name: {acc.account_name}")
                print(f"    Type: {acc.account_type}")
                print(f"    Broker: {acc.broker}")
                print()
        else:
            print(f"Found {len(accounts)} moomoo account(s):")
            for acc in accounts:
                print(f"\n  - ID: {acc.id}")
                print(f"    Name: {acc.account_name}")
                print(f"    Type: {acc.account_type}")
                print(f"    Broker: {acc.broker}")
                print(f"    Active: {acc.is_active}")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_accounts())
