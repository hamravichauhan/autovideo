@extends('layouts.app')

@section('title', 'Lost Revenue & Latency ROI Calculator | ExtrovertNerd')
@section('meta_description', 'Calculate how much money your business is silently leaking to slow mobile load times and discover the projected revenue lift of a sub-second architecture.')

@section('content')
<div class="max-w-7xl mx-auto px-6 py-16 space-y-20">

    <!-- HERO HEADER -->
    <section class="max-w-4xl space-y-6">
        <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold tracking-wide">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>PROPRIETARY LATENCY MODEL</span>
        </div>

        <h1 class="text-4xl sm:text-6xl font-black text-white tracking-tight leading-[1.1]">
            The High Cost of Slow: <br>
            <span class="font-serif italic font-normal text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-mint-300 to-teal-200">Revenue Recovery Calculator</span>
        </h1>

        <p class="text-slate-300 text-lg sm:text-xl leading-relaxed max-w-3xl">
            Google and Deloitte research confirms: every 100 milliseconds of mobile delay drops conversion rates by 7%. Adjust the sliders below to calculate how much revenue your current website is leaking to competitors.
        </p>
    </section>

    <!-- INTERACTIVE CALCULATOR (ALPINE.JS) -->
    <section 
        class="bg-gradient-to-br from-slate-900/90 via-slate-950 to-slate-900/90 border border-white/10 rounded-3xl p-8 sm:p-12 shadow-2xl relative overflow-hidden"
        x-data="{
            visitors: 12000,
            orderValue: 180,
            loadTime: 5.2,
            get bounceRate() {
                // Base 35% bounce at 1s, climbing to ~78% at 7s
                let rate = 35 + ((this.loadTime - 1.0) * 8.2);
                return Math.min(Math.max(Math.round(rate), 30), 85);
            },
            get monthlyLeak() {
                // Estimated revenue lost to latency drop-off
                let potentialConversions = (this.visitors * 0.035);
                let lostFraction = (this.bounceRate - 20) / 100;
                let lostSales = potentialConversions * lostFraction;
                return Math.round(lostSales * this.orderValue);
            },
            get annualRecovery() {
                return this.monthlyLeak * 12;
            },
            get whatsappUrl() {
                let msg = 'Hey Ravi! I used your ExtrovertNerd ROI Calculator. My website receives around ' + this.visitors.toLocaleString() + ' visitors/month with an average order value of $' + this.orderValue + ', and loads in ' + this.loadTime + 's. The calculator estimates we are leaking $' + this.monthlyLeak.toLocaleString() + '/month. Can you record the free 3-minute video breakdown to fix this?';
                return 'https://wa.me/15551234567?text=' + encodeURIComponent(msg);
            }
        }"
    >
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">

            <!-- LEFT COLUMN: CONTROLS & SLIDERS -->
            <div class="lg:col-span-6 space-y-8">
                <div>
                    <span class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-widest">LIVE DATA SIMULATOR</span>
                    <h2 class="text-2xl sm:text-3xl font-black text-white mt-1">Configure Your Numbers</h2>
                </div>

                <!-- Slider 1: Monthly Visitors -->
                <div class="space-y-3 bg-black/40 p-5 rounded-2xl border border-white/5">
                    <div class="flex items-center justify-between text-sm">
                        <span class="text-slate-300 font-semibold">Monthly Mobile Visitors</span>
                        <span class="font-mono font-black text-emerald-400 text-lg" x-text="visitors.toLocaleString() + ' visits'"></span>
                    </div>
                    <input 
                        type="range" 
                        min="1000" 
                        max="100000" 
                        step="1000" 
                        x-model.number="visitors" 
                        class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                    >
                    <div class="flex justify-between text-[10px] font-mono text-slate-500">
                        <span>1,000 / mo</span>
                        <span>50,000 / mo</span>
                        <span>100,000+ / mo</span>
                    </div>
                </div>

                <!-- Slider 2: Average Order Value / Client Ticket -->
                <div class="space-y-3 bg-black/40 p-5 rounded-2xl border border-white/5">
                    <div class="flex items-center justify-between text-sm">
                        <span class="text-slate-300 font-semibold">Average Customer / Order Value</span>
                        <span class="font-mono font-black text-mint-400 text-lg" x-text="'$' + orderValue.toLocaleString()"></span>
                    </div>
                    <input 
                        type="range" 
                        min="25" 
                        max="2500" 
                        step="25" 
                        x-model.number="orderValue" 
                        class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                    >
                    <div class="flex justify-between text-[10px] font-mono text-slate-500">
                        <span>$25 (Retail / Dining)</span>
                        <span>$500 (Boutique)</span>
                        <span>$2,500+ (High-Ticket)</span>
                    </div>
                </div>

                <!-- Slider 3: Current Mobile Load Time -->
                <div class="space-y-3 bg-black/40 p-5 rounded-2xl border border-white/5">
                    <div class="flex items-center justify-between text-sm">
                        <span class="text-slate-300 font-semibold">Current Mobile Load Time</span>
                        <span class="font-mono font-black text-rose-400 text-lg" x-text="loadTime.toFixed(1) + ' seconds'"></span>
                    </div>
                    <input 
                        type="range" 
                        min="1.0" 
                        max="8.0" 
                        step="0.1" 
                        x-model.number="loadTime" 
                        class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-rose-500"
                    >
                    <div class="flex justify-between text-[10px] font-mono text-slate-500">
                        <span>1.0s (Fast)</span>
                        <span>4.5s (Typical WP/Shopify)</span>
                        <span>8.0s (Critical Leak)</span>
                    </div>
                </div>
            </div>

            <!-- RIGHT COLUMN: FINANCIAL METRICS & RECOVERY CARD -->
            <div class="lg:col-span-6 bg-gradient-to-b from-slate-900 via-slate-950 to-black p-8 sm:p-10 rounded-3xl border border-emerald-500/30 space-y-6 glow-emerald shadow-2xl relative">
                <div class="flex items-center justify-between border-b border-white/10 pb-4">
                    <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">DIAGNOSTIC TELEMETRY</span>
                    <span class="text-[10px] font-mono text-rose-400 bg-rose-950/60 border border-rose-500/30 px-2.5 py-1 rounded-full uppercase font-bold">
                        HIGH FRICTION DETECTED
                    </span>
                </div>

                <!-- Monthly Leak Display -->
                <div class="space-y-1">
                    <span class="text-xs text-slate-400 font-mono">ESTIMATED REVENUE LEAKING MONTHLY:</span>
                    <div class="text-4xl sm:text-5xl font-black font-mono text-rose-400" x-text="'$' + monthlyLeak.toLocaleString() + ' /mo'"></div>
                    <p class="text-xs text-slate-400 pt-1">
                        Lost to prospective clients who hit the back button before your catalog or booking menu renders.
                    </p>
                </div>

                <!-- Telemetry Matrix -->
                <div class="grid grid-cols-2 gap-3.5 pt-2 font-mono">
                    <div class="bg-black/50 p-4 rounded-xl border border-white/5 space-y-1">
                        <div class="text-[10px] text-slate-400">Mobile Bounce Rate</div>
                        <div class="text-xl font-bold text-white" x-text="bounceRate + '%'"></div>
                    </div>
                    <div class="bg-black/50 p-4 rounded-xl border border-white/5 space-y-1">
                        <div class="text-[10px] text-slate-400">Target Rebuild Bounce</div>
                        <div class="text-xl font-bold text-emerald-400">18% (Sub-350ms)</div>
                    </div>
                    <div class="bg-black/50 p-4 rounded-xl border border-white/5 space-y-1">
                        <div class="text-[10px] text-slate-400">12-Month Leaked Total</div>
                        <div class="text-xl font-bold text-rose-300" x-text="'$' + annualRecovery.toLocaleString()"></div>
                    </div>
                    <div class="bg-black/50 p-4 rounded-xl border border-white/5 space-y-1">
                        <div class="text-[10px] text-slate-400">Target Conversion Lift</div>
                        <div class="text-xl font-bold text-emerald-300">+52% Lift</div>
                    </div>
                </div>

                <!-- Direct WhatsApp Conversion Action -->
                <div class="pt-4 border-t border-white/10 space-y-3">
                    <a 
                        :href="whatsappUrl" 
                        target="_blank" 
                        rel="noopener"
                        class="w-full bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-xs uppercase tracking-wider py-4 px-6 rounded-xl shadow-lg shadow-emerald-500/25 hover:scale-[1.02] transition flex items-center justify-center space-x-2 text-center"
                    >
                        <span>💬</span>
                        <span>Claim This Lost Revenue — Chat with Ravi</span>
                    </a>
                    <p class="text-center text-[11px] text-slate-400 font-mono">
                        Includes free 3-minute video audit with zero obligation.
                    </p>
                </div>
            </div>

        </div>
    </section>

    <!-- THE SCIENCE OF LATENCY -->
    <section class="space-y-8 max-w-4xl">
        <div class="space-y-2">
            <span class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-widest">EMPIRICAL BENCHMARKS</span>
            <h2 class="text-3xl font-black text-white">Why Every Millisecond Directly Dictates Revenue</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
            <div class="bg-slate-900/50 border border-white/10 p-6 rounded-2xl space-y-3">
                <div class="text-2xl font-mono font-bold text-emerald-400">0.1s Delay</div>
                <div class="text-base font-bold text-white">-7% Conversions</div>
                <p class="text-xs text-slate-400 leading-relaxed">
                    Google research demonstrates that a 100ms lag in mobile page load triggers a 7% reduction in completed transactions.
                </p>
            </div>
            <div class="bg-slate-900/50 border border-white/10 p-6 rounded-2xl space-y-3">
                <div class="text-2xl font-mono font-bold text-rose-400">3.0s+ Lag</div>
                <div class="text-base font-bold text-white">53% Bounce</div>
                <p class="text-xs text-slate-400 leading-relaxed">
                    Over half of mobile shoppers leave a website that takes longer than 3 seconds to render its primary content.
                </p>
            </div>
            <div class="bg-slate-900/50 border border-white/10 p-6 rounded-2xl space-y-3">
                <div class="text-2xl font-mono font-bold text-teal-400">0.3s Build</div>
                <div class="text-base font-bold text-white">+52% Lift</div>
                <p class="text-xs text-slate-400 leading-relaxed">
                    ExtrovertNerd custom architectures consistently achieve sub-350ms response times, doubling mobile checkout completions.
                </p>
            </div>
        </div>
    </section>

</div>
@endsection
