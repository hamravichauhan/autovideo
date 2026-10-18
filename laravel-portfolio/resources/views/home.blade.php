@extends('layouts.app')

@section('title', 'ExtrovertNerd — High-Speed Laravel Web Applications & Agency Hub')
@section('meta_description', 'ExtrovertNerd is a boutique web engineering studio led by Lead Architect Ravi. We transform slow, leaking websites into sub-second Laravel 11 conversion powerhouses with a guaranteed 100/100 Core Web Vitals score.')

@section('content')
<div class="space-y-32">

    <!-- ============================================================== -->
    <!-- 1. ARTISTIC HERO SECTION                                       -->
    <!-- ============================================================== -->
    <section class="max-w-7xl mx-auto px-6 pt-12 md:pt-24 relative">
        <div class="text-center max-w-4xl mx-auto space-y-8">

            <!-- Founder & Lab Pill -->
            <div class="inline-flex items-center space-x-2.5 px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold tracking-wide shadow-lg shadow-emerald-500/10">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span>EXTROVERTNERD BOUTIQUE LAB • LEAD ARCHITECT: RAVI</span>
            </div>

            <!-- Big Editorial Headline -->
            <h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black text-white tracking-tight leading-[1.08]">
                We Rebuild Slow Websites Into 
                <span class="font-serif italic font-normal text-emerald-400 shimmer-text block sm:inline">Sub-Second</span> 
                Conversion Machines.
            </h1>

            <p class="text-slate-300 text-lg md:text-xl font-normal leading-relaxed max-w-3xl mx-auto">
                Replace bloated WordPress, WooCommerce, and Shopify storefronts with custom <strong class="text-white">Laravel 11</strong> architectures that load in under 350ms, pass every Google Core Web Vital, and eliminate monthly SaaS fees.
            </p>

            <!-- Magnetic Action CTAs -->
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                <a 
                    href="#how-we-fix" 
                    class="w-full sm:w-auto bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-sm uppercase tracking-wider px-8 py-4 rounded-2xl shadow-xl shadow-emerald-500/25 hover:scale-105 transition duration-300 flex items-center justify-center space-x-2"
                >
                    <span>⚡</span>
                    <span>See How We Make It 100/100 Good</span>
                </a>

                <a 
                    href="/speed-checker" 
                    class="w-full sm:w-auto bg-slate-900/90 hover:bg-slate-800 text-white font-bold text-sm px-8 py-4 rounded-2xl border border-white/10 hover:border-emerald-500/40 transition flex items-center justify-center space-x-2 shadow-lg"
                >
                    <span>🔍</span>
                    <span>Test Your Website Speed (Free)</span>
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
                    <span>100/100 Core Web Vitals Guarantee</span>
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
        <div class="mt-20 bg-gradient-to-b from-slate-900/90 to-slate-950 border border-white/10 rounded-3xl p-6 sm:p-10 shadow-2xl relative overflow-hidden">
            <div class="absolute top-0 right-0 w-96 h-96 bg-emerald-500/5 blur-3xl pointer-events-none"></div>

            <div class="flex flex-col md:flex-row md:items-center justify-between pb-8 border-b border-white/10 gap-4">
                <div>
                    <span class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-widest">REAL-WORLD BENCHMARK STUDY</span>
                    <h2 class="text-2xl sm:text-3xl font-black text-white mt-1">Legacy Stack vs. ExtrovertNerd Laravel</h2>
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
                        Weighted down by 32 WordPress plugins, unminified tracking scripts, and slow database queries. 53% of mobile visitors abandon before seeing the product.
                    </p>
                </div>

                <!-- Stat 2: ExtrovertNerd Rebuild -->
                <div class="space-y-3 bg-emerald-950/20 border border-emerald-500/40 p-6 rounded-2xl relative">
                    <span class="text-[10px] font-mono font-black uppercase text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/30">
                        EXTROVERTNERD REBUILD
                    </span>
                    <div class="text-4xl sm:text-5xl font-black text-emerald-400 font-mono mt-2">
                        0.32s <span class="text-sm text-emerald-600 font-normal">instant</span>
                    </div>
                    <div class="text-xs text-emerald-300 font-mono">100/100 Mobile Score • 140KB Payload</div>
                    <p class="text-xs text-slate-400 leading-relaxed pt-1">
                        Compiled Laravel 11 routes with Redis in-memory RAM caching and instant Tailwind rendering. Pages appear faster than blinking.
                    </p>
                </div>

                <!-- Stat 3: Commercial ROI Lift -->
                <div class="space-y-3 bg-slate-950 border border-cyan-500/30 p-6 rounded-2xl relative">
                    <span class="text-[10px] font-mono font-black uppercase text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded-full border border-cyan-500/20">
                        BOTTOM LINE IMPACT
                    </span>
                    <div class="text-4xl sm:text-5xl font-black text-cyan-300 font-mono mt-2">
                        +52% <span class="text-sm text-slate-400 font-normal">sales</span>
                    </div>
                    <div class="text-xs text-cyan-400 font-mono">+Zero SaaS Plugin Subscriptions</div>
                    <p class="text-xs text-slate-400 leading-relaxed pt-1">
                        Frictionless 1-tap mobile checkout and instant booking alerts via direct WhatsApp Cloud webhooks save thousands in monthly app fees.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 2. "HOW WE MAKE YOUR WEBSITE GOOD" - 5-STEP BLUEPRINT          -->
    <!-- ============================================================== -->
    <section id="how-we-fix" class="max-w-7xl mx-auto px-6">
        <div class="text-center max-w-3xl mx-auto space-y-4 mb-20">
            <div class="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold uppercase tracking-widest">
                <span>THE ENGINEERING BLUEPRINT</span>
            </div>
            <h2 class="text-4xl sm:text-5xl md:text-6xl font-black text-white tracking-tight leading-tight">
                How ExtrovertNerd Makes Your Website <span class="font-serif italic font-normal text-emerald-400">100/100 Good</span>.
            </h2>
            <p class="text-slate-400 text-base md:text-lg leading-relaxed">
                We don't sell generic themes or band-aid optimization plugins. Here is our exact 5-step engineering framework to transform slow, leaking websites into sub-second revenue machines:
            </p>
        </div>

        <!-- 5 Steps Progression Grid -->
        <div class="space-y-8">

            <!-- STEP 1 -->
            <div class="bg-gradient-to-r from-slate-900/90 to-slate-950 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-8 md:p-12 transition duration-300 shadow-xl group">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-9 h-9 rounded-xl bg-emerald-500 text-slate-950 font-black font-mono text-base flex items-center justify-center shadow-lg shadow-emerald-500/20">
                                01
                            </span>
                            <span class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">PHASE 1: FORENSIC SPEED AUDIT</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">
                            We Extract Every Exact Latency Bottleneck & Quantify Lost Revenue
                        </h3>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            Before touching a line of code, we run deep-packet 4G latency captures on your real mobile visitors. We identify uncompressed 4MB hero graphics, render-blocking third-party trackers, and slow database queries causing bounce rates over 60%.
                        </p>
                        <div class="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-400 pt-2">
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ TTFB Analysis</span>
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ LCP & CLS Extraction</span>
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ Third-Party Bloat Audit</span>
                        </div>
                    </div>

                    <!-- Step Deliverable Card -->
                    <div class="bg-slate-950/80 border border-emerald-500/30 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3 text-xs font-mono">
                        <div class="text-emerald-400 font-bold uppercase">Deliverable to Client:</div>
                        <div class="text-white font-bold text-sm">3-Minute Video Breakdown</div>
                        <p class="text-slate-400 leading-relaxed">
                            Lead Architect Ravi personally records a private 3-minute screen teardown demonstrating where your visitors drop off and how to fix it.
                        </p>
                        <a href="https://wa.me/15551234567?text={{ urlencode('Hey Ravi! Send me the free 3-minute video breakdown for my website.') }}" target="_blank" class="inline-block text-emerald-400 hover:underline pt-2 font-bold">
                            Request Your Video Teardown ➔
                        </a>
                    </div>
                </div>
            </div>

            <!-- STEP 2 -->
            <div class="bg-gradient-to-r from-slate-900/90 to-slate-950 border border-white/10 hover:border-indigo-500/40 rounded-3xl p-8 md:p-12 transition duration-300 shadow-xl group">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-9 h-9 rounded-xl bg-indigo-500 text-white font-black font-mono text-base flex items-center justify-center shadow-lg shadow-indigo-500/20">
                                02
                            </span>
                            <span class="text-xs font-mono font-bold uppercase tracking-widest text-indigo-400">PHASE 2: DECOUPLE & ELIMINATE 30+ PLUGINS</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">
                            We Strip Bloated CMS Stacks Down to 140KB of Pure Compiled Code
                        </h3>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            WordPress and Shopify stores carry an average of 25–40 plugins just to display a booking form or gallery. We discard this fragile layer and re-architect your business logic into lightweight, compiled <strong>Laravel 11 Blade templates</strong> and minimal Alpine.js reactivity.
                        </p>
                        <div class="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-400 pt-2">
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ 96% Payload Reduction</span>
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ Zero Vulnerable Plugins</span>
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ Pure Tailwind CSS</span>
                        </div>
                    </div>

                    <!-- Step Deliverable Card -->
                    <div class="bg-slate-950/80 border border-indigo-500/30 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3 text-xs font-mono">
                        <div class="text-indigo-400 font-bold uppercase">Before vs. After Payload:</div>
                        <div class="text-rose-400">Before: 5.8MB (34 Scripts)</div>
                        <div class="text-emerald-400 font-bold text-sm">After: 140KB (0 Bloat)</div>
                        <p class="text-slate-400 leading-relaxed pt-1">
                            Your server uses 90% less CPU and handles 10x higher concurrent user traffic with zero crashes.
                        </p>
                    </div>
                </div>
            </div>

            <!-- STEP 3 -->
            <div class="bg-gradient-to-r from-slate-900/90 to-slate-950 border border-white/10 hover:border-teal-500/40 rounded-3xl p-8 md:p-12 transition duration-300 shadow-xl group">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-9 h-9 rounded-xl bg-teal-400 text-slate-950 font-black font-mono text-base flex items-center justify-center shadow-lg shadow-teal-400/20">
                                03
                            </span>
                            <span class="text-xs font-mono font-bold uppercase tracking-widest text-teal-400">PHASE 3: IN-MEMORY RAM CACHING & WEBP PIPELINE</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">
                            We Serve Pages Directly from Server RAM in Under 120ms
                        </h3>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            We implement enterprise Redis in-memory page caching and automated AVIF/WebP image compression. Visitors receive fully rendered HTML pages before their browser even sends the second packet.
                        </p>
                        <div class="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-400 pt-2">
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ Redis RAM Response</span>
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ AVIF/WebP Automated Pipeline</span>
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ Edge Cloudflare Routing</span>
                        </div>
                    </div>

                    <!-- Step Deliverable Card -->
                    <div class="bg-slate-950/80 border border-teal-500/30 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3 text-xs font-mono">
                        <div class="text-teal-400 font-bold uppercase">Response Benchmark:</div>
                        <div class="text-3xl font-black text-emerald-400 font-mono">118ms TTFB</div>
                        <p class="text-slate-400 leading-relaxed">
                            Google rewards ultra-low Time-to-First-Byte with higher organic local rankings across search engines.
                        </p>
                    </div>
                </div>
            </div>

            <!-- STEP 4 -->
            <div class="bg-gradient-to-r from-slate-900/90 to-slate-950 border border-white/10 hover:border-amber-500/40 rounded-3xl p-8 md:p-12 transition duration-300 shadow-xl group">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-9 h-9 rounded-xl bg-amber-400 text-slate-950 font-black font-mono text-base flex items-center justify-center shadow-lg shadow-amber-400/20">
                                04
                            </span>
                            <span class="text-xs font-mono font-bold uppercase tracking-widest text-amber-400">PHASE 4: FRICTIONLESS 1-TAP CONVERSION UX</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">
                            We Turn Mobile Browsers into Immediate Inbound Inquiries
                        </h3>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            Speed alone isn't enough without conversion science. We eliminate layout shifts (0.00 CLS), re-engineer navigation for single-thumb mobile browsing, and embed high-converting deep links directly into WhatsApp click-to-chat prompts.
                        </p>
                        <div class="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-400 pt-2">
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ 1-Tap WhatsApp Lead Capture</span>
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ 0.00 Cumulative Layout Shift</span>
                            <span class="px-3 py-1 rounded-lg bg-slate-950 border border-white/10">✓ Frictionless Checkout Flow</span>
                        </div>
                    </div>

                    <!-- Step Deliverable Card -->
                    <div class="bg-slate-950/80 border border-amber-500/30 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3 text-xs font-mono">
                        <div class="text-amber-400 font-bold uppercase">Conversion Metric Lift:</div>
                        <div class="text-3xl font-black text-amber-300 font-mono">+52% Inquiries</div>
                        <p class="text-slate-400 leading-relaxed">
                            Fewer steps between interest and inquiry means direct revenue expansion without increasing ad spend.
                        </p>
                    </div>
                </div>
            </div>

            <!-- STEP 5 -->
            <div class="bg-gradient-to-r from-emerald-950/40 via-slate-900 to-teal-950/30 border-2 border-emerald-500/50 rounded-3xl p-8 md:p-12 transition duration-300 shadow-2xl relative overflow-hidden">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-9 h-9 rounded-xl bg-emerald-400 text-slate-950 font-black font-mono text-base flex items-center justify-center shadow-lg shadow-emerald-400/30">
                                05
                            </span>
                            <span class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-300">PHASE 5: THE IRONCLAD 100/100 GUARANTEE</span>
                        </div>
                        <h2 class="text-2xl sm:text-3xl md:text-4xl font-black text-white">
                            100/100 Core Web Vitals Pass or You Don't Pay. Period.
                        </h2>
                        <p class="text-slate-200 text-sm sm:text-base leading-relaxed">
                            We back every custom Laravel rebuild with an ironclad contractual performance guarantee. If your rebuilt website does not score in the green tier (95–100/100) on Google PageSpeed Insights under real-world mobile throttling, we refund 100% of your investment.
                        </p>
                        <div class="flex items-center space-x-3 text-xs font-mono text-emerald-400 pt-2 font-bold">
                            <span>🛡️ Zero Financial Risk</span>
                            <span>•</span>
                            <span>📋 Signed Performance SLA</span>
                            <span>•</span>
                            <span>🤝 Lead Architect Accountability</span>
                        </div>
                    </div>

                    <!-- Step Deliverable Card -->
                    <div class="bg-slate-950 border border-emerald-500/50 rounded-2xl p-6 lg:w-80 shrink-0 space-y-4 text-center">
                        <div class="text-5xl font-black text-emerald-400 font-mono">100<span class="text-lg text-slate-500">/100</span></div>
                        <div class="text-xs font-mono text-white font-bold uppercase">Google PageSpeed Verified</div>
                        <a 
                            href="https://wa.me/15551234567?text={{ urlencode('Hey Ravi! I saw your 100/100 guarantee. I want to discuss rebuilding my website.') }}" 
                            target="_blank"
                            class="block w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider py-3.5 rounded-xl shadow-lg transition"
                        >
                            Claim Your Guarantee ➔
                        </a>
                    </div>
                </div>
            </div>

        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 3. INTERACTIVE REVENUE RECOVERY CALCULATOR (ALPINE.JS)         -->
    <!-- ============================================================== -->
    <section id="calculator" class="max-w-5xl mx-auto px-6" x-data="{
        visitors: 8000,
        ticket: 120,
        get currentLoss() {
            // Formula: ~7% drop per second above 2s latency. Avg 5.5s mobile = ~24% loss of potential purchasers (assuming 2.5% baseline)
            let baseBuyers = (this.visitors * 0.025);
            let lostBuyers = baseBuyers * 0.28;
            return Math.round(lostBuyers * this.ticket);
        },
        get annualRecovered() {
            return this.currentLoss * 12;
        }
    }">
        <div class="bg-gradient-to-br from-slate-900 via-slate-900/90 to-emerald-950/40 border border-emerald-500/30 rounded-3xl p-8 sm:p-14 shadow-2xl space-y-10">
            <div class="text-center max-w-2xl mx-auto space-y-3">
                <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">INTERACTIVE ROI CALCULATOR</span>
                <h3 class="text-3xl sm:text-4xl font-black text-white">How Much Revenue Are You Leaking to Slow Speed?</h3>
                <p class="text-slate-400 text-sm">
                    Drag the sliders below to estimate how much revenue your current mobile latency loses every single month:
                </p>
            </div>

            <!-- Sliders Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Slider 1: Monthly Visitors -->
                <div class="bg-slate-950/70 border border-white/10 rounded-2xl p-6 space-y-4">
                    <div class="flex items-center justify-between text-sm">
                        <span class="font-bold text-white">Monthly Website Visitors</span>
                        <span class="font-mono text-emerald-400 font-bold text-base" x-text="Number(visitors).toLocaleString() + ' visits'"></span>
                    </div>
                    <input 
                        type="range" 
                        min="1000" 
                        max="50000" 
                        step="500" 
                        x-model="visitors"
                        class="w-full accent-emerald-500 cursor-pointer"
                    >
                    <div class="flex justify-between text-[11px] font-mono text-slate-500">
                        <span>1,000 / mo</span>
                        <span>25,000 / mo</span>
                        <span>50,000 / mo</span>
                    </div>
                </div>

                <!-- Slider 2: Average Order Value / Lead Value -->
                <div class="bg-slate-950/70 border border-white/10 rounded-2xl p-6 space-y-4">
                    <div class="flex items-center justify-between text-sm">
                        <span class="font-bold text-white">Avg. Order Value / Client Ticket</span>
                        <span class="font-mono text-emerald-400 font-bold text-base" x-text="'$' + ticket"></span>
                    </div>
                    <input 
                        type="range" 
                        min="20" 
                        max="1000" 
                        step="20" 
                        x-model="ticket"
                        class="w-full accent-emerald-500 cursor-pointer"
                    >
                    <div class="flex justify-between text-[11px] font-mono text-slate-500">
                        <span>$20</span>
                        <span>$500</span>
                        <span>$1,000+</span>
                    </div>
                </div>
            </div>

            <!-- Dynamic Output Results Bar -->
            <div class="bg-black/60 border border-white/10 rounded-2xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
                <div class="space-y-1">
                    <div class="text-xs font-mono text-slate-500 uppercase">Estimated Monthly Leak (5.5s Delay)</div>
                    <div class="text-3xl sm:text-4xl font-black text-rose-500 font-mono" x-text="'$' + Number(currentLoss).toLocaleString() + ' / month'"></div>
                </div>

                <div class="space-y-1 border-t md:border-t-0 md:border-l border-white/10 pt-4 md:pt-0 md:pl-8">
                    <div class="text-xs font-mono text-emerald-400 uppercase font-bold">Annual Revenue Recovered with Laravel 11</div>
                    <div class="text-3xl sm:text-4xl font-black text-emerald-400 font-mono" x-text="'+$' + Number(annualRecovered).toLocaleString() + ' / year'"></div>
                </div>

                <a 
                    :href="'https://wa.me/15551234567?text=' + encodeURIComponent('Hey Ravi! My website gets ~' + Number(visitors).toLocaleString() + ' visits with $' + ticket + ' ticket. I want to recover the estimated $' + Number(currentLoss).toLocaleString() + '/mo leak with a Laravel rebuild.')"
                    target="_blank" 
                    rel="noopener"
                    class="w-full md:w-auto shrink-0 bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-4 rounded-xl shadow-xl shadow-emerald-500/20 hover:scale-105 transition duration-300 text-center"
                >
                    Recover This Revenue on WhatsApp ➔
                </a>
            </div>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 4. CORE SERVICES MATRIX                                        -->
    <!-- ============================================================== -->
    <section id="services" class="max-w-7xl mx-auto px-6">
        <div class="text-center max-w-3xl mx-auto space-y-4 mb-16">
            <span class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">WHAT WE BUILD</span>
            <h2 class="text-4xl md:text-5xl font-black text-white tracking-tight">
                Boutique Web Engineering Services
            </h2>
            <p class="text-slate-400 text-base">
                Engineered from clean source code with zero vulnerable third-party plugins.
            </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Service 1 -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-8 space-y-5 transition duration-300 shadow-xl group">
                <div class="w-14 h-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-2xl group-hover:scale-110 transition">
                    🛍️
                </div>
                <h3 class="text-2xl font-extrabold text-white">High-Speed Headless E-Commerce</h3>
                <p class="text-slate-400 text-sm leading-relaxed">
                    Custom Laravel storefronts delivering sub-350ms checkout flows. Zero 2% platform transaction penalties, unlimited product variations, and bespoke measurement pipelines.
                </p>
                <ul class="space-y-2 text-xs text-slate-300 font-mono pt-2">
                    <li class="flex items-center space-x-2 text-emerald-400"><span>✓</span> <span>0% Platform Sales Tax</span></li>
                    <li class="flex items-center space-x-2 text-emerald-400"><span>✓</span> <span>1-Tap Instant Checkout Flow</span></li>
                    <li class="flex items-center space-x-2 text-emerald-400"><span>✓</span> <span>Sub-second product filtering</span></li>
                </ul>
            </div>

            <!-- Service 2 -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-cyan-500/40 rounded-3xl p-8 space-y-5 transition duration-300 shadow-xl group">
                <div class="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-bold text-2xl group-hover:scale-110 transition">
                    📱
                </div>
                <h3 class="text-2xl font-extrabold text-white">Automated Management Portals</h3>
                <p class="text-slate-400 text-sm leading-relaxed">
                    Internal business dashboards that automate table reservations, villa bookings, and client inquiries via direct WhatsApp Cloud API webhooks with zero monthly SaaS subscriptions.
                </p>
                <ul class="space-y-2 text-xs text-slate-300 font-mono pt-2">
                    <li class="flex items-center space-x-2 text-cyan-400"><span>✓</span> <span>Automated WhatsApp Alerts</span></li>
                    <li class="flex items-center space-x-2 text-cyan-400"><span>✓</span> <span>Multi-calendar iCal sync</span></li>
                    <li class="flex items-center space-x-2 text-cyan-400"><span>✓</span> <span>Direct Client CRM Portal</span></li>
                </ul>
            </div>

            <!-- Service 3 -->
            <div class="bg-slate-900/60 border border-white/10 hover:border-indigo-500/40 rounded-3xl p-8 space-y-5 transition duration-300 shadow-xl group">
                <div class="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 font-bold text-2xl group-hover:scale-110 transition">
                    ⚡
                </div>
                <h3 class="text-2xl font-extrabold text-white">Legacy Re-Architecture & Speed</h3>
                <p class="text-slate-400 text-sm leading-relaxed">
                    Migrate bloated WordPress, WooCommerce, and Shopify stores to lightweight Laravel 11 with Tailwind CSS. Slash page weights from 6MB to under 180KB and secure a 100/100 PageSpeed score.
                </p>
                <ul class="space-y-2 text-xs text-slate-300 font-mono pt-2">
                    <li class="flex items-center space-x-2 text-indigo-400"><span>✓</span> <span>100/100 Google PageSpeed Guarantee</span></li>
                    <li class="flex items-center space-x-2 text-indigo-400"><span>✓</span> <span>Zero Layout Shift (0.00 CLS)</span></li>
                    <li class="flex items-center space-x-2 text-indigo-400"><span>✓</span> <span>Sub-350ms TTFB on Mobile 4G</span></li>
                </ul>
            </div>
        </div>
    </section>

    <!-- ============================================================== -->
    <!-- 5. RECENT FIELD CASE STUDIES                                   -->
    <!-- ============================================================== -->
    <section class="max-w-7xl mx-auto px-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-12 gap-4">
            <div class="space-y-2">
                <span class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">REAL DATA & BENCHMARKS</span>
                <h2 class="text-3xl sm:text-4xl font-black text-white">Recent Engineering Case Studies</h2>
            </div>
            <a href="/blog" class="text-emerald-400 hover:text-emerald-300 font-bold text-sm flex items-center space-x-1">
                <span>View All Teardowns</span>
                <span>➔</span>
            </a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            @if(!empty($recentArticles))
            @foreach($recentArticles as $article)
            <article class="bg-slate-900/80 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-6 flex flex-col justify-between group transition duration-300 shadow-xl hover:-translate-y-1">
                <div class="space-y-3">
                    <div class="flex items-center justify-between text-xs font-mono">
                        <span class="bg-emerald-500/10 text-emerald-400 px-2.5 py-0.5 rounded font-bold border border-emerald-500/20">
                            📍 {{ $article['city'] ?? 'Local' }}
                        </span>
                        <span class="text-slate-500">{{ $article['read_time'] ?? '7 min' }}</span>
                    </div>
                    <h3 class="text-lg font-bold text-white group-hover:text-emerald-300 transition">
                        <a href="/blog/{{ $article['slug'] }}">{{ $article['title'] }}</a>
                    </h3>
                    <p class="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                        {{ $article['description'] }}
                    </p>
                </div>
                <div class="pt-4 mt-6 border-t border-white/10 flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-500">{{ $article['date'] ?? date('Y-m-d') }}</span>
                    <a href="/blog/{{ $article['slug'] }}" class="text-emerald-400 font-bold hover:translate-x-1 transition flex items-center space-x-1">
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
    <!-- 6. LEAD ARCHITECT DOSSIER & FINAL DIRECT CTA                    -->
    <!-- ============================================================== -->
    <section id="architect" class="max-w-5xl mx-auto px-6">
        <div class="bg-gradient-to-br from-slate-900 via-slate-900/90 to-emerald-950/40 border border-emerald-500/40 rounded-3xl p-8 sm:p-14 shadow-2xl relative overflow-hidden">
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
                    <h2 class="text-3xl sm:text-4xl font-black text-white">Crafted Personally by Ravi</h2>
                    <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                        "At ExtrovertNerd, we do not pass your business to junior freelancers or configure slow pre-made WordPress themes. Every web application is architected directly in clean, verified Laravel 11 code with strict Core Web Vitals guarantees."
                    </p>
                    <div class="pt-2 flex flex-wrap items-center justify-center md:justify-start gap-4">
                        <a 
                            href="{{ $whatsappUrl }}" 
                            target="_blank" 
                            rel="noopener" 
                            class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase px-7 py-4 rounded-xl shadow-xl shadow-emerald-500/25 transition flex items-center space-x-2"
                        >
                            <span>💬</span>
                            <span>Chat Personally with Ravi on WhatsApp</span>
                        </a>
                        <a 
                            href="/speed-checker" 
                            class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs px-6 py-4 rounded-xl border border-white/10 transition"
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
