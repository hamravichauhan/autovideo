<?php

namespace App\Services;

/**
 * Lightweight, zero-dependency router for the ExtrovertNerd Laravel application.
 * Supports exact paths, route parameters ({slug}), closures, and [Controller::class, 'method'].
 */
class Router
{
    protected array $routes = [
        'GET' => [],
        'POST' => [],
    ];

    /**
     * Register a GET route.
     */
    public function get(string $path, $handler): self
    {
        $this->routes['GET'][$path] = $handler;
        return $this;
    }

    /**
     * Register a POST route.
     */
    public function post(string $path, $handler): self
    {
        $this->routes['POST'][$path] = $handler;
        return $this;
    }

    /**
     * Dispatch an incoming HTTP request.
     */
    public function dispatch(string $method, string $uri)
    {
        $method = strtoupper($method);
        // Normalize URI: strip query string and clean trailing slash
        $path = parse_url($uri, PHP_URL_PATH) ?: '/';
        if ($path !== '/' && str_ends_with($path, '/')) {
            $path = rtrim($path, '/');
        }

        // Parse query string into $_GET
        $queryString = parse_url($uri, PHP_URL_QUERY);
        if ($queryString) {
            parse_str($queryString, $queryParams);
            $_GET = array_merge($_GET, $queryParams);
        }

        $routesForMethod = $this->routes[$method] ?? [];

        // 1. Direct exact match
        if (isset($routesForMethod[$path])) {
            return $this->invokeHandler($routesForMethod[$path], []);
        }

        // 2. Pattern match for parameterized routes (e.g., /blog/{slug})
        foreach ($routesForMethod as $routePath => $handler) {
            if (!str_contains($routePath, '{')) {
                continue;
            }

            // Convert {param} to named regex capture group
            $pattern = preg_replace('/\{([a-zA-Z0-9_]+)\}/', '(?P<$1>[^/]+)', $routePath);
            $pattern = '#^' . $pattern . '$#';

            if (preg_match($pattern, $path, $matches)) {
                $params = [];
                foreach ($matches as $key => $val) {
                    if (!is_int($key)) {
                        $params[$key] = urldecode($val);
                    }
                }
                return $this->invokeHandler($handler, $params);
            }
        }

        // 3. Not Found
        abort(404, "Route not found for [{$method}] {$path}");
    }

    /**
     * Invoke the route handler (closure or controller method).
     */
    protected function invokeHandler($handler, array $params = [])
    {
        if (is_callable($handler)) {
            $response = call_user_func_array($handler, array_values($params));
        } elseif (is_array($handler) && count($handler) === 2) {
            [$class, $method] = $handler;
            $instance = new $class();
            $response = call_user_func_array([$instance, $method], array_values($params));
        } else {
            abort(500, "Invalid route handler specified");
        }

        if (is_string($response)) {
            echo $response;
        }

        return $response;
    }
}
