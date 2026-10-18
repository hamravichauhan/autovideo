@extends('layouts.admin')

@section('title', 'Prospecting & Lead CRM | ExtrovertNerd Admin')

@section('content')
<div class="space-y-8 max-w-7xl mx-auto" x-data="{ 
    addModal: false, 
    outreachModal: false, 
    selectedProspect: null,
    copyFeedback: '' 
}">

    <!-- HEADER -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
            <div class="text-xs font-mono text-indigo-400 font-bold uppercase tracking-wider mb-1">
                OUTBOUND REVENUE PIPELINE
            </div>
            <h1 class="text-3xl font-black text-white tracking-tight">
                Local Prospecting & <span class="font-serif italic font-normal text-indigo-400">Lead CRM</span>
            </h1>
            <p class="text-slate-400 text-sm mt-1">
                Target commercial businesses with slow mobile storefronts across Goa, Mumbai, Bangalore, and Dubai.
            </p>
        </div>

        <div class="flex items-center space-x-3">
            <button 
                @click="addModal = true" 
                class="bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs uppercase tracking-wider px-4 py-2.5 rounded-xl border border-white/10 transition flex items-center space-x-1.5"
            >
                <span>+</span>
                <span>Add Target</span>
            </button>

            <form action="/admin/prospects/scrape" method="POST" class="inline">
                <input type="hidden" name="city" value="goa">
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-500 text-white font-black text-xs uppercase tracking-wider px-4 py-2.5 rounded-xl shadow-lg shadow-indigo-600/20 transition flex items-center space-x-1.5">
                    <span>🎯</span>
                    <span>Scrape Local Leads</span>
                </button>
            </form>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- 1. FUNNEL STAGE METRIC CARDS                                   -->
    <!-- ============================================================== -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-slate-900/60 border border-white/10 p-4 rounded-2xl">
            <div class="text-xs font-mono text-slate-400">Total Scraped</div>
            <div class="text-2xl font-black text-white font-mono mt-1">{{ $counts['total'] }}</div>
        </div>

        <div class="bg-slate-900/60 border border-white/10 p-4 rounded-2xl">
            <div class="text-xs font-mono text-amber-400">In Outreach / Contacted</div>
            <div class="text-2xl font-black text-amber-300 font-mono mt-1">{{ $counts['contacted'] }}</div>
        </div>

        <div class="bg-slate-900/60 border border-white/10 p-4 rounded-2xl">
            <div class="text-xs font-mono text-emerald-400">Converted Clients</div>
            <div class="text-2xl font-black text-emerald-400 font-mono mt-1">{{ $counts['converted'] }}</div>
        </div>

        <div class="bg-slate-900/60 border border-white/10 p-4 rounded-2xl">
            <div class="text-xs font-mono text-slate-400">Pipeline Value Lost</div>
            <div class="text-2xl font-black text-rose-400 font-mono mt-1">$48k/mo</div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- 2. PROSPECTS PIPELINE TABLE                                    -->
    <!-- ============================================================== -->
    <div class="bg-slate-900/80 border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
        <div class="p-5 border-b border-white/10 flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center space-x-2">
                <span>🎯</span>
                <span>Active Targets ({{ count($prospects) }})</span>
            </h3>
            <span class="text-xs font-mono text-slate-400">Simulated 4G PageSpeed Diagnostics</span>
        </div>

        @if(empty($prospects))
        <div class="text-center py-16 text-slate-500 space-y-3">
            <div class="text-3xl">🎯</div>
            <p class="text-sm">No prospects found in output/prospects.json</p>
            <form action="/admin/prospects/scrape" method="POST">
                <button type="submit" class="bg-indigo-600 text-white font-bold text-xs uppercase px-4 py-2 rounded-xl">
                    Run Prospecting Scraper Now
                </button>
            </form>
        </div>
        @else
        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
                <thead class="bg-slate-950/80 border-b border-white/10 text-xs font-mono text-slate-400 uppercase tracking-wider">
                    <tr>
                        <th class="py-3.5 px-6">Business / Domain</th>
                        <th class="py-3.5 px-4">Market</th>
                        <th class="py-3.5 px-4">Mobile Speed</th>
                        <th class="py-3.5 px-4">Est. Loss</th>
                        <th class="py-3.5 px-4">Funnel Status</th>
                        <th class="py-3.5 px-6 text-right">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-white/5">
                    @foreach($prospects as $p)
                    <tr class="hover:bg-slate-800/40 transition">
                        <td class="py-4 px-6">
                            <div class="font-bold text-white">{{ $p['name'] ?? 'Target' }}</div>
                            <div class="text-xs text-slate-500 font-mono mt-0.5">{{ $p['domain'] ?? '' }}</div>
                        </td>
                        <td class="py-4 px-4 font-mono text-xs">
                            <span class="inline-block px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 font-bold">
                                📍 {{ $p['city'] ?? 'India' }}
                            </span>
                            <div class="text-slate-400 text-[11px] mt-1">{{ $p['niche'] ?? '' }}</div>
                        </td>
                        <td class="py-4 px-4 font-mono text-xs">
                            <div class="flex items-center space-x-1.5 font-bold {{ ($p['speed_score'] ?? 30) < 40 ? 'text-rose-400' : 'text-amber-400' }}">
                                <span>⚠️</span>
                                <span>{{ $p['speed_score'] ?? 24 }}/100</span>
                            </div>
                            <div class="text-slate-500 text-[11px]">{{ $p['load_time_sec'] ?? '5.8' }}s load</div>
                        </td>
                        <td class="py-4 px-4 font-mono text-xs text-rose-300 font-bold">
                            {{ $p['est_monthly_loss'] ?? '$6,500/mo' }}
                        </td>
                        <td class="py-4 px-4 font-mono text-xs">
                            <form action="/admin/prospects/status" method="POST" class="inline">
                                <input type="hidden" name="domain" value="{{ $p['domain'] ?? '' }}">
                                <select 
                                    name="status" 
                                    onchange="this.form.submit()" 
                                    class="bg-slate-950 border border-white/10 rounded-lg px-2.5 py-1 text-xs font-mono text-slate-300 focus:border-indigo-500 outline-none cursor-pointer"
                                >
                                    @php $currentStatus = $p['status'] ?? 'Scraped'; @endphp
                                    <option value="Scraped" {{ $currentStatus === 'Scraped' ? 'selected' : '' }}>Scraped</option>
                                    <option value="Email Sent" {{ $currentStatus === 'Email Sent' ? 'selected' : '' }}>Email Sent</option>
                                    <option value="DM Sent" {{ $currentStatus === 'DM Sent' ? 'selected' : '' }}>DM Sent</option>
                                    <option value="Converted" {{ $currentStatus === 'Converted' ? 'selected' : '' }}>Converted 🏆</option>
                                    <option value="Rejected" {{ $currentStatus === 'Rejected' ? 'selected' : '' }}>Rejected</option>
                                </select>
                            </form>
                        </td>
                        <td class="py-4 px-6 text-right space-x-2">
                            <a 
                                href="/speed-checker?url={{ urlencode($p['domain'] ?? '') }}" 
                                target="_blank" 
                                class="inline-block px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-xs font-mono border border-white/10 transition"
                            >
                                Audit Tool ↗
                            </a>
                            <button 
                                type="button"
                                @click='selectedProspect = @json($p); outreachModal = true'
                                class="inline-block px-3 py-1 rounded-lg bg-indigo-500/10 text-indigo-300 hover:bg-indigo-500/20 text-xs font-mono border border-indigo-500/30 transition"
                            >
                                Pitch Draft 💬
                            </button>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
        @endif
    </div>

    <!-- ============================================================== -->
    <!-- ADD TARGET PROSPECT MODAL                                      -->
    <!-- ============================================================== -->
    <div 
        x-show="addModal" 
        x-cloak 
        class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
        @click.away="addModal = false"
    >
        <div class="bg-slate-900 border border-white/10 rounded-3xl p-6 md:p-8 max-w-lg w-full space-y-5 shadow-2xl">
            <div class="flex items-center justify-between border-b border-white/10 pb-4">
                <h3 class="text-xl font-bold text-white">Add New Target Business</h3>
                <button @click="addModal = false" class="text-slate-400 hover:text-white">✕</button>
            </div>

            <form action="/admin/prospects/add" method="POST" class="space-y-4 text-xs font-mono">
                <div class="space-y-1">
                    <label class="text-slate-400 uppercase">Business Name</label>
                    <input type="text" name="name" placeholder="e.g. Goa Heritage Boutique" required class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white">
                </div>
                <div class="space-y-1">
                    <label class="text-slate-400 uppercase">Website Domain</label>
                    <input type="text" name="domain" placeholder="e.g. goaheritage.com" required class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white">
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-1">
                        <label class="text-slate-400 uppercase">City</label>
                        <input type="text" name="city" value="Goa" required class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white">
                    </div>
                    <div class="space-y-1">
                        <label class="text-slate-400 uppercase">Niche</label>
                        <input type="text" name="niche" value="Boutique Hotels" required class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white">
                    </div>
                </div>
                <div class="space-y-1">
                    <label class="text-slate-400 uppercase">Simulated Mobile Score (1-100)</label>
                    <input type="number" name="speed_score" value="28" min="10" max="90" required class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white">
                </div>

                <div class="pt-4 flex items-center justify-between border-t border-white/10">
                    <button type="button" @click="addModal = false" class="text-slate-400">Cancel</button>
                    <button type="submit" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-5 py-2.5 rounded-xl uppercase">
                        Add to CRM
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- OUTREACH PITCH & SCRIPTS DRAWER / MODAL                        -->
    <!-- ============================================================== -->
    <div 
        x-show="outreachModal" 
        x-cloak 
        class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
        @click.away="outreachModal = false"
    >
        <div class="bg-slate-900 border border-white/10 rounded-3xl p-6 md:p-8 max-w-2xl w-full space-y-6 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar">
            <div class="flex items-center justify-between border-b border-white/10 pb-4">
                <div>
                    <h3 class="text-xl font-bold text-white flex items-center space-x-2">
                        <span>💬</span>
                        <span x-text="'Outreach Pitch: ' + (selectedProspect ? selectedProspect.name : '')"></span>
                    </h3>
                    <div class="text-xs font-mono text-slate-400 mt-0.5" x-text="selectedProspect ? selectedProspect.domain : ''"></div>
                </div>
                <button @click="outreachModal = false" class="text-slate-400 hover:text-white">✕</button>
            </div>

            <template x-if="selectedProspect">
                <div class="space-y-5 text-sm">
                    <!-- WhatsApp Deep Link Box -->
                    <div class="bg-emerald-950/30 border border-emerald-500/30 rounded-2xl p-4 space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-mono font-bold text-emerald-400 uppercase">WhatsApp Instant Pitch</span>
                            <span class="text-[11px] font-mono text-slate-400">Direct Click-to-Chat</span>
                        </div>
                        <p class="text-xs text-slate-300 font-mono">
                            "Hey! Noticed <span x-text="selectedProspect.name"></span> takes 5.8s to load on mobile 4G (scoring 28/100). We built a 0.3s Laravel rebuild demo. Can I send the free 3-minute video breakdown?"
                        </p>
                        <a 
                            :href="'https://wa.me/15551234567?text=' + encodeURIComponent('Hey! Noticed ' + selectedProspect.name + ' takes 5.8s to load on mobile 4G. Sending over the free video audit.')"
                            target="_blank"
                            class="inline-block bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase px-4 py-2 rounded-xl transition"
                        >
                            Open Pre-Filled WhatsApp ➔
                        </a>
                    </div>

                    <!-- Cold Email Script -->
                    <div class="bg-slate-950 border border-white/10 rounded-2xl p-4 space-y-3 font-mono text-xs">
                        <div class="flex items-center justify-between border-b border-white/10 pb-2">
                            <span class="text-slate-400 font-bold uppercase">Executive Cold Email</span>
                            <button 
                                @click="navigator.clipboard.writeText('Subject: Mobile speed bottleneck on ' + selectedProspect.domain + '\n\nHi ' + selectedProspect.name + ' team,\n\nI was browsing ' + selectedProspect.domain + ' on mobile in ' + selectedProspect.city + ' and noticed the mobile experience takes over 5.5s to load, failing Google Core Web Vitals.\n\nAt ExtrovertNerd, we build sub-second custom web architectures that pass Core Web Vitals.\n\nWould you like a complimentary 5-point performance video breakdown?\n\nBest,\nExtrovertNerd Engineering\nWeb Architecture Studio'); copyFeedback = 'Email copied!'" 
                                class="text-indigo-400 hover:underline"
                            >
                                Copy Script 📋
                            </button>
                        </div>
                        <div class="text-slate-300 leading-relaxed space-y-2">
                            <div><strong>Subject:</strong> Mobile speed bottleneck on <span x-text="selectedProspect.domain"></span></div>
                            <p>Hi <span x-text="selectedProspect.name"></span> team,</p>
                            <p>I was browsing <span x-text="selectedProspect.domain"></span> on mobile in <span x-text="selectedProspect.city"></span> and noticed the mobile page takes over 5.5s to load, failing Google Core Web Vitals.</p>
                            <p>At ExtrovertNerd, we rebuild slow stores into sub-second custom Laravel architectures that score 100/100.</p>
                            <p>Would you like a complimentary 5-point video breakdown?</p>
                        </div>
                    </div>

                    <!-- Direct Audit Link -->
                    <div class="text-center pt-2">
                        <a 
                            :href="'/speed-checker?url=' + encodeURIComponent(selectedProspect.domain)" 
                            target="_blank" 
                            class="text-xs font-mono text-slate-400 hover:text-emerald-400 underline"
                        >
                            Launch interactive speed checker audit for this prospect ➔
                        </a>
                    </div>
                </div>
            </template>
        </div>
    </div>

</div>
@endsection
