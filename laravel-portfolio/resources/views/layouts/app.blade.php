<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'ExtrovertNerd — Full-Stack Web Engineering & Custom Digital Systems')</title>
    <meta name="description" content="@yield('meta_description', 'Boutique full-stack engineering studio led by Lead Architect Ravi. We build sub-second web applications, high-converting stores, and automated management dashboards across any modern stack: Laravel, Next.js, React, Node.js, Python, or Go.')">
    
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
                        slate: {
                            850: '#0f172a',
                            900: '#0a0f1d',
                            950: '#030712',
                        }
                    }
                }
            }
        }
    </script>

    <style>
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #030712;
            color: #f3f4f6;
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
            background-size: 38px 38px;
            background-image: 
                linear-gradient(to right, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
        }
        .glow-emerald {
            box-shadow: 0 0 60px -10px rgba(16, 185, 129, 0.28);
        }
        .glow-indigo {
            box-shadow: 0 0 60px -10px rgba(99, 102, 241, 0.28);
        }
        .glass-nav {
            background: rgba(3, 7, 18, 0.82);
            backdrop-filter: blur(24px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glass-card {
            background: rgba(11, 17, 32, 0.7);
            backdrop-filter: blur(16px);
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
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col selection:bg-emerald-500 selection:text-slate-950 antialiased relative bg-grid-ambient">

    <!-- AMBIENT TOP LIGHTING GLOWS -->
    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[450px] bg-gradient-to-b from-emerald-500/10 via-indigo-500/5 to-transparent blur-3xl pointer-events-none -z-10"></div>
    <div class="fixed top-1/3 -right-48 w-[500px] h-[500px] bg-teal-500/5 blur-3xl pointer-events-none -z-10"></div>
    <div class="fixed bottom-1/4 -left-48 w-[500px] h-[500px] bg-indigo-500/5 blur-3xl pointer-events-none -z-10"></div>

    <!-- TOP ANNOUNCEMENT BANNER -->
    <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-indigo-950/80 border-b border-emerald-500/20 py-2.5 px-4 text-center text-xs text-slate-300 relative z-50">
        <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-center gap-2 sm:gap-4">
            <span class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 uppercase tracking-widest">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
                <span>FREE FORENSIC AUDIT</span>
            </span>
            <span class="text-slate-300">Test how much revenue your slow website loses to mobile latency:</span>
            <a href="/speed-checker" class="text-emerald-400 hover:text-emerald-300 font-bold underline decoration-emerald-500/40 flex items-center space-x-1">
                <span>Launch Speed Diagnostic</span>
                <span>➔</span>
            </a>
        </div>
    </div>

    <!-- MAIN NAVBAR -->
    <header class="sticky top-0 z-40 glass-nav">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <!-- Brand Logo -->
            <a href="/" class="flex items-center space-x-3.5 group">
                <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-indigo-500 p-0.5 shadow-xl shadow-emerald-500/20 group-hover:scale-105 transition duration-300">
                    <div class="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center font-black text-emerald-400 text-xl">
                        ⚡
                    </div>
                </div>
                <div>
                    <span class="text-xl font-black tracking-tight text-white block group-hover:text-emerald-300 transition">
                        Extrovert<span class="text-emerald-400 font-serif italic font-normal">Nerd</span>
                    </span>
                    <span class="text-[10px] font-mono text-slate-400 tracking-wider uppercase block -mt-1 flex items-center space-x-1">
                        <span>Architect: Ravi</span>
                        <span class="text-emerald-400">●</span>
                        <span class="text-slate-400">Full-Stack (Any Tech Stack)</span>
                    </span>
                </div>
            </a>

            <!-- Navigation Links -->
            <nav class="hidden md:flex items-center space-x-8 text-sm font-semibold text-slate-300">
                <a href="/#how-we-fix" class="hover:text-white transition flex items-center space-x-1">
                    <span>How We Make It Good</span>
                    <span class="text-[10px] text-emerald-400 font-mono font-bold bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/30">BLUEPRINT</span>
                </a>
                <a href="/#tech-stack" class="hover:text-white transition flex items-center space-x-1">
                    <span>Tech Arsenal</span>
                    <span class="text-[10px] text-indigo-400 font-mono font-bold bg-indigo-500/10 px-1.5 py-0.5 rounded border border-indigo-500/30">ANY STACK</span>
                </a>
                <a href="/#services" class="hover:text-white transition">Services</a>
                <a href="/speed-checker" class="hover:text-emerald-400 flex items-center space-x-1.5 transition">
                    <span>Speed Checker</span>
                    <span class="text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-1.5 py-0.5 rounded font-mono">100/100</span>
                </a>
                <a href="/blog" class="hover:text-white transition">Case Studies</a>
                <a href="/#calculator" class="hover:text-white transition text-xs font-mono text-indigo-300">ROI Calculator</a>
                <a href="/admin" class="hover:text-emerald-400 font-mono text-xs flex items-center space-x-1 text-slate-400 border border-white/10 px-2.5 py-1.5 rounded-xl hover:border-emerald-500/40 hover:bg-slate-900 transition">
                    <span>⚡</span>
                    <span>Admin</span>
                </a>
            </nav>

            <!-- CTA Button -->
            <div class="flex items-center space-x-4">
                <a 
                    href="https://wa.me/15551234567?text={{ urlencode('Hey Ravi! I saw ExtrovertNerd and want to see how you can make my website 100/100 fast.') }}" 
                    target="_blank" 
                    rel="noopener" 
                    class="bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-black text-xs uppercase tracking-wider px-5 py-3 rounded-xl shadow-lg shadow-emerald-500/25 hover:scale-105 transition flex items-center space-x-2"
                >
                    <span>💬</span>
                    <span>WhatsApp Ravi</span>
                </a>
            </div>
        </div>
    </header>

    <!-- CONTENT WRAPPER -->
    <main class="flex-grow">
        @yield('content')
    </main>

    <!-- ARTISTIC BOUTIQUE FOOTER -->
    <footer class="bg-slate-950/90 border-t border-white/10 pt-20 pb-14 mt-28 relative">
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
                        Boutique web engineering studio led by Lead Architect Ravi. We build bespoke sub-second Laravel 11 web applications, high-converting e-commerce storefronts, and automated management dashboards with a guaranteed <strong class="text-white">100/100 Core Web Vitals score</strong>.
                    </p>
                    <div class="flex items-center space-x-3 pt-2">
                        <div class="w-10 h-10 rounded-2xl bg-slate-900 border border-emerald-500/30 flex items-center justify-center font-bold text-sm text-emerald-400 shadow-inner">
                            R
                        </div>
                        <div class="text-xs">
                            <div class="font-bold text-white">Lead Web Architect: Ravi</div>
                            <div class="text-slate-500 font-mono">Boutique Craftsmanship • Zero Plugin Bloat</div>
                        </div>
                    </div>
                </div>

                <!-- Col 2: The Rebuild Blueprint -->
                <div class="space-y-4">
                    <div class="text-xs font-mono font-bold uppercase tracking-widest text-emerald-400">The 100/100 Rebuild</div>
                    <ul class="space-y-2.5 text-sm text-slate-300">
                        <li><a href="/#how-we-fix" class="hover:text-emerald-400 transition">5-Step Engineering Blueprint</a></li>
                        <li><a href="/#calculator" class="hover:text-emerald-400 transition">Lost Revenue ROI Calculator</a></li>
                        <li><a href="/speed-checker" class="hover:text-emerald-400 transition">Free Mobile Speed Audit</a></li>
                        <li><a href="/blog" class="hover:text-emerald-400 transition">Local Engineering Teardowns</a></li>
                        <li><a href="/#architect" class="hover:text-emerald-400 transition">The Ironclad 100/100 Guarantee</a></li>
                    </ul>
                </div>

                <!-- Col 3: Commercial Target Hubs -->
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
                    &copy; {{ date('Y') }} ExtrovertNerd Agency. Hand-crafted with Laravel 11, Tailwind CSS & Alpine.js. Zero SaaS taxes.
                </div>
                <div class="flex items-center space-x-6">
                    <span class="text-emerald-400 flex items-center space-x-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span>All Builds 100% Core Web Vitals Pass</span>
                    </span>
                    <a href="https://wa.me/15551234567" target="_blank" class="hover:text-white transition">Direct WhatsApp ➔</a>
                </div>
            </div>
        </div>
    </footer>

</body>
</html>
