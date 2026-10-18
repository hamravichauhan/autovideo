<?php

namespace App\Http\Controllers;

/**
 * Interactive Website Speed Checker Micro-Tool Controller.
 *
 * Simulates and benchmarks mobile performance bottlenecks
 * against ExtrovertNerd's verified sub-second Laravel architecture.
 */
class SpeedCheckerController
{
    /**
     * Display the Speed Checker tool or audit results.
     */
    public function index()
    {
        $url = request('url', '');
        $auditResult = null;

        if (!empty($url)) {
            $auditResult = $this->runSpeedDiagnostic($url);
        }

        return view('speed-checker', [
            'url' => $url,
            'result' => $auditResult,
        ]);
    }

    /**
     * Handle POST form submission.
     */
    public function audit()
    {
        $url = request('url', '');
        if (empty($url)) {
            return redirect('/speed-checker');
        }

        return redirect('/speed-checker?url=' . urlencode($url));
    }

    /**
     * Diagnostic analysis generator for a given URL.
     */
    protected function runSpeedDiagnostic(string $rawUrl): array
    {
        $cleanUrl = filter_var($rawUrl, FILTER_VALIDATE_URL) ? $rawUrl : 'https://' . ltrim($rawUrl, '/');
        $host = parse_url($cleanUrl, PHP_URL_HOST) ?: $cleanUrl;

        // Generate consistent simulated diagnostics based on domain hash
        $hash = crc32($host);
        $score = 22 + (abs($hash) % 18); // 22 to 40/100
        $loadTime = 4.8 + ((abs($hash) % 25) / 10); // 4.8s to 7.3s
        $ttfb = 1800 + (abs($hash) % 1200); // 1.8s to 3.0s
        $scriptsCount = 22 + (abs($hash) % 16); // 22 to 38 scripts
        $lostRevenue = 4500 + ((abs($hash) % 12) * 500); // $4,500 to $10,500/mo

        $platforms = [
            'WordPress (WooCommerce + 28 Active Plugins)',
            'Shopify Storefront (19 Apps & Tracking Scripts)',
            'Elementor Legacy Theme (3.8MB Unminified JS)',
            'Wix / Squarespace Slow Rendering Container',
        ];
        $detectedPlatform = $platforms[abs($hash) % count($platforms)];

        // Pre-populated WhatsApp deep link
        $whatsappMessage = "Hey Ravi! I just ran my site ({$cleanUrl}) through ExtrovertNerd's speed checker and scored {$score}/100 with {$loadTime}s load time. Can you send me the free 3-minute video breakdown of how to fix this?";
        $whatsappUrl = 'https://wa.me/15551234567?text=' . urlencode($whatsappMessage);

        return [
            'url' => $cleanUrl,
            'host' => $host,
            'current' => [
                'score' => $score,
                'load_time' => "{$loadTime}s",
                'ttfb' => "{$ttfb}ms",
                'cls' => '0.38 (Poor)',
                'scripts_count' => $scriptsCount,
                'platform' => $detectedPlatform,
                'bounce_rate' => '68%',
                'estimated_leak' => '$' . number_format($lostRevenue) . '/mo',
                'status' => 'Fails Core Web Vitals',
            ],
            'laravel_benchmark' => [
                'score' => 100,
                'load_time' => '0.32s',
                'ttfb' => '140ms (Redis RAM Cache)',
                'cls' => '0.00 (Flawless)',
                'scripts_count' => '0 Bloat (Pure Tailwind & Alpine)',
                'platform' => 'ExtrovertNerd Laravel 11 Stack',
                'bounce_rate' => '18%',
                'conversion_lift' => '+52%',
                'status' => '100% Green Core Web Vitals',
            ],
            'whatsapp_url' => $whatsappUrl,
        ];
    }
}
