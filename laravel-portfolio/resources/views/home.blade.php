@extends('layouts.app')

@section('title', 'ExtrovertNerd — Full-Stack Web Engineering & Custom Digital Systems')
@section('meta_description', 'ExtrovertNerd is a boutique web engineering studio. We transform slow, leaking websites into sub-second custom architectures engineered for speed, clean code, and resilient infrastructure.')

@section('content')
<div class="space-y-28 md:space-y-36">

    <!-- ============================================================== -->
    <!-- 1. ARTISTIC HERO SECTION                                       -->
    <!-- ============================================================== -->
    <section class="max-w-7xl mx-auto px-6 pt-12 md:pt-24 relative">
        <div class="text-center max-w-4xl mx-auto space-y-8">

            <!-- Studio Pill with Live Tactile Pulse -->
            <div class="inline-flex items-center space-x-2.5 px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold tracking-wide shadow-lg shadow-emerald-500/10">
                <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span>EXTROVERTNERD STUDIO • BESPOKE WEB ARCHITECTURES</span>
            </div>

            <!-- Big Editorial Headline (Plus Jakarta Sans + Playfair Display Italic) -->
            <h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black text-white tracking-tight leading-[1.08]">
                We Rebuild Slow Websites Into 
                <span class="font-serif italic font-normal text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-mint-300 to-teal-200 block sm:inline">Sub-Second Conversion Machines</span>.
            </h1>

            <!-- Tailored Copy -->
            <p class="text-slate-300 text-lg md:text-xl font-normal leading-relaxed max-w-3xl mx-auto">
                Replace bloated WordPress, WooCommerce, and Shopify storefronts with bespoke, sub-second architectures engineered for your exact business requirements. Whether you need high-speed frontend interfaces, robust backend microservices, or custom automation pipelines — ExtrovertNerd builds with whatever stack matches your vision, optimized for Core Web Vitals.
            </p>

            <!-- Multi-Page Action CTAs -->
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                <a 
                    href="/speed-checker" 
                    class="w-full sm:w-auto bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-sm uppercase tracking-wider px-8 py-4 rounded-2xl shadow-xl shadow-emerald-500/25 hover:scale-105 transition duration-300 flex items-center justify-center space-x-2"
                >
                    <span>⚡</span>
                    <span>Launch Free Speed Teardown</span>
                </a>

                <a 
                    href="/how-we-work" 
                    class="w-full sm:w-auto bg-slate-900/90 hover:bg-slate-800 text-white font-bold text-sm px-8 py-4 rounded-2xl border border-white/10 hover:border-emerald-500/40 transition flex items-center justify-center space-x-2 shadow-lg"
                >
                    <span>🔍</span>
                    <span>Explore How We Work</span>
                </a>
            </div>

            <!-- Verified Telemetry Badges -->
            <div class="pt-8 flex flex-wrap items-center justify-center gap-6 sm:gap-10 text-xs font-mono text-slate-400">
                <div class="flex items-center space-x-2">
                    <span class="text-emerald-400 font-bold text-sm">⚡</span>
                    <span>Sub-320ms TTFB Verified</span>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="text-emerald-400 font-bold text-sm">🛡️</span>
                    <span>Verified Core Web Vitals Standards</span>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="text-emerald-400 font-bold text-sm">📈</span>
                    <span>+52% Avg Mobile Conversion Lift</span>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="text-emerald-400 font-bold text-sm">🚫</span>
                    <span>0% Platform Transaction Penalties</span>
                </div>
            </div>

        </div>

        <!-- ============================================================== -->
        <!-- LIVE BEFORE VS AFTER BENCHMARK SHOWCASE                        -->
        <!-- ============================================================== -->
        <div class="mt-20 bg-gradient-to-b from-slate-900/80 to-slate-950 border border-white/10 rounded-3xl p-6 sm:p-10 shadow-2xl relative overflow-hidden">
            <div class="absolute top-0 right-0 w-96 h-96 bg-emerald-500/5 blur-3xl pointer-events-none"></div>

            <div class="flex flex-col md:flex-row md:items-center justify-between pb-8 border-b border-white/10 gap-4">
                <div>
                    <span class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-widest">REAL-WORLD BENCHMARK STUDY</span>
                    <h2 class="text-2xl sm:text-3xl font-black text-white mt-1">Legacy CMS Stack vs. ExtrovertNerd Custom Engine</h2>
                </div>
                <div class="text-xs font-mono text-slate-400 bg-slate-950 px-4 py-2 rounded-xl border border-white/10">
                    Standard 4G Mobile Throttling Emulation (Lighthouse v12)
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 pt-8">
                <!-- Stat 1: Failing Legacy -->
                <div class="space-y-3 bg-rose-950/20 border border-rose-500/30 p-6 rounded-2xl relative">
                    <span class="text-[10px] font-mono font-black uppercase text-rose-400 bg-rose-500/10 px-2.5 py-1 rounded-full border border-rose-500/20">
                        TYPICAL CLIENT SITE
                    </span>
                    <div class="text-4xl sm:text-5xl font-black text-rose-500 font-mono mt-2">
                        5.8s <span class="text-sm text-slate-400 font-normal">load</span>
                    </div>
                    <div class="text-xs text-rose-300 font-mono">24/100 Mobile Score • 6.2MB Payload</div>
                    <p class="text-xs text-slate-400 leading-relaxed pt-1">
                        Weighted down by 32 plugins, unminified tracking scripts, and slow database queries. 53% of mobile visitors abandon before seeing the product.
                    </p>
                </div>

                <!-- Stat 2: ExtrovertNerd Rebuild -->
                <div class="space-y-3 bg-emerald-950/20 border border-emerald-500/40 p-6 rounded-2xl relative">
                    <span class="text-[10px] font-mono font-black uppercase text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/30">
                        EXTROVERTNERD CUSTOM REBUILD
                    </span>
                    <div class="text-4xl sm:text-5xl font-black text-emerald-400 font-mono mt-2">
                        0.32s <span class="text-sm text-emerald-600 font-normal">instant</span>
                    </div>
                    <div class="text-xs text-emerald-300 font-mono">100/100 Mobile Score • 140KB Payload</div>
                    <p class="text-xs text-slate-400 leading-relaxed pt-1">
                        Tailored architecture with in-memory RAM caching and purged CSS. Pages render instantaneously on mobile 4G.
                    </p>
                </div>

                <!-- Stat 3: Commercial ROI Lift -->
                <div class="space-y-3 bg-slate-950 border border-teal-500/30 p-6 rounded-2xl relative">
                    <span class="text-[10px] font-mono font-black uppercase text-teal-400 bg-teal-500/10 px-2.5 py-1 rounded-full border border-teal-500/20">
                        BOTTOM LINE IMPACT
                    </span>
                    <div class="text-4xl sm:text-5xl font-black text-teal-300 font-mono mt-2">
                        +52% <span class="text-sm text-slate-400 font-normal">sales</span>
                    </div>
                    <div class="text-xs text-teal-400 font-mono">+Zero SaaS Plugin Subscriptions</div>
                    <p class="text-xs text-slate-400 leading-relaxed pt-1">
                        Frictionless 1-tap mobile checkout and instant booking alerts via direct WhatsApp webhooks save thousands in monthly SaaS fees.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 2. "HOW WE WORK" - 5-STEP BLUEPRINT SUMMARY TEASER             -->
    <!-- ============================================================== -->
    <section class="max-w-7xl mx-auto px-6">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
            <div class="space-y-3 max-w-2xl">
                <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold uppercase tracking-widest">
                    <span>THE ENGINEERING BLUEPRINT</span>
                </div>
                <h2 class="text-4xl sm:text-5xl font-black text-white tracking-tight">
                    How We Make Your Website <span class="font-serif italic font-normal text-emerald-400">100/100 Good</span>.
                </h2>
                <p class="text-slate-300 text-base leading-relaxed">
                    We don't sell generic themes or band-aid optimization plugins. Here is our 5-phase forensic methodology to take your website to sub-second speed:
                </p>
            </div>
            <a 
                href="/how-we-work" 
                class="inline-flex items-center space-x-2 bg-slate-900 hover:bg-slate-800 text-emerald-400 border border-emerald-500/30 font-bold text-xs uppercase tracking-wider px-6 py-3.5 rounded-xl transition duration-200 shrink-0"
            >
                <span>Read Full 5-Step Breakdown</span>
                <span>➔</span>
            </a>
        </div>

        <!-- 5 Steps Preview Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-slate-900/50 border border-white/10 hover:border-emerald-500/30 rounded-2xl p-7 space-y-3 transition">
                <div class="flex items-center justify-between">
                    <span class="font-mono text-xs font-bold text-emerald-400">PHASE 01</span>
                    <span class="text-[10px] font-mono text-slate-500 uppercase">Audit</span>
                </div>
                <h3 class="text-xl font-bold text-white">Forensic Speed Audit</h3>
                <p class="text-xs text-slate-400 leading-relaxed">
                    Chrome DevTools trace isolating 4MB hero graphics, database locks, and render-blocking JavaScript scripts.
                </p>
                <div class="text-[11px] font-mono text-slate-300 pt-2 border-t border-white/5">
                    Deliverable: 3-Min Personalized Video Teardown
                </div>
            </div>

            <div class="bg-slate-900/50 border border-white/10 hover:border-teal-500/30 rounded-2xl p-7 space-y-3 transition">
                <div class="flex items-center justify-between">
                    <span class="font-mono text-xs font-bold text-teal-400">PHASE 02</span>
                    <span class="text-[10px] font-mono text-slate-500 uppercase">Architecture</span>
                </div>
                <h3 class="text-xl font-bold text-white">Decouple & Tailored Rebuild</h3>
                <p class="text-xs text-slate-400 leading-relaxed">
                    Eradicating 96% of payload. Built in your optimal stack (Next.js, Laravel, Node, Python) with zero plugin bloat.
                </p>
                <div class="text-[11px] font-mono text-slate-300 pt-2 border-t border-white/5">
                    Deliverable: 140KB Clean Production Core
                </div>
            </div>

            <div class="bg-slate-900/50 border border-white/10 hover:border-emerald-500/30 rounded-2xl p-7 space-y-3 transition">
                <div class="flex items-center justify-between">
                    <span class="font-mono text-xs font-bold text-emerald-400">PHASE 03</span>
                    <span class="text-[10px] font-mono text-slate-500 uppercase">Performance</span>
                </div>
                <h3 class="text-xl font-bold text-white">In-Memory RAM Caching</h3>
                <p class="text-xs text-slate-400 leading-relaxed">
                    Redis in-memory caching serving pages in 28ms, plus automated AVIF/WebP image pipeline with zero layout shift.
                </p>
                <div class="text-[11px] font-mono text-slate-300 pt-2 border-t border-white/5">
                    Deliverable: Sub-120ms Server TTFB
                </div>
            </div>

            <div class="bg-slate-900/50 border border-white/10 hover:border-teal-500/30 rounded-2xl p-7 space-y-3 transition">
                <div class="flex items-center justify-between">
                    <span class="font-mono text-xs font-bold text-teal-400">PHASE 04</span>
                    <span class="text-[10px] font-mono text-slate-500 uppercase">Conversion</span>
                </div>
                <h3 class="text-xl font-bold text-white">Frictionless 1-Tap UX</h3>
                <p class="text-xs text-slate-400 leading-relaxed">
                    Direct WhatsApp booking funnels, frictionless checkout, and instant webhook dispatches without third-party SaaS fees.
                </p>
                <div class="text-[11px] font-mono text-slate-300 pt-2 border-t border-white/5">
                    Deliverable: +52% Mobile Inquiry Surge
                </div>
            </div>

            <div class="bg-gradient-to-br from-emerald-950/40 to-slate-900/80 border border-emerald-500/40 rounded-2xl p-7 space-y-3 transition md:col-span-2">
                <div class="flex items-center justify-between">
                    <span class="font-mono text-xs font-bold text-emerald-300">PHASE 05</span>
                    <span class="text-[10px] font-mono text-emerald-400 uppercase font-bold">Verified Delivery</span>
                </div>
                <h3 class="text-xl font-bold text-white">Real-World Core Web Vitals Verification</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                    Every client build is rigorously stress-tested on real mobile 4G latency. We benchmark sub-second LCP and green Core Web Vitals before production deployment.
                </p>
                <div class="text-[11px] font-mono text-emerald-300 pt-2 border-t border-emerald-500/20 font-bold">
                    Rigorous Throttled 4G Testing • Real-World Performance
                </div>
            </div>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 3. TECH-AGNOSTIC ARSENAL: ANY TOOL • ANY STACK                 -->
    <!-- ============================================================== -->
    <section class="max-w-7xl mx-auto px-6">
        <div class="text-center max-w-3xl mx-auto space-y-4 mb-16">
            <div class="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-400 text-xs font-mono font-bold uppercase tracking-widest">
                <span>TECH-AGNOSTIC CRAFTSMANSHIP</span>
            </div>
            <h2 class="text-4xl sm:text-5xl font-black text-white tracking-tight leading-tight">
                Any Tech Stack. Any Tool. <br>
                <span class="font-serif italic font-normal text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300">Engineered for Your Exact Requirements</span>.
            </h2>
            <p class="text-slate-300 text-base md:text-lg leading-relaxed">
                We don't force dogmatic templates or lock you into one framework. ExtrovertNerd builds with whatever tool matches your product roadmap, scale, and performance needs.
            </p>
        </div>

        <!-- 4 Pillars Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

            <!-- Pillar 1: Modern Frontend -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-6 space-y-5 transition duration-300 shadow-xl group flex flex-col justify-between">
                <div class="space-y-4">
                    <div class="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-2xl font-bold group-hover:scale-110 transition">
                        ⚛️
                    </div>
                    <div>
                        <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-widest">Frontend & Reactive Web</span>
                        <h3 class="text-xl font-black text-white mt-1">Next.js, React & Modern UI</h3>
                    </div>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        Server Components, App Router, zero-runtime CSS, dynamic SEO metadata, and fluid micro-interactions.
                    </p>
                </div>
                <div class="pt-4 border-t border-white/10 space-y-2">
                    <div class="flex flex-wrap gap-1.5 font-mono text-[11px]">
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Next.js 15</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">React 19</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Vue 3</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">SvelteKit</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Tailwind</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">TypeScript</span>
                    </div>
                </div>
            </div>

            <!-- Pillar 2: High-Throughput Backend -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-teal-500/40 rounded-3xl p-6 space-y-5 transition duration-300 shadow-xl group flex flex-col justify-between">
                <div class="space-y-4">
                    <div class="w-12 h-12 rounded-2xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400 text-2xl font-bold group-hover:scale-110 transition">
                        ⚡
                    </div>
                    <div>
                        <span class="text-[10px] font-mono text-teal-400 font-bold uppercase tracking-widest">Backends & APIs</span>
                        <h3 class="text-xl font-black text-white mt-1">Laravel, Node.js, Python & Go</h3>
                    </div>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        From ultra-fast monoliths to high-throughput event queues, AI pipelines, and websocket real-time engines.
                    </p>
                </div>
                <div class="pt-4 border-t border-white/10 space-y-2">
                    <div class="flex flex-wrap gap-1.5 font-mono text-[11px]">
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Laravel 11</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">PHP 8.4</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Node.js</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Python</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">FastAPI</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Go</span>
                    </div>
                </div>
            </div>

            <!-- Pillar 3: Database & Caching -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-6 space-y-5 transition duration-300 shadow-xl group flex flex-col justify-between">
                <div class="space-y-4">
                    <div class="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-2xl font-bold group-hover:scale-110 transition">
                        🗄️
                    </div>
                    <div>
                        <span class="text-[10px] font-mono text-emerald-400 font-bold uppercase tracking-widest">Data & In-Memory</span>
                        <h3 class="text-xl font-black text-white mt-1">Postgres, Redis & Supabase</h3>
                    </div>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        Sub-millisecond Redis RAM caches, ACID-compliant relational schemas, vector indexing, and automatic backups.
                    </p>
                </div>
                <div class="pt-4 border-t border-white/10 space-y-2">
                    <div class="flex flex-wrap gap-1.5 font-mono text-[11px]">
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">PostgreSQL</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Redis RAM</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">MySQL 8</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Supabase</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">MongoDB</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">SQLite</span>
                    </div>
                </div>
            </div>

            <!-- Pillar 4: Mobile, Cloud & Infra -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-teal-500/40 rounded-3xl p-6 space-y-5 transition duration-300 shadow-xl group flex flex-col justify-between">
                <div class="space-y-4">
                    <div class="w-12 h-12 rounded-2xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400 text-2xl font-bold group-hover:scale-110 transition">
                        ☁️
                    </div>
                    <div>
                        <span class="text-[10px] font-mono text-teal-400 font-bold uppercase tracking-widest">Mobile, Cloud & DevOps</span>
                        <h3 class="text-xl font-black text-white mt-1">Flutter, Cloudflare & AWS</h3>
                    </div>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        Cross-platform native iOS/Android apps, edge worker distributions, zero-downtime CI/CD, and serverless tasks.
                    </p>
                </div>
                <div class="pt-4 border-t border-white/10 space-y-2">
                    <div class="flex flex-wrap gap-1.5 font-mono text-[11px]">
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Flutter</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">React Native</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Cloudflare</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">AWS</span>
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-white/10">Docker</span>
                    </div>
                </div>
            </div>

        </div>

        <!-- Callout Banner: "Tell Us What Stack You Want" -->
        <div class="mt-10 bg-gradient-to-r from-emerald-950/30 via-slate-900 to-teal-950/30 border border-emerald-500/30 rounded-3xl p-8 sm:p-10 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
            <div class="space-y-2 text-center md:text-left">
                <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">HAVE A SPECIFIC STACK REQUIREMENT?</span>
                <h4 class="text-2xl font-bold text-white">We Engineer Your Project on Your Terms.</h4>
                <p class="text-slate-300 text-sm max-w-2xl leading-relaxed">
                    Have an existing React/Node codebase? Need a Python machine learning integration? Or want a monolithic Laravel application? We assess your product goals and build with the ideal technologies.
                </p>
            </div>
            <a 
                href="https://wa.me/15551234567?text={{ urlencode('Hey ExtrovertNerd! I have a project requirement and want to discuss what tech stack is best.') }}" 
                target="_blank" 
                rel="noopener"
                class="shrink-0 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-4 rounded-xl shadow-lg shadow-emerald-500/25 transition duration-300"
            >
                Discuss Your Architecture ➔
            </a>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 4. REVENUE RECOVERY CALCULATOR TEASER                           -->
    <!-- ============================================================== -->
    <section class="max-w-5xl mx-auto px-6">
        <div class="bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-white/10 rounded-3xl p-8 sm:p-12 shadow-2xl space-y-8 text-center md:text-left flex flex-col md:flex-row items-center justify-between gap-8">
            <div class="space-y-3 max-w-xl">
                <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">INTERACTIVE CALCULATOR</span>
                <h3 class="text-3xl font-black text-white">How Much Revenue Are You Leaking to Latency?</h3>
                <p class="text-slate-400 text-sm leading-relaxed">
                    Every 100 milliseconds of mobile lag cuts conversion rates by 7%. Run our proprietary latency model to see your exact dollar leakage and projected recovery.
                </p>
                <div class="pt-2 flex items-center space-x-6 text-xs font-mono text-slate-300 justify-center md:justify-start">
                    <span>⚡ Real-Time Model</span>
                    <span>•</span>
                    <span>📈 +52% Projected Lift</span>
                </div>
            </div>
            <a 
                href="/roi-calculator" 
                class="shrink-0 bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-xs uppercase tracking-wider px-8 py-4 rounded-xl shadow-xl shadow-emerald-500/20 hover:scale-105 transition"
            >
                Open Full-Screen Calculator ➔
            </a>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 5. RECENT FIELD CASE STUDIES PREVIEW                           -->
    <!-- ============================================================== -->
    <section class="max-w-7xl mx-auto px-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-12 gap-4">
            <div class="space-y-2">
                <span class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">REAL DATA & BENCHMARKS</span>
                <h2 class="text-3xl sm:text-4xl font-black text-white">Recent Engineering Case Studies</h2>
            </div>
            <a href="/case-studies" class="text-emerald-400 hover:text-emerald-300 font-bold text-sm flex items-center space-x-1">
                <span>View All Case Studies</span>
                <span>➔</span>
            </a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            @if(!empty($recentArticles))
            @foreach($recentArticles as $article)
            <article class="bg-slate-900/60 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-6 flex flex-col justify-between group transition duration-300 shadow-xl hover:-translate-y-1">
                <div class="space-y-3">
                    <div class="flex items-center justify-between text-xs font-mono">
                        <span class="bg-emerald-500/10 text-emerald-400 px-2.5 py-0.5 rounded font-bold border border-emerald-500/20">
                            📍 {{ $article['city'] ?? 'Local' }}
                        </span>
                        <span class="text-slate-500">{{ $article['read_time'] ?? '7 min' }}</span>
                    </div>
                    <h3 class="text-lg font-bold text-white group-hover:text-emerald-300 transition">
                        <a href="/case-studies/{{ $article['slug'] }}">{{ $article['title'] }}</a>
                    </h3>
                    <p class="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                        {{ $article['description'] }}
                    </p>
                </div>
                <div class="pt-4 mt-6 border-t border-white/10 flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-500">{{ $article['date'] ?? date('Y-m-d') }}</span>
                    <a href="/case-studies/{{ $article['slug'] }}" class="text-emerald-400 font-bold hover:translate-x-1 transition flex items-center space-x-1">
                        <span>Read Case Study</span>
                        <span>➔</span>
                    </a>
                </div>
            </article>
            @endforeach
            @else
            <div class="col-span-3 text-center py-12 bg-slate-900/40 rounded-2xl border border-white/10 text-slate-400 text-sm">
                Case studies are compiling in the lab. <a href="/speed-checker" class="text-emerald-400 underline">Run a free speed audit</a> in the meantime.
            </div>
            @endif
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 6. LEAD ARCHITECT DOSSIER & FINAL DIRECT CTA                   -->
    <!-- ============================================================== -->
    <section class="max-w-5xl mx-auto px-6">
        <div class="bg-gradient-to-br from-slate-900 via-slate-950 to-emerald-950/30 border border-emerald-500/40 rounded-3xl p-8 sm:p-14 shadow-2xl relative overflow-hidden">
            <div class="flex flex-col md:flex-row items-center gap-10">
                <div class="w-32 h-32 rounded-3xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-indigo-500 p-1 shadow-2xl shrink-0">
                    <div class="w-full h-full bg-[#020617] rounded-[22px] flex items-center justify-center text-emerald-400 font-black text-4xl font-mono">
                        R
                    </div>
                </div>

                <div class="space-y-4 text-center md:text-left">
                    <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-mono font-bold">
                        <span class="relative flex h-2 w-2">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                        </span>
                        <span>WEB ARCHITECTURE STUDIO • ONLINE & ACTIVE</span>
                    </div>
                    <h2 class="text-3xl sm:text-4xl font-black text-white">Engineered by ExtrovertNerd</h2>
                    <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                        "At ExtrovertNerd, we don't pass client work to junior freelancers or configure slow pre-made templates. Whether your vision demands a reactive Next.js/React frontend, a high-throughput Python API, a Node.js websocket backend, or a sub-second Laravel store, every digital architecture is built with clean code, sub-second latency, and verified Core Web Vitals optimization."
                    </p>
                    <div class="pt-2 flex flex-wrap items-center justify-center md:justify-start gap-4">
                        <a 
                            href="{{ $whatsappUrl }}" 
                            target="_blank" 
                            rel="noopener" 
                            class="bg-gradient-to-r from-emerald-500 to-teal-400 text-slate-950 font-black text-xs uppercase px-7 py-4 rounded-xl shadow-xl shadow-emerald-500/25 transition flex items-center space-x-2 hover:scale-105"
                        >
                            <span>💬</span>
                            <span>Chat with ExtrovertNerd on WhatsApp</span>
                        </a>
                        <a 
                            href="/speed-checker" 
                            class="bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs px-6 py-4 rounded-xl border border-white/10 transition"
                        >
                            Run Free Speed Audit ➔
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>

</div>
@endsection
