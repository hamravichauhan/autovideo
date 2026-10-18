@extends('layouts.app')

@section('title', 'How We Work — The 5-Step Engineering Blueprint | ExtrovertNerd')
@section('meta_description', 'Discover how ExtrovertNerd transforms slow, bloated websites into sub-second revenue machines using our proprietary 5-phase engineering blueprint and rigorous Core Web Vitals optimization.')

@section('content')
<div class="max-w-7xl mx-auto px-6 py-16 space-y-24">

    <!-- HERO SECTION -->
    <section class="max-w-4xl space-y-6">
        <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold tracking-wide">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>THE ENGINEERING PHILOSOPHY & BLUEPRINT</span>
        </div>

        <h1 class="text-4xl sm:text-6xl font-black text-white tracking-tight leading-[1.1]">
            How We Make Your Website <br>
            <span class="font-serif italic font-normal text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-mint-300 to-teal-200">100/100 Good</span>
        </h1>

        <p class="text-slate-300 text-lg sm:text-xl leading-relaxed max-w-3xl">
            We do not install off-the-shelf templates or stack 30 fragile plugins. We approach web development as precision software engineering—auditing bottlenecks, eliminating bloat, and deploying tailored architectures that load in under 350ms on mobile 4G.
        </p>

        <div class="flex flex-wrap items-center gap-4 pt-4">
            <a 
                href="{{ $whatsappUrl }}" 
                target="_blank" 
                rel="noopener" 
                class="bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-4 rounded-xl shadow-xl shadow-emerald-500/25 hover:scale-105 transition flex items-center space-x-2"
            >
                <span>💬</span>
                <span>Claim Phase 1 Free Video Audit</span>
            </a>
            <a 
                href="/speed-checker" 
                class="bg-slate-900 hover:bg-slate-800 border border-white/10 hover:border-emerald-500/40 text-white font-bold text-xs uppercase tracking-wider px-6 py-4 rounded-xl transition flex items-center space-x-2"
            >
                <span>⚡ Test Your Current Score</span>
            </a>
        </div>
    </section>

    <!-- THE 5 PHASES DEEP DIVE -->
    <section class="space-y-16">
        <div class="border-b border-white/10 pb-6">
            <span class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-widest">THE 5-PHASE EXECUTION ROADMAP</span>
            <h2 class="text-3xl font-black text-white mt-2">From Sluggish Bottleneck to High-Speed Machine</h2>
        </div>

        <div class="space-y-12">

            <!-- PHASE 1 -->
            <div class="bg-slate-900/40 border border-slate-800/80 hover:border-emerald-500/30 rounded-3xl p-8 sm:p-12 transition duration-300 relative overflow-hidden group">
                <div class="absolute top-0 right-0 w-80 h-80 bg-emerald-500/5 blur-3xl pointer-events-none"></div>
                <div class="flex flex-col lg:flex-row gap-8 items-start justify-between">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center font-mono font-black text-emerald-400 text-lg">
                                01
                            </span>
                            <span class="text-xs font-mono uppercase tracking-widest text-emerald-400 font-bold">Phase 1: Diagnostic</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">Forensic Speed & Revenue Leak Audit</h3>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            Before writing a single line of code, ExtrovertNerd Engineering performs a forensic inspection of your website's network cascade using Chrome DevTools, WebPageTest, and Google Lighthouse. We isolate unminified JavaScript bundles, render-blocking stylesheets, and database queries locking your server.
                        </p>
                        <div class="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono text-slate-300">
                            <div class="flex items-center space-x-2 text-emerald-400">
                                <span>✓</span>
                                <span>LCP, INP & CLS Core Web Vitals breakdown</span>
                            </div>
                            <div class="flex items-center space-x-2 text-emerald-400">
                                <span>✓</span>
                                <span>Third-party tracking script footprint analysis</span>
                            </div>
                            <div class="flex items-center space-x-2 text-emerald-400">
                                <span>✓</span>
                                <span>Time-To-First-Byte (TTFB) server latency test</span>
                            </div>
                            <div class="flex items-center space-x-2 text-emerald-400">
                                <span>✓</span>
                                <span>Mobile 4G throttled customer checkout review</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-black/60 border border-white/10 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3">
                        <div class="text-[10px] font-mono uppercase text-slate-400 font-bold tracking-wider">PHASE DELIVERABLE</div>
                        <div class="text-base font-bold text-white">3-Minute Video Breakdown</div>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            A screen recording recorded by ExtrovertNerd Engineering explaining your bottlenecks and demonstrating the exact technical solution.
                        </p>
                        <div class="text-[10px] font-mono text-emerald-400 font-bold pt-2">TURNAROUND: 24 HOURS • 100% FREE</div>
                    </div>
                </div>
            </div>

            <!-- PHASE 2 -->
            <div class="bg-slate-900/40 border border-slate-800/80 hover:border-emerald-500/30 rounded-3xl p-8 sm:p-12 transition duration-300 relative overflow-hidden group">
                <div class="absolute top-0 right-0 w-80 h-80 bg-teal-500/5 blur-3xl pointer-events-none"></div>
                <div class="flex flex-col lg:flex-row gap-8 items-start justify-between">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center font-mono font-black text-teal-400 text-lg">
                                02
                            </span>
                            <span class="text-xs font-mono uppercase tracking-widest text-teal-400 font-bold">Phase 2: Decouple & Rebuild</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">Decouple from Bloated CMS to Custom Engine</h3>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            We eradicate 96% of legacy codebase weight. We don't force a rigid stack onto your project; we choose the exact technologies that fit your business model—whether that means a lightning-fast Laravel 11 monolith, a reactive Next.js 15 interface with React Server Components, a Node.js real-time service, or a Python FastAPI data engine.
                        </p>
                        <div class="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono text-slate-300">
                            <div class="flex items-center space-x-2 text-teal-400">
                                <span>✓</span>
                                <span>Zero unvetted third-party plugins</span>
                            </div>
                            <div class="flex items-center space-x-2 text-teal-400">
                                <span>✓</span>
                                <span>Tailwind CSS purge (under 14KB total CSS)</span>
                            </div>
                            <div class="flex items-center space-x-2 text-teal-400">
                                <span>✓</span>
                                <span>Clean relational schema design (MySQL / Postgres)</span>
                            </div>
                            <div class="flex items-center space-x-2 text-teal-400">
                                <span>✓</span>
                                <span>Eliminates all monthly Shopify/WP plugin fees</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-black/60 border border-white/10 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3">
                        <div class="text-[10px] font-mono uppercase text-slate-400 font-bold tracking-wider">PHASE DELIVERABLE</div>
                        <div class="text-base font-bold text-white">Tailored Bespoke Core</div>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Complete source code ownership. Zero recurring platform subscription costs, fully hosted on your private server or cloud edge.
                        </p>
                        <div class="text-[10px] font-mono text-teal-400 font-bold pt-2">WEIGHT REDUCTION: -96% PAYLOAD</div>
                    </div>
                </div>
            </div>

            <!-- PHASE 3 -->
            <div class="bg-slate-900/40 border border-slate-800/80 hover:border-emerald-500/30 rounded-3xl p-8 sm:p-12 transition duration-300 relative overflow-hidden group">
                <div class="absolute top-0 right-0 w-80 h-80 bg-emerald-500/5 blur-3xl pointer-events-none"></div>
                <div class="flex flex-col lg:flex-row gap-8 items-start justify-between">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center font-mono font-black text-emerald-400 text-lg">
                                03
                            </span>
                            <span class="text-xs font-mono uppercase tracking-widest text-emerald-400 font-bold">Phase 3: Performance Layer</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">In-Memory RAM Caching & WebP Pipeline</h3>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            Database queries are the silent killer of mobile speed during traffic spikes. We implement Redis in-memory key-value caching so recurring catalog data, inventory items, and dynamic pages render in under 30 milliseconds directly from RAM.
                        </p>
                        <div class="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono text-slate-300">
                            <div class="flex items-center space-x-2 text-emerald-400">
                                <span>✓</span>
                                <span>Redis full-page and model fragment caching</span>
                            </div>
                            <div class="flex items-center space-x-2 text-emerald-400">
                                <span>✓</span>
                                <span>Automated WebP/AVIF responsive image pipeline</span>
                            </div>
                            <div class="flex items-center space-x-2 text-emerald-400">
                                <span>✓</span>
                                <span>Zero layout shift (CLS = 0.00) strict aspect ratios</span>
                            </div>
                            <div class="flex items-center space-x-2 text-emerald-400">
                                <span>✓</span>
                                <span>OPcache and asynchronous job worker queues</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-black/60 border border-white/10 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3">
                        <div class="text-[10px] font-mono uppercase text-slate-400 font-bold tracking-wider">PHASE DELIVERABLE</div>
                        <div class="text-base font-bold text-white">Sub-120ms TTFB</div>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Server response time slashed from 2,400ms down to 120ms, making mobile browsing feel instantaneous like a native iOS app.
                        </p>
                        <div class="text-[10px] font-mono text-emerald-400 font-bold pt-2">CORE WEB VITALS: 100/100 GREEN</div>
                    </div>
                </div>
            </div>

            <!-- PHASE 4 -->
            <div class="bg-slate-900/40 border border-slate-800/80 hover:border-emerald-500/30 rounded-3xl p-8 sm:p-12 transition duration-300 relative overflow-hidden group">
                <div class="absolute top-0 right-0 w-80 h-80 bg-teal-500/5 blur-3xl pointer-events-none"></div>
                <div class="flex flex-col lg:flex-row gap-8 items-start justify-between">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center font-mono font-black text-teal-400 text-lg">
                                04
                            </span>
                            <span class="text-xs font-mono uppercase tracking-widest text-teal-400 font-bold">Phase 4: Conversion UX</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">Frictionless 1-Tap Conversion UX & Automations</h3>
                        <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
                            Fast websites that don't convert are worthless. We design custom mobile checkout workflows, 1-tap WhatsApp reservation deep links, and automated webhook alerts that instantly notify your team the moment a high-value prospect submits an inquiry.
                        </p>
                        <div class="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono text-slate-300">
                            <div class="flex items-center space-x-2 text-teal-400">
                                <span>✓</span>
                                <span>Direct WhatsApp Click-to-Chat pre-filled funnels</span>
                            </div>
                            <div class="flex items-center space-x-2 text-teal-400">
                                <span>✓</span>
                                <span>Real-time webhook routing to your CRM / Slack</span>
                            </div>
                            <div class="flex items-center space-x-2 text-teal-400">
                                <span>✓</span>
                                <span>Zero redirect payment gateways (Stripe / Razorpay)</span>
                            </div>
                            <div class="flex items-center space-x-2 text-teal-400">
                                <span>✓</span>
                                <span>Instant automated confirmation emails & SMS</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-black/60 border border-white/10 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3">
                        <div class="text-[10px] font-mono uppercase text-slate-400 font-bold tracking-wider">PHASE DELIVERABLE</div>
                        <div class="text-base font-bold text-white">Automated Lead Engine</div>
                        <p class="text-xs text-slate-400 leading-relaxed">
                            Zero manual copy-paste. High-value client inquiries trigger instant smartphone notifications and automated calendar reservations.
                        </p>
                        <div class="text-[10px] font-mono text-teal-400 font-bold pt-2">CONVERSION LIFT: +52% AVERAGE</div>
                    </div>
                </div>
            </div>

            <!-- PHASE 5 -->
            <div class="bg-gradient-to-br from-emerald-950/30 via-slate-900/60 to-slate-950 border border-emerald-500/40 rounded-3xl p-8 sm:p-12 transition duration-300 relative overflow-hidden group shadow-2xl">
                <div class="flex flex-col lg:flex-row gap-8 items-start justify-between">
                    <div class="space-y-4 max-w-2xl">
                        <div class="flex items-center space-x-3">
                            <span class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center font-mono font-black text-emerald-300 text-lg">
                                05
                            </span>
                            <span class="text-xs font-mono uppercase tracking-widest text-emerald-300 font-bold">Phase 5: Verification & Delivery</span>
                        </div>
                        <h3 class="text-2xl sm:text-3xl font-black text-white">Rigorous Real-World Core Web Vitals Verification</h3>
                        <p class="text-slate-200 text-sm sm:text-base leading-relaxed">
                            We don't make vague promises about "optimizing your site". We stress-test every build under simulated mobile 4G latency and packet loss. We ensure your production website passes Google Mobile Core Web Vitals with green scores across LCP, INP, and CLS before going live.
                        </p>
                        <div class="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono text-emerald-300">
                            <div class="flex items-center space-x-2">
                                <span>✓</span>
                                <span>Largest Contentful Paint &lt; 0.8s</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <span>✓</span>
                                <span>Interaction to Next Paint &lt; 50ms</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <span>✓</span>
                                <span>Cumulative Layout Shift = 0.00</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <span>✓</span>
                                <span>Throttled Real Mobile 4G Verification</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-emerald-950/60 border border-emerald-500/30 rounded-2xl p-6 lg:w-80 shrink-0 space-y-3">
                        <div class="text-[10px] font-mono uppercase text-emerald-400 font-bold tracking-wider">ENGINEERING INTEGRITY</div>
                        <div class="text-lg font-black text-white">Verified Benchmarks</div>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            "Every build is tested and verified on real mobile devices under throttled 4G conditions before production handover."
                        </p>
                        <div class="text-[10px] font-mono text-emerald-300 font-bold pt-2">EXTROVERTNERD ENGINEERING</div>
                    </div>
                </div>
            </div>

        </div>
    </section>

    <!-- COMPARISON MATRIX: TRADITIONAL AGENCY VS EXTROVERTNERD -->
    <section class="space-y-8">
        <div class="text-center max-w-2xl mx-auto space-y-2">
            <span class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-widest">HOW WE COMPARE</span>
            <h2 class="text-3xl font-black text-white">Why Founders Choose ExtrovertNerd</h2>
            <p class="text-slate-400 text-sm">
                Most agencies outsource work or install heavy drag-and-drop page builders. Here is the difference:
            </p>
        </div>

        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm border-collapse rounded-2xl overflow-hidden border border-white/10">
                <thead>
                    <tr class="bg-slate-900/90 text-xs font-mono uppercase tracking-wider text-slate-400 border-b border-white/10">
                        <th class="p-4 sm:p-5">Feature / Standard</th>
                        <th class="p-4 sm:p-5 text-rose-400">Traditional Agency (WordPress / Shopify)</th>
                        <th class="p-4 sm:p-5 text-emerald-400 bg-emerald-950/20">ExtrovertNerd Custom Engineering</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-white/5 font-mono text-xs">
                    <tr class="hover:bg-slate-900/40">
                        <td class="p-4 sm:p-5 font-bold text-white">Lead Engineer</td>
                        <td class="p-4 sm:p-5 text-slate-400">Junior offshore freelancer or account manager</td>
                        <td class="p-4 sm:p-5 text-emerald-300 font-bold bg-emerald-950/10">Engineered directly by ExtrovertNerd</td>
                    </tr>
                    <tr class="hover:bg-slate-900/40">
                        <td class="p-4 sm:p-5 font-bold text-white">Mobile Load Time</td>
                        <td class="p-4 sm:p-5 text-rose-300">4.5s – 8.0s (Fails Google Core Web Vitals)</td>
                        <td class="p-4 sm:p-5 text-emerald-300 font-bold bg-emerald-950/10">Sub-350ms (Passes 100/100 Vitals)</td>
                    </tr>
                    <tr class="hover:bg-slate-900/40">
                        <td class="p-4 sm:p-5 font-bold text-white">Third-Party Plugins</td>
                        <td class="p-4 sm:p-5 text-slate-400">25–40 plugins requiring constant updates</td>
                        <td class="p-4 sm:p-5 text-emerald-300 font-bold bg-emerald-950/10">Zero plugin bloat (Pure verified code)</td>
                    </tr>
                    <tr class="hover:bg-slate-900/40">
                        <td class="p-4 sm:p-5 font-bold text-white">Monthly Platform Fees</td>
                        <td class="p-4 sm:p-5 text-rose-300">$49 – $399/mo + 2% transaction fee cuts</td>
                        <td class="p-4 sm:p-5 text-emerald-300 font-bold bg-emerald-950/10">$0 Platform Tax (Self-Hosted on your server)</td>
                    </tr>
                    <tr class="hover:bg-slate-900/40">
                        <td class="p-4 sm:p-5 font-bold text-white">Tech Stack Flexibility</td>
                        <td class="p-4 sm:p-5 text-slate-400">Locked to whatever theme builder they sell</td>
                        <td class="p-4 sm:p-5 text-emerald-300 font-bold bg-emerald-950/10">100% tailored (Next.js, Laravel, Node, Python, Go)</td>
                    </tr>
                    <tr class="hover:bg-slate-900/40">
                        <td class="p-4 sm:p-5 font-bold text-white">Performance Standards</td>
                        <td class="p-4 sm:p-5 text-slate-400">None ("Page speed depends on your host")</td>
                        <td class="p-4 sm:p-5 text-emerald-300 font-bold bg-emerald-950/10">Strict Sub-Second Mobile Core Web Vitals Targets</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- CALL TO ACTION BANNER -->
    <section class="bg-gradient-to-r from-emerald-950/50 via-slate-900 to-teal-950/50 border border-emerald-500/30 rounded-3xl p-8 sm:p-14 text-center space-y-6 shadow-2xl">
        <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">GET STARTED TODAY</span>
        <h3 class="text-3xl sm:text-5xl font-black text-white">Ready for Phase 1 of Your Rebuild?</h3>
        <p class="text-slate-300 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
            Message ExtrovertNerd directly on WhatsApp. Within 24 hours, you'll receive a personalized 3-minute video teardown of your website's speed bottlenecks and exact roadmap.
        </p>
        <div class="pt-4 flex flex-wrap items-center justify-center gap-4">
            <a 
                href="{{ $whatsappUrl }}" 
                target="_blank" 
                rel="noopener" 
                class="bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-xs uppercase tracking-wider px-8 py-4 rounded-xl shadow-xl shadow-emerald-500/25 hover:scale-105 transition flex items-center space-x-2"
            >
                <span>💬</span>
                <span>Message ExtrovertNerd on WhatsApp</span>
            </a>
            <a 
                href="/speed-checker" 
                class="bg-slate-900 hover:bg-slate-800 border border-white/10 text-white font-bold text-xs uppercase tracking-wider px-8 py-4 rounded-xl transition"
            >
                Run Instant Speed Diagnostic ➔
            </a>
        </div>
    </section>

</div>
@endsection
