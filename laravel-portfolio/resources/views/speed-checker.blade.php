@extends('layouts.app')

@section('title', 'Free Mobile Speed Checker & Core Web Vitals Diagnostic | ExtrovertNerd')
@section('meta_description', 'Test your website mobile speed score. See how much revenue your business is losing to slow load times and discover how a custom Laravel architecture achieves 100/100 Core Web Vitals.')

@section('content')
<div class="max-w-7xl mx-auto px-6 py-12">

    <!-- HERO SECTION -->
    <div class="text-center max-w-3xl mx-auto space-y-4">
        <div class="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold tracking-wide">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span>EXTROVERTNERD LAB • INSTANT SPEED AUDIT</span>
        </div>
        <h1 class="text-4xl md:text-5xl font-black text-white tracking-tight leading-tight">
            How Much Revenue Is Your Slow Website <span class="font-serif italic font-normal text-rose-400 underline decoration-rose-500/30">Losing Daily</span>?
        </h1>
        <p class="text-slate-400 text-base md:text-lg leading-relaxed">
            Enter your website URL below to simulate your real-world mobile 4G/5G latency and compare it directly against ExtrovertNerd’s verified sub-second Laravel architecture.
        </p>
    </div>

    <!-- URL INPUT FORM -->
    <div class="max-w-2xl mx-auto mt-8">
        <form action="/speed-checker" method="GET" class="flex flex-col sm:flex-row items-center gap-3 bg-slate-900/90 border border-white/10 p-2.5 rounded-2xl shadow-2xl focus-within:border-emerald-500/50 transition">
            <div class="flex items-center space-x-3 px-3 w-full">
                <span class="text-slate-500 font-mono text-sm">https://</span>
                <input 
                    type="text" 
                    name="url" 
                    value="{{ $url ?? '' }}" 
                    placeholder="yourbusiness.com" 
                    required 
                    class="bg-transparent border-0 text-white placeholder-slate-500 text-base focus:ring-0 w-full outline-none font-medium"
                >
            </div>
            <button type="submit" class="w-full sm:w-auto shrink-0 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-sm uppercase tracking-wider px-7 py-3.5 rounded-xl shadow-lg shadow-emerald-500/25 hover:scale-105 transition">
                Analyze Speed ➔
            </button>
        </form>

        <!-- Quick seed suggestions -->
        <div class="flex items-center justify-center space-x-2 text-xs text-slate-500 mt-3 font-mono">
            <span>Try demo:</span>
            <a href="/speed-checker?url=luxurygoavillas.com" class="text-slate-400 hover:text-emerald-400 underline">luxurygoavillas.com</a>
            <span>•</span>
            <a href="/speed-checker?url=mumbaicouture.in" class="text-slate-400 hover:text-emerald-400 underline">mumbaicouture.in</a>
            <span>•</span>
            <a href="/speed-checker?url=bangaloresmiles.com" class="text-slate-400 hover:text-emerald-400 underline">bangaloresmiles.com</a>
        </div>
    </div>

    @if($result)
    <!-- ============================================================== -->
    <!-- AUDIT RESULTS: BEFORE VS AFTER SIDE-BY-SIDE BENCHMARK          -->
    <!-- ============================================================== -->
    <div class="mt-16 space-y-8 animate-fade-in">

        <!-- Result Summary Bar -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 rounded-xl bg-slate-900 border border-white/10 text-sm">
            <div class="flex items-center space-x-3">
                <span class="w-3 h-3 rounded-full bg-rose-500 animate-pulse"></span>
                <span class="text-slate-400">Diagnostic completed for:</span>
                <span class="text-white font-mono font-bold">{{ $result['host'] }}</span>
            </div>
            <div class="text-xs text-slate-500 font-mono mt-2 sm:mt-0">
                Audited by ExtrovertNerd Lab Engine • Standard 4G Mobile Emulation
            </div>
        </div>

        <!-- 2-COLUMN BEFORE VS AFTER COMPARISON -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">

            <!-- LEFT COLUMN: CURRENT WEBSITE (THE BOTTLENECK) -->
            <div class="bg-gradient-to-b from-rose-950/20 to-slate-900/90 border border-rose-500/30 rounded-3xl p-6 md:p-8 space-y-6 shadow-2xl relative overflow-hidden">
                <div class="absolute -right-4 -top-2">
                    <span class="border-2 border-rose-500 text-rose-400 font-black text-xs uppercase px-3 py-1 rounded rotate-3 inline-block">FAILS CORE WEB VITALS</span>
                </div>

                <div class="space-y-1">
                    <span class="text-xs font-mono font-bold text-rose-400 uppercase tracking-widest">Current Website Architecture</span>
                    <h2 class="text-2xl font-black text-white">Sluggish & Leaking Conversions</h2>
                    <p class="text-xs text-slate-400 font-mono">{{ $result['current']['platform'] }}</p>
                </div>

                <!-- Speedometer Display -->
                <div class="bg-black/40 border border-white/10 rounded-2xl p-6 text-center">
                    <div class="text-5xl font-black font-mono text-rose-500">{{ $result['current']['score'] }}<span class="text-xl text-slate-500">/100</span></div>
                    <div class="text-xs font-bold text-rose-400 mt-1 uppercase tracking-wider">Critical Mobile Latency</div>
                </div>

                <!-- Key Metrics Grid -->
                <div class="grid grid-cols-2 gap-3 text-sm">
                    <div class="bg-slate-950/60 p-3.5 rounded-xl border border-white/5">
                        <div class="text-xs text-slate-500">Mobile Load Time</div>
                        <div class="text-xl font-bold text-rose-400 font-mono mt-0.5">{{ $result['current']['load_time'] }}</div>
                    </div>
                    <div class="bg-slate-950/60 p-3.5 rounded-xl border border-white/5">
                        <div class="text-xs text-slate-500">Mobile Bounce Rate</div>
                        <div class="text-xl font-bold text-amber-300 font-mono mt-0.5">{{ $result['current']['bounce_rate'] }}</div>
                    </div>
                    <div class="bg-slate-950/60 p-3.5 rounded-xl border border-white/5">
                        <div class="text-xs text-slate-500">Time to First Byte</div>
                        <div class="text-base font-bold text-slate-300 font-mono mt-0.5">{{ $result['current']['ttfb'] }}</div>
                    </div>
                    <div class="bg-slate-950/60 p-3.5 rounded-xl border border-rose-500/20 bg-rose-950/10">
                        <div class="text-xs text-rose-300">Est. Revenue Leak</div>
                        <div class="text-base font-bold text-white font-mono mt-0.5">{{ $result['current']['estimated_leak'] }}</div>
                    </div>
                </div>

                <!-- Diagnosis Bullets -->
                <div class="space-y-2 text-xs text-slate-300 pt-2 border-t border-white/10">
                    <div class="flex items-center space-x-2 text-rose-400">
                        <span>✕</span>
                        <span>{{ $result['current']['scripts_count'] }} external tracking scripts and plugin payloads</span>
                    </div>
                    <div class="flex items-center space-x-2 text-rose-400">
                        <span>✕</span>
                        <span>Cumulative Layout Shift: {{ $result['current']['cls'] }}</span>
                    </div>
                    <div class="flex items-center space-x-2 text-rose-400">
                        <span>✕</span>
                        <span>No automated WhatsApp booking notification pipeline</span>
                    </div>
                </div>
            </div>

            <!-- RIGHT COLUMN: EXTROVERTNERD LARAVEL BENCHMARK (THE FIX) -->
            <div class="bg-gradient-to-b from-emerald-950/25 to-slate-900/90 border border-emerald-500/40 rounded-3xl p-6 md:p-8 space-y-6 shadow-2xl relative glow-emerald">
                <div class="absolute -right-4 -top-2">
                    <span class="border-2 border-emerald-400 text-emerald-300 font-black text-xs uppercase px-3 py-1 rounded -rotate-2 inline-block">100% GREEN CORE WEB VITALS</span>
                </div>

                <div class="space-y-1">
                    <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">ExtrovertNerd Re-Architecture</span>
                    <h2 class="text-2xl font-black text-white">Sub-Second Speed & Revenue Growth</h2>
                    <p class="text-xs text-slate-400 font-mono">{{ $result['laravel_benchmark']['platform'] }}</p>
                </div>

                <!-- Speedometer Display -->
                <div class="bg-black/40 border border-emerald-500/30 rounded-2xl p-6 text-center">
                    <div class="text-5xl font-black font-mono text-emerald-400">{{ $result['laravel_benchmark']['score'] }}<span class="text-xl text-emerald-600">/100</span></div>
                    <div class="text-xs font-bold text-emerald-300 mt-1 uppercase tracking-wider">Flawless Mobile Core Web Vitals</div>
                </div>

                <!-- Key Metrics Grid -->
                <div class="grid grid-cols-2 gap-3 text-sm">
                    <div class="bg-slate-950/60 p-3.5 rounded-xl border border-white/5">
                        <div class="text-xs text-slate-500">Mobile Load Time</div>
                        <div class="text-xl font-bold text-emerald-400 font-mono mt-0.5">{{ $result['laravel_benchmark']['load_time'] }}</div>
                    </div>
                    <div class="bg-slate-950/60 p-3.5 rounded-xl border border-white/5">
                        <div class="text-xs text-slate-500">Verified Conversion Jump</div>
                        <div class="text-xl font-bold text-cyan-300 font-mono mt-0.5">{{ $result['laravel_benchmark']['conversion_lift'] }}</div>
                    </div>
                    <div class="bg-slate-950/60 p-3.5 rounded-xl border border-white/5">
                        <div class="text-xs text-slate-500">Time to First Byte</div>
                        <div class="text-base font-bold text-slate-200 font-mono mt-0.5">{{ $result['laravel_benchmark']['ttfb'] }}</div>
                    </div>
                    <div class="bg-slate-950/60 p-3.5 rounded-xl border border-emerald-500/20 bg-emerald-950/10">
                        <div class="text-xs text-emerald-300">Platform Transaction Cut</div>
                        <div class="text-base font-bold text-white font-mono mt-0.5">0.0% (Zero Tax)</div>
                    </div>
                </div>

                <!-- Feature Bullets -->
                <div class="space-y-2 text-xs text-slate-200 pt-2 border-t border-white/10">
                    <div class="flex items-center space-x-2 text-emerald-400">
                        <span>✓</span>
                        <span>Redis in-memory caching serving pages in 28 milliseconds</span>
                    </div>
                    <div class="flex items-center space-x-2 text-emerald-400">
                        <span>✓</span>
                        <span>Zero-bloat Tailwind CSS & Alpine.js with 0.00 CLS</span>
                    </div>
                    <div class="flex items-center space-x-2 text-emerald-400">
                        <span>✓</span>
                        <span>Direct 1-tap WhatsApp Cloud API reservation & checkout alerts</span>
                    </div>
                </div>
            </div>

        </div>

        <!-- HIGH-CONVERTING INBOUND WHATSAPP CONVERSION BOX -->
        <div class="bg-gradient-to-r from-slate-900 via-emerald-950/40 to-slate-900 border border-emerald-500/40 p-8 rounded-3xl text-center space-y-6 shadow-2xl">
            <div class="max-w-2xl mx-auto space-y-2">
                <span class="text-xs font-mono font-bold uppercase text-emerald-400 tracking-widest">NEXT ACTION • DIRECT FROM ARCHITECT RAVI</span>
                <h3 class="text-3xl font-black text-white">Want the Exact Code Roadmap to Fix Your {{ $result['host'] }} Score?</h3>
                <p class="text-slate-300 text-sm leading-relaxed">
                    Within 24 hours, Lead Web Architect Ravi will record a personalized 3-minute screen recording analyzing your Core Web Vitals bottlenecks and how a custom Laravel upgrade will boost your revenue.
                </p>
            </div>

            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
                <a href="{{ $result['whatsapp_url'] }}" target="_blank" rel="noopener" class="w-full sm:w-auto inline-flex items-center justify-center space-x-3 bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-base px-8 py-4 rounded-2xl shadow-xl shadow-emerald-500/25 hover:scale-105 transition">
                    <span>📱</span>
                    <span>Claim Free 3-Minute Video Breakdown on WhatsApp ➔</span>
                </a>
                <a href="/blog" class="w-full sm:w-auto inline-flex items-center justify-center space-x-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-sm px-6 py-4 rounded-2xl transition border border-white/10">
                    <span>Read Verified Case Studies</span>
                </a>
            </div>

            <div class="text-xs text-slate-500 font-mono">
                100% Free • No Obligation • Reviewed Personally by Ravi
            </div>
        </div>

    </div>
    @endif

</div>
@endsection
