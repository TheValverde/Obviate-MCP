# Docker Setup for Kanban For Agents MCP Server

This document provides instructions for running the Kanban For Agents MCP Server using Docker Compose.

## Quick Start

1. **Clone and navigate to the project directory:**
   ```bash
   cd /path/to/kanban-mcp-server
   ```

2. **Copy the environment file:**
   ```bash
   cp env.example .env
   ```

3. **Edit the environment variables in `.env` as needed:**
   ```bash
   nano .env
   ```

4. **Start the services:**
   ```bash
   docker compose up -d
   ```

5. **Check the status:**
   ```bash
   docker compose ps
   ```

## Services

The Docker Compose setup includes the following services:

### Core Services

- **kanban-mcp-server**: The main MCP server (port 12007)
- **kanban-api**: The Kanban API service (port 12003)
- **postgres**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)

### Optional Services

- **nginx**: Reverse proxy for routing (ports 80, 443)

## Configuration

### Environment Variables

Key environment variables you can configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `KANBAN_API_BASE_URL` | `http://kanban-api:12003` | Base URL of the Kanban API |
| `DEFAULT_TENANT_ID` | `default` | Default tenant ID |
| `LOG_LEVEL` | `INFO` | Logging level |
| `DEBUG_MODE` | `false` | Enable debug mode |

### Ports

| Service | Port | Description |
|---------|------|-------------|
| MCP Server | 12007 | Main MCP server endpoint |
| Kanban API | 12003 | Kanban API endpoint |
| PostgreSQL | 5432 | Database connection |
| Redis | 6379 | Cache connection |
| Nginx | 80/443 | Web proxy |

## Usage

### Starting Services

```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d kanban-mcp-server

# View logs
docker compose logs -f kanban-mcp-server
```

### Stopping Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### Development Mode

For development, use the override file:

```bash
# Start in development mode (with debugger)
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### Building Images

```bash
# Build the MCP server image
docker compose build kanban-mcp-server

# Build all images
docker compose build
```

## Health Checks

All services include health checks:

```bash
# Check health status
docker compose ps

# View health check logs
docker compose logs kanban-mcp-server
```

## Connecting to the MCP Server

### From MCP Clients

Configure your MCP client to connect to:

```
http://localhost:12007/mcp/
```

### Example MCP Client Configuration

For Claude Desktop (`~/.claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "kanban_mcp": {
      "command": "docker",
      "args": ["exec", "-i", "kanban-mcp-server", "python", "server.py"]
    }
  }
}
```

For Cursor (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "kanban_mcp": {
      "command": "docker",
      "args": ["exec", "-i", "kanban-mcp-server", "python", "server.py"]
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 12007, 12003, 5432, and 6379 are not in use
2. **Permission issues**: Ensure Docker has proper permissions
3. **API connection**: Verify the Kanban API is running and accessible

### Debugging

```bash
# View all logs
docker compose logs

# View specific service logs
docker compose logs kanban-mcp-server

# Execute commands in container
docker compose exec kanban-mcp-server bash

# Check service status
docker compose ps
```

### Reset Everything

```bash
# Stop and remove everything
docker compose down -v --remove-orphans

# Remove images
docker compose down --rmi all

# Start fresh
docker compose up -d
```

## Production Deployment

For production deployment:

1. **Use production environment variables**
2. **Enable SSL/TLS with proper certificates**
3. **Set up proper logging and monitoring**
4. **Configure backup strategies for the database**
5. **Use secrets management for sensitive data**

### Production Environment Variables

```bash
# Production settings
DEBUG_MODE=false
LOG_LEVEL=WARNING
ENABLE_LOGGING=true
LOG_SENSITIVE_DATA=false
```

## Monitoring

### Health Endpoints

- MCP Server: `http://localhost:12007/health`
- Kanban API: `http://localhost:12003/health`
- Nginx: `http://localhost/health`

### Logs

```bash
# Follow logs in real-time
docker compose logs -f

# View logs with timestamps
docker compose logs -t
```

## Security Considerations

1. **Change default passwords** in production
2. **Use secrets management** for sensitive data
3. **Enable SSL/TLS** for external access
4. **Regular security updates** for base images
5. **Network isolation** between services

## Backup and Restore

### Database Backup

```bash
# Backup PostgreSQL
docker compose exec postgres pg_dump -U kanban_user kanban_db > backup.sql

# Restore PostgreSQL
docker compose exec -T postgres psql -U kanban_user kanban_db < backup.sql
```

### Volume Backup

```bash
# Backup volumes
docker run --rm -v kanban-mcp_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

## Support

For issues and questions:

1. Check the logs: `docker compose logs`
2. Verify configuration: `docker compose config`
3. Test connectivity: `curl http://localhost:12007/health`
4. Review the main README.md for API documentation
