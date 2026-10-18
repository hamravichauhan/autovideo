<?php

namespace App\Http\Controllers;

use App\Services\MarkdownService;

class AdminDashboardController
{
    protected string $baseDir;

    public function __construct()
    {
        $this->baseDir = project_root();
    }

    public function index()
    {
        // 1. Stats: pSEO articles
        $blogsPath = $this->baseDir . '/output/blogs';
        $articles = [];
        if (is_dir($blogsPath)) {
            $articles = glob($blogsPath . '/*.md');
        }
        $totalArticles = count($articles);

        // 2. Stats: Prospects
        $prospectsFile = $this->baseDir . '/output/prospects.json';
        $prospects = [];
        if (file_exists($prospectsFile)) {
            $prospects = json_decode(file_get_contents($prospectsFile), true) ?: [];
        }
        $totalProspects = count($prospects);

        // 3. Stats: Social campaigns & preview
        $socialFile = $this->baseDir . '/output/social_preview.json';
        $socialCampaign = [];
        if (file_exists($socialFile)) {
            $socialCampaign = json_decode(file_get_contents($socialFile), true) ?: [];
        }

        // 4. Automation Log
        $logFile = $this->baseDir . '/output/automation_log.json';
        $automationLog = [];
        if (file_exists($logFile)) {
            $automationLog = json_decode(file_get_contents($logFile), true) ?: [];
        }

        // 5. Recent case studies preview
        $markdownService = new MarkdownService();
        $recentArticles = [];
        foreach (array_slice($articles, 0, 4) as $artFile) {
            $parsed = $markdownService->parseFile($artFile);
            if (!empty($parsed['meta']['title'])) {
                $recentArticles[] = $parsed['meta'];
            }
        }

        // Estimated metrics
        $whatsappLeads = 38 + ($totalProspects * 2);
        $totalPageviews = 6840 + ($totalArticles * 320);

        return view('admin.dashboard', [
            'activeNav' => 'dashboard',
            'totalArticles' => $totalArticles,
            'totalProspects' => $totalProspects,
            'whatsappLeads' => $whatsappLeads,
            'totalPageviews' => $totalPageviews,
            'socialCampaign' => $socialCampaign,
            'automationLog' => $automationLog,
            'recentArticles' => $recentArticles,
            'recentProspects' => array_slice($prospects, 0, 5),
        ]);
    }
}
