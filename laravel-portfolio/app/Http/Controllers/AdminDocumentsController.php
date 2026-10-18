<?php

namespace App\Http\Controllers;

class AdminDocumentsController
{
    protected string $storagePath;
    protected string $notesFile;

    public function __construct()
    {
        $this->storagePath = project_root() . '/laravel-portfolio/storage/documents';
        $this->notesFile = project_root() . '/laravel-portfolio/storage/notes.json';

        if (!is_dir($this->storagePath)) {
            mkdir($this->storagePath, 0755, true);
        }

        // Initialize seed notes if not exists
        if (!file_exists($this->notesFile)) {
            $defaultNotes = [
                [
                    'id' => 'note_1',
                    'title' => 'Agency Standard Operating Procedures (SOP)',
                    'category' => 'Operations',
                    'updated_at' => date('Y-m-d H:i'),
                    'content' => "# ExtrovertNerd Agency SOP\n\n1. Run daily prospecting bot targeting local businesses with sub-40 mobile scores.\n2. Dispatch 4-slide before/after carousels to Instagram and X.\n3. Send 1-click WhatsApp speed audit audits within 15 minutes of response.\n4. Deliver 100/100 Core Web Vitals guarantees on all custom Laravel builds.",
                ],
                [
                    'id' => 'note_2',
                    'title' => 'Laravel 11 Sub-Second Performance Blueprint',
                    'category' => 'Engineering',
                    'updated_at' => date('Y-m-d H:i'),
                    'content' => "# Performance Architecture Checklist\n\n- Redis full-page response cache (TTFB < 150ms)\n- Inline Tailwind critical CSS + Alpine.js zero-bloat reactivity\n- AVIF/WebP image pipeline via Intervention Image\n- Zero unminified third-party analytics trackers in head tag.",
                ]
            ];
            file_put_contents($this->notesFile, json_encode($defaultNotes, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
        }
    }

    public function index()
    {
        // 1. Scan documents
        $documents = [];
        $files = glob($this->storagePath . '/*');
        foreach ($files as $file) {
            if (is_file($file)) {
                $documents[] = [
                    'name' => basename($file),
                    'size' => round(filesize($file) / 1024, 1) . ' KB',
                    'modified' => date('Y-m-d H:i', filemtime($file)),
                    'ext' => strtolower(pathinfo($file, PATHINFO_EXTENSION)),
                ];
            }
        }

        // 2. Read notes
        $notes = [];
        if (file_exists($this->notesFile)) {
            $notes = json_decode(file_get_contents($this->notesFile), true) ?: [];
        }

        return view('admin.documents.index', [
            'activeNav' => 'documents',
            'documents' => $documents,
            'notes' => $notes,
        ]);
    }

    public function upload()
    {
        if (isset($_FILES['document']) && $_FILES['document']['error'] === UPLOAD_ERR_OK) {
            $name = basename($_FILES['document']['name']);
            $target = $this->storagePath . '/' . preg_replace('/[^a-zA-Z0-9_\.-]/', '_', $name);
            move_uploaded_file($_FILES['document']['tmp_name'], $target);
            session_flash('success', "Document '{$name}' uploaded securely.");
        } else {
            session_flash('error', 'Failed to upload document. Check file permissions.');
        }

        redirect('/admin/documents');
    }

    public function delete()
    {
        $filename = request('file');
        if ($filename) {
            $target = $this->storagePath . '/' . basename($filename);
            if (file_exists($target)) {
                unlink($target);
                session_flash('success', "Document '{$filename}' deleted.");
            }
        }

        redirect('/admin/documents');
    }

    public function saveNote()
    {
        $id = request('id', 'note_' . time());
        $title = request('title', 'Untitled Note');
        $category = request('category', 'General');
        $content = request('content', '');

        $notes = [];
        if (file_exists($this->notesFile)) {
            $notes = json_decode(file_get_contents($this->notesFile), true) ?: [];
        }

        $found = false;
        foreach ($notes as &$n) {
            if ($n['id'] === $id) {
                $n['title'] = $title;
                $n['category'] = $category;
                $n['content'] = $content;
                $n['updated_at'] = date('Y-m-d H:i');
                $found = true;
                break;
            }
        }

        if (!$found) {
            array_unshift($notes, [
                'id' => $id,
                'title' => $title,
                'category' => $category,
                'updated_at' => date('Y-m-d H:i'),
                'content' => $content,
            ]);
        }

        file_put_contents($this->notesFile, json_encode($notes, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
        session_flash('success', "Knowledge base note '{$title}' saved.");
        redirect('/admin/documents');
    }

    public function deleteNote()
    {
        $id = request('id');
        if ($id && file_exists($this->notesFile)) {
            $notes = json_decode(file_get_contents($this->notesFile), true) ?: [];
            $notes = array_values(array_filter($notes, fn($n) => ($n['id'] ?? '') !== $id));
            file_put_contents($this->notesFile, json_encode($notes, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
            session_flash('success', 'Note removed from knowledge base.');
        }
        redirect('/admin/documents');
    }
}
