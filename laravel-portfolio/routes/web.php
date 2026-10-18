<?php

use App\Http\Controllers\HomeController;
use App\Http\Controllers\SpeedCheckerController;
use App\Http\Controllers\BlogController;

/**
 * ExtrovertNerd Agency Web Routes
 */

// Landing Page
$routes->get('/', [HomeController::class, 'index']);

// Interactive Speed Checker Micro-Tool
$routes->get('/speed-checker', [SpeedCheckerController::class, 'index']);
$routes->post('/speed-checker', [SpeedCheckerController::class, 'audit']);

// Programmatic SEO Case Studies & Blog
$routes->get('/blog', [BlogController::class, 'index']);
$routes->get('/blog/{slug}', [BlogController::class, 'show']);

// Direct WhatsApp Inbound Redirect
$routes->get('/audit', function () {
    $msg = 'Hey Ravi! I saw ExtrovertNerd and want a free 5-point website speed audit.';
    header('Location: https://wa.me/15551234567?text=' . urlencode($msg));
    exit;
});
