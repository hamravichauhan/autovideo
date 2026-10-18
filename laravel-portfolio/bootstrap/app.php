<?php

/**
 * ExtrovertNerd Laravel Application Bootstrap & Lightweight Runtime Engine.
 */

define('LARAVEL_START', microtime(true));

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
