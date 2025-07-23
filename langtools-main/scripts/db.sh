#!/bin/bash

# Database management script for langtools-main

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

show_help() {
    echo "Database Management Script (PostgreSQL)"
    echo ""
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  start     Start PostgreSQL container"
    echo "  stop      Stop PostgreSQL container"
    echo "  restart   Restart PostgreSQL container"
    echo "  logs      Show PostgreSQL container logs"
    echo "  migrate   Run database migrations"
    echo "  reset     Reset database (WARNING: destroys all data)"
    echo "  shell     Connect to PostgreSQL shell"
    echo "  status    Show database status"
    echo ""
}

start_db() {
    echo "🐘 Starting PostgreSQL container..."
    docker-compose up -d postgres
    echo "✅ PostgreSQL is starting up. Use '$0 logs' to monitor startup."
    echo "💡 Run '$0 migrate' to apply database migrations."
}

stop_db() {
    echo "🛑 Stopping PostgreSQL container..."
    docker-compose stop postgres
    echo "✅ PostgreSQL stopped."
}

restart_db() {
    echo "🔄 Restarting PostgreSQL container..."
    docker-compose restart postgres
    echo "✅ PostgreSQL restarted."
}

show_logs() {
    echo "📋 PostgreSQL container logs:"
    docker-compose logs -f postgres
}

run_migrations() {
    echo "🔄 Running database migrations..."
    uv run alembic upgrade head
    echo "✅ Migrations completed."
}

reset_database() {
    echo "⚠️  WARNING: This will destroy ALL data in the database!"
    read -p "Are you sure? Type 'yes' to continue: " confirm
    if [ "$confirm" = "yes" ]; then
        echo "🗑️  Resetting database..."
        docker-compose down postgres
        docker volume rm langtools-main_postgres_data 2>/dev/null || true
        docker-compose up -d postgres
        echo "⏳ Waiting for database to be ready..."
        sleep 5
        run_migrations
        echo "✅ Database reset completed."
    else
        echo "❌ Reset cancelled."
    fi
}

connect_shell() {
    echo "🐘 Connecting to PostgreSQL shell..."
    docker-compose exec postgres psql -U langtools -d langtools
}

show_status() {
    echo "📊 Database Status:"
    echo ""
    
    if docker-compose ps postgres | grep -q "Up"; then
        echo "✅ PostgreSQL container: Running"
        
        # Check if database is responding
        if docker-compose exec -T postgres pg_isready -U langtools -d langtools >/dev/null 2>&1; then
            echo "✅ Database connection: OK"
            
            # Show basic stats
            echo ""
            echo "Database info:"
            docker-compose exec -T postgres psql -U langtools -d langtools -c "
                SELECT 
                    current_database() as database,
                    current_user as user,
                    version() as version;
            " 2>/dev/null || echo "❌ Could not fetch database info"
            
        else
            echo "❌ Database connection: Failed"
        fi
    else
        echo "❌ PostgreSQL container: Not running"
        echo "💡 Run '$0 start' to start the database."
    fi
}

case "${1:-}" in
    start)
        start_db
        ;;
    stop)
        stop_db
        ;;
    restart)
        restart_db
        ;;
    logs)
        show_logs
        ;;
    migrate)
        run_migrations
        ;;
    reset)
        reset_database
        ;;
    shell)
        connect_shell
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        echo "❌ No command specified."
        echo ""
        show_help
        exit 1
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac