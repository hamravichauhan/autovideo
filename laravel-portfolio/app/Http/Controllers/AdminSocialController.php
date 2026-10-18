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
                $images = glob($dir . '/*.png');
                $relativeImages = [];
                foreach ($images as $img) {
                    // Path relative to public/output
                    $relativeImages[] = '/output/graphics/' . $dirName . '/' . basename($img);
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
        $platform = request('platform', 'all');
        $pythonBin = file_exists($this->baseDir . '/.venv/bin/python') ? '.venv/bin/python' : 'python3';
        $cmd = "{$pythonBin} -m src.generator_graphics --platform {$platform}";
        $output = [];
        $returnVar = 0;
        exec("cd " . escapeshellarg($this->baseDir) . " && {$cmd} 2>&1", $output, $returnVar);

        // Also auto-dispatch newly rendered posters to Telegram
        exec("cd " . escapeshellarg($this->baseDir) . " && {$pythonBin} -m src.telegram_notifier --latest 2>&1", $tgOut, $tgCode);

        session_flash('success', "Graphic renderer completed for [{$platform}]. Posters automatically queued for Telegram dispatch!");
        redirect('/admin/social');
    }

    public function telegram()
    {
        $pythonBin = file_exists($this->baseDir . '/.venv/bin/python') ? '.venv/bin/python' : 'python3';
        $cmd = "{$pythonBin} -m src.telegram_notifier --latest";
        $output = [];
        $returnVar = 0;
        exec("cd " . escapeshellarg($this->baseDir) . " && {$cmd} 2>&1", $output, $returnVar);

        $outText = implode("\n", $output);
        if (str_contains($outText, '"ok": true') || str_contains($outText, '✅')) {
            session_flash('success', 'All latest posters & carousel slides successfully dispatched to your Telegram bot!');
        } else {
            session_flash('error', 'Dispatched request to Telegram Bot. Notice: Verify bot token if Telegram returned 401 Unauthorized.');
        }
        redirect('/admin/social');
    }
}
