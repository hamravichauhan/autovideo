@extends('layouts.app')

@section('title', 'ExtrovertNerd — High-Speed Laravel Web Applications & Agency Hub')
@section('meta_description', 'ExtrovertNerd is a boutique web engineering studio led by Ravi. We build sub-second Laravel e-commerce stores, automated management dashboards, and high-converting web apps.')

@section('content')
<div class="space-y-28">

    <!-- ============================================================== -->
    <!-- 1. HERO SECTION                                                -->
    <!-- ============================================================== -->
    <section class="max-w-7xl mx-auto px-6 pt-12 md:pt-20">
        <div class="text-center max-w-4xl mx-auto space-y-6">
            <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold tracking-wide">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span>EXTROVERTNERD DIGITAL STUDIO • LEAD ARCHITECT: RAVI</span>
            </div>

            <h1 class="text-5xl md:text-7xl font-black text-white tracking-tight leading-[1.1]">
                We Engineer High-Speed Laravel Web Apps That Turn Lost Visitors Into 
                <span class="font-serif italic font-normal text-emerald-400">Paying Clients</span>.
            </h1>

            <p class="text-slate-300 text-lg md:text-xl font-normal leading-relaxed max-w-2xl mx-auto">
                Sub-second e-commerce stores, automated management dashboards, and modern web applications with <strong class="text-white">zero SaaS percentage taxes</strong>.
            </p>

            <!-- Dual Action CTAs -->
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                <a href="/speed-checker" class="w-full sm:w-auto bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-sm uppercase tracking-wider px-8 py-4 rounded-2xl shadow-xl shadow-emerald-500/25 hover:scale-105 transition flex items-center justify-center space-x-2">
                    <span>⚡</span>
                    <span>Test Your Website Speed (Free Tool)</span>
                </a>
                <a href="{{ $whatsappUrl }}" target="_blank" rel="noopener" class="w-full sm:w-auto bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm px-8 py-4 rounded-2xl border border-white/10 hover:border-emerald-500/30 transition flex items-center justify-center space-x-2">
                    <span>📱</span>
                    <span>Direct WhatsApp Chat</span>
                </a>
            </div>

            <!-- Social proof metrics -->
            <div class="pt-8 flex flex-wrap items-center justify-center gap-8 text-xs font-mono text-slate-400">
                <div class="flex items-center space-x-2">
                    <span class="text-emerald-400 font-bold">✓</span>
                    <span>Sub-350ms TTFB Verified</span>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="text-emerald-400 font-bold">✓</span>
                    <span>0% Platform Sales Tax</span>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="text-emerald-400 font-bold">✓</span>
                    <span>100% Core Web Vitals Pass</span>
                </div>
            </div>
        </div>

        <!-- BENCHMARK DISPLAY CARD -->
        <div class="mt-16 bg-gradient-to-b from-slate-900/90 to-slate-950 border border-white/10 rounded-3xl p-6 md:p-10 shadow-2xl">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 divide-y md:divide-y-0 md:divide-x divide-white/10">
                
                <!-- Stat 1 -->
                <div class="space-y-2 md:pr-6 text-center md:text-left">
                    <div class="text-xs font-mono text-slate-500 uppercase">Legacy Platforms (WordPress/Shopify)</div>
                    <div class="text-4xl font-black text-rose-500 font-mono">5.8s <span class="text-lg text-slate-500">Mobile Delay</span></div>
                    <p class="text-xs text-slate-400">Over 53% of potential clients bounce before seeing your offer.</p>
                </div>

                <!-- Stat 2 -->
                <div class="space-y-2 md:px-6 pt-6 md:pt-0 text-center md:text-left">
                    <div class="text-xs font-mono text-emerald-400 uppercase">ExtrovertNerd Laravel Architecture</div>
                    <div class="text-4xl font-black text-emerald-400 font-mono">0.32s <span class="text-lg text-emerald-600">Instant</span></div>
                    <p class="text-xs text-slate-400">Redis in-memory caching serving pages faster than a heartbeat.</p>
                </div>

                <!-- Stat 3 -->
                <div class="space-y-2 md:pl-6 pt-6 md:pt-0 text-center md:text-left">
                    <div class="text-xs font-mono text-cyan-400 uppercase">Verified Business Impact</div>
                    <div class="text-4xl font-black text-cyan-300 font-mono">+52% <span class="text-lg text-slate-500">Conversions</span></div>
                    <p class="text-xs text-slate-400">Higher booking rates and zero recurring monthly third-party app fees.</p>
                </div>

            </div>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 2. SPEED CHECKER QUICK LAUNCHER                                 -->
    <!-- ============================================================== -->
    <section class="max-w-5xl mx-auto px-6">
        <div class="bg-gradient-to-r from-emerald-950/40 via-slate-900 to-indigo-950/40 border border-emerald-500/30 p-8 md:p-12 rounded-3xl text-center space-y-6 relative overflow-hidden">
            <div class="max-w-2xl mx-auto space-y-2">
                <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">INTERACTIVE MICRO-TOOL</span>
                <h2 class="text-3xl font-black text-white">Test Your Website Speed in 5 Seconds</h2>
                <p class="text-slate-400 text-sm">
                    Enter your domain to see your Core Web Vitals score and estimate your monthly revenue leak:
                </p>
            </div>

            <form action="/speed-checker" method="GET" class="max-w-xl mx-auto flex flex-col sm:flex-row items-center gap-3 bg-black/60 border border-white/15 p-2 rounded-2xl">
                <div class="flex items-center space-x-2 px-3 w-full">
                    <span class="text-slate-500 font-mono text-xs">https://</span>
                    <input type="text" name="url" placeholder="yourbusiness.com" required class="bg-transparent border-0 text-white placeholder-slate-500 text-sm focus:ring-0 w-full outline-none">
                </div>
                <button type="submit" class="w-full sm:w-auto bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase px-6 py-3 rounded-xl transition shrink-0">
                    Run Audit ➔
                </button>
            </form>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 3. SERVICES SECTION                                            -->
    <!-- ============================================================== -->
    <section id="services" class="max-w-7xl mx-auto px-6">
        <div class="text-center max-w-3xl mx-auto space-y-4 mb-16">
            <span class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">CORE CAPABILITIES</span>
            <h2 class="text-4xl md:text-5xl font-black text-white tracking-tight">
                Engineered for Speed, Scale & Autonomy
            </h2>
            <p class="text-slate-400 text-base">
                We replace fragile plugin stacks with battle-tested custom Laravel engineering.
            </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Service 1 -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-8 space-y-5 transition duration-300">
                <div class="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-xl">
                    🛍️
                </div>
                <h3 class="text-2xl font-extrabold text-white">High-Speed Headless E-Commerce</h3>
                <p class="text-slate-400 text-sm leading-relaxed">
                    Custom Laravel storefronts delivering sub-350ms checkout flows. Zero 2% platform transaction penalties, unlimited product variations, and bespoke measurement pipelines.
                </p>
                <ul class="space-y-2 text-xs text-slate-300 font-mono pt-2">
                    <li class="flex items-center space-x-2 text-emerald-400"><span>✓</span> <span>0% Platform Transaction Cut</span></li>
                    <li class="flex items-center space-x-2 text-emerald-400"><span>✓</span> <span>Sub-second 1-tap checkout</span></li>
                </ul>
            </div>

            <!-- Service 2 -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-8 space-y-5 transition duration-300">
                <div class="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-bold text-xl">
                    📱
                </div>
                <h3 class="text-2xl font-extrabold text-white">Automated Management Portals</h3>
                <p class="text-slate-400 text-sm leading-relaxed">
                    Internal business dashboards that automate table reservations, villa bookings, and client inquiries via direct WhatsApp Cloud API webhooks with zero monthly SaaS subscriptions.
                </p>
                <ul class="space-y-2 text-xs text-slate-300 font-mono pt-2">
                    <li class="flex items-center space-x-2 text-cyan-400"><span>✓</span> <span>Instant automated WhatsApp alerts</span></li>
                    <li class="flex items-center space-x-2 text-cyan-400"><span>✓</span> <span>Multi-calendar iCal synchronization</span></li>
                </ul>
            </div>

            <!-- Service 3 -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-8 space-y-5 transition duration-300">
                <div class="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 font-bold text-xl">
                    ⚡
                </div>
                <h3 class="text-2xl font-extrabold text-white">Legacy Re-Architecture & Speed</h3>
                <p class="text-slate-400 text-sm leading-relaxed">
                    Migrate bloated WordPress, WooCommerce, and Shopify stores to lightweight Laravel 11 with Tailwind CSS. Slash page weights from 6MB to under 180KB and secure a 100/100 PageSpeed score.
                </p>
                <ul class="space-y-2 text-xs text-slate-300 font-mono pt-2">
                    <li class="flex items-center space-x-2 text-indigo-400"><span>✓</span> <span>100/100 Google PageSpeed guarantee</span></li>
                    <li class="flex items-center space-x-2 text-indigo-400"><span>✓</span> <span>Zero Layout Shift (0.00 CLS)</span></li>
                </ul>
            </div>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 4. RECENT CASE STUDIES                                         -->
    <!-- ============================================================== -->
    <section class="max-w-7xl mx-auto px-6">
        <div class="flex items-end justify-between mb-12">
            <div class="space-y-2">
                <span class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">REAL DATA & BENCHMARKS</span>
                <h2 class="text-3xl md:text-4xl font-black text-white">Recent Engineering Case Studies</h2>
            </div>
            <a href="/blog" class="text-emerald-400 hover:text-emerald-300 font-bold text-sm hidden md:flex items-center space-x-1">
                <span>View All Case Studies</span>
                <span>➔</span>
            </a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            @if(!empty($recentArticles))
            @foreach($recentArticles as $article)
            <article class="bg-slate-900/80 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-6 flex flex-col justify-between group transition duration-300">
                <div class="space-y-3">
                    <div class="flex items-center justify-between text-xs font-mono">
                        <span class="bg-emerald-500/10 text-emerald-400 px-2.5 py-0.5 rounded font-bold">📍 {{ $article['city'] ?? 'Local' }}</span>
                        <span class="text-slate-500">{{ $article['read_time'] ?? '7 min' }}</span>
                    </div>
                    <h3 class="text-lg font-bold text-white group-hover:text-emerald-300 transition">
                        <a href="/blog/{{ $article['slug'] }}">{{ $article['title'] }}</a>
                    </h3>
                    <p class="text-xs text-slate-400 line-clamp-3">
                        {{ $article['description'] }}
                    </p>
                </div>
                <div class="pt-4 mt-4 border-t border-white/10 flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-500">{{ $article['date'] ?? date('Y-m-d') }}</span>
                    <a href="/blog/{{ $article['slug'] }}" class="text-emerald-400 font-bold hover:translate-x-1 transition">Read ➔</a>
                </div>
            </article>
            @endforeach
            @else
            <div class="col-span-3 text-center py-12 bg-slate-900/40 rounded-2xl border border-white/10 text-slate-400 text-sm">
                Case studies are being compiled. <a href="/speed-checker" class="text-emerald-400 underline">Run a speed audit</a> on your site in the meantime.
            </div>
            @endif
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 5. ARCHITECT DOSSIER & FINAL FUNNEL                             -->
    <!-- ============================================================== -->
    <section id="architect" class="max-w-5xl mx-auto px-6">
        <div class="bg-gradient-to-br from-slate-900 via-slate-900/90 to-emerald-950/30 border border-emerald-500/40 rounded-3xl p-8 md:p-14 shadow-2xl relative overflow-hidden">
            <div class="flex flex-col md:flex-row items-center gap-10">
                <div class="w-32 h-32 rounded-3xl bg-gradient-to-tr from-emerald-500 via-cyan-400 to-indigo-500 p-1 shadow-2xl shrink-0">
                    <div class="w-full h-full bg-slate-950 rounded-[22px] flex items-center justify-center text-emerald-400 font-black text-4xl font-mono">
                        R
                    </div>
                </div>

                <div class="space-y-4 text-center md:text-left">
                    <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-mono font-bold">
                        <span>FOUNDER & LEAD WEB ARCHITECT</span>
                    </div>
                    <h2 class="text-3xl md:text-4xl font-black text-white">Engineered Personally by Ravi</h2>
                    <p class="text-slate-300 text-sm md:text-base leading-relaxed">
                        "At ExtrovertNerd, we don't pass client work to junior developers or assemble slow drag-and-drop templates. Every web application is architected from clean Laravel source code with strict Core Web Vitals guarantees."
                    </p>
                    <div class="pt-2 flex flex-wrap items-center justify-center md:justify-start gap-4">
                        <a href="{{ $whatsappUrl }}" target="_blank" rel="noopener" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase px-6 py-3.5 rounded-xl shadow-lg transition">
                            Chat Directly with Ravi on WhatsApp
                        </a>
                        <a href="/speed-checker" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs px-6 py-3.5 rounded-xl border border-white/10 transition">
                            Test Your Site
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>

</div>
@endsection
