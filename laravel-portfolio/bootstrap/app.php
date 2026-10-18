<?php

/**
 * ExtrovertNerd Laravel Application Bootstrap & Lightweight Runtime Engine.
 */

define('LARAVEL_START', microtime(true));

// Start session if not started and not in CLI
if (session_status() === PHP_SESSION_NONE && php_sapi_name() !== 'cli') {
    @session_start();
}

// Autoloader for App namespace
spl_autoload_register(function ($class) {
    $prefix = 'App\\';
    $baseDir = dirname(__DIR__) . '/app/';

    $len = strlen($prefix);
    if (strncmp($prefix, $class, $len) !== 0) {
        return;
    }

    $relativeClass = substr($class, $len);
    $file = $baseDir . str_replace('\\', '/', $relativeClass) . '.php';

    if (file_exists($file)) {
        require_once $file;
    }
});

// Helper functions for blade / view rendering
if (!function_exists('view')) {
    function view(string $viewName, array $data = []) {
        return \App\Services\ViewRenderer::render($viewName, $data);
    }
}

if (!function_exists('request')) {
    function request(?string $key = null, $default = null) {
        if ($key === null) {
            return array_merge($_GET, $_POST);
        }
        return $_POST[$key] ?? $_GET[$key] ?? $default;
    }
}

if (!function_exists('redirect')) {
    function redirect(string $url) {
        header('Location: ' . $url);
        exit;
    }
}

if (!function_exists('abort')) {
    function abort(int $code, string $message = 'Not Found') {
        http_response_code($code);
        echo "<!DOCTYPE html><html><head><title>{$code} {$message}</title><script src='https://cdn.tailwindcss.com'></script></head><body class='bg-slate-950 text-white min-h-screen flex items-center justify-center p-6 text-center'><div class='space-y-4'><div class='text-5xl font-mono text-emerald-400 font-bold'>{$code}</div><h1 class='text-2xl font-bold'>{$message}</h1><a href='/' class='inline-block bg-emerald-500 text-slate-950 px-6 py-2.5 rounded-xl font-bold text-xs uppercase'>Return Home</a></div></body></html>";
        exit;
    }
}

if (!function_exists('session')) {
    function session($key = null, $default = null) {
        if ($key === null) {
            return $_SESSION ?? [];
        }
        if (is_array($key)) {
            foreach ($key as $k => $v) {
                $_SESSION[$k] = $v;
            }
            return null;
        }
        return $_SESSION[$key] ?? $default;
    }
}

if (!function_exists('session_flash')) {
    function session_flash(string $key, $value) {
        $_SESSION['flash'][$key] = $value;
    }
}

if (!function_exists('get_flash')) {
    function get_flash(string $key, $default = null) {
        $val = $_SESSION['flash'][$key] ?? $default;
        unset($_SESSION['flash'][$key]);
        return $val;
    }
}

if (!function_exists('json_response')) {
    function json_response($data, int $statusCode = 200) {
        http_response_code($statusCode);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
        exit;
    }
}

if (!function_exists('project_root')) {
    function project_root(): string {
        $dir = __DIR__;
        for ($i = 0; $i < 6; $i++) {
            if (file_exists($dir . '/requirements.txt') || file_exists($dir . '/content/blog_topics.json')) {
                return $dir;
            }
            $dir = dirname($dir);
        }
        return dirname(__DIR__, 2);
    }
}

if (!function_exists('current_path')) {
    function current_path(): string {
        $uri = $_SERVER['REQUEST_URI'] ?? '/';
        $path = parse_url($uri, PHP_URL_PATH) ?: '/';
        return ($path !== '/' && str_ends_with($path, '/')) ? rtrim($path, '/') : $path;
    }
}

if (!function_exists('is_active_path')) {
    function is_active_path(string $path): bool {
        $current = current_path();
        if ($path === '/') {
            return $current === '/';
        }
        return str_starts_with($current, $path);
    }
}

