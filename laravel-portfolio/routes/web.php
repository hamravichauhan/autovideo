<?php

use App\Http\Controllers\HomeController;
use App\Http\Controllers\SpeedCheckerController;
use App\Http\Controllers\BlogController;
use App\Http\Controllers\AdminDashboardController;
use App\Http\Controllers\AdminContentController;
use App\Http\Controllers\AdminSocialController;
use App\Http\Controllers\AdminProspectsController;
use App\Http\Controllers\AdminDocumentsController;
use App\Http\Controllers\AdminSystemController;

/**
 * ExtrovertNerd Agency Web Routes
 */

// ==============================================================
// 1. PUBLIC AGENCY HUB ROUTES (MULTI-PAGE)
// ==============================================================

// Landing Page
$routes->get('/', [HomeController::class, 'index']);

// How We Work: The 5-Step Engineering Blueprint & Philosophy
$routes->get('/how-we-work', [HomeController::class, 'howWeWork']);

// Interactive Speed Checker Micro-Tool
$routes->get('/speed-checker', [SpeedCheckerController::class, 'index']);
$routes->post('/speed-checker', [SpeedCheckerController::class, 'audit']);

// Case Studies & Technical Performance Logs
$routes->get('/case-studies', [BlogController::class, 'index']);
$routes->get('/case-studies/{slug}', [BlogController::class, 'show']);
$routes->get('/blog', [BlogController::class, 'index']);
$routes->get('/blog/{slug}', [BlogController::class, 'show']);

// Lost Revenue & ROI Calculator
$routes->get('/roi-calculator', [HomeController::class, 'roiCalculator']);

// Direct WhatsApp Inbound Redirect
$routes->get('/audit', function () {
    $msg = 'Hey Ravi! I saw ExtrovertNerd and want a free 5-point website speed audit.';
    header('Location: https://wa.me/15551234567?text=' . urlencode($msg));
    exit;
});

// ==============================================================
// 2. ADMIN DASHBOARD & MISSION CONTROL ROUTES
// ==============================================================

// Module A: Mission Control & Analytics Overview
$routes->get('/admin', [AdminDashboardController::class, 'index']);
$routes->get('/admin/dashboard', [AdminDashboardController::class, 'index']);

// Module B: Content & pSEO Command Center
$routes->get('/admin/content', [AdminContentController::class, 'index']);
$routes->get('/admin/content/edit', [AdminContentController::class, 'edit']);
$routes->post('/admin/content/update', [AdminContentController::class, 'update']);
$routes->get('/admin/content/delete', [AdminContentController::class, 'delete']);
$routes->get('/admin/content/topics', [AdminContentController::class, 'topics']);
$routes->post('/admin/content/topics/save', [AdminContentController::class, 'saveTopics']);
$routes->post('/admin/content/generate', [AdminContentController::class, 'generate']);

// Module C: Visual Assets & Social Media Queue
$routes->get('/admin/social', [AdminSocialController::class, 'index']);
$routes->post('/admin/social/publish', [AdminSocialController::class, 'publish']);
$routes->post('/admin/social/generate', [AdminSocialController::class, 'generate']);
$routes->post('/admin/social/telegram', [AdminSocialController::class, 'telegram']);

// Module D: Prospecting & Lead CRM
$routes->get('/admin/prospects', [AdminProspectsController::class, 'index']);
$routes->post('/admin/prospects/status', [AdminProspectsController::class, 'updateStatus']);
$routes->post('/admin/prospects/add', [AdminProspectsController::class, 'add']);
$routes->post('/admin/prospects/scrape', [AdminProspectsController::class, 'scrape']);

// Module E: Document Vault & Knowledge Base
$routes->get('/admin/documents', [AdminDocumentsController::class, 'index']);
$routes->post('/admin/documents/upload', [AdminDocumentsController::class, 'upload']);
$routes->get('/admin/documents/delete', [AdminDocumentsController::class, 'delete']);
$routes->post('/admin/documents/notes/save', [AdminDocumentsController::class, 'saveNote']);
$routes->get('/admin/documents/notes/delete', [AdminDocumentsController::class, 'deleteNote']);

// Module F: System Automation & CLI Trigger
$routes->get('/admin/system', [AdminSystemController::class, 'index']);
$routes->post('/admin/system/trigger', [AdminSystemController::class, 'trigger']);
$routes->post('/admin/system/config', [AdminSystemController::class, 'saveConfig']);
$routes->post('/admin/system/clear-logs', [AdminSystemController::class, 'clearLogs']);
