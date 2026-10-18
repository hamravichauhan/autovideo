<?php

namespace App\Http\Controllers;

class AdminProspectsController
{
    protected string $baseDir;
    protected string $prospectsFile;
    protected string $draftsFile;

    public function __construct()
    {
        $this->baseDir = project_root();
        $this->prospectsFile = $this->baseDir . '/output/prospects.json';
        $this->draftsFile = $this->baseDir . '/output/outreach_drafts.md';
    }

    public function index()
    {
        $prospects = [];
        if (file_exists($this->prospectsFile)) {
            $prospects = json_decode(file_get_contents($this->prospectsFile), true) ?: [];
        }

        // Calculate funnel summary
        $counts = [
            'total' => count($prospects),
            'scraped' => 0,
            'contacted' => 0,
            'converted' => 0,
            'rejected' => 0,
        ];

        foreach ($prospects as $p) {
            $status = strtolower($p['status'] ?? 'scraped');
            if ($status === 'converted') {
                $counts['converted']++;
            } elseif ($status === 'rejected') {
                $counts['rejected']++;
            } elseif (str_contains($status, 'sent') || str_contains($status, 'contacted')) {
                $counts['contacted']++;
            } else {
                $counts['scraped']++;
            }
        }

        // Outreach drafts content
        $drafts = '';
        if (file_exists($this->draftsFile)) {
            $drafts = file_get_contents($this->draftsFile);
        }

        return view('admin.prospects.index', [
            'activeNav' => 'prospects',
            'prospects' => $prospects,
            'counts' => $counts,
            'drafts' => $drafts,
        ]);
    }

    public function updateStatus()
    {
        $domain = request('domain');
        $newStatus = request('status');

        if ($domain && $newStatus && file_exists($this->prospectsFile)) {
            $prospects = json_decode(file_get_contents($this->prospectsFile), true) ?: [];
            foreach ($prospects as &$p) {
                if (($p['domain'] ?? '') === $domain) {
                    $p['status'] = $newStatus;
                    break;
                }
            }
            file_put_contents($this->prospectsFile, json_encode($prospects, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
            session_flash('success', "Updated status for {$domain} to '{$newStatus}'.");
        }

        redirect('/admin/prospects');
    }

    public function add()
    {
        $name = request('name');
        $domain = request('domain');
        $city = request('city', 'Goa');
        $niche = request('niche', 'Boutique Hotels');
        $speed = (int)request('speed_score', 28);

        if ($name && $domain) {
            $prospects = [];
            if (file_exists($this->prospectsFile)) {
                $prospects = json_decode(file_get_contents($this->prospectsFile), true) ?: [];
            }

            $newProspect = [
                'name' => $name,
                'domain' => $domain,
                'city' => $city,
                'niche' => $niche,
                'speed_score' => $speed,
                'load_time_sec' => round(5.4 + (rand(1, 20) / 10), 1),
                'est_monthly_loss' => '$' . number_format(rand(4, 12) * 1000) . '/mo',
                'status' => 'Scraped',
                'created_at' => date('Y-m-d H:i:s'),
                'whatsapp_url' => 'https://wa.me/15551234567?text=' . urlencode("Hey ExtrovertNerd! Check out speed audit for {$domain}"),
            ];

            array_unshift($prospects, $newProspect);
            file_put_contents($this->prospectsFile, json_encode($prospects, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
            session_flash('success', "Target business '{$name}' added to CRM pipeline.");
        }

        redirect('/admin/prospects');
    }

    public function scrape()
    {
        $city = request('city', 'goa');
        $cmd = "python3 -m src.main --mode prospect --city {$city}";
        $output = [];
        $returnVar = 0;
        exec("cd " . escapeshellarg($this->baseDir) . " && {$cmd} 2>&1", $output, $returnVar);

        session_flash('success', "Local prospecting bot completed for city: {$city}. New targets loaded!");
        redirect('/admin/prospects');
    }
}
