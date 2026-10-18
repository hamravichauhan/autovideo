<?php

namespace App\Services;

/**
 * Pure PHP Markdown & YAML Frontmatter Parser.
 *
 * Parses YAML frontmatter and renders GitHub-flavored Markdown
 * into semantic HTML with Tailwind CSS utility styling without
 * requiring external Composer dependencies.
 */
class MarkdownService
{
    /**
     * Parse a markdown file with optional YAML frontmatter.
     */
    public function parseFile(string $filePath): array
    {
        if (!file_exists($filePath)) {
            return [
                'meta' => [],
                'content' => '',
                'html' => '',
            ];
        }

        $raw = file_get_contents($filePath);
        return $this->parseString($raw);
    }

    /**
     * Parse markdown string with frontmatter.
     */
    public function parseString(string $raw): array
    {
        $meta = [];
        $markdown = $raw;

        // Check for YAML frontmatter between --- and ---
        if (preg_match('/^---\s*\n(.*?)\n---\s*\n(.*)$/s', $raw, $matches)) {
            $yaml = $matches[1];
            $markdown = $matches[2];
            $meta = $this->parseYaml($yaml);
        }

        $html = $this->markdownToHtml($markdown);

        return [
            'meta' => $meta,
            'content' => $markdown,
            'html' => $html,
        ];
    }

    /**
     * Lightweight YAML frontmatter parser for basic key/value & list structures.
     */
    protected function parseYaml(string $yaml): array
    {
        $lines = explode("\n", $yaml);
        $data = [];
        $currentListKey = null;

        foreach ($lines as $line) {
            $trimmed = trim($line);
            if ($trimmed === '' || str_starts_with($trimmed, '#')) {
                continue;
            }

            // List item: - "value"
            if (preg_match('/^-\s+["\']?(.*?)["\']?$/', $trimmed, $listMatches)) {
                if ($currentListKey) {
                    $data[$currentListKey][] = $listMatches[1];
                }
                continue;
            }

            // Key-Value: key: "value" or key:
            if (preg_match('/^([a-zA-Z0-9_-]+):\s*(.*)$/', $trimmed, $kvMatches)) {
                $key = $kvMatches[1];
                $val = trim($kvMatches[2], " \"'");

                if ($val === '') {
                    // Start of a list
                    $currentListKey = $key;
                    $data[$key] = [];
                } else {
                    $currentListKey = null;
                    $data[$key] = $val;
                }
            }
        }

        return $data;
    }

    /**
     * Converts Markdown string to clean semantic HTML with Tailwind styling.
     */
    public function markdownToHtml(string $md): string
    {
        $lines = explode("\n", $md);
        $html = [];
        $inTable = false;
        $tableRows = [];

        foreach ($lines as $line) {
            $trimmed = trim($line);

            // Table rows
            if (str_starts_with($trimmed, '|')) {
                // Table separator | :--- | :--- |
                if (preg_match('/^\|(\s*[:-]+[-| :]*)\|$/', $trimmed)) {
                    continue;
                }
                $cells = array_map('trim', explode('|', trim($trimmed, '|')));
                $tableRows[] = $cells;
                $inTable = true;
                continue;
            } elseif ($inTable) {
                // Flush accumulated table
                $html[] = $this->renderTable($tableRows);
                $tableRows = [];
                $inTable = false;
            }

            // Headings
            if (preg_match('/^######\s+(.*)$/', $trimmed, $m)) {
                $html[] = '<h6 class="text-sm font-bold text-slate-300 mt-6 mb-2">' . $this->inlineFormat($m[1]) . '</h6>';
            } elseif (preg_match('/^#####\s+(.*)$/', $trimmed, $m)) {
                $html[] = '<h5 class="text-base font-bold text-slate-200 mt-6 mb-2">' . $this->inlineFormat($m[1]) . '</h5>';
            } elseif (preg_match('/^####\s+(.*)$/', $trimmed, $m)) {
                $html[] = '<h4 class="text-lg font-bold text-white mt-8 mb-3">' . $this->inlineFormat($m[1]) . '</h4>';
            } elseif (preg_match('/^###\s+(.*)$/', $trimmed, $m)) {
                $html[] = '<h3 class="text-xl font-extrabold text-white mt-8 mb-4 tracking-tight">' . $this->inlineFormat($m[1]) . '</h3>';
            } elseif (preg_match('/^##\s+(.*)$/', $trimmed, $m)) {
                $html[] = '<h2 class="text-2xl md:text-3xl font-extrabold text-white mt-12 mb-5 pb-3 border-b border-white/10 tracking-tight">' . $this->inlineFormat($m[1]) . '</h2>';
            } elseif (preg_match('/^#\s+(.*)$/', $trimmed, $m)) {
                $html[] = '<h1 class="text-3xl md:text-4xl font-black text-white mt-4 mb-6 tracking-tight leading-tight">' . $this->inlineFormat($m[1]) . '</h1>';
            }
            // Blockquote
            elseif (preg_match('/^>\s*(.*)$/', $trimmed, $m)) {
                $html[] = '<blockquote class="border-l-4 border-emerald-400 bg-slate-900/60 p-4 rounded-r-xl text-slate-300 italic my-6 text-base leading-relaxed">' . $this->inlineFormat($m[1]) . '</blockquote>';
            }
            // Horizontal rule
            elseif ($trimmed === '---' || $trimmed === '***') {
                $html[] = '<hr class="border-white/10 my-10" />';
            }
            // List item (unordered)
            elseif (preg_match('/^[*-]\s+(.*)$/', $trimmed, $m)) {
                $html[] = '<div class="flex items-start space-x-3 my-2 text-slate-300 text-base leading-relaxed"><span class="text-emerald-400 font-bold shrink-0 mt-0.5">•</span><span>' . $this->inlineFormat($m[1]) . '</span></div>';
            }
            // List item (ordered)
            elseif (preg_match('/^([0-9]+)\.\s+(.*)$/', $trimmed, $m)) {
                $html[] = '<div class="flex items-start space-x-3 my-2.5 text-slate-300 text-base leading-relaxed"><span class="font-mono text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded shrink-0 mt-0.5">' . $m[1] . '</span><span>' . $this->inlineFormat($m[2]) . '</span></div>';
            }
            // Empty line
            elseif ($trimmed === '') {
                // spacing
            }
            // Standard paragraph
            else {
                $html[] = '<p class="text-slate-300 text-base md:text-lg leading-relaxed my-4 font-normal">' . $this->inlineFormat($line) . '</p>';
            }
        }

        if ($inTable && !empty($tableRows)) {
            $html[] = $this->renderTable($tableRows);
        }

        return implode("\n", $html);
    }

    /**
     * Formats inline Markdown syntax (bold, italic, links, inline code).
     */
    protected function inlineFormat(string $text): string
    {
        // Links: [text](url)
        $text = preg_replace_callback('/\[(.*?)\]\((.*?)\)/', function ($m) {
            $isWhatsApp = str_contains($m[2], 'wa.me');
            $class = $isWhatsApp 
                ? 'inline-flex items-center space-x-1.5 text-emerald-400 hover:text-emerald-300 font-semibold underline decoration-emerald-500/40 decoration-2 transition'
                : 'text-cyan-400 hover:text-cyan-300 font-medium underline decoration-cyan-500/30 transition';
            return '<a href="' . htmlspecialchars($m[2]) . '" target="_blank" rel="noopener" class="' . $class . '">' . $m[1] . '</a>';
        }, $text);

        // Bold: **text**
        $text = preg_replace('/\*\*(.*?)\*\*/', '<strong class="font-bold text-white">$1</strong>', $text);

        // Inline Code: `code`
        $text = preg_replace('/`(.*?)`/', '<code class="font-mono text-xs font-semibold bg-slate-900 border border-white/10 text-emerald-300 px-2 py-0.5 rounded">$1</code>', $text);

        return $text;
    }

    /**
     * Renders Markdown table rows into clean Tailwind HTML table.
     */
    protected function renderTable(array $rows): string
    {
        if (empty($rows)) {
            return '';
        }

        $html = '<div class="overflow-x-auto my-8 border border-white/10 rounded-2xl bg-slate-900/40 backdrop-blur">';
        $html .= '<table class="w-full text-left border-collapse text-sm">';

        // Header
        $header = array_shift($rows);
        $html .= '<thead class="bg-slate-950/80 border-b border-white/10 text-xs font-bold uppercase tracking-wider text-slate-400">';
        $html .= '<tr>';
        foreach ($header as $th) {
            $html .= '<th class="px-5 py-4">' . $this->inlineFormat($th) . '</th>';
        }
        $html .= '</tr></thead>';

        // Body
        $html .= '<tbody class="divide-y divide-white/5">';
        foreach ($rows as $row) {
            $html .= '<tr class="hover:bg-white/[0.02] transition">';
            foreach ($row as $td) {
                $html .= '<td class="px-5 py-4 text-slate-300 leading-normal">' . $this->inlineFormat($td) . '</td>';
            }
            $html .= '</tr>';
        }
        $html .= '</tbody></table></div>';

        return $html;
    }
}
