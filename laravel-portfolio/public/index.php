<?php

/**
 * ExtrovertNerd Agency - Public Web Entry Point
 * Branded under ExtrovertNerd (Lead Web Architect: Ravi)
 */

// If serving via PHP built-in web server, allow direct serving of static files if they exist
if (php_sapi_name() === 'cli-server') {
    $uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    if ($uri !== '/' && file_exists(__DIR__ . $uri)) {
        return false;
    }
}

// 1. Bootstrap application & autoloader
require_once dirname(__DIR__) . '/bootstrap/app.php';

// 2. Initialize Router
$routes = new \App\Services\Router();

// 3. Load Application Web Routes
require_once dirname(__DIR__) . '/routes/web.php';

// 4. Dispatch the incoming HTTP request
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$uri = $_SERVER['REQUEST_URI'] ?? '/';

$routes->dispatch($method, $uri);
