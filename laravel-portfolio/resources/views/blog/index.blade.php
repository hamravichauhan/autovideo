@extends('layouts.app')

@section('title', 'Case Studies & Performance Teardowns | ExtrovertNerd')
@section('meta_description', 'Read in-depth technical case studies and forensic mobile speed teardowns for local businesses across Goa, Mumbai, Bangalore, Delhi NCR, and Dubai.')

@section('content')
<div class="max-w-7xl mx-auto px-6 py-14 space-y-12">

    <!-- HEADER -->
    <div class="max-w-3xl space-y-4">
        <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>FIELD AUDITS & REAL METRICS</span>
        </div>
        <h1 class="text-4xl md:text-5xl font-black text-white tracking-tight leading-tight">
            Case Studies & <span class="font-serif italic font-normal text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-mint-300 to-teal-200">Field Teardowns</span>
        </h1>
        <p class="text-slate-300 text-base md:text-lg leading-relaxed">
            Real performance benchmarks and architecture audits for local commercial hubs. See how replacing bloated legacy CMS templates with custom, sub-second architectures delivers 100/100 Core Web Vitals and surges conversion rates.
        </p>
    </div>

    <!-- CITY FILTER PILLS -->
    <div class="flex items-center space-x-2.5 overflow-x-auto py-4 border-b border-white/10 scrollbar-none">
        <a href="/case-studies" class="px-4 py-2 rounded-xl text-xs font-bold font-mono uppercase tracking-wider transition shrink-0 {{ empty($currentCity) ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20' : 'bg-slate-900 border border-white/10 text-slate-300 hover:text-white' }}">
            All Cities
        </a>
        @foreach($cities as $city)
        <a href="/case-studies?city={{ urlencode($city) }}" class="px-4 py-2 rounded-xl text-xs font-bold font-mono uppercase tracking-wider transition shrink-0 {{ ($currentCity && strtolower($currentCity) === strtolower($city)) ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20' : 'bg-slate-900 border border-white/10 text-slate-300 hover:text-white' }}">
            {{ $city }}
        </a>
        @endforeach
    </div>

    <!-- ARTICLES GRID -->
    @if(empty($articles))
    <div class="text-center py-20 bg-slate-900/40 rounded-3xl border border-white/10 mt-8 space-y-4">
        <div class="text-4xl">⚡</div>
        <h3 class="text-xl font-bold text-white">No Case Studies Found for this Filter</h3>
        <p class="text-slate-400 text-sm">Run our Python generator (`python -m src.generator_pseo`) to assemble fresh articles.</p>
        <a href="/case-studies" class="inline-block bg-emerald-500 text-slate-950 font-bold text-xs uppercase tracking-wider px-5 py-2.5 rounded-xl">View All Case Studies</a>
    </div>
    @else
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        @foreach($articles as $article)
        <article class="bg-gradient-to-b from-slate-900/70 to-slate-950 border border-white/10 hover:border-emerald-500/40 rounded-3xl p-7 flex flex-col justify-between group transition duration-300 shadow-xl hover:-translate-y-1">
            <div class="space-y-4">
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full font-bold">
                        📍 {{ $article['city'] }}
                    </span>
                    <span class="text-slate-400">{{ $article['read_time'] }}</span>
                </div>

                <h2 class="text-xl font-extrabold text-white group-hover:text-emerald-300 transition leading-snug">
                    <a href="/case-studies/{{ $article['slug'] }}">{{ $article['title'] }}</a>
                </h2>

                <p class="text-slate-400 text-sm leading-relaxed line-clamp-3">
                    {{ $article['description'] }}
                </p>
            </div>

            <div class="pt-6 mt-6 border-t border-white/10 flex items-center justify-between text-xs font-mono">
                <span class="text-slate-500">{{ $article['date'] }}</span>
                <a href="/case-studies/{{ $article['slug'] }}" class="text-emerald-400 font-bold flex items-center space-x-1 hover:translate-x-1 transition">
                    <span>Read Teardown</span>
                    <span>➔</span>
                </a>
            </div>
        </article>
        @endforeach
    </div>
    @endif

    <!-- BOTTOM FUNNEL CTA -->
    <div class="mt-20 bg-gradient-to-r from-emerald-950/40 via-slate-900 to-teal-950/40 border border-emerald-500/30 rounded-3xl p-8 md:p-12 text-center space-y-6">
        <h3 class="text-3xl font-black text-white">Want Your Business Tested in Our Lab?</h3>
        <p class="text-slate-300 text-base max-w-xl mx-auto">
            Run your URL through our free speed checker or chat directly with ExtrovertNerd for a complimentary 5-point teardown.
        </p>
        <div class="flex flex-wrap items-center justify-center gap-4">
            <a href="/speed-checker" class="bg-gradient-to-r from-emerald-500 to-teal-400 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-3.5 rounded-xl shadow-lg shadow-emerald-500/20 hover:scale-105 transition">
                Launch Speed Checker ➔
            </a>
            <a 
                href="https://wa.me/15551234567?text={{ urlencode('Hey ExtrovertNerd! I read your case studies on ExtrovertNerd and want a free speed audit of my business.') }}" 
                target="_blank" 
                rel="noopener" 
                class="bg-slate-900 hover:bg-slate-800 text-white border border-white/10 font-bold text-xs uppercase tracking-wider px-6 py-3.5 rounded-xl transition"
            >
                Message ExtrovertNerd on WhatsApp
            </a>
        </div>
    </div>

</div>
@endsection
