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

        $whatsappUrl = 'https://wa.me/15551234567?text=' . urlencode('Hey Ravi! I saw the ExtrovertNerd agency website and want to discuss a custom Laravel rebuild.');

        return view('home', [
            'recentArticles' => $recentArticles,
            'whatsappUrl' => $whatsappUrl,
        ]);
    }
}
