@extends('layouts.admin')

@section('title', 'System Automation & CLI Trigger | ExtrovertNerd Admin')

@section('content')
<div class="space-y-8 max-w-7xl mx-auto" x-data="{ activeSection: 'workflows' }">

    <!-- HEADER -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
            <div class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-wider mb-1">
                CORE AUTOMATION & SYSTEM ENVIRONMENT
            </div>
            <h1 class="text-3xl font-black text-white tracking-tight">
                System Automation & <span class="font-serif italic font-normal text-emerald-400">Environment Control</span>
            </h1>
            <p class="text-slate-400 text-sm mt-1">
                Trigger Python automation routines, update API secrets, and inspect real-time execution logs.
            </p>
        </div>

        <!-- Section Switcher -->
        <div class="flex items-center space-x-2 bg-slate-900 p-1.5 rounded-2xl border border-white/10 font-mono text-xs">
            <button 
                @click="activeSection = 'workflows'" 
                :class="activeSection === 'workflows' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'"
                class="px-4 py-2 rounded-xl transition"
            >
                ⚙️ Workflows & CLI
            </button>
            <button 
                @click="activeSection = 'config'" 
                :class="activeSection === 'config' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'"
                class="px-4 py-2 rounded-xl transition"
            >
                🔐 Agency Config & .env
            </button>
            <button 
                @click="activeSection = 'logs'" 
                :class="activeSection === 'logs' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'"
                class="px-4 py-2 rounded-xl transition"
            >
                📜 Execution Logs
            </button>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- 1. WORKFLOW CONTROL CENTER                                     -->
    <!-- ============================================================== -->
    <div x-show="activeSection === 'workflows'" class="space-y-6">

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

            <!-- Card 1: Daily Autonomous Run -->
            <div class="bg-gradient-to-b from-emerald-950/20 to-slate-900/90 border border-emerald-500/30 rounded-3xl p-6 flex flex-col justify-between space-y-4 shadow-xl">
                <div class="space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-mono font-bold text-emerald-400 uppercase">24/7 Engine</span>
                        <span class="text-xl">⚡</span>
                    </div>
                    <h3 class="text-lg font-black text-white">Full Daily Automation</h3>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        Executes pSEO case study builder, multi-platform graphics renderer, social queue assembly, and local prospecting.
                    </p>
                </div>
                <form action="/admin/system/trigger" method="POST">
                    <input type="hidden" name="action" value="daily">
                    <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider py-3 rounded-xl shadow-lg transition">
                        Run Daily Pipeline ➔
                    </button>
                </form>
            </div>

            <!-- Card 2: Local Prospecting Bot -->
            <div class="bg-gradient-to-b from-indigo-950/20 to-slate-900/90 border border-indigo-500/30 rounded-3xl p-6 flex flex-col justify-between space-y-4 shadow-xl">
                <div class="space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-mono font-bold text-indigo-400 uppercase">Lead Scraper</span>
                        <span class="text-xl">🎯</span>
                    </div>
                    <h3 class="text-lg font-black text-white">Prospecting Bot</h3>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        Scans directories for slow mobile business storefronts and compiles ready-to-send WhatsApp and email pitch drafts.
                    </p>
                </div>
                <form action="/admin/system/trigger" method="POST">
                    <input type="hidden" name="action" value="prospect">
                    <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-black text-xs uppercase tracking-wider py-3 rounded-xl shadow-lg transition">
                        Scrape Local Targets ➔
                    </button>
                </form>
            </div>

            <!-- Card 3: Multi-Platform Graphics -->
            <div class="bg-gradient-to-b from-teal-950/20 to-slate-900/90 border border-teal-500/30 rounded-3xl p-6 flex flex-col justify-between space-y-4 shadow-xl">
                <div class="space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-mono font-bold text-teal-400 uppercase">Headless Browser</span>
                        <span class="text-xl">🎨</span>
                    </div>
                    <h3 class="text-lg font-black text-white">Multi-Platform Graphics</h3>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        Renders 4-slide carousels across Instagram 4:5 vertical, Twitter 16:9 widescreen, and Square 1:1 feeds.
                    </p>
                </div>
                <form action="/admin/system/trigger" method="POST">
                    <input type="hidden" name="action" value="graphics">
                    <button type="submit" class="w-full bg-teal-600 hover:bg-teal-500 text-white font-black text-xs uppercase tracking-wider py-3 rounded-xl shadow-lg transition">
                        Render All Graphic Sets ➔
                    </button>
                </form>
            </div>

        </div>

        <!-- LIVE TERMINAL CONSOLE VIEWER -->
        <div class="bg-slate-950 border border-white/10 rounded-3xl p-6 shadow-2xl space-y-3 font-mono">
            <div class="flex items-center justify-between border-b border-white/10 pb-3">
                <div class="flex items-center space-x-2">
                    <span class="w-3 h-3 rounded-full bg-rose-500 inline-block"></span>
                    <span class="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
                    <span class="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
                    <span class="text-xs text-slate-400 pl-2">Live CLI Execution Output</span>
                </div>
                @if(!empty($lastCommand))
                <span class="text-[11px] text-emerald-400">{{ $lastCommand }}</span>
                @endif
            </div>

            <div class="p-4 bg-black/60 rounded-2xl text-xs text-slate-300 overflow-x-auto max-h-96 custom-scrollbar leading-relaxed">
                @if(empty($lastOutput))
                <div class="text-slate-600">
                    // Trigger any workflow card above to see real-time execution logs and output here.
                </div>
                @else
                <pre class="text-emerald-400">{{ $lastOutput }}</pre>
                @endif
            </div>
        </div>

    </div>

    <!-- ============================================================== -->
    <!-- 2. ENVIRONMENT & AGENCY CONFIG EDITOR (.ENV)                   -->
    <!-- ============================================================== -->
    <div x-show="activeSection === 'config'" class="space-y-6">

        <form action="/admin/system/config" method="POST" class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 md:p-8 space-y-6 shadow-2xl">
            <div class="flex items-center justify-between border-b border-white/10 pb-4">
                <div>
                    <h3 class="text-lg font-bold text-white flex items-center space-x-2">
                        <span>🔐</span>
                        <span>Agency Brand & Contact Endpoints (.env)</span>
                    </h3>
                    <p class="text-xs text-slate-400 mt-0.5">Directly controls funnel links, WhatsApp CTA number, and API tokens.</p>
                </div>
                <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-2.5 rounded-xl shadow-lg transition">
                    Save Config ➔
                </button>
            </div>

            <!-- Brand Row -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
                <div class="space-y-1">
                    <label class="text-xs font-mono text-slate-400 uppercase">Agency Name</label>
                    <input type="text" name="brand_name" value="{{ $envVars['BRAND_NAME'] ?? 'ExtrovertNerd' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-sm">
                </div>
                <div class="space-y-1">
                    <label class="text-xs font-mono text-slate-400 uppercase">Social Handle</label>
                    <input type="text" name="brand_handle" value="{{ $envVars['BRAND_HANDLE'] ?? '@extrovertnerd' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-sm">
                </div>
                <div class="space-y-1">
                    <label class="text-xs font-mono text-slate-400 uppercase">Website URL</label>
                    <input type="text" name="website_url" value="{{ $envVars['WEBSITE_URL'] ?? 'https://extrovertnerd.com' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-sm font-mono">
                </div>
            </div>

            <!-- Founder Attribution Row -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div class="space-y-1">
                    <label class="text-xs font-mono text-slate-400 uppercase">Lead Architect / Founder Name</label>
                    <input type="text" name="founder_name" value="{{ $envVars['FOUNDER_NAME'] ?? 'Ravi' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-sm">
                </div>
                <div class="space-y-1">
                    <label class="text-xs font-mono text-slate-400 uppercase">Founder Title</label>
                    <input type="text" name="founder_role" value="{{ $envVars['FOUNDER_ROLE'] ?? 'Lead Web Architect' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-sm">
                </div>
            </div>

            <!-- WhatsApp Inbound Funnel -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div class="space-y-1">
                    <label class="text-xs font-mono text-emerald-400 uppercase font-bold">WhatsApp Phone Number (With Country Code)</label>
                    <input type="text" name="whatsapp_phone_number" value="{{ $envVars['WHATSAPP_PHONE_NUMBER'] ?? '15551234567' }}" class="w-full bg-slate-950 border border-emerald-500/30 rounded-xl px-4 py-2 text-white font-mono text-sm">
                </div>
                <div class="space-y-1">
                    <label class="text-xs font-mono text-slate-400 uppercase">Google Form Intake URL (Optional)</label>
                    <input type="text" name="google_form_intake_url" value="{{ $envVars['GOOGLE_FORM_INTAKE_URL'] ?? '' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-sm font-mono">
                </div>
            </div>

            <div class="space-y-1">
                <label class="text-xs font-mono text-slate-400 uppercase">Default WhatsApp Click-to-Chat Prompt</label>
                <input type="text" name="whatsapp_default_message" value="{{ $envVars['WHATSAPP_DEFAULT_MESSAGE'] ?? 'Hey Ravi! I saw ExtrovertNerd and want a free 5-point website speed audit.' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-sm">
            </div>

            <!-- Social API Keys (Optional) -->
            <div class="pt-4 border-t border-white/10 space-y-4">
                <h4 class="text-sm font-bold text-white uppercase font-mono tracking-wider">Social Publishing API Keys (Optional for Cloud Dispatch)</h4>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div class="space-y-1">
                        <label class="text-[11px] font-mono text-slate-500 uppercase">Meta Graph Access Token</label>
                        <input type="password" name="meta_access_token" value="{{ $envVars['META_ACCESS_TOKEN'] ?? '' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-xs font-mono">
                    </div>
                    <div class="space-y-1">
                        <label class="text-[11px] font-mono text-slate-500 uppercase">Instagram Account ID</label>
                        <input type="text" name="instagram_account_id" value="{{ $envVars['INSTAGRAM_ACCOUNT_ID'] ?? '' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-xs font-mono">
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div class="space-y-1">
                        <label class="text-[11px] font-mono text-slate-500 uppercase">Twitter / X API Key</label>
                        <input type="password" name="twitter_api_key" value="{{ $envVars['TWITTER_API_KEY'] ?? '' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-xs font-mono">
                    </div>
                    <div class="space-y-1">
                        <label class="text-[11px] font-mono text-slate-500 uppercase">Twitter / X Bearer Token</label>
                        <input type="password" name="twitter_bearer_token" value="{{ $envVars['TWITTER_BEARER_TOKEN'] ?? '' }}" class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-xs font-mono">
                    </div>
                </div>
            </div>

            <div class="flex items-center justify-end pt-4 border-t border-white/10">
                <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-8 py-3 rounded-xl shadow-lg transition">
                    Save All Environment Variables ➔
                </button>
            </div>
        </form>

    </div>

    <!-- ============================================================== -->
    <!-- 3. AUTOMATION LOG VIEWER                                       -->
    <!-- ============================================================== -->
    <div x-show="activeSection === 'logs'" class="space-y-6">

        <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 md:p-8 space-y-4 shadow-2xl">
            <div class="flex items-center justify-between border-b border-white/10 pb-4">
                <div>
                    <h3 class="text-base font-bold text-white flex items-center space-x-2">
                        <span>📜</span>
                        <span>output/automation_log.json Viewer</span>
                    </h3>
                    <p class="text-xs text-slate-400 mt-0.5">Metrics from the most recent headless browser and publisher runs.</p>
                </div>
                <form action="/admin/system/clear-logs" method="POST">
                    <button type="submit" onclick="return confirm('Clear execution logs?');" class="text-xs font-mono text-rose-400 hover:underline">
                        Clear Logs ✕
                    </button>
                </form>
            </div>

            <div class="p-4 bg-slate-950 rounded-2xl overflow-x-auto max-h-[600px] custom-scrollbar">
                <pre class="font-mono text-xs text-emerald-400 leading-relaxed">{{ $rawLog }}</pre>
            </div>
        </div>

    </div>

</div>
@endsection
