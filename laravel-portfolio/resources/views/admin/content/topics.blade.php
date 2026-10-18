@extends('layouts.admin')

@section('title', 'Topic Matrix Editor | ExtrovertNerd Admin')

@section('content')
<div class="space-y-6 max-w-6xl mx-auto">

    <div class="flex items-center justify-between pb-6 border-b border-white/10">
        <div>
            <a href="/admin/content" class="text-xs font-mono text-emerald-400 hover:underline flex items-center space-x-1 mb-2">
                <span>←</span>
                <span>Back to Article Manager</span>
            </a>
            <h1 class="text-3xl font-black text-white">Topic Matrix & Niche Matrix</h1>
            <p class="text-xs text-slate-400 font-mono mt-0.5">Direct configuration for content/blog_topics.json</p>
        </div>
    </div>

    <!-- CITIES & NICHES PILLS OVERVIEW -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <!-- Cities Box -->
        <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="text-base font-bold text-white flex items-center space-x-2">
                    <span>📍</span>
                    <span>Target Cities ({{ count($topics['cities'] ?? []) }})</span>
                </h3>
            </div>
            <div class="flex flex-wrap gap-2">
                @foreach($topics['cities'] ?? [] as $city)
                <span class="px-3 py-1.5 rounded-xl bg-slate-950 border border-white/10 text-xs font-mono text-slate-300">
                    {{ $city['name'] ?? 'City' }} <span class="text-slate-500">({{ $city['id'] ?? '' }})</span>
                </span>
                @endforeach
            </div>
        </div>

        <!-- Niches Box -->
        <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="text-base font-bold text-white flex items-center space-x-2">
                    <span>🏢</span>
                    <span>Target Niches ({{ count($topics['niches'] ?? []) }})</span>
                </h3>
            </div>
            <div class="flex flex-wrap gap-2">
                @foreach($topics['niches'] ?? [] as $niche)
                <span class="px-3 py-1.5 rounded-xl bg-slate-950 border border-white/10 text-xs font-mono text-slate-300">
                    {{ $niche['name'] ?? 'Niche' }}
                </span>
                @endforeach
            </div>
        </div>

    </div>

    <!-- RAW JSON MATRIX EDITOR -->
    <form action="/admin/content/topics/save" method="POST" class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 md:p-8 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between">
            <div>
                <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                    <span>⚙️</span>
                    <span>JSON Matrix Editor</span>
                </h3>
                <p class="text-xs text-slate-400 mt-0.5">Edit target parameters, pain points, and comparison technologies.</p>
            </div>
            <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-5 py-2.5 rounded-xl shadow-lg shadow-emerald-500/20 transition">
                Save Matrix JSON ➔
            </button>
        </div>

        <textarea 
            name="json_content" 
            rows="22" 
            class="w-full bg-slate-950 border border-white/10 rounded-2xl p-4 font-mono text-xs text-emerald-400 leading-relaxed focus:border-emerald-500/50 outline-none custom-scrollbar"
        >{{ $rawJson }}</textarea>
    </form>

</div>
@endsection
