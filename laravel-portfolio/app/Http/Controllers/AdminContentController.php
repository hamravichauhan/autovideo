<?php

namespace App\Http\Controllers;

use App\Services\MarkdownService;

class AdminContentController
{
    protected string $baseDir;
    protected string $blogsPath;
    protected string $topicsFile;
    protected MarkdownService $markdownService;

    public function __construct()
    {
        $this->baseDir = project_root();
        $this->blogsPath = $this->baseDir . '/output/blogs';
        $this->topicsFile = $this->baseDir . '/content/blog_topics.json';
        $this->markdownService = new MarkdownService();
    }

    /**
     * List all programmatic SEO articles.
     */
    public function index()
    {
        $articles = [];
        if (is_dir($this->blogsPath)) {
            $files = glob($this->blogsPath . '/*.md');
            foreach ($files as $file) {
                $filename = basename($file);
                $parsed = $this->markdownService->parseFile($file);
                $meta = $parsed['meta'] ?? [];
                
                // Calculate word count
                $rawContent = file_get_contents($file);
                $wordCount = str_word_count(strip_tags($parsed['html'] ?? $rawContent));

                $articles[] = [
                    'filename' => $filename,
                    'title' => $meta['title'] ?? $filename,
                    'slug' => $meta['slug'] ?? pathinfo($filename, PATHINFO_FILENAME),
                    'city' => $meta['city'] ?? 'India',
                    'niche' => $meta['niche'] ?? 'Web Dev',
                    'date' => $meta['date'] ?? date('Y-m-d', filemtime($file)),
                    'read_time' => $meta['read_time'] ?? '7 min',
                    'word_count' => $wordCount,
                    'size' => round(filesize($file) / 1024, 1) . ' KB',
                ];
            }
        }

        // Sort descending by date
        usort($articles, fn($a, $b) => strcmp($b['date'], $a['date']));

        return view('admin.content.index', [
            'activeNav' => 'content',
            'articles' => $articles,
        ]);
    }

    /**
     * Edit an article.
     */
    public function edit()
    {
        $filename = request('file');
        if (!$filename) {
            redirect('/admin/content');
        }

        $filepath = $this->blogsPath . '/' . basename($filename);
        if (!file_exists($filepath)) {
            session_flash('error', "Article [{$filename}] not found.");
            redirect('/admin/content');
        }

        $rawContent = file_get_contents($filepath);
        $parsed = $this->markdownService->parseFile($filepath);

        // Separate frontmatter and body
        $body = '';
        if (preg_match('/^---\s*\n(.*?)\n---\s*\n(.*)$/s', $rawContent, $matches)) {
            $body = trim($matches[2]);
        } else {
            $body = $rawContent;
        }

        return view('admin.content.edit', [
            'activeNav' => 'content',
            'filename' => $filename,
            'meta' => $parsed['meta'] ?? [],
            'body' => $body,
        ]);
    }

    /**
     * Update an article.
     */
    public function update()
    {
        $filename = request('filename');
        if (!$filename) {
            redirect('/admin/content');
        }

        $filepath = $this->blogsPath . '/' . basename($filename);
        
        $title = request('title', '');
        $city = request('city', '');
        $niche = request('niche', '');
        $slug = request('slug', '');
        $description = request('description', '');
        $body = request('body', '');

        // Reconstruct frontmatter
        $content = "---\n";
        $content .= "title: \"" . addslashes($title) . "\"\n";
        $content .= "slug: \"" . addslashes($slug) . "\"\n";
        $content .= "city: \"" . addslashes($city) . "\"\n";
        $content .= "niche: \"" . addslashes($niche) . "\"\n";
        $content .= "date: \"" . date('Y-m-d') . "\"\n";
        $content .= "read_time: \"7 min read\"\n";
        $content .= "description: \"" . addslashes($description) . "\"\n";
        $content .= "---\n\n";
        $content .= $body;

        file_put_contents($filepath, $content);

        session_flash('success', "Article '{$title}' updated successfully.");
        redirect('/admin/content');
    }

    /**
     * Delete an article.
     */
    public function delete()
    {
        $filename = request('file');
        if ($filename) {
            $filepath = $this->blogsPath . '/' . basename($filename);
            if (file_exists($filepath)) {
                unlink($filepath);
                session_flash('success', "Article {$filename} was deleted.");
            }
        }
        redirect('/admin/content');
    }

    /**
     * Topic Matrix Editor (content/blog_topics.json).
     */
    public function topics()
    {
        $data = [];
        if (file_exists($this->topicsFile)) {
            $data = json_decode(file_get_contents($this->topicsFile), true) ?: [];
        }

        return view('admin.content.topics', [
            'activeNav' => 'content',
            'topics' => $data,
            'rawJson' => json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES),
        ]);
    }

    /**
     * Save updated topic matrix.
     */
    public function saveTopics()
    {
        $jsonInput = request('json_content');
        if (!empty($jsonInput)) {
            $decoded = json_decode($jsonInput, true);
            if ($decoded === null) {
                session_flash('error', 'Invalid JSON syntax. Please correct and retry.');
                redirect('/admin/content/topics');
            }
            file_put_contents($this->topicsFile, json_encode($decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
            session_flash('success', 'Topic matrix (cities & niches) saved successfully.');
        }
        redirect('/admin/content/topics');
    }

    /**
     * Trigger pSEO generator.
     */
    public function generate()
    {
        $cmd = 'python3 -m src.generator_pseo';
        $output = [];
        $returnVar = 0;
        exec("cd " . escapeshellarg($this->baseDir) . " && {$cmd} 2>&1", $output, $returnVar);

        if ($returnVar === 0) {
            session_flash('success', 'New programmatic SEO case studies successfully generated!');
        } else {
            session_flash('error', 'Generator completed with note: ' . implode(' ', array_slice($output, -2)));
        }

        redirect('/admin/content');
    }
}
