#!/usr/bin/env python3
"""
Enriches content/top100_websites.json with bespoke 'what_it_does' and 'hook'
fields for all 100 websites, ensuring strict ExtrovertNerd brand integrity and high-signal engineering copy.
"""

import json
from pathlib import Path

TOP_100_DESCRIPTIONS = {
    1: {
        "what_it_does": "Global payments infrastructure and financial APIs powering online checkout, billing, and fraud prevention for millions of internet businesses.",
        "hook": "How does Stripe process over $1 Trillion in checkout volume at 60fps without blocking a single PCI-compliant payment validation thread?"
    },
    2: {
        "what_it_does": "High-performance issue tracking and engineering project management tool built with local-first synchronisation architecture.",
        "hook": "Why does Linear feel faster and more responsive than native desktop binaries despite running entirely inside a browser tab?"
    },
    3: {
        "what_it_does": "Consumer electronics giant and luxury digital retail showcase presenting hardware, operating systems, and services.",
        "hook": "How does Apple orchestrate photorealistic 4K scroll-bound video scrubs on mobile browsers without dropping a single frame?"
    },
    4: {
        "what_it_does": "The world's largest developer platform and code collaboration hub hosting over 100 million open-source and enterprise repositories.",
        "hook": "Why did GitHub reject client-side SPA frameworks in favor of lightning-fast server-rendered HTML and native Web Components at planetary scale?"
    },
    5: {
        "what_it_does": "Global edge network, CDN, and cybersecurity platform providing DNS, DDoS mitigation, and serverless compute across 330+ cities worldwide.",
        "hook": "How does Cloudflare resolve 55+ million HTTP requests per second with single-digit millisecond latency across 95% of the world's population?"
    },
    6: {
        "what_it_does": "Global e-commerce marketplace, cloud infrastructure provider, and supply chain logistics network serving hundreds of millions of consumers.",
        "hook": "Why does Amazon treat every 100ms of page latency as a 1% direct loss in multi-billion dollar checkout revenue?"
    },
    7: {
        "what_it_does": "Cloud deployment platform and developer frontend cloud specializing in Next.js, React Server Components, and zero-config edge rendering.",
        "hook": "How does Vercel deliver sub-50ms Time to First Byte worldwide using Edge Middleware and streaming React Server Components?"
    },
    8: {
        "what_it_does": "Global hospitality marketplace and travel booking engine connecting millions of property hosts with international travelers.",
        "hook": "How does Airbnb render fluid 60fps map panning across tens of thousands of active listings on low-end mobile devices?"
    },
    9: {
        "what_it_does": "Digital music, podcast, and media streaming ecosystem serving over 600 million monthly active listeners worldwide.",
        "hook": "How does Spotify's web player maintain uninterrupted, hardware-decoded audio streams while users navigate complex dynamic pages?"
    },
    10: {
        "what_it_does": "Global subscription video-on-demand service streaming movies, television, and original productions to over 260 million households.",
        "hook": "How does Netflix stream high-definition interactive previews and personalized dynamic row UI across thousands of disparate screen sizes?"
    },
    11: {
        "what_it_does": "Leading commerce platform powering online storefronts, retail POS systems, and merchant operations for millions of independent brands.",
        "hook": "How does Shopify process $4+ Billion during Black Friday checkout surges without crashing or exceeding 300ms server response times?"
    },
    12: {
        "what_it_does": "Connected workspace for notes, documentation, task management, and knowledge bases built on an infinite block-based editor.",
        "hook": "How does Notion maintain buttery document scrolling when a single workspace contains tens of thousands of reactive block nodes?"
    },
    13: {
        "what_it_does": "Collaborative web-first interface design, prototyping, and vector graphics tool used by millions of product designers globally.",
        "hook": "How did Figma bring a complete C++ desktop vector engine into the browser tab at 60fps using WebAssembly and WebGL?"
    },
    14: {
        "what_it_does": "Extensible developer productivity launcher and command palette designed to automate desktop workflows and system controls.",
        "hook": "Why does Raycast's web presence boast the highest-fidelity dark-mode kinetic typography and micro-interactions on the modern web?"
    },
    15: {
        "what_it_does": "Open-source Firebase alternative providing PostgreSQL databases, authentication, instant REST APIs, and realtime edge subscriptions.",
        "hook": "How does Supabase broadcast millions of PostgreSQL row-level change events to browser clients in real time using Elixir edge nodes?"
    },
    16: {
        "what_it_does": "Creators of Tailwind CSS, Tailwind UI, and Catalyst — the modern utility-first styling system dominating contemporary web engineering.",
        "hook": "How does Tailwind Labs compile millions of possible CSS utility combinations down to a sub-10KB production stylesheet with zero runtime cost?"
    },
    17: {
        "what_it_does": "Serverless MySQL database platform powered by Vitess, offering horizontal sharding, non-blocking schema migrations, and high availability.",
        "hook": "How does PlanetScale handle zero-downtime database schema migrations on petabyte-scale production tables without locking a single row?"
    },
    18: {
        "what_it_does": "Real-time voice, video, and text communication platform serving gaming communities, developer groups, and friend circles globally.",
        "hook": "How does Discord broadcast voice channels and text chats to 200+ million active users with sub-50ms latency using Elixir and Rust?"
    },
    19: {
        "what_it_does": "Developer-first email delivery API and modern email infrastructure designed for transactional notifications and React-based templates.",
        "hook": "How does Resend render complex React email components into bulletproof multi-client HTML in under 12 milliseconds at the edge?"
    },
    20: {
        "what_it_does": "Interactive website builder and visual design platform that compiles motion design and responsive layouts directly into optimized React code.",
        "hook": "How does Framer produce published websites that score 99+ on Google Core Web Vitals while supporting complex scroll animations and physics?"
    },
    21: {
        "what_it_does": "The world's dominant search engine indexing billions of web pages and answering trillions of search queries every year.",
        "hook": "Why does Google Search keep its homepage payload under 50KB and execute searches across petabytes of index data in under 180 milliseconds?"
    },
    22: {
        "what_it_does": "Planetary video sharing and streaming platform hosting billions of user-generated videos, live streams, and shorts.",
        "hook": "How does YouTube buffer and stream 4K video instantly across erratic cellular connections using adaptive chunk streaming and AV1 codec?"
    },
    23: {
        "what_it_does": "Free, multilingual, open-collaboration online encyclopedia containing over 60 million human-curated reference articles.",
        "hook": "Why does Wikipedia serve billions of monthly pageviews on an ultra-lean PHP and caching stack with an average payload under 150KB?"
    },
    24: {
        "what_it_does": "Global microblogging and real-time social network delivering breaking news, technical discussions, and direct messaging.",
        "hook": "How does X stream breaking news feeds and high-concurrency event timelines to 500+ million users with instant optimistic UI updates?"
    },
    25: {
        "what_it_does": "The premier professional networking platform connecting over 1 billion professionals, recruiters, and companies worldwide.",
        "hook": "How does LinkedIn maintain high-throughput feed rendering and multi-tier social graph lookups without ballooning client memory usage?"
    },
    26: {
        "what_it_does": "Massive network of user-curated interest communities, forums, and discussion threads organizing the front page of the internet.",
        "hook": "Why did Reddit rewrite its core web architecture to prioritize server-rendered web components and sub-second cold boot times?"
    },
    27: {
        "what_it_does": "Live streaming platform specializing in gaming, esports, creative broadcasts, and high-concurrency interactive chat channels.",
        "hook": "How does Twitch synchronize millions of live video frames with millions of high-velocity chat messages per minute with sub-second delay?"
    },
    28: {
        "what_it_does": "Online visual communication and graphic design platform empowering non-designers to create presentations, posters, and social graphics.",
        "hook": "How does Canva render multi-layer visual canvases with hundreds of typographic elements directly in the browser using WebGL and WASM?"
    },
    29: {
        "what_it_does": "Cloud storage, file synchronization, and workspace collaboration service safeguarding billions of personal and enterprise documents.",
        "hook": "How does Dropbox synchronize multi-gigabyte files across disparate client devices using block-level deduplication and delta sync?"
    },
    30: {
        "what_it_does": "Global mobility, ridesharing, and food delivery platform matching millions of riders with drivers across 70+ countries.",
        "hook": "How does Uber's web booking engine render live GPS driver trajectories on interactive map overlays using low-bandwidth WebSockets?"
    },
    31: {
        "what_it_does": "Visual discovery engine and digital mood-board platform helping users find recipes, home inspiration, and design ideas.",
        "hook": "How does Pinterest lazy-load and layout millions of varied-height image tiles in an infinite waterfall grid without causing layout shifts?"
    },
    32: {
        "what_it_does": "The definitive question-and-answer knowledge platform for computer programmers and software engineers worldwide.",
        "hook": "Why does Stack Overflow still run its entire planetary traffic on just a few dozen bare-metal IIS/SQL servers with sub-10ms response times?"
    },
    33: {
        "what_it_does": "Curated social news website run by Y Combinator focusing on computer science, entrepreneurship, and technical intellectual curiosity.",
        "hook": "Why is Hacker News revered as one of the fastest websites on the internet, loading raw HTML in under 40ms without a single line of client JS?"
    },
    34: {
        "what_it_does": "Iconic hyper-local classified advertisements website covering housing, jobs, goods, and local community notices.",
        "hook": "Why has Craigslist kept its brutalist 1990s HTML architecture unchanged for 30 years while handling billions of views with near-zero overhead?"
    },
    35: {
        "what_it_does": "Privacy-focused search engine that protects user anonymity by refusing to track search histories or construct advertising profiles.",
        "hook": "How does DuckDuckGo deliver sub-second search results without collecting user cookies, fingerprints, or tracking telemetry?"
    },
    36: {
        "what_it_does": "Complete open-source DevOps and Git lifecycle platform offering code review, CI/CD pipelines, and security scanning.",
        "hook": "How does GitLab manage complex mono-repo code diffs with tens of thousands of lines without locking browser UI rendering?"
    },
    37: {
        "what_it_does": "Container virtualization platform and registry enabling developers to package, distribute, and run software anywhere.",
        "hook": "How does Docker Hub distribute millions of container layers across worldwide developer workstations with automated caching and deduplication?"
    },
    38: {
        "what_it_does": "Official documentation and reference manual for Kubernetes, the industry-standard container orchestration engine.",
        "hook": "Why do the Kubernetes documentation docs load instantaneously across thousands of technical pages using static site generation and Algolia search?"
    },
    39: {
        "what_it_does": "Leading API development platform enabling developers to design, test, document, and mock APIs collaboratively.",
        "hook": "How does Postman's web client execute cross-origin HTTP and gRPC network requests directly from the browser sandbox?"
    },
    40: {
        "what_it_does": "Observability, monitoring, and cloud security platform providing full-stack telemetry and performance analytics for modern enterprises.",
        "hook": "How does Datadog ingest and visualize billions of real-time server metrics per second across live interactive dashboard charts?"
    },
    41: {
        "what_it_does": "Open-source analytics and interactive metric visualization platform for time-series databases, logs, and traces.",
        "hook": "How does Grafana render tens of thousands of real-time time-series data points across custom canvas charts at 60fps?"
    },
    42: {
        "what_it_does": "Application performance monitoring and error tracking software helping engineers diagnose bugs, stack traces, and crashes in real time.",
        "hook": "How does Sentry de-obfuscate minified JavaScript stack traces and pinpoint exact source code lines in under 2 seconds at planetary scale?"
    },
    43: {
        "what_it_does": "Infrastructure automation and cloud security software company behind Terraform, Vault, Consul, and Nomad.",
        "hook": "How does HashiCorp deliver immaculate interactive infrastructure documentation with live code playground execution and zero layout jitter?"
    },
    44: {
        "what_it_does": "Distributed, RESTful search and analytics engine built on Apache Lucene for log analytics, enterprise search, and security.",
        "hook": "How does Elasticsearch index billions of JSON documents and execute full-text fuzzy queries across petabytes in milliseconds?"
    },
    45: {
        "what_it_does": "Document-oriented NoSQL database platform designed for developer productivity, flexible JSON schemas, and horizontal scaling.",
        "hook": "How does MongoDB Atlas manage automated database failovers and cross-region replica sets with sub-second switchover windows?"
    },
    46: {
        "what_it_does": "In-memory data store and caching engine used by millions of applications as a database, cache, message broker, and streaming engine.",
        "hook": "Why is Redis able to process over 1 million operations per second per CPU core using single-threaded event loop architecture?"
    },
    47: {
        "what_it_does": "Cloud management web console for Amazon Web Services, providing control over hundreds of compute, storage, and database services.",
        "hook": "How does AWS manage the sheer complexity of thousands of cloud services within a unified micro-frontend web console?"
    },
    48: {
        "what_it_does": "Enterprise cloud computing console providing infrastructure, machine learning, BigQuery analytics, and Kubernetes management.",
        "hook": "How does Google Cloud Console visualize planetary VPC networks and live Kubernetes cluster nodes with real-time health telemetry?"
    },
    49: {
        "what_it_does": "Microsoft's enterprise cloud platform portal orchestrating virtual machines, AI models, active directory, and hybrid cloud solutions.",
        "hook": "How does Azure Portal orchestrate dynamic blade-style navigation panes without losing state or blocking background management tasks?"
    },
    50: {
        "what_it_does": "Artificial intelligence research and deployment company behind ChatGPT, GPT-4o, and the industry's premier foundational models.",
        "hook": "How does OpenAI stream tokenized text responses from multi-billion parameter LLMs directly into browser interfaces with sub-100ms TTFB?"
    },
    51: {
        "what_it_does": "AI safety and research laboratory creating Claude — leading foundational AI models with 200K+ context windows and advanced reasoning.",
        "hook": "How does Claude's web interface render live interactive Artifacts alongside real-time markdown streaming without UI freeze?"
    },
    52: {
        "what_it_does": "Independent research lab generating photorealistic imagery and generative art from natural language prompts via Discord and the web.",
        "hook": "How does Midjourney display infinite grids of ultra-high-resolution AI artworks with seamless lazy-loading and GPU texture caching?"
    },
    53: {
        "what_it_does": "The central collaboration platform and open-source model hub for the machine learning community, hosting models, datasets, and spaces.",
        "hook": "How does Hugging Face serve thousands of interactive machine learning demo spaces running on distributed GPUs across the globe?"
    },
    54: {
        "what_it_does": "Data infrastructure platform for artificial intelligence providing labeled datasets and RLHF pipelines for foundation model development.",
        "hook": "How does Scale AI power multi-million dollar enterprise AI training data pipelines with millimeter-precise browser annotation tooling?"
    },
    55: {
        "what_it_does": "Applied AI research company building generative video tools, creative suites, and synthetic media generation platforms.",
        "hook": "How does Runway allow creators to edit and generate high-definition video directly in the browser using WebCodecs and WebGPU?"
    },
    56: {
        "what_it_does": "Collaborative, browser-based cloud development environment and hosting platform enabling instant code execution in 50+ languages.",
        "hook": "How does Replit spin up isolated Linux execution environments and attach collaborative code editors in under 2 seconds in a browser?"
    },
    57: {
        "what_it_does": "AI-first code editor and development environment designed to supercharge developer velocity with intelligent multi-file code generation.",
        "hook": "Why does Cursor's landing page load in under 400ms with instant code snippet previews that feel like a high-speed terminal?"
    },
    58: {
        "what_it_does": "Online cloud development platform for rapid web application prototyping, code sandboxes, and full-stack developer collaboration.",
        "hook": "How does CodeSandbox run full Node.js servers and containerized microservices directly in browser sandboxes using WebContainers?"
    },
    59: {
        "what_it_does": "Instant, full-stack web development environments running entirely within browser tabs powered by WebAssembly-based Node.js runtimes.",
        "hook": "How did StackBlitz create WebContainers — booting a full Node.js operating environment directly inside your browser in milliseconds?"
    },
    60: {
        "what_it_does": "AI pair programmer that provides autocomplete suggestions and multi-line code completions across IDEs and the web.",
        "hook": "How does GitHub Copilot stream context-aware code suggestions in under 150ms without disrupting developer keyboard cadence?"
    },
    61: {
        "what_it_does": "Workflow automation platform connecting thousands of web applications to automate repetitive business tasks and data synchronization.",
        "hook": "How does Zapier execute billions of automated multi-app workflow steps every month without dropping a single webhook trigger?"
    },
    62: {
        "what_it_does": "Visual automation platform that lets users design, build, and automate complex multi-step workflows across hundreds of web applications.",
        "hook": "How does Make render complex interactive visual workflow graphs with hundreds of interconnected nodes at 60fps in SVG?"
    },
    63: {
        "what_it_does": "Fastest way to build internal tools, database GUIs, admin panels, and customer support dashboards using pre-built components.",
        "hook": "How does Retool bind client-side UI components to SQL queries and REST APIs with zero boilerplate and optimistic state management?"
    },
    64: {
        "what_it_does": "Visual web design tool and CMS that generates clean, semantic semantic HTML, CSS, and JavaScript without manual coding.",
        "hook": "How does Webflow compile visual drag-and-drop designs into production-grade HTML and CSS that score 95+ on Core Web Vitals?"
    },
    65: {
        "what_it_does": "No-code visual development platform enabling entrepreneurs to build complete, database-backed web applications without code.",
        "hook": "How does Bubble execute complete server-side workflows and database logic while letting non-technical founders build full SaaS platforms?"
    },
    66: {
        "what_it_does": "Conversational form and survey platform designed to turn data collection into an engaging, one-question-at-a-time experience.",
        "hook": "Why do Typeforms convert 3x higher than standard HTML forms by mastering keyboard-driven kinetic micro-animations?"
    },
    67: {
        "what_it_does": "Video messaging and screen recording tool designed for asynchronous workplace communication and video feedback.",
        "hook": "How does Loom record, transcode, and generate shareable video links in the cloud the exact second a user finishes speaking?"
    },
    68: {
        "what_it_does": "Visual collaboration workspace and infinite digital whiteboard platform for distributed teams to brainstorm and map ideas.",
        "hook": "How does Miro render millions of sticky notes, wireframes, and diagrams on an infinite zoomable canvas without memory crashes?"
    },
    69: {
        "what_it_does": "Work management and project tracking platform helping teams coordinate tasks, sprint planning, and company-wide strategic goals.",
        "hook": "How does Asana keep complex Gantt charts and multi-tier task dependencies synchronized across thousands of team members simultaneously?"
    },
    70: {
        "what_it_does": "Work OS platform for managing tasks, project roadmaps, CRM pipelines, and team collaboration through customizable visual tables.",
        "hook": "How does Monday.com manage real-time updates across massive grid spreadsheets with hundreds of columns without browser freeze?"
    },
    71: {
        "what_it_does": "Pioneering project management and team communication software known for calm, deliberate, and distraction-free collaboration.",
        "hook": "Why does Basecamp advocate for simple monolithic server-rendered HTML over complex SPAs to deliver 15+ years of lightning reliability?"
    },
    72: {
        "what_it_does": "All-in-one productivity platform combining tasks, docs, chat, goals, and whiteboards into a unified workspace.",
        "hook": "How did ClickUp re-engineer its web architecture to eliminate UI lag across multi-view project dashboards?"
    },
    73: {
        "what_it_does": "Visual collaboration tool that organizes projects into boards, lists, and cards inspired by the Kanban methodology.",
        "hook": "How does Trello render fluid drag-and-drop card animations across dense task columns using hardware-accelerated CSS transforms?"
    },
    74: {
        "what_it_does": "Issue tracking and agile project management software used by thousands of engineering teams for software delivery.",
        "hook": "How does Jira process millions of enterprise issue updates and sprint transitions while supporting custom workflows and custom fields?"
    },
    75: {
        "what_it_does": "Team collaboration workspace and knowledge documentation hub for technical specifications, product requirements, and meeting notes.",
        "hook": "How does Confluence handle real-time collaborative rich-text editing across globally distributed teams without document conflicts?"
    },
    76: {
        "what_it_does": "The premier channel-based messaging platform connecting teams, software integrations, and enterprise workflows worldwide.",
        "hook": "How did Slack rebuild its desktop and web client to slash memory consumption by 50% and launch 33% faster?"
    },
    77: {
        "what_it_does": "Web version of Telegram providing encrypted instant messaging, high-capacity channels, and multi-gigabyte file transfers.",
        "hook": "Why is Telegram Web K/A recognized as one of the fastest web apps ever built, rendering millions of messages with instant zero-lag scroll?"
    },
    78: {
        "what_it_does": "Browser client for WhatsApp allowing users to mirror end-to-end encrypted chats, voice notes, and media from mobile devices.",
        "hook": "How does WhatsApp Web decrypt and synchronize thousands of end-to-end encrypted message blobs locally inside the browser IndexedDB?"
    },
    79: {
        "what_it_does": "Video communications platform providing high-definition video meetings, screen sharing, webinars, and team chat.",
        "hook": "How does Zoom's web client stream multi-party video conferences directly in a browser tab without installing plugins or apps?"
    },
    80: {
        "what_it_does": "Enterprise video conferencing platform built on Google's global infrastructure for secure, high-definition virtual meetings.",
        "hook": "How does Google Meet use WebRTC, VP9 video codecs, and client-side WebAssembly to cancel background audio noise in real time?"
    },
    81: {
        "what_it_does": "Customer engagement and cloud communications platform providing APIs for SMS, voice, video, and WhatsApp messaging.",
        "hook": "How does Twilio dispatch billions of SMS and voice calls across hundreds of global telecom carriers with sub-second API delivery?"
    },
    82: {
        "what_it_does": "Cloud-based email delivery platform sending over 100 billion marketing and transactional emails every month.",
        "hook": "How does SendGrid process and deliver 3+ billion emails per day while preserving 99.9% inbox placement rates?"
    },
    83: {
        "what_it_does": "Official documentation and release center for PostgreSQL, the world's most advanced open-source relational database system.",
        "hook": "Why does the PostgreSQL documentation site load in under 50ms worldwide using pure semantic HTML and zero tracking bloat?"
    },
    84: {
        "what_it_does": "Non-profit organization and official web hub supporting the development, distribution, and documentation of the Python programming language.",
        "hook": "Why does Python.org maintain a pristine sub-second load time across millions of developer visits using Fastly edge caching?"
    },
    85: {
        "what_it_does": "Official hub and documentation for Rust, the systems programming language empowering developers to build reliable and efficient software.",
        "hook": "Why does Rust's official website achieve a perfect 100/100 Core Web Vitals score across every single mobile audit?"
    },
    86: {
        "what_it_does": "Official portal for Go (Golang), the open-source programming language supported by Google for building simple, fast, and reliable software.",
        "hook": "How does Go.dev embed interactive, live-compiling code playgrounds directly into technical documentation pages with sub-second response?"
    },
    87: {
        "what_it_does": "Official web home and API reference for Node.js, the asynchronous event-driven JavaScript runtime built on Chrome's V8 engine.",
        "hook": "How did Node.js redesign its documentation to achieve instant client navigation and comprehensive multi-version API search?"
    },
    88: {
        "what_it_does": "Mozilla Developer Network — the definitive documentation resource for web developers learning HTML, CSS, JavaScript, and Web APIs.",
        "hook": "Why is MDN Web Docs considered the benchmark for developer documentation, serving instant offline-capable search across thousands of APIs?"
    },
    89: {
        "what_it_does": "World Wide Web Consortium — the international standards organization developing open protocols and guidelines for the Web.",
        "hook": "Why does W3C champion semantic HTML and accessible web standards that load on any device or network in under 100 milliseconds?"
    },
    90: {
        "what_it_does": "Internet Engineering Task Force — the open international community developing internet standards including TCP/IP, HTTP, and TLS.",
        "hook": "Why do IETF RFC specifications rely entirely on plain text and raw HTML to ensure perpetual accessibility across decades?"
    },
    91: {
        "what_it_does": "Low-overhead, cross-platform 3D graphics and compute API providing direct access to modern GPUs across desktop and mobile devices.",
        "hook": "How does Vulkan's web documentation explain complex hardware GPU pipelining with zero layout jitter and instant diagram renders?"
    },
    92: {
        "what_it_does": "The next-generation web standard for low-level graphics and general-purpose compute on GPUs inside browser environments.",
        "hook": "Why is WebGPU revolutionizing browser performance by allowing web apps to execute machine learning models and 3D scenes directly on the GPU?"
    },
    93: {
        "what_it_does": "Open consortium of leading hardware and software companies creating royalty-free standards for 3D graphics, VR/AR, and compute.",
        "hook": "How does Khronos Group coordinate open standards like WebGL, glTF, and OpenXR to unify visual computing across the web?"
    },
    94: {
        "what_it_does": "Developer assessment platform helping companies evaluate programming skills and conduct technical hiring challenges.",
        "hook": "How does HackerEarth securely compile and execute arbitrary code in 40+ programming languages in real time during live coding tests?"
    },
    95: {
        "what_it_does": "The premier online coding platform for software engineers practicing algorithmic problem solving and preparing for technical interviews.",
        "hook": "How does LeetCode execute code submissions against thousands of hidden test cases and return millisecond runtime percentiles in under 2 seconds?"
    },
    96: {
        "what_it_does": "Interactive online learning platform teaching programming, web development, data science, and AI through in-browser exercises.",
        "hook": "How does Codecademy create seamless interactive coding environments that validate learner code syntax directly inside the browser?"
    },
    97: {
        "what_it_does": "Non-profit community that has helped millions of people learn to code for free through hands-on curriculum and open-source projects.",
        "hook": "Why does freeCodeCamp run its entire curriculum platform on static Jamstack architecture, saving millions of dollars in server costs?"
    },
    98: {
        "what_it_does": "Global online learning platform partnering with universities and organizations to offer online courses, certifications, and degrees.",
        "hook": "How does Coursera stream interactive lecture transcripts synchronized with high-definition video playback across hundreds of languages?"
    },
    99: {
        "what_it_does": "The world's most popular language learning app using gamification, spaced repetition, and bite-sized interactive lessons.",
        "hook": "How does Duolingo use kinetic UI animations, audio synthesis, and psychology-driven micro-rewards to achieve a 98% lesson completion rate?"
    },
    100: {
        "what_it_does": "Non-profit educational organization providing free, world-class education for anyone, anywhere through interactive exercises and videos.",
        "hook": "How does Khan Academy deliver interactive math exercises and personalized learning mastery paths with zero layout shifts on low-end school tablets?"
    }
}

def main():
    json_path = Path("content/top100_websites.json")
    if not json_path.exists():
        print(f"Error: {json_path} does not exist.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entries.")

    updated_count = 0
    for site in data:
        rank = site.get("global_rank") or site.get("id")
        if rank in TOP_100_DESCRIPTIONS:
            info = TOP_100_DESCRIPTIONS[rank]
            site["what_it_does"] = info["what_it_does"]
            site["hook"] = info["hook"]
            updated_count += 1
        else:
            # Fallback if any is missing
            cat = site.get("category", "Web Architecture")
            name = site.get("name", "Platform")
            site["what_it_does"] = f"Industry-leading {cat.lower()} platform powering millions of daily interactions worldwide."
            site["hook"] = f"How does {name} maintain sub-second performance while scaling to millions of concurrent users?"
            updated_count += 1

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully enriched {updated_count} entries in {json_path}!")

if __name__ == "__main__":
    main()
