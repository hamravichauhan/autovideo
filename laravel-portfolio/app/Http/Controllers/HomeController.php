<?php

namespace App\Http\Controllers;

use App\Services\MarkdownService;

class HomeController
{
    /**
     * Display the ExtrovertNerd agency landing page.
     */
    public function index()
    {
        $markdownService = new MarkdownService();
        $primary = dirname(__DIR__, 3) . '/output/blogs';
        $fallback = dirname(__DIR__, 4) . '/output/blogs';
        $blogsPath = is_dir($primary) ? $primary : $fallback;

        $recentArticles = [];
        if (is_dir($blogsPath)) {
            $files = glob($blogsPath . '/*.md');
            foreach (array_slice($files, 0, 3) as $file) {
                $parsed = $markdownService->parseFile($file);
                if (!empty($parsed['meta']['title'])) {
                    $recentArticles[] = $parsed['meta'];
                }
            }
        }

        $whatsappUrl = 'https://wa.me/15551234567?text=' . urlencode('Hey ExtrovertNerd! I saw your engineering work and want to see how you can make my website fast.');

        return view('home', [
            'recentArticles' => $recentArticles,
            'whatsappUrl' => $whatsappUrl,
        ]);
    }

    /**
     * Display the dedicated "How We Work / 5-Step Engineering Blueprint" page.
     */
    public function howWeWork()
    {
        $whatsappUrl = 'https://wa.me/15551234567?text=' . urlencode('Hey ExtrovertNerd! I read your 5-step engineering blueprint on How We Work and want to get started with Phase 1 audit.');

        return view('how-we-work', [
            'whatsappUrl' => $whatsappUrl,
        ]);
    }

    /**
     * Display the dedicated "Lost Revenue & ROI Calculator" page.
     */
    public function roiCalculator()
    {
        $whatsappUrl = 'https://wa.me/15551234567?text=' . urlencode('Hey ExtrovertNerd! I used your ROI calculator and calculated our website latency loss. Can we run the free 3-minute video audit?');

        return view('roi-calculator', [
            'whatsappUrl' => $whatsappUrl,
        ]);
    }
}
