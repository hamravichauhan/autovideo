@extends('layouts.admin')

@section('title', 'Visual Assets & Social Media Queue | ExtrovertNerd Admin')

@section('content')
<div class="space-y-8 max-w-7xl mx-auto" x-data="{ previewModal: false, activeImage: '', activeTab: 'instagram' }">

    <!-- HEADER -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
            <div class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-wider mb-1">
                MULTI-CHANNEL DISTRIBUTION PIPELINE
            </div>
            <h1 class="text-3xl font-black text-white tracking-tight">
                Visual Assets & <span class="font-serif italic font-normal text-emerald-400">Social Queue</span>
            </h1>
            <p class="text-slate-400 text-sm mt-1">
                Inspect Playwright-rendered carousel sets and review automated captions queued for Instagram, Facebook, and X.
            </p>
        </div>

        <div class="flex flex-wrap items-center gap-2">
            <form action="/admin/social/generate" method="POST" class="inline">
                <input type="hidden" name="type" value="top100">
                <button type="submit" class="bg-gradient-to-r from-emerald-500 to-teal-400 text-slate-950 font-black text-xs uppercase tracking-wider px-3.5 py-2.5 rounded-xl shadow-lg transition flex items-center space-x-1.5 hover:scale-105">
                    <span>🏆</span>
                    <span>Render Top 100 Daily</span>
                </button>
            </form>

            <form action="/admin/social/generate" method="POST" class="inline">
                <input type="hidden" name="type" value="tech_news">
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs uppercase tracking-wider px-3.5 py-2.5 rounded-xl shadow-lg transition flex items-center space-x-1.5">
                    <span>📡</span>
                    <span>Render Tech News</span>
                </button>
            </form>

            <form action="/admin/social/generate" method="POST" class="inline">
                <input type="hidden" name="type" value="website_tip">
                <button type="submit" class="bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs uppercase tracking-wider px-3.5 py-2.5 rounded-xl shadow-lg transition flex items-center space-x-1.5">
                    <span>🛠️</span>
                    <span>Render Website Tip</span>
                </button>
            </form>

            <form action="/admin/social/telegram" method="POST" class="inline">
                <button type="submit" class="bg-sky-500 hover:bg-sky-400 text-slate-950 font-black text-xs uppercase tracking-wider px-3.5 py-2.5 rounded-xl shadow-lg shadow-sky-500/20 transition flex items-center space-x-1.5">
                    <span>📲</span>
                    <span>Telegram</span>
                </button>
            </form>

            <form action="/admin/social/generate" method="POST" class="inline">
                <input type="hidden" name="type" value="carousel">
                <input type="hidden" name="platform" value="vertical">
                <button type="submit" class="bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs uppercase tracking-wider px-3 py-2.5 rounded-xl border border-white/10 transition flex items-center space-x-1.5">
                    <span>📐</span>
                    <span>Local Carousel</span>
                </button>
            </form>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- 1. ACTIVE PUBLISHING QUEUE & COPY PREVIEW                      -->
    <!-- ============================================================== -->
    <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 md:p-8 shadow-2xl space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-4">
            <div>
                <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                    <span>📣</span>
                    <span>Current Active Social Campaign</span>
                </h3>
                <div class="text-xs font-mono text-slate-400 mt-0.5">
                    Target: {{ $campaign['campaign']['city'] ?? 'Goa' }} • {{ $campaign['campaign']['niche'] ?? 'Boutique Hotels' }}
                </div>
            </div>

            <!-- Tab Switcher -->
            <div class="flex items-center space-x-2 bg-slate-950 p-1 rounded-xl border border-white/10 font-mono text-xs">
                <button 
                    @click="activeTab = 'instagram'" 
                    :class="activeTab === 'instagram' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'"
                    class="px-3.5 py-1.5 rounded-lg transition"
                >
                    📸 Instagram / FB
                </button>
                <button 
                    @click="activeTab = 'twitter'" 
                    :class="activeTab === 'twitter' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'"
                    class="px-3.5 py-1.5 rounded-lg transition"
                >
                    🐦 Twitter / X Thread
                </button>
            </div>
        </div>

        <!-- Instagram Tab Content -->
        <div x-show="activeTab === 'instagram'" class="space-y-4">
            <div class="bg-slate-950/70 border border-white/10 rounded-2xl p-5 space-y-3 font-sans text-sm">
                <div class="flex items-center justify-between text-xs font-mono text-slate-500 border-b border-white/5 pb-2">
                    <span>Format: Multi-Slide Carousel (4 Slides)</span>
                    <span class="text-emerald-400 font-bold">Ready to Dispatch</span>
                </div>
                <div class="text-slate-200 whitespace-pre-line leading-relaxed font-mono text-xs">
{{ $campaign['instagram']['caption'] ?? "Local business owners: Is your mobile site losing customers to slow load times? Swipe through to see the before vs after teardown." }}
                </div>
                <div class="text-xs text-indigo-400 font-mono pt-2">
                    {{ $campaign['instagram']['hashtags'] ?? '#WebDevelopment #Laravel #CoreWebVitals #GoaBusiness' }}
                </div>
            </div>
        </div>

        <!-- Twitter Thread Tab Content -->
        <div x-show="activeTab === 'twitter'" class="space-y-3">
            <div class="space-y-2">
                @php $tweets = $campaign['twitter_thread'] ?? []; @endphp
                @if(empty($tweets))
                <div class="p-4 bg-slate-950 rounded-xl text-xs font-mono text-slate-400">
                    Thread generated during daily automation run.
                </div>
                @else
                @foreach($tweets as $index => $tweet)
                <div class="bg-slate-950/70 border border-white/10 rounded-xl p-4 flex items-start space-x-3 text-xs font-mono">
                    <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold shrink-0">
                        {{ $index + 1 }}/{{ count($tweets) }}
                    </span>
                    <p class="text-slate-200 leading-relaxed">{{ $tweet }}</p>
                </div>
                @endforeach
                @endif
            </div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- 2. RENDERED GRAPHIC CAROUSELS GALLERY                          -->
    <!-- ============================================================== -->
    <div class="space-y-6">
        <div class="flex items-center justify-between">
            <div>
                <h3 class="text-xl font-bold text-white flex items-center space-x-2">
                    <span>🖼️</span>
                    <span>Generated Carousel Sets & Visual Assets ({{ count($graphicSets) }})</span>
                </h3>
                <p class="text-xs text-slate-400 mt-0.5">Rendered via Playwright Chromium into high-resolution PNGs with human-centric sticky notes.</p>
            </div>
        </div>

        @if(empty($graphicSets))
        <div class="text-center py-16 bg-slate-900/40 rounded-3xl border border-white/10 text-slate-400 text-sm space-y-3">
            <div class="text-3xl">🎨</div>
            <p>No rendered graphics found in output/graphics/</p>
            <form action="/admin/social/generate" method="POST">
                <input type="hidden" name="platform" value="all">
                <button type="submit" class="bg-emerald-500 text-slate-950 font-bold text-xs uppercase px-4 py-2 rounded-xl">
                    Render Graphics Now
                </button>
            </form>
        </div>
        @else
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            @foreach($graphicSets as $set)
            <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 space-y-4 shadow-xl">
                <div class="flex items-center justify-between border-b border-white/10 pb-3">
                    <div>
                        <h4 class="text-base font-bold text-white">{{ $set['name'] }}</h4>
                        <span class="text-xs font-mono text-slate-500">{{ $set['count'] }} visual assets</span>
                    </div>
                    <span class="text-xs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full">
                        PNG Asset
                    </span>
                </div>

                <!-- Slide Thumbnails Grid -->
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    @foreach($set['images'] as $img)
                    <div 
                        @click="activeImage = '{{ $img }}'; previewModal = true"
                        class="aspect-[4/5] rounded-xl overflow-hidden bg-black/40 border border-white/10 hover:border-emerald-400 cursor-pointer group relative transition shadow-md"
                    >
                        <img src="{{ $img }}" alt="Slide" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-white text-xs font-mono">
                            🔍 Zoom
                        </div>
                    </div>
                    @endforeach
                </div>
            </div>
            @endforeach
        </div>
        @endif
    </div>

    <!-- LIGHTBOX MODAL -->
    <div 
        x-show="previewModal" 
        x-cloak 
        class="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4"
        @click.away="previewModal = false"
    >
        <div class="relative max-w-4xl max-h-[90vh] flex flex-col items-center">
            <button 
                @click="previewModal = false" 
                class="absolute -top-10 right-0 text-white font-mono text-sm hover:text-emerald-400 bg-slate-900 px-3 py-1 rounded-full border border-white/20"
            >
                ✕ Close
            </button>
            <img :src="activeImage" alt="Preview" class="max-h-[80vh] w-auto rounded-2xl shadow-2xl border border-white/20">
        </div>
    </div>

</div>
@endsection
