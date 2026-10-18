<?php

namespace App\Http\Controllers;

use App\Services\MarkdownService;

class BlogController
{
    protected MarkdownService $markdownService;
    protected string $blogsPath;

    public function __construct()
    {
        $this->markdownService = new MarkdownService();
        // Path to pSEO generated blog markdown articles
        $primary = dirname(__DIR__, 3) . '/output/blogs';
        $fallback = dirname(__DIR__, 4) . '/output/blogs';
        $this->blogsPath = is_dir($primary) ? $primary : $fallback;
    }

    /**
     * Display list of programmatic SEO articles and case studies.
     */
    public function index(?string $cityFilter = null)
    {
        $articles = [];

        if (is_dir($this->blogsPath)) {
            $files = glob($this->blogsPath . '/*.md');
            foreach ($files as $file) {
                $parsed = $this->markdownService->parseFile($file);
                $meta = $parsed['meta'] ?? [];
                if (!empty($meta['slug']) && !empty($meta['title'])) {
                    // Check city filter if set
                    if ($cityFilter && strtolower($meta['city'] ?? '') !== strtolower($cityFilter)) {
                        continue;
                    }

                    $articles[] = [
                        'title' => $meta['title'],
                        'slug' => $meta['slug'],
                        'date' => $meta['date'] ?? date('Y-m-d'),
                        'city' => $meta['city'] ?? 'India',
                        'niche' => $meta['niche'] ?? 'Web Development',
                        'read_time' => $meta['read_time'] ?? '7 min read',
                        'description' => $meta['description'] ?? '',
                        'keywords' => $meta['keywords'] ?? [],
                    ];
                }
            }
        }

        // Sort by date descending
        usort($articles, fn($a, $b) => strcmp($b['date'], $a['date']));

        return view('blog.index', [
            'articles' => $articles,
            'currentCity' => $cityFilter,
            'cities' => ['Goa', 'Mumbai', 'Bangalore', 'Delhi NCR', 'Dubai', 'Hyderabad'],
        ]);
    }

    /**
     * Display a single pSEO case study article.
     */
    public function show(string $slug)
    {
        $targetFile = $this->blogsPath . '/' . basename($slug) . '.md';

        if (!file_exists($targetFile)) {
            // Try searching by slug in all markdown files
            $found = null;
            if (is_dir($this->blogsPath)) {
                foreach (glob($this->blogsPath . '/*.md') as $file) {
                    if (str_contains($file, $slug)) {
                        $found = $file;
                        break;
                    }
                }
            }

            if (!$found) {
                abort(404, 'Case study not found');
            }
            $targetFile = $found;
        }

        $parsed = $this->markdownService->parseFile($targetFile);

        return view('blog.show', [
            'meta' => $parsed['meta'],
            'html' => $parsed['html'],
            'whatsappUrl' => 'https://wa.me/15551234567?text=' . urlencode('Hey ExtrovertNerd! I read your case study on ' . ($parsed['meta']['title'] ?? 'web speed') . ' and want a free audit.'),
        ]);
    }
}
