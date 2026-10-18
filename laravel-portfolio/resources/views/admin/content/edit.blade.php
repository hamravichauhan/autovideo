@extends('layouts.admin')

@section('title', 'Edit Case Study | ExtrovertNerd Admin')

@section('content')
<div class="space-y-6 max-w-5xl mx-auto">

    <div class="flex items-center justify-between pb-6 border-b border-white/10">
        <div>
            <a href="/admin/content" class="text-xs font-mono text-emerald-400 hover:underline flex items-center space-x-1 mb-2">
                <span>←</span>
                <span>Back to Article Manager</span>
            </a>
            <h1 class="text-2xl font-black text-white">Edit Programmatic Article</h1>
            <p class="text-xs text-slate-400 font-mono mt-0.5">Editing: {{ $filename }}</p>
        </div>
    </div>

    <form action="/admin/content/update" method="POST" class="bg-slate-900/80 border border-white/10 rounded-3xl p-6 md:p-8 space-y-6 shadow-2xl">
        <input type="hidden" name="filename" value="{{ $filename }}">

        <!-- Metadata Row 1 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="space-y-2">
                <label class="text-xs font-mono text-slate-400 uppercase tracking-wider">Article Title</label>
                <input 
                    type="text" 
                    name="title" 
                    value="{{ $meta['title'] ?? '' }}" 
                    required 
                    class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2.5 text-white text-sm focus:border-emerald-500/50 outline-none"
                >
            </div>

            <div class="space-y-2">
                <label class="text-xs font-mono text-slate-400 uppercase tracking-wider">URL Slug</label>
                <input 
                    type="text" 
                    name="slug" 
                    value="{{ $meta['slug'] ?? '' }}" 
                    required 
                    class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2.5 text-white text-sm font-mono focus:border-emerald-500/50 outline-none"
                >
            </div>
        </div>

        <!-- Metadata Row 2 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="space-y-2">
                <label class="text-xs font-mono text-slate-400 uppercase tracking-wider">Target City</label>
                <input 
                    type="text" 
                    name="city" 
                    value="{{ $meta['city'] ?? '' }}" 
                    required 
                    class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2.5 text-white text-sm focus:border-emerald-500/50 outline-none"
                >
            </div>

            <div class="space-y-2">
                <label class="text-xs font-mono text-slate-400 uppercase tracking-wider">Target Niche</label>
                <input 
                    type="text" 
                    name="niche" 
                    value="{{ $meta['niche'] ?? '' }}" 
                    required 
                    class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2.5 text-white text-sm focus:border-emerald-500/50 outline-none"
                >
            </div>
        </div>

        <!-- SEO Meta Description -->
        <div class="space-y-2">
            <label class="text-xs font-mono text-slate-400 uppercase tracking-wider">SEO Meta Description</label>
            <textarea 
                name="description" 
                rows="2" 
                class="w-full bg-slate-950 border border-white/10 rounded-xl px-4 py-2 text-white text-sm focus:border-emerald-500/50 outline-none"
            >{{ $meta['description'] ?? '' }}</textarea>
        </div>

        <!-- Markdown Body -->
        <div class="space-y-2">
            <div class="flex items-center justify-between">
                <label class="text-xs font-mono text-slate-400 uppercase tracking-wider">Article Markdown Content</label>
                <span class="text-[11px] text-slate-500 font-mono">Supports GitHub Flavored Markdown</span>
            </div>
            <textarea 
                name="body" 
                rows="18" 
                class="w-full bg-slate-950 border border-white/10 rounded-2xl p-4 text-slate-200 font-mono text-sm leading-relaxed focus:border-emerald-500/50 outline-none custom-scrollbar"
            >{{ $body }}</textarea>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-between pt-4 border-t border-white/10">
            <a href="/admin/content" class="text-xs font-mono text-slate-400 hover:text-white">Cancel</a>
            <button type="submit" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-3 rounded-xl shadow-lg shadow-emerald-500/20 transition">
                Save & Update Article ➔
            </button>
        </div>
    </form>

</div>
@endsection
