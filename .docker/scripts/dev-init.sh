#!/bin/bash
echo "🚀 Development Environment Ready!"
echo "================================="
echo "📁 Workspace: /workspace"
echo "🐘 PostgreSQL: ${POSTGRES_HOST:-postgres}:${POSTGRES_PORT:-5432}"
echo "🔴 Redis: ${REDIS_HOST:-redis}:${REDIS_PORT:-6379}"
echo "================================="
