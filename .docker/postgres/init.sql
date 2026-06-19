-- Базовые расширения
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Приветственное сообщение
SELECT 'Database initialized successfully!' AS status;
