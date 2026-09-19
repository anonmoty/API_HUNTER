import os

class Config:
    VERSION = "2.0"
    NAME = "APIHunter"
    TIMEOUT = 8
    MAX_THREADS = 40
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    HEADERS = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUT = os.path.join(BASE, "output")

    API_PATHS = [
        "/api", "/api/", "/api/v1", "/api/v2", "/api/v3", "/api/v4",
        "/api/users", "/api/user", "/api/login", "/api/auth", "/api/auth/login",
        "/api/auth/register", "/api/auth/logout", "/api/auth/refresh",
        "/api/products", "/api/orders", "/api/search", "/api/config",
        "/api/settings", "/api/admin", "/api/upload", "/api/download",
        "/api/export", "/api/import", "/api/notifications", "/api/messages",
        "/api/payments", "/api/billing", "/api/subscription", "/api/webhook",
        "/api/callback", "/api/events", "/api/logs", "/api/reports",
        "/api/dashboard", "/api/profile", "/api/account", "/api/roles",
        "/api/permissions", "/api/keys", "/api/tokens", "/api/sessions",
        "/api/health", "/api/status", "/api/version", "/api/info",
        "/api/metrics", "/api/debug", "/api/test", "/api/docs",
        "/v1", "/v2", "/v3", "/v1/", "/v2/", "/v3/",
        "/v1/users", "/v1/auth", "/v1/search", "/v1/products",
        "/v2/users", "/v2/auth", "/v2/search",
        "/rest", "/rest/api", "/rest/v1", "/rest/v2",
        "/graphql", "/api/graphql", "/gql", "/graph",
        "/swagger", "/swagger.json", "/swagger-ui.html", "/swagger-ui/",
        "/api-docs", "/api/swagger.json", "/openapi.json", "/openapi.yaml",
        "/docs", "/redoc", "/api/docs", "/api/v1/docs",
        "/health", "/status", "/metrics", "/actuator", "/actuator/health",
        "/actuator/env", "/actuator/info", "/actuator/mappings",
        "/.well-known/openid-configuration", "/.well-known/security.txt",
        "/api/register", "/api/refresh", "/api/token",
        "/api/v1/graphql", "/api/v2/graphql",
        "/api/internal", "/api/external", "/api/public", "/api/private",
        "/api/mobile", "/api/app", "/api/client", "/api/server",
        "/api/graphql/playground", "/api/graphql/explorer",
        "/graphiql", "/playground", "/altair",
        "/api/v1/health", "/api/v2/health",
        "/api/v1/config", "/api/v2/config",
        "/api/v1/admin", "/api/v2/admin",
        "/api/batch", "/api/graphql/batch",
        "/api/soap", "/wsdl", "/api/wsdl",
        "/api/v1/upload", "/api/v1/download",
        "/api/v1/export", "/api/v1/import",
        "/api/v1/webhook", "/api/v1/callback",
    ]

    SWAGGER_PATHS = [
        "/swagger.json", "/swagger.yaml", "/swagger/v1/swagger.json",
        "/swagger/v2/swagger.json", "/swagger-ui.html", "/swagger-ui/",
        "/api/swagger.json", "/api/swagger.yaml", "/api-docs",
        "/api-docs/swagger.json", "/v2/api-docs", "/v3/api-docs",
        "/openapi.json", "/openapi.yaml", "/openapi/v3.json",
        "/api/openapi.json", "/docs/swagger.json", "/swagger/swagger.json",
        "/api/v1/swagger.json", "/api/v2/swagger.json",
        "/api/v1/openapi.json", "/api/v2/openapi.json",
        "/swagger-resources", "/swagger-resources/configuration/ui",
    ]

    GRAPHQL_PATHS = [
        "/graphql", "/api/graphql", "/v1/graphql", "/v2/graphql",
        "/graph", "/gql", "/api/gql", "/graphql/v1", "/graphql/api",
        "/query", "/api/query", "/graphql/playground", "/graphql/explorer",
        "/graphiql", "/playground", "/api/v1/graphql", "/api/v2/graphql",
        "/graphql/console", "/graphql/schema", "/graphql/batch",
    ]

    API_SUBDOMAINS = [
        "api", "api1", "api2", "api3", "api-dev", "api-staging",
        "api-prod", "api-test", "api-v1", "api-v2", "api-v3",
        "graphql", "gql", "rest", "gateway", "backend", "be",
        "admin-api", "internal-api", "public-api", "private-api",
        "dev-api", "staging-api", "prod-api", "test-api",
        "auth", "oauth", "sso", "login", "accounts", "identity",
        "mobile-api", "app-api", "client-api", "partner-api",
        "webhook", "hooks", "events", "stream", "ws", "wss",
    ]

    JS_API_PATTERNS = [
        r'["\'](/api/[a-zA-Z0-9_/\-?&=.]+)["\']',
        r'["\'](/v[0-9]+/[a-zA-Z0-9_/\-?&=.]+)["\']',
        r'["\'](/rest/[a-zA-Z0-9_/\-?&=.]+)["\']',
        r'["\'](/graphql[a-zA-Z0-9_/\-?&=]*)["\']',
        r'["\'](https?://[a-zA-Z0-9.\-:]+/api/[a-zA-Z0-9_/\-?&=.]+)["\']',
        r'["\'](https?://[a-zA-Z0-9.\-:]+/v[0-9]+/[a-zA-Z0-9_/\-?&=.]+)["\']',
        r'fetch\(["\']([^"\']{4,150})["\']',
        r'axios\.[a-z]+\(["\']([^"\']{4,150})["\']',
        r'\.(?:get|post|put|delete|patch)\(["\']([^"\']{4,150})["\']',
        r'\.ajax\(\{[^}]*url:\s*["\']([^"\']+)["\']',
        r'XMLHttpRequest[^;]*open\([^,]*,\s*["\']([^"\']+)["\']',
        r'(?:endpoint|apiUrl|baseUrl|apiBase|apiEndpoint|apiURL|API_URL|BASE_URL|API_BASE)["\s:=]+["\']([^"\']{4,150})["\']',
        r'new\s+URL\(["\']([^"\']{4,150})["\']',
        r'window\.location\s*=\s*["\']([^"\']{4,150})["\']',
        r'href\s*[:=]\s*["\'](/api/[^"\']+)["\']',
        r'action\s*[:=]\s*["\'](/api/[^"\']+)["\']',
        r'url\s*[:=]\s*["\'](/v[0-9]+/[^"\']+)["\']',
    ]
