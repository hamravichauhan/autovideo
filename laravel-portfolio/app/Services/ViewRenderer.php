<?php

namespace App\Services;

/**
 * Lightweight Blade-Compatible View Renderer.
 *
 * Compiles and renders Blade templates including @extends, @section,
 * @yield, @foreach, @if, and {{ }} tags without requiring the full
 * Illuminate/View framework package for local standalone execution.
 */
class ViewRenderer
{
    protected static string $viewsPath;
    protected static array $sections = [];
    protected static ?string $layout = null;

    public static function render(string $viewName, array $data = []): string
    {
        self::$viewsPath = dirname(__DIR__, 2) . '/resources/views';
        self::$sections = [];
        self::$layout = null;

        $viewFile = self::resolveViewPath($viewName);
        if (!file_exists($viewFile)) {
            throw new \RuntimeException("View [{$viewName}] not found at {$viewFile}");
        }

        extract($data);
        $content = file_get_contents($viewFile);

        // Parse @extends
        if (preg_match("/@extends\(['\"](.*?)['\"]\)/", $content, $matches)) {
            self::$layout = $matches[1];
            $content = str_replace($matches[0], '', $content);
        }

        // Parse inline @section('key', 'value')
        $content = preg_replace_callback("/@section\(['\"](.*?)['\"],\s*['\"](.*?)['\"]\)/", function ($m) {
            self::$sections[$m[1]] = $m[2];
            return '';
        }, $content);

        // Parse block @section('key') ... @endsection
        $content = preg_replace_callback("/@section\(['\"](.*?)['\"]\)(.*?)@endsection/s", function ($m) {
            self::$sections[$m[1]] = $m[2];
            return '';
        }, $content);

        // If no explicit content section, treat remaining content as content
        if (!isset(self::$sections['content']) && trim($content) !== '') {
            self::$sections['content'] = $content;
        }

        // If layout exists, compile and render through layout
        if (self::$layout) {
            $layoutFile = self::resolveViewPath(self::$layout);
            if (!file_exists($layoutFile)) {
                throw new \RuntimeException("Layout [" . self::$layout . "] not found at {$layoutFile}");
            }
            $layoutContent = file_get_contents($layoutFile);

            // Replace @yield('key', 'default')
            $compiled = preg_replace_callback("/@yield\(['\"](.*?)['\"](?:,\s*['\"](.*?)['\"])?\)/", function ($m) {
                $key = $m[1];
                $default = $m[2] ?? '';
                return self::$sections[$key] ?? $default;
            }, $layoutContent);

            return self::evaluatePhp($compiled, $data);
        }

        return self::evaluatePhp($content, $data);
    }

    protected static function resolveViewPath(string $view): string
    {
        $normalized = str_replace('.', '/', $view);
        return self::$viewsPath . '/' . $normalized . '.blade.php';
    }

    /**
     * Replace blade directives that contain balanced parentheses.
     */
    protected static function replaceBalancedDirective(string $content, string $directive, string $phpPrefix): string
    {
        $offset = 0;
        $needle = '@' . $directive;
        $needleLen = strlen($needle);

        while (($pos = strpos($content, $needle, $offset)) !== false) {
            // Find opening parenthesis
            $parenStart = strpos($content, '(', $pos);
            if ($parenStart === false) {
                break;
            }

            // Ensure only optional whitespace between @directive and '('
            $between = substr($content, $pos + $needleLen, $parenStart - ($pos + $needleLen));
            if (trim($between) !== '') {
                $offset = $pos + 1;
                continue;
            }

            // Match balanced parentheses
            $depth = 1;
            $i = $parenStart + 1;
            $len = strlen($content);
            while ($i < $len && $depth > 0) {
                if ($content[$i] === '(') {
                    $depth++;
                } elseif ($content[$i] === ')') {
                    $depth--;
                }
                $i++;
            }

            if ($depth === 0) {
                // Extract inner expression
                $expr = substr($content, $parenStart + 1, ($i - 1) - ($parenStart + 1));
                $replacement = "<?php " . $phpPrefix . " (" . $expr . "): ?>";
                $content = substr_replace($content, $replacement, $pos, $i - $pos);
                $offset = $pos + strlen($replacement);
            } else {
                $offset = $pos + 1;
            }
        }

        return $content;
    }

    protected static function evaluatePhp(string $template, array $data): string
    {
        // 0. @php ... @endphp code blocks
        $template = preg_replace('/@php\b(.*?)@endphp/s', '<?php $1; ?>', $template);

        // 1. Raw {!! $var !!}
        $template = preg_replace('/\{\!\!(.*?)\!\!\}/s', '<?php echo $1; ?>', $template);

        // 2. Escaped {{ $var }}
        $template = preg_replace('/\{\{(.*?)\}\}/s', '<?php echo htmlspecialchars((string)($1), ENT_QUOTES, "UTF-8"); ?>', $template);

        // 3. Balanced directives: @if, @elseif, @foreach, @unless
        $template = self::replaceBalancedDirective($template, 'if', 'if');
        $template = self::replaceBalancedDirective($template, 'elseif', 'elseif');
        $template = self::replaceBalancedDirective($template, 'foreach', 'foreach');
        $template = self::replaceBalancedDirective($template, 'unless', 'if (!');

        // 4. Simple directives
        $template = preg_replace('/@else\b/', '<?php else: ?>', $template);
        $template = preg_replace('/@endif\b/', '<?php endif; ?>', $template);
        $template = preg_replace('/@endforeach\b/', '<?php endforeach; ?>', $template);
        $template = preg_replace('/@endunless\b/', '<?php endif; ?>', $template);

        // Evaluate in isolated scope
        ob_start();
        extract($data);
        eval('?>' . $template);
        return ob_get_clean();
    }
}
