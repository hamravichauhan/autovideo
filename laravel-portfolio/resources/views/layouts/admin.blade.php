<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'ExtrovertNerd • Mission Control & Automation Hub')</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220%22><text y=%2226%22 font-size=%2228%22>⚡</text></svg>">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Playfair+Display:ital,wght@0,600;1,400;1,600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        serif: ['"Playfair Display"', 'serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        slate: {
                            850: '#0f172a',
                            900: '#0b1120',
                            950: '#030712',
                        }
                    }
                }
            }
        }
    </script>

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

    <style>
        body {
            background-color: #030712;
            color: #f3f4f6;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11";
        }
        .glow-emerald {
            box-shadow: 0 0 25px -5px rgba(16, 185, 129, 0.15);
        }
        .glow-indigo {
            box-shadow: 0 0 25px -5px rgba(99, 102, 241, 0.15);
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #0b1120;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #10b981;
        }
    </style>
</head>
<body class="min-h-screen bg-slate-950 font-sans antialiased text-slate-200 selection:bg-emerald-500 selection:text-slate-950" x-data="{ sidebarOpen: false }">

    <div class="flex min-h-screen">

        <!-- ============================================================== -->
        <!-- SIDEBAR NAVIGATION                                             -->
        <!-- ============================================================== -->
        <aside 
            :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
            class="fixed inset-y-0 left-0 z-50 w-72 bg-slate-900/95 backdrop-blur-xl border-r border-white/10 transition-transform duration-300 ease-in-out flex flex-col justify-between"
        >
            <!-- Top Branding -->
            <div>
                <div class="p-6 border-b border-white/10 flex items-center justify-between">
                    <a href="/admin/dashboard" class="flex items-center space-x-3 group">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-300 flex items-center justify-center font-black text-slate-950 text-xl shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition">
                            ⚡
                        </div>
                        <div>
                            <div class="font-black text-lg text-white tracking-tight flex items-center space-x-1.5">
                                <span>Extrovert</span><span class="text-emerald-400 font-serif italic">Nerd</span>
                            </div>
                            <div class="text-[10px] font-mono font-bold tracking-widest text-emerald-400/80 uppercase">
                                Mission Control Hub
                            </div>
                        </div>
                    </a>
                    <button @click="sidebarOpen = false" class="lg:hidden text-slate-400 hover:text-white p-1">
                        ✕
                    </button>
                </div>

                <!-- Architect Badge -->
                <div class="mx-4 my-4 p-3 rounded-2xl bg-slate-950/60 border border-emerald-500/20 flex items-center justify-between">
                    <div class="flex items-center space-x-2.5">
                        <div class="relative">
                            <div class="w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-xs font-bold text-emerald-400">
                                R
                            </div>
                            <span class="absolute bottom-0 right-0 w-2 h-2 rounded-full bg-emerald-400 ring-2 ring-slate-900"></span>
                        </div>
                        <div>
                            <div class="text-xs font-bold text-white leading-none">Ravi</div>
                            <div class="text-[10px] text-slate-400 font-mono mt-0.5">Lead Web Architect</div>
                        </div>
                    </div>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Admin</span>
                </div>

                <!-- Navigation Links -->
                <nav class="px-3 space-y-1 text-sm font-medium">
                    <a href="/admin/dashboard" class="flex items-center space-x-3 px-3.5 py-2.5 rounded-xl transition {{ ($activeNav ?? '') === 'dashboard' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800/60' }}">
                        <span class="text-base">📊</span>
                        <span>Mission Control</span>
                    </a>

                    <a href="/admin/content" class="flex items-center space-x-3 px-3.5 py-2.5 rounded-xl transition {{ ($activeNav ?? '') === 'content' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800/60' }}">
                        <span class="text-base">✍️</span>
                        <span>Content & pSEO Engine</span>
                    </a>

                    <a href="/admin/social" class="flex items-center space-x-3 px-3.5 py-2.5 rounded-xl transition {{ ($activeNav ?? '') === 'social' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800/60' }}">
                        <span class="text-base">🎨</span>
                        <span>Visuals & Social Queue</span>
                    </a>

                    <a href="/admin/prospects" class="flex items-center space-x-3 px-3.5 py-2.5 rounded-xl transition {{ ($activeNav ?? '') === 'prospects' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800/60' }}">
                        <span class="text-base">🎯</span>
                        <span>Prospecting & Leads CRM</span>
                    </a>

                    <a href="/admin/documents" class="flex items-center space-x-3 px-3.5 py-2.5 rounded-xl transition {{ ($activeNav ?? '') === 'documents' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800/60' }}">
                        <span class="text-base">📁</span>
                        <span>Documents & Notes</span>
                    </a>

                    <a href="/admin/system" class="flex items-center space-x-3 px-3.5 py-2.5 rounded-xl transition {{ ($activeNav ?? '') === 'system' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800/60' }}">
                        <span class="text-base">⚙️</span>
                        <span>System & Automation</span>
                    </a>
                </nav>
            </div>

            <!-- Bottom Quick Links & Actions -->
            <div class="p-4 border-t border-white/10 space-y-3">
                <a href="/" target="_blank" class="flex items-center justify-between px-3.5 py-2 rounded-xl bg-slate-950/80 border border-white/10 text-xs font-mono text-slate-300 hover:text-emerald-400 hover:border-emerald-500/30 transition">
                    <span class="flex items-center space-x-2">
                        <span>🌐</span>
                        <span>View Live Agency</span>
                    </span>
                    <span>↗</span>
                </a>

                <div class="text-[11px] font-mono text-slate-500 text-center">
                    ExtrovertNerd Engine v2.0 • Zero-Cost
                </div>
            </div>
        </aside>

        <!-- ============================================================== -->
        <!-- MAIN CONTENT AREA                                              -->
        <!-- ============================================================== -->
        <div class="flex-1 lg:pl-72 flex flex-col min-h-screen">

            <!-- Top Header Bar -->
            <header class="h-16 border-b border-white/10 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 px-6 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <button @click="sidebarOpen = true" class="lg:hidden text-slate-400 hover:text-white p-2 rounded-lg bg-slate-900 border border-white/10">
                        ☰
                    </button>
                    <div class="text-sm font-mono text-slate-400 flex items-center space-x-2">
                        <span class="text-emerald-400">●</span>
                        <span class="hidden sm:inline">Engine Status:</span>
                        <span class="text-white font-bold">24/7 Autonomous Funnel Active</span>
                    </div>
                </div>

                <!-- Top Quick Actions -->
                <div class="flex items-center space-x-3">
                    <a href="/speed-checker" target="_blank" class="hidden sm:inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-white/10 text-xs font-mono text-slate-300 hover:text-white hover:border-emerald-500/40 transition">
                        <span>⚡</span>
                        <span>Speed Checker</span>
                    </a>

                    <form action="/admin/system/trigger" method="POST" class="inline">
                        <input type="hidden" name="action" value="daily">
                        <button type="submit" class="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider shadow-md shadow-emerald-500/20 transition">
                            <span>▶</span>
                            <span>Run Daily Engine</span>
                        </button>
                    </form>
                </div>
            </header>

            <!-- Flash Toast Alerts -->
            <?php 
                $flashSuccess = get_flash('success'); 
                $flashError = get_flash('error');
            ?>
            @if(!empty($flashSuccess))
            <div class="mx-6 mt-6 p-4 rounded-2xl bg-emerald-950/40 border border-emerald-500/50 text-emerald-300 text-sm flex items-center justify-between shadow-xl">
                <div class="flex items-center space-x-2">
                    <span class="text-lg">✅</span>
                    <span class="font-medium">{{ $flashSuccess }}</span>
                </div>
            </div>
            @endif

            @if(!empty($flashError))
            <div class="mx-6 mt-6 p-4 rounded-2xl bg-rose-950/40 border border-rose-500/50 text-rose-300 text-sm flex items-center justify-between shadow-xl">
                <div class="flex items-center space-x-2">
                    <span class="text-lg">⚠️</span>
                    <span class="font-medium">{{ $flashError }}</span>
                </div>
            </div>
            @endif

            <!-- Page Body -->
            <main class="flex-1 p-6 md:p-8">
                @yield('content')
            </main>

            <!-- Admin Footer -->
            <footer class="border-t border-white/5 py-4 px-8 text-center text-xs font-mono text-slate-600 flex flex-col sm:flex-row items-center justify-between gap-2">
                <div>ExtrovertNerd Agency • Lead Web Architect: Ravi</div>
                <div>Autonomous B2B Pipeline • Zero-Cost Cloud Automation</div>
            </footer>

        </div>

    </div>

</body>
</html>
