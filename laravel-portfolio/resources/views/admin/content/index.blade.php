@extends('layouts.admin')

@section('title', 'Content & pSEO Command Center | ExtrovertNerd Admin')

@section('content')
<div class="space-y-6 max-w-7xl mx-auto">

    <!-- HEADER & ACTIONS -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
            <div class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-wider mb-1">
                AUTOMATED INBOUND ASSETS
            </div>
            <h1 class="text-3xl font-black text-white tracking-tight">
                Programmatic SEO & <span class="font-serif italic font-normal text-emerald-400">Case Study Matrix</span>
            </h1>
            <p class="text-slate-400 text-sm mt-1">
                Manage, edit, and expand 1,500+ word engineering teardowns targeting local business search intents.
            </p>
        </div>

        <div class="flex items-center space-x-3">
            <a href="/admin/content/topics" class="bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs uppercase tracking-wider px-4 py-2.5 rounded-xl border border-white/10 transition flex items-center space-x-2">
                <span>🗺️</span>
                <span>Edit Topic Matrix</span>
            </a>

            <form action="/admin/content/generate" method="POST">
                <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-4 py-2.5 rounded-xl shadow-lg shadow-emerald-500/20 transition flex items-center space-x-1.5">
                    <span>⚡</span>
                    <span>Generate New Articles</span>
                </button>
            </form>
        </div>
    </div>

    <!-- STATS SUMMARY BAR -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="bg-slate-900/60 border border-white/10 p-4 rounded-2xl flex items-center justify-between">
            <div>
                <div class="text-xs font-mono text-slate-400">Total Articles Generated</div>
                <div class="text-2xl font-black text-white font-mono mt-0.5">{{ count($articles) }}</div>
            </div>
            <span class="text-emerald-400 text-xl">📄</span>
        </div>

        <div class="bg-slate-900/60 border border-white/10 p-4 rounded-2xl flex items-center justify-between">
            <div>
                <div class="text-xs font-mono text-slate-400">Storage Location</div>
                <div class="text-sm font-bold text-white font-mono mt-1">output/blogs/*.md</div>
            </div>
            <span class="text-indigo-400 text-xl">📁</span>
        </div>

        <div class="bg-slate-900/60 border border-white/10 p-4 rounded-2xl flex items-center justify-between">
            <div>
                <div class="text-xs font-mono text-slate-400">Funnel Conversion Endpoint</div>
                <div class="text-sm font-bold text-emerald-400 font-mono mt-1">WhatsApp Direct CTA</div>
            </div>
            <span class="text-teal-400 text-xl">💬</span>
        </div>
    </div>

    <!-- ARTICLES TABLE -->
    <div class="bg-slate-900/80 border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
        <div class="p-5 border-b border-white/10 flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>📚</span>
                <span>Active Published Case Studies ({{ count($articles) }})</span>
            </h3>
            <span class="text-xs font-mono text-slate-400">Auto-synchronized with portfolio routes</span>
        </div>

        @if(empty($articles))
        <div class="text-center py-16 text-slate-500 space-y-3">
            <div class="text-3xl">📝</div>
            <p class="text-sm">No markdown articles found in output/blogs/</p>
            <form action="/admin/content/generate" method="POST">
                <button type="submit" class="bg-emerald-500 text-slate-950 font-bold text-xs uppercase px-4 py-2 rounded-xl">
                    Generate Batch Now
                </button>
            </form>
        </div>
        @else
        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
                <thead class="bg-slate-950/80 border-b border-white/10 text-xs font-mono text-slate-400 uppercase tracking-wider">
                    <tr>
                        <th class="py-3.5 px-6">Article Title</th>
                        <th class="py-3.5 px-4">Target Market</th>
                        <th class="py-3.5 px-4">Metrics</th>
                        <th class="py-3.5 px-4">Date</th>
                        <th class="py-3.5 px-6 text-right">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-white/5">
                    @foreach($articles as $art)
                    <tr class="hover:bg-slate-800/40 transition">
                        <td class="py-4 px-6">
                            <div class="font-bold text-white hover:text-emerald-300 transition">
                                <a href="/blog/{{ $art['slug'] }}" target="_blank">{{ $art['title'] }}</a>
                            </div>
                            <div class="text-xs text-slate-500 font-mono mt-0.5">
                                slug: /blog/{{ $art['slug'] }}
                            </div>
                        </td>
                        <td class="py-4 px-4 font-mono text-xs">
                            <span class="inline-block px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
                                📍 {{ $art['city'] }}
                            </span>
                            <div class="text-slate-400 text-[11px] mt-1">{{ $art['niche'] }}</div>
                        </td>
                        <td class="py-4 px-4 font-mono text-xs text-slate-400">
                            <div>{{ number_format($art['word_count']) }} words</div>
                            <div class="text-slate-500 text-[11px]">{{ $art['size'] }}</div>
                        </td>
                        <td class="py-4 px-4 font-mono text-xs text-slate-400">
                            {{ $art['date'] }}
                        </td>
                        <td class="py-4 px-6 text-right space-x-2">
                            <a href="/blog/{{ $art['slug'] }}" target="_blank" class="inline-block px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-xs font-mono border border-white/10 transition">
                                Preview ↗
                            </a>
                            <a href="/admin/content/edit?file={{ urlencode($art['filename']) }}" class="inline-block px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 text-xs font-mono border border-emerald-500/30 transition">
                                Edit ✍️
                            </a>
                            <a href="/admin/content/delete?file={{ urlencode($art['filename']) }}" onclick="return confirm('Delete this case study?');" class="inline-block px-2.5 py-1 rounded-lg bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 text-xs font-mono border border-rose-500/30 transition">
                                ✕
                            </a>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
        @endif
    </div>

</div>
@endsection
