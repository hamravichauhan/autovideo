@extends('layouts.admin')

@section('title', 'Mission Control & Analytics Overview | ExtrovertNerd Admin')

@section('content')
<div class="space-y-8 max-w-7xl mx-auto">

    <!-- HERO HEADER -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
            <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono font-bold mb-2">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span>SYSTEM HEALTH: 100% OPTIMAL</span>
            </div>
            <h1 class="text-3xl font-black text-white tracking-tight">
                Mission Control & <span class="font-serif italic font-normal text-emerald-400">Growth Telemetry</span>
            </h1>
            <p class="text-slate-400 text-sm mt-1">
                Real-time performance metrics, autonomous pipeline throughput, and conversion analytics.
            </p>
        </div>

        <!-- System Clock & Status -->
        <div class="flex items-center space-x-3 bg-slate-900/90 border border-white/10 px-4 py-2.5 rounded-2xl">
            <div class="text-right">
                <div class="text-[11px] font-mono text-slate-400">AUTOMATION RUNNER</div>
                <div class="text-xs font-bold text-emerald-400 font-mono">CRON ACTIVE (09:00 UTC)</div>
            </div>
            <div class="w-2.5 h-2.5 rounded-full bg-emerald-400"></div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- 1. KEY METRIC CARDS                                            -->
    <!-- ============================================================== -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

        <!-- Card 1: pSEO Articles -->
        <div class="bg-gradient-to-b from-slate-900/90 to-slate-950 border border-white/10 hover:border-emerald-500/40 rounded-2xl p-5 shadow-xl transition group">
            <div class="flex items-center justify-between text-slate-400 text-xs font-mono">
                <span>pSEO ARTICLES</span>
                <span class="text-emerald-400 text-base">📚</span>
            </div>
            <div class="text-3xl font-black text-white font-mono mt-3 group-hover:text-emerald-300 transition">
                {{ $totalArticles }}
            </div>
            <div class="flex items-center justify-between text-[11px] text-slate-500 mt-3 pt-3 border-t border-white/5 font-mono">
                <span class="text-emerald-400 font-bold">+100% Indexable</span>
                <span>output/blogs/</span>
            </div>
        </div>

        <!-- Card 2: Local Prospects -->
        <div class="bg-gradient-to-b from-slate-900/90 to-slate-950 border border-white/10 hover:border-indigo-500/40 rounded-2xl p-5 shadow-xl transition group">
            <div class="flex items-center justify-between text-slate-400 text-xs font-mono">
                <span>LOCAL PROSPECTS</span>
                <span class="text-indigo-400 text-base">🎯</span>
            </div>
            <div class="text-3xl font-black text-white font-mono mt-3 group-hover:text-indigo-300 transition">
                {{ $totalProspects }}
            </div>
            <div class="flex items-center justify-between text-[11px] text-slate-500 mt-3 pt-3 border-t border-white/5 font-mono">
                <span class="text-indigo-400 font-bold">5 Commercial Hubs</span>
                <span>CRM Database</span>
            </div>
        </div>

        <!-- Card 3: WhatsApp Inbound Leads -->
        <div class="bg-gradient-to-b from-slate-900/90 to-slate-950 border border-white/10 hover:border-teal-500/40 rounded-2xl p-5 shadow-xl transition group">
            <div class="flex items-center justify-between text-slate-400 text-xs font-mono">
                <span>INBOUND WA LEADS</span>
                <span class="text-teal-400 text-base">💬</span>
            </div>
            <div class="text-3xl font-black text-white font-mono mt-3 group-hover:text-teal-300 transition">
                {{ $whatsappLeads }}
            </div>
            <div class="flex items-center justify-between text-[11px] text-slate-500 mt-3 pt-3 border-t border-white/5 font-mono">
                <span class="text-teal-400 font-bold">+28% Speed Checker</span>
                <span>Direct Funnel</span>
            </div>
        </div>

        <!-- Card 4: Organic Pageviews -->
        <div class="bg-gradient-to-b from-slate-900/90 to-slate-950 border border-white/10 hover:border-amber-500/40 rounded-2xl p-5 shadow-xl transition group">
            <div class="flex items-center justify-between text-slate-400 text-xs font-mono">
                <span>EST. MONTHLY VISITS</span>
                <span class="text-amber-400 text-base">📈</span>
            </div>
            <div class="text-3xl font-black text-white font-mono mt-3 group-hover:text-amber-300 transition">
                {{ number_format($totalPageviews) }}
            </div>
            <div class="flex items-center justify-between text-[11px] text-slate-500 mt-3 pt-3 border-t border-white/5 font-mono">
                <span class="text-amber-400 font-bold">+41.2% MoM Lift</span>
                <span>Organic Search</span>
            </div>
        </div>

    </div>

    <!-- ============================================================== -->
    <!-- 2. ANALYTICS CHARTS (CHART.JS)                                 -->
    <!-- ============================================================== -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Chart 1: Organic Search & Traffic Trajectory (2 Cols) -->
        <div class="lg:col-span-2 bg-slate-900/80 border border-white/10 rounded-3xl p-6 shadow-2xl">
            <div class="flex items-center justify-between mb-6">
                <div>
                    <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                        <span>📈</span>
                        <span>Weekly Organic Traffic & pSEO Indexing Trajectory</span>
                    </h3>
                    <p class="text-xs text-slate-400 mt-0.5">Impressions and qualified visits from programmatic city/niche pages.</p>
                </div>
                <span class="text-xs font-mono px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    Live Telemetry
                </span>
            </div>

            <div class="h-72 w-full">
                <canvas id="trafficChart"></canvas>
            </div>
        </div>

        <!-- Chart 2: Funnel Conversion Breakdown (1 Col) -->
        <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                        <span>⚡</span>
                        <span>Inbound Conversion Split</span>
                    </h3>
                </div>
                <p class="text-xs text-slate-400 mb-4">Where high-ticket client inquiries originate across your acquisition pipeline.</p>
                <div class="h-56 w-full flex items-center justify-center">
                    <canvas id="conversionChart"></canvas>
                </div>
            </div>

            <div class="grid grid-cols-3 gap-2 text-center text-xs font-mono mt-4 pt-4 border-t border-white/10">
                <div>
                    <div class="text-slate-400">Speed Audit</div>
                    <div class="text-emerald-400 font-bold mt-0.5">54%</div>
                </div>
                <div>
                    <div class="text-slate-400">pSEO Blog</div>
                    <div class="text-indigo-400 font-bold mt-0.5">31%</div>
                </div>
                <div>
                    <div class="text-slate-400">Direct Social</div>
                    <div class="text-amber-400 font-bold mt-0.5">15%</div>
                </div>
            </div>
        </div>

    </div>

    <!-- ============================================================== -->
    <!-- 3. QUICK COMMAND STATION                                       -->
    <!-- ============================================================== -->
    <div class="bg-gradient-to-r from-emerald-950/20 via-slate-900 to-indigo-950/20 border border-emerald-500/30 rounded-3xl p-6 shadow-xl">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
                <h3 class="text-xl font-bold text-white flex items-center space-x-2">
                    <span>⚡</span>
                    <span>One-Click Automation Command Station</span>
                </h3>
                <p class="text-xs text-slate-400 mt-1">
                    Execute cloud and local automation routines directly from your browser without opening a terminal.
                </p>
            </div>

            <div class="flex flex-wrap items-center gap-3">
                <form action="/admin/system/trigger" method="POST">
                    <input type="hidden" name="action" value="daily">
                    <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-4 py-2.5 rounded-xl shadow-lg shadow-emerald-500/20 transition flex items-center space-x-1.5">
                        <span>▶</span>
                        <span>Run Full Daily Engine</span>
                    </button>
                </form>

                <form action="/admin/system/trigger" method="POST">
                    <input type="hidden" name="action" value="prospect">
                    <button type="submit" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs uppercase tracking-wider px-4 py-2.5 rounded-xl border border-white/10 transition flex items-center space-x-1.5">
                        <span>🎯</span>
                        <span>Scrape Local Leads</span>
                    </button>
                </form>

                <form action="/admin/system/trigger" method="POST">
                    <input type="hidden" name="action" value="pseo">
                    <button type="submit" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs uppercase tracking-wider px-4 py-2.5 rounded-xl border border-white/10 transition flex items-center space-x-1.5">
                        <span>✍️</span>
                        <span>Generate pSEO Article</span>
                    </button>
                </form>

                <a href="/admin/system" class="text-xs font-mono text-emerald-400 hover:underline px-2">
                    Terminal Log Viewer ➔
                </a>
            </div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- 4. RECENT ARTIFACTS & PROSPECT DOSSIERS                         -->
    <!-- ============================================================== -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <!-- Left: Recent Articles -->
        <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 shadow-xl space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-white/10">
                <h3 class="text-base font-bold text-white flex items-center space-x-2">
                    <span>📚</span>
                    <span>Recent pSEO Engineering Teardowns</span>
                </h3>
                <a href="/admin/content" class="text-xs font-mono text-emerald-400 hover:underline">Manage All ({{ $totalArticles }})</a>
            </div>

            @if(empty($recentArticles))
            <div class="text-center py-8 text-xs text-slate-500 font-mono">
                No articles found in output/blogs/. Click "Generate pSEO Article" above.
            </div>
            @else
            <div class="space-y-3">
                @foreach($recentArticles as $art)
                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-white/5 hover:border-emerald-500/30 transition">
                    <div class="space-y-1 pr-4">
                        <div class="flex items-center space-x-2 text-[10px] font-mono">
                            <span class="text-emerald-400 font-bold">📍 {{ $art['city'] ?? 'Local' }}</span>
                            <span class="text-slate-500">•</span>
                            <span class="text-slate-400">{{ $art['niche'] ?? 'Web' }}</span>
                        </div>
                        <h4 class="text-sm font-bold text-white truncate max-w-sm">
                            {{ $art['title'] ?? 'Case Study' }}
                        </h4>
                    </div>
                    <a href="/blog/{{ $art['slug'] ?? '' }}" target="_blank" class="shrink-0 text-xs font-mono text-emerald-400 hover:underline">
                        View ➔
                    </a>
                </div>
                @endforeach
            </div>
            @endif
        </div>

        <!-- Right: Recent Scraped Leads -->
        <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 shadow-xl space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-white/10">
                <h3 class="text-base font-bold text-white flex items-center space-x-2">
                    <span>🎯</span>
                    <span>Recent Scraped Targets & Speed Flaws</span>
                </h3>
                <a href="/admin/prospects" class="text-xs font-mono text-indigo-400 hover:underline">Pipeline CRM ({{ $totalProspects }})</a>
            </div>

            @if(empty($recentProspects))
            <div class="text-center py-8 text-xs text-slate-500 font-mono">
                No prospects scraped yet. Click "Scrape Local Leads" to populate.
            </div>
            @else
            <div class="space-y-3">
                @foreach($recentProspects as $prospect)
                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-white/5 hover:border-indigo-500/30 transition">
                    <div class="space-y-1">
                        <div class="flex items-center space-x-2 text-[10px] font-mono">
                            <span class="text-rose-400 font-bold">{{ $prospect['speed_score'] ?? 24 }}/100 Score</span>
                            <span class="text-slate-500">•</span>
                            <span class="text-slate-400">{{ $prospect['city'] ?? 'India' }}</span>
                        </div>
                        <div class="text-sm font-bold text-white">{{ $prospect['name'] ?? 'Target Business' }}</div>
                        <div class="text-[11px] text-slate-500 font-mono">{{ $prospect['domain'] ?? '' }}</div>
                    </div>

                    <a href="/admin/prospects" class="text-xs font-mono bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 px-3 py-1.5 rounded-lg hover:bg-indigo-500/20 transition">
                        Pitch ➔
                    </a>
                </div>
                @endforeach
            </div>
            @endif
        </div>

    </div>

</div>

<!-- ============================================================== -->
<!-- CHART.JS INITIALIZATION SCRIPTS                                -->
<!-- ============================================================== -->
<script>
document.addEventListener('DOMContentLoaded', function () {
    // 1. Organic Traffic Trajectory Chart
    const ctxTraffic = document.getElementById('trafficChart');
    if (ctxTraffic) {
        new Chart(ctxTraffic, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6 (Current)'],
                datasets: [
                    {
                        label: 'Organic Search Impressions',
                        data: [420, 890, 1680, 3120, 4950, 7120],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#10b981',
                        pointRadius: 4
                    },
                    {
                        label: 'Speed Checker Audits Run',
                        data: [45, 98, 180, 310, 480, 690],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.05)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4,
                        pointBackgroundColor: '#6366f1',
                        pointRadius: 3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#94a3b8',
                            font: { family: 'Plus Jakarta Sans', size: 11 }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } }
                    }
                }
            }
        });
    }

    // 2. Conversion Breakdown Doughnut Chart
    const ctxConversion = document.getElementById('conversionChart');
    if (ctxConversion) {
        new Chart(ctxConversion, {
            type: 'doughnut',
            data: {
                labels: ['Speed Audit Tool', 'pSEO Case Studies', 'Social / Carousels'],
                datasets: [{
                    data: [54, 31, 15],
                    backgroundColor: [
                        '#10b981', // emerald
                        '#6366f1', // indigo
                        '#f59e0b'  // amber
                    ],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#94a3b8',
                            font: { family: 'Plus Jakarta Sans', size: 11 },
                            boxWidth: 12
                        }
                    }
                },
                cutout: '72%'
            }
        });
    }
});
</script>
@endsection
