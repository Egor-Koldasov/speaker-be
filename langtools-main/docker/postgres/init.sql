-- PostgreSQL initialization script for langtools development database
-- This script runs during container initialization as the postgres superuser

-- The langtools user and langtools database are already created by environment variables
-- We just need to create the test database and set up permissions

-- Create test database
CREATE DATABASE langtools_test;

-- Grant all privileges to langtools user on both databases
GRANT ALL PRIVILEGES ON DATABASE langtools TO langtools;
GRANT ALL PRIVILEGES ON DATABASE langtools_test TO langtools;

-- Connect to langtools database and grant schema permissions
\c langtools;
GRANT ALL ON SCHEMA public TO langtools;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO langtools;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO langtools;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO langtools;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO langtools;

-- Connect to langtools_test database and grant schema permissions
\c langtools_test;
GRANT ALL ON SCHEMA public TO langtools;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO langtools;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO langtools;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO langtools;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO langtools;