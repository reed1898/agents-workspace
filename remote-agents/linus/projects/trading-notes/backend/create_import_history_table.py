"""
手动创建 import_history 表
"""
from app.core.database import engine
from sqlalchemy import text

def create_import_history_table():
    """创建 import_history 表"""
    sql = """
    CREATE TABLE IF NOT EXISTS import_history (
        id UUID NOT NULL,
        account_id UUID NOT NULL,
        user_id UUID NOT NULL,
        filename VARCHAR(255) NOT NULL,
        broker_template VARCHAR(50) NOT NULL,
        import_source VARCHAR(20),
        total_rows INTEGER NOT NULL,
        success_count INTEGER DEFAULT 0,
        failed_count INTEGER DEFAULT 0,
        duplicate_count INTEGER DEFAULT 0,
        error_details JSONB,
        created_at TIMESTAMP WITHOUT TIME ZONE,
        completed_at TIMESTAMP WITHOUT TIME ZONE,
        CONSTRAINT import_history_pkey PRIMARY KEY (id),
        CONSTRAINT import_history_account_id_fkey FOREIGN KEY(account_id)
            REFERENCES trade_accounts (id) ON DELETE CASCADE,
        CONSTRAINT import_history_user_id_fkey FOREIGN KEY(user_id)
            REFERENCES users (id) ON DELETE CASCADE
    );
    """

    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
        print("✅ import_history 表创建成功!")

if __name__ == "__main__":
    create_import_history_table()
