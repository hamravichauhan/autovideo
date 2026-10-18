<?php

namespace App\Services;

/**
 * Native Telegram Bot API Service for ExtrovertNerd Admin & Automated Dispatch.
 * Supports testing bot token validity, sending single photos, sending media group albums,
 * and text notifications.
 */
class TelegramService
{
    protected string $botToken;
    protected string $chatId;
    protected string $baseUrl;

    public function __construct(?string $token = null, ?string $chatId = null)
    {
        $this->botToken = trim($token ?: (getenv('TELEGRAM_BOT_TOKEN') ?: '80208646:AAHbnjZm0ZhHrxXLkamH8yF7ozkmBX2zurw'));
        $this->chatId = trim($chatId ?: (getenv('TELEGRAM_CHAT_ID') ?: '1432790039'));
        $this->baseUrl = "https://api.telegram.org/bot{$this->botToken}";
    }

    /**
     * Test the Telegram bot token and fetch bot profile details.
     */
    public function testConnection(): array
    {
        $url = "{$this->baseUrl}/getMe";
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 10,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_USERAGENT => 'ExtrovertNerd/1.0',
        ]);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);

        if ($error) {
            return [
                'ok' => false,
                'status' => 'network_error',
                'error' => $error,
            ];
        }

        $json = json_decode($response, true) ?: [];

        if ($httpCode === 200 && ($json['ok'] ?? false)) {
            return [
                'ok' => true,
                'status' => 'connected',
                'bot' => $json['result'] ?? [],
                'chat_id' => $this->chatId,
            ];
        }

        return [
            'ok' => false,
            'status' => "HTTP {$httpCode}",
            'error' => $json['description'] ?? $response,
            'code' => $httpCode,
            'hint' => ($httpCode === 401) ? 'Telegram returned 401 Unauthorized. Check if there is a missing character in your token.' : null,
        ];
    }

    /**
     * Send a single photo with optional caption.
     */
    public function sendPhoto(string $filePath, ?string $caption = null): array
    {
        if (!file_exists($filePath)) {
            return ['ok' => false, 'error' => "File not found: {$filePath}"];
        }

        $url = "{$this->baseUrl}/sendPhoto";
        $postData = [
            'chat_id' => $this->chatId,
            'photo' => new \CURLFile($filePath),
        ];

        if ($caption) {
            $postData['caption'] = $caption;
            $postData['parse_mode'] = 'HTML';
        }

        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $postData,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_USERAGENT => 'ExtrovertNerd/1.0',
        ]);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);

        if ($error) {
            return ['ok' => false, 'error' => $error];
        }

        $json = json_decode($response, true) ?: [];
        return $json;
    }

    /**
     * Send a carousel album of up to 10 slides.
     */
    public function sendMediaGroup(array $filePaths, ?string $caption = null): array
    {
        $validFiles = array_filter($filePaths, fn($p) => file_exists($p));
        if (empty($validFiles)) {
            return ['ok' => false, 'error' => 'No valid image files provided.'];
        }

        $validFiles = array_slice($validFiles, 0, 10);
        $url = "{$this->baseUrl}/sendMediaGroup";

        $postData = [
            'chat_id' => $this->chatId,
        ];

        $media = [];
        $i = 0;
        foreach ($validFiles as $file) {
            $attachName = "photo_{$i}";
            $item = [
                'type' => 'photo',
                'media' => "attach://{$attachName}",
            ];
            if ($i === 0 && $caption) {
                $item['caption'] = $caption;
                $item['parse_mode'] = 'HTML';
            }
            $media[] = $item;
            $postData[$attachName] = new \CURLFile($file);
            $i++;
        }

        $postData['media'] = json_encode($media);

        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $postData,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 45,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_USERAGENT => 'ExtrovertNerd/1.0',
        ]);

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true) ?: ['ok' => false, 'error' => $response];
    }

    /**
     * Send a text message.
     */
    public function sendMessage(string $text): array
    {
        $url = "{$this->baseUrl}/sendMessage";
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => http_build_query([
                'chat_id' => $this->chatId,
                'text' => $text,
                'parse_mode' => 'HTML',
            ]),
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 15,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_USERAGENT => 'ExtrovertNerd/1.0',
        ]);

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true) ?: ['ok' => false, 'error' => $response];
    }
}
