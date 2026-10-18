<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'ExtrovertNerd — Full-Stack Web Engineering & Custom Digital Systems')</title>
    <meta name="description" content="@yield('meta_description', 'Boutique full-stack engineering studio led by Lead Architect Ravi. We build bespoke sub-second web applications, high-converting stores, and automated management dashboards tailored precisely to your business logic.')">
    
    <!-- Tailwind CSS CDN & Alpine.js -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <!-- Editorial Typography Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        serif: ['"Playfair Display"', 'Georgia', 'serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                        handwriting: ['"Caveat"', 'cursive'],
                    },
                    colors: {
                        obsidian: '#020617',
                        slate: {
                            850: '#0f172a',
                            900: '#0a0f1d',
                            950: '#020617',
                        },
                        mint: {
                            300: '#6ee7b7',
                            400: '#34d399',
                            500: '#10b981',
                        }
                    }
                }
            }
        }
    </script>

    <style>
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #020617;
            color: #f1f5f9;
            overflow-x: hidden;
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
        .bg-grid-ambient {
            background-size: 40px 40px;
            background-image: 
                linear-gradient(to right, rgba(255, 255, 255, 0.025) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
        }
        .glow-emerald {
            box-shadow: 0 0 60px -10px rgba(16, 185, 129, 0.28);
        }
        .glow-mint {
            box-shadow: 0 0 50px -8px rgba(52, 211, 153, 0.24);
        }
        .glass-nav {
            background: rgba(2, 6, 23, 0.85);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        }
        .glass-card {
            background: rgba(10, 15, 29, 0.65);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glass-card:hover {
            border-color: rgba(16, 185, 129, 0.35);
        }
        .shimmer-text {
            background: linear-gradient(90deg, #ffffff 0%, #a7f3d0 50%, #ffffff 100%);
            background-size: 200% auto;
            color: transparent;
            -webkit-background-clip: text;
            animation: shimmer 8s linear infinite;
        }
        @keyframes shimmer {
            to { background-position: 200% center; }
        }
    </style>
</head>
<body class="bg-[#020617] text-slate-100 min-h-screen flex flex-col selection:bg-emerald-500 selection:text-slate-950 antialiased relative bg-grid-ambient" x-data="{ mobileNav: false }">

    <!-- AMBIENT TOP LIGHTING GLOWS -->
    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[1100px] h-[480px] bg-gradient-to-b from-emerald-500/10 via-teal-500/5 to-transparent blur-3xl pointer-events-none -z-10"></div>
    <div class="fixed top-1/3 -right-48 w-[500px] h-[500px] bg-emerald-500/5 blur-3xl pointer-events-none -z-10"></div>
    <div class="fixed bottom-1/4 -left-48 w-[500px] h-[500px] bg-teal-500/5 blur-3xl pointer-events-none -z-10"></div>

    <!-- TOP ANNOUNCEMENT BANNER -->
    <div class="bg-gradient-to-r from-emerald-950/70 via-slate-950 to-teal-950/70 border-b border-emerald-500/20 py-2.5 px-4 text-center text-xs text-slate-300 relative z-50">
        <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-center gap-2 sm:gap-4">
            <span class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 uppercase tracking-widest">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
                <span>⚡ FREE FORENSIC AUDIT</span>
            </span>
            <span class="text-slate-300">Discover how much revenue your slow website loses to mobile latency.</span>
            <a href="/speed-checker" class="text-emerald-400 hover:text-emerald-300 font-bold underline decoration-emerald-500/40 flex items-center space-x-1 transition">
                <span>Launch Diagnostic</span>
                <span>➔</span>
            </a>
        </div>
    </div>

    <!-- MAIN NAVBAR -->
    <header class="sticky top-0 z-40 glass-nav">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            
            <!-- Brand Logo & Human Status -->
            <a href="/" class="flex items-center space-x-3.5 group">
                <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-emerald-300 p-0.5 shadow-xl shadow-emerald-500/20 group-hover:scale-105 transition duration-300">
                    <div class="w-full h-full bg-[#020617] rounded-[14px] flex items-center justify-center font-black text-emerald-400 text-xl">
                        ⚡
                    </div>
                </div>
                <div>
                    <div class="flex items-center space-x-2">
                        <span class="text-xl font-black tracking-tight text-white block group-hover:text-emerald-300 transition">
                            Extrovert<span class="text-emerald-400 font-serif italic font-normal">Nerd</span>
                        </span>
                        <!-- Status indicator pulse -->
                        <span class="inline-flex items-center gap-1.5 bg-emerald-950/60 border border-emerald-500/30 px-2 py-0.5 rounded-full">
                            <span class="relative flex h-2 w-2">
                                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                            </span>
                            <span class="text-emerald-300 font-mono text-[9px] font-bold tracking-wider uppercase">Online & Coding</span>
                        </span>
                    </div>
                    <!-- Refined human subtitle: ARCHITECT: RAVI | STATUS: BUILDING EXCLUSIVE SYSTEMS -->
                    <span class="text-[10px] font-mono text-slate-400 tracking-wider uppercase block mt-0.5">
                        <span class="text-slate-300 font-bold">ARCHITECT: RAVI</span>
                        <span class="text-emerald-500/70 mx-1">•</span>
                        <span class="text-slate-400">STATUS: BUILDING EXCLUSIVE SYSTEMS</span>
                    </span>
                </div>
            </a>

            <!-- Desktop Navigation Links (Streamlined Multi-Page) -->
            <nav class="hidden lg:flex items-center space-x-8 text-sm font-semibold">
                <!-- 1. How We Work -->
                <a 
                    href="/how-we-work" 
                    class="transition flex items-center space-x-1.5 py-1 relative {{ is_active_path('/how-we-work') ? 'text-emerald-400 font-bold' : 'text-slate-300 hover:text-white' }}"
                >
                    <span>How We Work</span>
                    @if(is_active_path('/how-we-work'))
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    @endif
                </a>

                <!-- 2. Speed Checker -->
                <a 
                    href="/speed-checker" 
                    class="transition flex items-center space-x-1.5 py-1 relative {{ is_active_path('/speed-checker') ? 'text-emerald-400 font-bold' : 'text-slate-300 hover:text-emerald-300' }}"
                >
                    <span>Speed Checker</span>
                    <span class="text-[10px] bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 px-1.5 py-0.5 rounded font-mono">100/100</span>
                </a>

                <!-- 3. Case Studies -->
                <a 
                    href="/case-studies" 
                    class="transition flex items-center space-x-1.5 py-1 relative {{ (is_active_path('/case-studies') || is_active_path('/blog')) ? 'text-emerald-400 font-bold' : 'text-slate-300 hover:text-white' }}"
                >
                    <span>Case Studies</span>
                    @if(is_active_path('/case-studies') || is_active_path('/blog'))
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    @endif
                </a>

                <!-- 4. ROI Calculator -->
                <a 
                    href="/roi-calculator" 
                    class="transition flex items-center space-x-1.5 py-1 relative {{ is_active_path('/roi-calculator') ? 'text-emerald-400 font-bold' : 'text-slate-300 hover:text-white' }}"
                >
                    <span>ROI Calculator</span>
                    @if(is_active_path('/roi-calculator'))
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    @endif
                </a>

                <!-- 5. Admin -->
                <a 
                    href="/admin/dashboard" 
                    class="font-mono text-xs flex items-center space-x-1.5 text-slate-400 border border-white/10 px-3 py-1.5 rounded-xl hover:border-emerald-500/40 hover:text-emerald-300 hover:bg-slate-900 transition"
                >
                    <span>⚡</span>
                    <span>Admin</span>
                </a>
            </nav>

            <!-- CTA Button & Mobile Hamburger -->
            <div class="flex items-center space-x-4">
                <a 
                    href="https://wa.me/15551234567?text={{ urlencode('Hey Ravi! I saw ExtrovertNerd and want to see how you can make my website 100/100 fast.') }}" 
                    target="_blank" 
                    rel="noopener" 
                    class="hidden sm:inline-flex bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-xs uppercase tracking-wider px-5 py-3 rounded-xl shadow-lg shadow-emerald-500/25 hover:scale-105 transition items-center space-x-2"
                >
                    <span>💬</span>
                    <span>WhatsApp Ravi</span>
                </a>

                <!-- Mobile Hamburger Toggle -->
                <button 
                    @click="mobileNav = !mobileNav" 
                    type="button" 
                    class="lg:hidden p-2 rounded-xl border border-white/10 text-slate-300 hover:text-white hover:bg-slate-900 focus:outline-none"
                    aria-label="Toggle navigation menu"
                >
                    <svg x-show="!mobileNav" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                    <svg x-show="mobileNav" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="display: none;">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        </div>

        <!-- Mobile Drawer Navigation -->
        <div 
            x-show="mobileNav" 
            x-transition:enter="transition ease-out duration-200"
            x-transition:enter-start="opacity-0 -translate-y-2"
            x-transition:enter-end="opacity-100 translate-y-0"
            x-transition:leave="transition ease-in duration-150"
            x-transition:leave-start="opacity-100 translate-y-0"
            x-transition:leave-end="opacity-0 -translate-y-2"
            class="lg:hidden border-b border-white/10 bg-[#020617]/95 backdrop-blur-2xl px-6 py-6 space-y-4"
            style="display: none;"
        >
            <div class="flex flex-col space-y-3 font-semibold text-base">
                <a href="/how-we-work" class="px-3 py-2 rounded-xl {{ is_active_path('/how-we-work') ? 'bg-emerald-500/10 text-emerald-400 font-bold' : 'text-slate-300 hover:text-white' }}">
                    How We Work
                </a>
                <a href="/speed-checker" class="px-3 py-2 rounded-xl flex items-center justify-between {{ is_active_path('/speed-checker') ? 'bg-emerald-500/10 text-emerald-400 font-bold' : 'text-slate-300 hover:text-emerald-300' }}">
                    <span>Speed Checker</span>
                    <span class="text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded font-mono">100/100</span>
                </a>
                <a href="/case-studies" class="px-3 py-2 rounded-xl {{ (is_active_path('/case-studies') || is_active_path('/blog')) ? 'bg-emerald-500/10 text-emerald-400 font-bold' : 'text-slate-300 hover:text-white' }}">
                    Case Studies
                </a>
                <a href="/roi-calculator" class="px-3 py-2 rounded-xl {{ is_active_path('/roi-calculator') ? 'bg-emerald-500/10 text-emerald-400 font-bold' : 'text-slate-300 hover:text-white' }}">
                    ROI Calculator
                </a>
                <a href="/admin/dashboard" class="px-3 py-2 rounded-xl text-slate-400 hover:text-white font-mono text-sm flex items-center space-x-2">
                    <span>⚡</span>
                    <span>Admin Command Center</span>
                </a>
            </div>

            <div class="pt-4 border-t border-white/10">
                <a 
                    href="https://wa.me/15551234567?text={{ urlencode('Hey Ravi! I saw ExtrovertNerd and want to discuss my website speed.') }}" 
                    target="_blank" 
                    rel="noopener" 
                    class="w-full bg-gradient-to-r from-emerald-500 to-teal-400 text-slate-950 font-black text-xs uppercase tracking-wider px-5 py-3.5 rounded-xl shadow-lg shadow-emerald-500/25 flex items-center justify-center space-x-2"
                >
                    <span>💬</span>
                    <span>WhatsApp Ravi Directly</span>
                </a>
            </div>
        </div>
    </header>

    <!-- CONTENT WRAPPER -->
    <main class="flex-grow">
        @yield('content')
    </main>

    <!-- ARTISTIC BOUTIQUE FOOTER -->
    <footer class="bg-[#020617] border-t border-white/10 pt-20 pb-14 mt-28 relative">
        <div class="max-w-7xl mx-auto px-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-12 pb-14 border-b border-white/10">
                <!-- Col 1: Brand & Founder -->
                <div class="md:col-span-2 space-y-5">
                    <div class="flex items-center space-x-3.5">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-300 flex items-center justify-center font-black text-slate-950 text-base shadow-lg">
                            ⚡
                        </div>
                        <span class="text-2xl font-black text-white">Extrovert<span class="text-emerald-400 font-serif italic font-normal">Nerd</span></span>
                    </div>
                    <p class="text-slate-400 text-sm leading-relaxed max-w-md">
                        Boutique digital engineering studio led by Lead Architect Ravi. We build bespoke sub-second web applications, high-converting storefronts, and automated management dashboards with a contractual <strong class="text-white">100/100 Core Web Vitals guarantee</strong>.
                    </p>
                    <div class="flex items-center space-x-3 pt-2">
                        <div class="w-10 h-10 rounded-2xl bg-slate-900 border border-emerald-500/30 flex items-center justify-center font-bold text-sm text-emerald-400 shadow-inner">
                            R
                        </div>
                        <div class="text-xs">
                            <div class="font-bold text-white flex items-center space-x-1.5">
                                <span>Lead Web Architect: Ravi</span>
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                            </div>
                            <div class="text-slate-400 font-mono">Bespoke Engineering • Zero Third-Party Bloat</div>
                        </div>
                    </div>
                </div>

                <!-- Col 2: The Multi-Page Navigation -->
                <div class="space-y-4">
                    <div class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">Navigation Hub</div>
                    <ul class="space-y-2.5 text-sm text-slate-300">
                        <li><a href="/how-we-work" class="hover:text-emerald-400 transition">How We Work (5-Step Blueprint)</a></li>
                        <li><a href="/speed-checker" class="hover:text-emerald-400 transition">Free Mobile Speed Audit</a></li>
                        <li><a href="/case-studies" class="hover:text-emerald-400 transition">Case Studies & Performance Logs</a></li>
                        <li><a href="/roi-calculator" class="hover:text-emerald-400 transition">Revenue Recovery Calculator</a></li>
                        <li><a href="/admin/dashboard" class="hover:text-emerald-400 transition font-mono text-xs">Admin Mission Control</a></li>
                    </ul>
                </div>

                <!-- Col 3: Target Commercial Hubs -->
                <div class="space-y-4">
                    <div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-400">Target Commercial Hubs</div>
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
            <div class="pt-8 flex flex-col md:flex-row items-center justify-between text-xs text-slate-500 space-y-4 md:space-y-0 font-mono">
                <div>
                    &copy; {{ date('Y') }} ExtrovertNerd Agency. Engineered with precision. Zero monthly SaaS tax.
                </div>
                <div class="flex items-center space-x-6">
                    <span class="text-emerald-400 flex items-center space-x-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span>100% Mobile Core Web Vitals Pass Guarantee</span>
                    </span>
                    <a href="https://wa.me/15551234567" target="_blank" rel="noopener" class="hover:text-white transition">Direct WhatsApp ➔</a>
                </div>
            </div>
        </div>
    </footer>

</body>
</html>
