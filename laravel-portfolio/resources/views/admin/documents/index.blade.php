@extends('layouts.admin')

@section('title', 'Documents & Knowledge Base | ExtrovertNerd Admin')

@section('content')
<div class="space-y-8 max-w-7xl mx-auto" x-data="{ 
    activeTab: 'notes', 
    uploadModal: false,
    selectedNote: @json($notes[0] ?? ['id' => '', 'title' => '', 'category' => 'General', 'content' => ''])
}">

    <!-- HEADER -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
            <div class="text-xs font-mono text-emerald-400 font-bold uppercase tracking-wider mb-1">
                REPOSITORY & KNOWLEDGE VAULT
            </div>
            <h1 class="text-3xl font-black text-white tracking-tight">
                Document Vault & <span class="font-serif italic font-normal text-emerald-400">Engineering Notes</span>
            </h1>
            <p class="text-slate-400 text-sm mt-1">
                Store client project briefs, audit contracts, and maintain your internal engineering blueprints.
            </p>
        </div>

        <!-- Tab Selector -->
        <div class="flex items-center space-x-2 bg-slate-900 p-1.5 rounded-2xl border border-white/10 font-mono text-xs">
            <button 
                @click="activeTab = 'notes'" 
                :class="activeTab === 'notes' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'"
                class="px-4 py-2 rounded-xl transition"
            >
                📝 Knowledge Scratchpad
            </button>
            <button 
                @click="activeTab = 'files'" 
                :class="activeTab === 'files' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'"
                class="px-4 py-2 rounded-xl transition"
            >
                📁 Client Files & Briefs ({{ count($documents) }})
            </button>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- 1. MARKDOWN SCRATCHPAD & KNOWLEDGE BASE                        -->
    <!-- ============================================================== -->
    <div x-show="activeTab === 'notes'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Left Column: Notes List -->
        <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 space-y-4">
            <div class="flex items-center justify-between border-b border-white/10 pb-3">
                <h3 class="text-base font-bold text-white">Saved SOPs & Blueprints</h3>
                <button 
                    @click="selectedNote = { id: 'note_' + Date.now(), title: 'New Note', category: 'General', content: '# New Note Title\n\nWrite engineering notes here...' }"
                    class="text-xs font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 rounded-lg hover:bg-emerald-500/20"
                >
                    + New Note
                </button>
            </div>

            <div class="space-y-2.5">
                @foreach($notes as $n)
                <div 
                    @click='selectedNote = @json($n)'
                    :class="selectedNote.id === '{{ $n['id'] }}' ? 'border-emerald-500 bg-slate-950' : 'border-white/5 bg-slate-950/60 hover:border-white/20'"
                    class="p-3.5 rounded-2xl border cursor-pointer transition space-y-1"
                >
                    <div class="flex items-center justify-between text-[10px] font-mono">
                        <span class="text-emerald-400 font-bold uppercase">{{ $n['category'] ?? 'General' }}</span>
                        <span class="text-slate-500">{{ $n['updated_at'] ?? '' }}</span>
                    </div>
                    <div class="text-sm font-bold text-white truncate">{{ $n['title'] }}</div>
                </div>
                @endforeach
            </div>
        </div>

        <!-- Right Column: Note Editor -->
        <div class="lg:col-span-2 bg-slate-900/80 border border-white/10 rounded-3xl p-6 md:p-8 space-y-5 shadow-2xl">
            <form action="/admin/documents/notes/save" method="POST" class="space-y-4">
                <input type="hidden" name="id" :value="selectedNote.id">

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div class="sm:col-span-2 space-y-1">
                        <label class="text-xs font-mono text-slate-400 uppercase">Note Title</label>
                        <input 
                            type="text" 
                            name="title" 
                            :value="selectedNote.title" 
                            required 
                            class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white font-bold text-sm focus:border-emerald-500 outline-none"
                        >
                    </div>

                    <div class="space-y-1">
                        <label class="text-xs font-mono text-slate-400 uppercase">Category</label>
                        <select name="category" class="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-slate-200 text-xs font-mono focus:border-emerald-500 outline-none">
                            <option value="Engineering">Engineering</option>
                            <option value="Operations">Operations</option>
                            <option value="Client Log">Client Log</option>
                            <option value="Outreach">Outreach</option>
                        </select>
                    </div>
                </div>

                <div class="space-y-1">
                    <div class="flex items-center justify-between">
                        <label class="text-xs font-mono text-slate-400 uppercase">Markdown Scratchpad Content</label>
                        <span class="text-[11px] text-slate-500 font-mono">Auto-formats Markdown</span>
                    </div>
                    <textarea 
                        name="content" 
                        rows="16" 
                        x-model="selectedNote.content"
                        class="w-full bg-slate-950 border border-white/10 rounded-2xl p-4 font-mono text-xs text-slate-200 leading-relaxed focus:border-emerald-500 outline-none custom-scrollbar"
                    ></textarea>
                </div>

                <div class="flex items-center justify-between pt-3 border-t border-white/10">
                    <a 
                        :href="'/admin/documents/notes/delete?id=' + selectedNote.id" 
                        onclick="return confirm('Delete this note?');" 
                        class="text-xs font-mono text-rose-400 hover:underline"
                    >
                        Delete Note
                    </a>
                    <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-2.5 rounded-xl shadow-lg shadow-emerald-500/20 transition">
                        Save Changes ➔
                    </button>
                </div>
            </form>
        </div>

    </div>

    <!-- ============================================================== -->
    <!-- 2. CLIENT BRIEFS & SECURE FILE MANAGER                         -->
    <!-- ============================================================== -->
    <div x-show="activeTab === 'files'" class="space-y-6">

        <!-- Upload Bar -->
        <div class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 md:p-8 shadow-xl">
            <h3 class="text-lg font-bold text-white mb-2">Upload Client Assets or Contract Briefs</h3>
            <p class="text-xs text-slate-400 mb-6">Files are securely stored in storage/documents/ with zero public indexing.</p>

            <form action="/admin/documents/upload" method="POST" enctype="multipart/form-data" class="flex flex-col sm:flex-row items-center gap-4">
                <input 
                    type="file" 
                    name="document" 
                    required 
                    class="w-full sm:w-auto bg-slate-950 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-slate-300 font-mono file:mr-4 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-emerald-500 file:text-slate-950"
                >
                <button type="submit" class="w-full sm:w-auto bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-3 rounded-xl shadow-lg transition">
                    Upload File ➔
                </button>
            </form>
        </div>

        <!-- Files List Table -->
        <div class="bg-slate-900/80 border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
            <div class="p-5 border-b border-white/10">
                <h3 class="text-base font-bold text-white">Repository Files ({{ count($documents) }})</h3>
            </div>

            @if(empty($documents))
            <div class="text-center py-12 text-slate-500 text-xs font-mono">
                No documents uploaded yet. Upload client contracts, RFP briefs, or brand kits above.
            </div>
            @else
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead class="bg-slate-950 text-xs font-mono text-slate-400 uppercase">
                        <tr>
                            <th class="py-3 px-6">File Name</th>
                            <th class="py-3 px-4">Size</th>
                            <th class="py-3 px-4">Uploaded</th>
                            <th class="py-3 px-6 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 font-mono text-xs">
                        @foreach($documents as $doc)
                        <tr class="hover:bg-slate-800/40">
                            <td class="py-4 px-6 font-bold text-white flex items-center space-x-2">
                                <span>📄</span>
                                <span>{{ $doc['name'] }}</span>
                            </td>
                            <td class="py-4 px-4 text-slate-400">{{ $doc['size'] }}</td>
                            <td class="py-4 px-4 text-slate-500">{{ $doc['modified'] }}</td>
                            <td class="py-4 px-6 text-right">
                                <a href="/admin/documents/delete?file={{ urlencode($doc['name']) }}" onclick="return confirm('Delete document?');" class="text-rose-400 hover:underline">
                                    Delete ✕
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

</div>
@endsection
