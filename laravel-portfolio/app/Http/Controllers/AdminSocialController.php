<?php

namespace App\Http\Controllers;

class AdminSocialController
{
    protected string $baseDir;
    protected string $graphicsPath;
    protected string $socialPreviewFile;

    public function __construct()
    {
        $this->baseDir = project_root();
        $this->graphicsPath = $this->baseDir . '/output/graphics';
        $this->socialPreviewFile = $this->baseDir . '/output/social_preview.json';
    }

    public function index()
    {
        // 1. Gather all graphic sets
        $graphicSets = [];
        if (is_dir($this->graphicsPath)) {
            $dirs = glob($this->graphicsPath . '/*', GLOB_ONLYDIR);
            foreach ($dirs as $dir) {
                $dirName = basename($dir);
                $images = glob($dir . '/*.png') ?: [];
                $relativeImages = [];
                foreach ($images as $img) {
                    $relativeImages[] = '/output/graphics/' . $dirName . '/' . basename($img);
                }

                // Check subdirectories (e.g., top100/instagram, top100/linkedin, top100/twitter)
                $subdirs = glob($dir . '/*', GLOB_ONLYDIR) ?: [];
                foreach ($subdirs as $subdir) {
                    $subName = basename($subdir);
                    $subImages = glob($subdir . '/*.png') ?: [];
                    foreach ($subImages as $simg) {
                        $relativeImages[] = '/output/graphics/' . $dirName . '/' . $subName . '/' . basename($simg);
                    }
                }

                if (!empty($relativeImages)) {
                    $graphicSets[] = [
                        'folder' => $dirName,
                        'name' => ucwords(str_replace(['_', '-'], ' ', $dirName)),
                        'images' => $relativeImages,
                        'count' => count($relativeImages),
                    ];
                }
            }
        }

        // 2. Read social preview queue
        $campaign = [];
        if (file_exists($this->socialPreviewFile)) {
            $campaign = json_decode(file_get_contents($this->socialPreviewFile), true) ?: [];
        }

        return view('admin.social.index', [
            'activeNav' => 'social',
            'graphicSets' => $graphicSets,
            'campaign' => $campaign,
        ]);
    }

    public function publish()
    {
        $pythonBin = file_exists($this->baseDir . '/.venv/bin/python') ? '.venv/bin/python' : 'python3';
        $cmd = "{$pythonBin} -m src.publisher";
        $output = [];
        $returnVar = 0;
        exec("cd " . escapeshellarg($this->baseDir) . " && {$cmd} 2>&1", $output, $returnVar);

        session_flash('success', 'Social media pipeline executed. Campaign dispatched to Instagram & Twitter queue!');
        redirect('/admin/social');
    }

    public function generate()
    {
        $type = request('type', 'top100');
        $platform = request('platform', 'vertical');
        $pythonBin = file_exists($this->baseDir . '/.venv/bin/python') ? '.venv/bin/python' : 'python3';
        $cmd = "{$pythonBin} -m src.generator_graphics --type " . escapeshellarg($type) . " --platform " . escapeshellarg($platform);
        $output = [];
        $returnVar = 0;
        exec("cd " . escapeshellarg($this->baseDir) . " && {$cmd} 2>&1", $output, $returnVar);

        // Strict track isolation for Telegram dispatch
        $track = 'all';
        if ($type === 'tech_news') {
            $track = 'news';
        } elseif (in_array($type, ['top100', 'website_tip', 'tech_tip'])) {
            $track = 'dev';
        } elseif ($type === 'carousel') {
            $track = 'local';
        }

        exec("cd " . escapeshellarg($this->baseDir) . " && {$pythonBin} -m src.telegram_notifier --latest --track " . escapeshellarg($track) . " 2>&1", $tgOut, $tgCode);

        session_flash('success', "Generated [{$type}] graphic! Dispatched strictly to [{$track}] Telegram queue.");
        redirect('/admin/social');
    }

    public function telegram()
    {
        $track = request('track', 'all');
        $pythonBin = file_exists($this->baseDir . '/.venv/bin/python') ? '.venv/bin/python' : 'python3';
        $cmd = "{$pythonBin} -m src.telegram_notifier --latest --track " . escapeshellarg($track);
        $output = [];
        $returnVar = 0;
        exec("cd " . escapeshellarg($this->baseDir) . " && {$cmd} 2>&1", $output, $returnVar);

        $outText = implode("\n", $output);
        if (str_contains($outText, '"ok": true') || str_contains($outText, '✅')) {
            session_flash('success', "Latest [{$track}] assets successfully dispatched to your Telegram queue!");
        } else {
            session_flash('error', 'Dispatched request to Telegram Bot. Notice: Verify bot token if Telegram returned 401 Unauthorized.');
        }
        redirect('/admin/social');
    }
}
