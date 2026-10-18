@extends('layouts.app')

@section('title', ($meta['title'] ?? 'Case Study') . ' | ExtrovertNerd')
@section('meta_description', $meta['description'] ?? 'Technical web performance case study by ExtrovertNerd.')

@section('content')
<div class="max-w-7xl mx-auto px-6 py-12">

    <!-- BREADCRUMBS -->
    <nav class="flex items-center space-x-2 text-xs font-mono text-slate-500 mb-8">
        <a href="/" class="hover:text-slate-300 transition">Home</a>
        <span>/</span>
        <a href="/blog" class="hover:text-slate-300 transition">Case Studies</a>
        <span>/</span>
        <span class="text-emerald-400 truncate">{{ $meta['city'] ?? 'Local' }} {{ $meta['niche'] ?? 'Audit' }}</span>
    </nav>

    <!-- 2-COLUMN ARTICLE LAYOUT -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">

        <!-- MAIN ARTICLE COLUMN (8 cols) -->
        <article class="lg:col-span-8 bg-slate-900/40 border border-white/10 rounded-3xl p-6 md:p-10 shadow-2xl">
            <!-- Article Header -->
            <div class="pb-8 border-b border-white/10 space-y-4">
                <div class="flex flex-wrap items-center gap-2.5 text-xs font-mono">
                    <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1 rounded-full font-bold">
                        📍 {{ $meta['city'] ?? 'Local Market' }}
                    </span>
                    <span class="bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-3 py-1 rounded-full font-semibold">
                        {{ $meta['category'] ?? 'Architecture' }}
                    </span>
                    <span class="text-slate-500">{{ $meta['read_time'] ?? '7 min read' }}</span>
                </div>

                <h1 class="text-3xl md:text-5xl font-black text-white tracking-tight leading-tight">
                    {{ $meta['title'] }}
                </h1>

                <div class="flex items-center space-x-3 text-xs text-slate-400 font-mono pt-2">
                    <span>Published: {{ $meta['date'] ?? date('Y-m-d') }}</span>
                    <span>•</span>
                    <span>Reviewed by Lead Architect: Ravi</span>
                </div>
            </div>

            <!-- Parsed Article Body (HTML from MarkdownService) -->
            <div class="prose prose-invert max-w-none pt-8">
                {!! $html !!}
            </div>

            <!-- In-Article WhatsApp CTA Box -->
            <div class="mt-12 bg-gradient-to-r from-emerald-950/60 via-slate-900 to-slate-950 border border-emerald-500/40 rounded-2xl p-6 md:p-8 space-y-4">
                <div class="flex items-center space-x-2 text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">
                    <span>⚡</span>
                    <span>Free Speed & Core Web Vitals Teardown</span>
                </div>
                <h3 class="text-2xl font-black text-white">Own a {{ $meta['niche'] ?? 'business' }} in {{ $meta['city'] ?? 'your city' }}?</h3>
                <p class="text-slate-300 text-sm leading-relaxed">
                    Stop letting 4+ second mobile load times kill your conversions. We will review your website live and record a 3-minute video breakdown of your bottlenecks.
                </p>
                <div class="pt-2">
                    <a href="{{ $whatsappUrl }}" target="_blank" rel="noopener" class="inline-flex items-center space-x-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-3.5 rounded-xl shadow-lg shadow-emerald-500/20 hover:scale-105 transition">
                        <span>📱</span>
                        <span>Claim Your Free Video Audit on WhatsApp ➔</span>
                    </a>
                </div>
            </div>
        </article>

        <!-- STICKY SIDEBAR (4 cols) -->
        <aside class="lg:col-span-4 space-y-8 sticky top-28">

            <!-- Lead Architect Dossier -->
            <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 space-y-4">
                <div class="flex items-center space-x-3.5 pb-4 border-b border-white/10">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-500 via-cyan-400 to-indigo-500 p-0.5 shadow-lg">
                        <div class="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center text-emerald-400 font-extrabold text-base font-mono">
                            R
                        </div>
                    </div>
                    <div>
                        <div class="text-sm font-extrabold text-white">Ravi</div>
                        <div class="text-xs text-emerald-400 font-medium">Lead Web Architect</div>
                        <div class="text-[11px] text-slate-500 font-mono">ExtrovertNerd Agency</div>
                    </div>
                </div>

                <p class="text-xs text-slate-400 leading-relaxed">
                    "We specialize in engineering sub-350ms custom Laravel web apps, automated booking dashboards, and high-converting e-commerce stores with 0% platform transaction taxes."
                </p>

                <div class="pt-2">
                    <a href="https://wa.me/15551234567" target="_blank" class="w-full block text-center bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs py-2.5 rounded-xl border border-white/10 transition">
                        Direct WhatsApp Chat
                    </a>
                </div>
            </div>

            <!-- Instant Speed Checker Banner -->
            <div class="bg-gradient-to-b from-indigo-950/40 to-slate-900 border border-indigo-500/30 rounded-3xl p-6 space-y-4">
                <div class="text-xs font-mono font-bold text-indigo-400 uppercase tracking-widest">Interactive Micro-Tool</div>
                <h4 class="text-lg font-black text-white">Test Your Own Website Now</h4>
                <p class="text-xs text-slate-400 leading-relaxed">
                    Simulate your real-world mobile 4G latency and compare it against ExtrovertNerd's verified 100/100 Core Web Vitals benchmark.
                </p>
                <a href="/speed-checker" class="block w-full text-center bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold text-xs uppercase tracking-wider py-3 rounded-xl shadow-lg transition">
                    Open Speed Checker ➔
                </a>
            </div>

            <!-- Quick Audit Checklist -->
            <div class="bg-slate-900/50 border border-white/10 rounded-3xl p-6 space-y-3 text-xs text-slate-400">
                <div class="font-bold text-white uppercase font-mono tracking-wider">Audit Standards</div>
                <div class="flex items-center space-x-2 text-emerald-400">
                    <span>✓</span>
                    <span class="text-slate-300">Target TTFB: Under 350ms</span>
                </div>
                <div class="flex items-center space-x-2 text-emerald-400">
                    <span>✓</span>
                    <span class="text-slate-300">Layout Shift (CLS): 0.00</span>
                </div>
                <div class="flex items-center space-x-2 text-emerald-400">
                    <span>✓</span>
                    <span class="text-slate-300">Platform Tax: 0% Direct</span>
                </div>
                <div class="flex items-center space-x-2 text-emerald-400">
                    <span>✓</span>
                    <span class="text-slate-300">Automated WhatsApp API</span>
                </div>
            </div>

        </aside>

    </div>

</div>
@endsection
