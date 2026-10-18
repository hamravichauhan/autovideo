<?php

namespace App\Http\Controllers;

class AdminSystemController
{
    protected string $baseDir;
    protected string $envFile;
    protected string $rootEnvFile;
    protected string $logFile;

    public function __construct()
    {
        $this->baseDir = project_root();
        $this->envFile = dirname(__DIR__, 2) . '/.env';
        $this->rootEnvFile = $this->baseDir . '/.env';
        $this->logFile = $this->baseDir . '/output/automation_log.json';
    }

    public function index()
    {
        // 1. Read automation log
        $automationLog = [];
        if (file_exists($this->logFile)) {
            $automationLog = json_decode(file_get_contents($this->logFile), true) ?: [];
        }

        // 2. Read environment variables
        $envVars = $this->readEnvFile();

        // 3. Last run terminal output if stored in session
        $lastOutput = session('last_terminal_output', null);
        $lastCommand = session('last_command', null);

        return view('admin.system.index', [
            'activeNav' => 'system',
            'automationLog' => $automationLog,
            'rawLog' => json_encode($automationLog, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES),
            'envVars' => $envVars,
            'lastOutput' => $lastOutput,
            'lastCommand' => $lastCommand,
        ]);
    }

    public function trigger()
    {
        $action = request('action', 'daily');
        $pythonBin = file_exists($this->baseDir . '/.venv/bin/python') ? '.venv/bin/python' : 'python3';
        $cmd = '';

        switch ($action) {
            case 'daily':
                $cmd = "{$pythonBin} -m src.main --mode daily --platform all";
                break;
            case 'pseo':
                $cmd = "{$pythonBin} -m src.main --mode pseo";
                break;
            case 'graphics':
                $cmd = "{$pythonBin} -m src.main --mode graphics --platform all";
                break;
            case 'telegram':
                $cmd = "{$pythonBin} -m src.main --mode telegram";
                break;
            case 'prospect':
                $city = escapeshellarg(request('city', 'goa'));
                $cmd = "{$pythonBin} -m src.main --mode prospect --city {$city}";
                break;
            case 'publish':
                $cmd = "{$pythonBin} -m src.main --mode publish";
                break;
            default:
                $cmd = "{$pythonBin} -m src.main --help";
        }

        $output = [];
        $returnVar = 0;
        $start = microtime(true);
        exec("cd " . escapeshellarg($this->baseDir) . " && {$cmd} 2>&1", $output, $returnVar);
        $elapsed = round(microtime(true) - $start, 2);

        $terminalOutput = implode("\n", $output);
        session(['last_terminal_output' => $terminalOutput, 'last_command' => $cmd . " (Completed in {$elapsed}s)"]);

        if ($returnVar === 0) {
            session_flash('success', "Workflow [{$action}] executed successfully in {$elapsed}s.");
        } else {
            session_flash('error', "Workflow [{$action}] exited with code {$returnVar}. Inspect terminal log below.");
        }

        redirect('/admin/system');
    }

    public function saveConfig()
    {
        $vars = [
            'BRAND_NAME' => request('brand_name', 'ExtrovertNerd'),
            'BRAND_HANDLE' => request('brand_handle', '@extrovertnerd'),
            'WEBSITE_URL' => request('website_url', 'https://extrovertnerd.com'),
            'FOUNDER_NAME' => request('founder_name', 'ExtrovertNerd'),
            'FOUNDER_ROLE' => request('founder_role', 'Web Architecture Studio'),
            'WHATSAPP_PHONE_NUMBER' => request('whatsapp_phone_number', '15551234567'),
            'WHATSAPP_DEFAULT_MESSAGE' => request('whatsapp_default_message', 'Hey ExtrovertNerd! I saw your engineering work and want a free 5-point website speed audit.'),
            'GOOGLE_FORM_INTAKE_URL' => request('google_form_intake_url', ''),
            'TELEGRAM_BOT_TOKEN' => request('telegram_bot_token', '80208646:AAHbnjZm0ZhHrxXLkamH8yF7ozkmBX2zurw'),
            'TELEGRAM_CHAT_ID' => request('telegram_chat_id', '1432790039'),
            'META_ACCESS_TOKEN' => request('meta_access_token', ''),
            'INSTAGRAM_ACCOUNT_ID' => request('instagram_account_id', ''),
            'TWITTER_API_KEY' => request('twitter_api_key', ''),
            'TWITTER_API_SECRET' => request('twitter_api_secret', ''),
            'TWITTER_ACCESS_TOKEN' => request('twitter_access_token', ''),
            'TWITTER_ACCESS_TOKEN_SECRET' => request('twitter_access_token_secret', ''),
            'TWITTER_BEARER_TOKEN' => request('twitter_bearer_token', ''),
        ];

        $envContent = "";
        foreach ($vars as $key => $val) {
            $escaped = str_contains($val, ' ') ? '"' . addslashes($val) . '"' : $val;
            $envContent .= "{$key}={$escaped}\n";
        }

        // Save to root .env
        file_put_contents($this->rootEnvFile, $envContent);
        // Save to laravel-portfolio/.env
        file_put_contents($this->envFile, $envContent);

        session_flash('success', 'Agency environment configuration saved successfully.');
        redirect('/admin/system');
    }

    public function clearLogs()
    {
        if (file_exists($this->logFile)) {
            file_put_contents($this->logFile, json_encode(['last_run' => date('Y-m-d H:i:s'), 'status' => 'cleared'], JSON_PRETTY_PRINT));
        }
        session(['last_terminal_output' => null, 'last_command' => null]);
        session_flash('success', 'Execution logs cleared.');
        redirect('/admin/system');
    }

    protected function readEnvFile(): array
    {
        $target = file_exists($this->rootEnvFile) ? $this->rootEnvFile : (file_exists($this->envFile) ? $this->envFile : null);
        $vars = [];

        if ($target && file_exists($target)) {
            $lines = file($target, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            foreach ($lines as $line) {
                if (str_starts_with(trim($line), '#') || !str_contains($line, '=')) {
                    continue;
                }
                [$k, $v] = explode('=', $line, 2);
                $vars[trim($k)] = trim($v, " \t\n\r\0\x0B\"'");
            }
        }

        return $vars;
    }
}
