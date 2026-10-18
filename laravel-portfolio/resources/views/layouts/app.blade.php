<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'ExtrovertNerd — High-Speed Laravel Web Applications & Agency Hub')</title>
    <meta name="description" content="@yield('meta_description', 'Boutique digital engineering agency led by Ravi. We build sub-second Laravel e-commerce stores, automated management dashboards, and modern web applications.')">
    
    <!-- Tailwind CSS CDN & Fonts -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Playfair+Display:ital,wght@1,500;1,600;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    
    <style>
        * {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .font-serif {
            font-family: 'Playfair Display', Georgia, serif;
        }
        .font-mono {
            font-family: 'JetBrains Mono', monospace;
        }
        .font-handwriting {
            font-family: 'Caveat', cursive;
        }
        .glow-emerald {
            box-shadow: 0 0 50px -10px rgba(16, 185, 129, 0.25);
        }
        .glow-indigo {
            box-shadow: 0 0 50px -10px rgba(99, 102, 241, 0.25);
        }
        .glass-nav {
            background: rgba(7, 10, 17, 0.82);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col selection:bg-emerald-500 selection:text-slate-950 antialiased">

    <!-- TOP ANNOUNCEMENT BANNER -->
    <div class="bg-gradient-to-r from-emerald-950 via-slate-900 to-indigo-950 border-b border-emerald-500/20 py-2 px-4 text-center text-xs text-slate-300">
        <div class="max-w-7xl mx-auto flex items-center justify-center space-x-3">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 uppercase tracking-wider">LIVE AUDIT LAB</span>
            <span>Test any website with our free speed diagnostic micro-tool:</span>
            <a href="/speed-checker" class="text-emerald-400 hover:text-emerald-300 font-bold underline decoration-emerald-500/40">Launch Speed Checker ➔</a>
        </div>
    </div>

    <!-- MAIN NAVBAR -->
    <header class="sticky top-0 z-50 glass-nav">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <!-- Brand Logo -->
            <a href="/" class="flex items-center space-x-3 group">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 via-cyan-400 to-indigo-500 p-0.5 shadow-lg group-hover:scale-105 transition">
                    <div class="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center font-black text-emerald-400 text-lg">
                        ⚡
                    </div>
                </div>
                <div>
                    <span class="text-lg font-black tracking-tight text-white block">Extrovert<span class="text-emerald-400">Nerd</span></span>
                    <span class="text-[10px] font-mono text-slate-400 tracking-wider uppercase block -mt-1">Architect: Ravi</span>
                </div>
            </a>

            <!-- Navigation Links -->
            <nav class="hidden md:flex items-center space-x-8 text-sm font-semibold text-slate-300">
                <a href="/#services" class="hover:text-white transition">Services</a>
                <a href="/speed-checker" class="hover:text-emerald-400 flex items-center space-x-1.5 transition">
                    <span>Speed Checker</span>
                    <span class="text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-1.5 py-0.5 rounded">FREE</span>
                </a>
                <a href="/blog" class="hover:text-white transition">Case Studies</a>
                <a href="/#architect" class="hover:text-white transition">Lead Architect</a>
                <a href="/admin" class="hover:text-emerald-400 font-mono text-xs flex items-center space-x-1 text-slate-400 border border-white/10 px-2.5 py-1 rounded-lg hover:border-emerald-500/30 transition">
                    <span>⚡</span>
                    <span>Admin</span>
                </a>
            </nav>

            <!-- CTA Button -->
            <div class="flex items-center space-x-4">
                <a href="https://wa.me/15551234567?text={{ urlencode('Hey Ravi! I saw ExtrovertNerd and want a free 5-point website speed audit.') }}" target="_blank" rel="noopener" class="bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-extrabold text-xs uppercase tracking-wider px-5 py-2.5 rounded-xl shadow-lg shadow-emerald-500/20 hover:scale-105 transition flex items-center space-x-2">
                    <span>📱</span>
                    <span>Free Audit (WhatsApp)</span>
                </a>
            </div>
        </div>
    </header>

    <!-- CONTENT WRAPPER -->
    <main class="flex-grow">
        @yield('content')
    </main>

    <!-- FOOTER -->
    <footer class="bg-slate-950 border-t border-white/10 pt-16 pb-12 mt-20">
        <div class="max-w-7xl mx-auto px-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-12 pb-12 border-b border-white/10">
                <!-- Col 1: Brand & Founder -->
                <div class="md:col-span-2 space-y-4">
                    <div class="flex items-center space-x-3">
                        <div class="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center font-black text-slate-950 text-sm">
                            ⚡
                        </div>
                        <span class="text-xl font-black text-white">Extrovert<span class="text-emerald-400">Nerd</span></span>
                    </div>
                    <p class="text-slate-400 text-sm leading-relaxed max-w-md">
                        High-speed custom Laravel engineering studio. We build sub-second web applications, automated business management dashboards, and zero-commission e-commerce stores for ambitious local businesses and founders.
                    </p>
                    <div class="flex items-center space-x-3 pt-2">
                        <div class="w-9 h-9 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center font-bold text-xs text-emerald-400">
                            R
                        </div>
                        <div class="text-xs">
                            <div class="font-bold text-white">Lead Web Architect: Ravi</div>
                            <div class="text-slate-500 font-mono">ExtrovertNerd Studio • @extrovertnerd</div>
                        </div>
                    </div>
                </div>

                <!-- Col 2: Inbound Micro-Tools -->
                <div class="space-y-3">
                    <div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-400">Micro-Tools & Lab</div>
                    <ul class="space-y-2.5 text-sm text-slate-300">
                        <li><a href="/speed-checker" class="hover:text-emerald-400 transition">Interactive Speed Checker</a></li>
                        <li><a href="/blog" class="hover:text-emerald-400 transition">pSEO Local Case Studies</a></li>
                        <li><a href="https://wa.me/15551234567" target="_blank" class="hover:text-emerald-400 transition">WhatsApp Direct Intake</a></li>
                        <li><a href="/#services" class="hover:text-emerald-400 transition">Laravel Architecture Specs</a></li>
                    </ul>
                </div>

                <!-- Col 3: Target Hubs -->
                <div class="space-y-3">
                    <div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-400">Client Locations</div>
                    <ul class="space-y-2 text-xs text-slate-400 font-mono">
                        <li>📍 Goa (Assagao, Anjuna, Panjim)</li>
                        <li>📍 Mumbai (Bandra, BKC, Colaba)</li>
                        <li>📍 Bangalore (Indiranagar, Koramangala)</li>
                        <li>📍 Dubai (Downtown, Marina, DIFC)</li>
                        <li>📍 Delhi NCR (Cyber Hub, Vasant Kunj)</li>
                    </ul>
                </div>
            </div>

            <!-- Bottom legal & copyright -->
            <div class="pt-8 flex flex-col md:flex-row items-center justify-between text-xs text-slate-500 space-y-4 md:space-y-0">
                <div>
                    &copy; {{ date('Y') }} ExtrovertNerd Agency. Engineered with Laravel 11 & Tailwind CSS. Zero bloat.
                </div>
                <div class="flex items-center space-x-6">
                    <span class="text-emerald-400 font-mono">● All Systems Sub-350ms</span>
                    <a href="https://extrovertnerd.com" class="hover:text-slate-300 transition">extrovertnerd.com</a>
                </div>
            </div>
        </div>
    </footer>

</body>
</html>
