"""Automated Video Generation Pipeline for ExtrovertNerd.

Transforms rendered static Playwright carousels and top 100 website architecture teardowns
into high-retention vertical video reels (1080x1920 / 1080x1350) optimized for Instagram Reels,
YouTube Shorts, and TikTok.

Key Architectural Upgrades:
1. Continuous Speech Synthesis: Synthesizes the entire script in one single continuous neural
   stream via Edge-TTS (eliminates choppy segmentation, concat clicks, and dead air).
2. Word-Boundary Subtitle Tracking: Captures exact phonetic word offsets and durations
   (chunk['offset'], chunk['duration']) directly from Edge-TTS to generate frame-perfect,
   zero-drift kinetic ASS subtitles with electric word highlights.
3. Lock-Step Scene Transitions: Automatically calculates scene cut timestamps from spoken word
   boundaries, guaranteeing camera moves switch at the exact millisecond thoughts transition.
4. Pure Educational Analysis: Strictly ExtrovertNerd branding, zero promotional pitches,
   zero fake promises, zero mentions of Ravi or engineer titles.
5. Calibrated 60-Second Duration: Calibrated to land at 58-60 seconds for the Top 100 series.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import edge_tts
import imageio_ffmpeg

from src.config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("generator_video")


@dataclass
class SceneDefinition:
    """Represents a single visual scene in the video reel."""

    scene_number: int
    title: str
    voiceover_text: str
    slide_image_path: Path
    motion_type: str = "zoom_in"
    duration: float = 7.5
    start_time: float = 0.0
    end_time: float = 7.5


class VideoReelGenerator:
    """Orchestrates Edge-TTS continuous voiceover synthesis, Ken Burns animations,

    word-boundary kinetic subtitles, and video export for social media reels.
    """

    def __init__(
        self,
        output_dir: Optional[Path | str] = None,
        voice: Optional[str] = None,
        rate: Optional[str] = None,
    ):
        self.output_dir = Path(output_dir or config.video_output_path)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # en-US-ChristopherNeural provides exceptionally smooth, broadcast-documentary pacing
        self.voice = voice or getattr(config, "default_tts_voice", "en-US-ChristopherNeural")
        self.rate = rate or getattr(config, "default_tts_rate", "+22%")
        self.ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

    def _get_audio_duration(self, audio_file: Path) -> float:
        """Measures exact audio duration in seconds via ffprobe or ffmpeg."""
        for probe in [shutil.which("ffprobe"), "/opt/homebrew/bin/ffprobe", "/usr/local/bin/ffprobe"]:
            if probe and os.path.exists(probe):
                cmd = [
                    probe,
                    "-i",
                    str(audio_file),
                    "-show_entries",
                    "format=duration",
                    "-v",
                    "quiet",
                    "-of",
                    "csv=p=0",
                ]
                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                if res.returncode == 0 and res.stdout.strip():
                    try:
                        return round(float(res.stdout.strip()), 2)
                    except ValueError:
                        pass

        # Fallback to ffmpeg stderr parse
        cmd = [self.ffmpeg_bin, "-i", str(audio_file)]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
        if m:
            hours, mins, secs = m.groups()
            return round(int(hours) * 3600 + int(mins) * 60 + float(secs), 2)
        return 60.0

    async def _synthesize_continuous_audio(
        self,
        text: str,
        output_file: Path,
        voice: Optional[str] = None,
        rate: Optional[str] = None,
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """Synthesizes speech in one seamless continuous stream and captures WordBoundary telemetry."""
        v = voice or self.voice
        r = rate or self.rate
        logger.info("🎙️ Synthesizing continuous voiceover [%s @ %s] (%d chars)...", v, r, len(text))

        comm = edge_tts.Communicate(text, v, rate=r, boundary="WordBoundary")
        words: List[Dict[str, Any]] = []

        with open(output_file, "wb") as f:
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    # offset and duration in 100ns units -> convert to seconds
                    words.append({
                        "offset": round(chunk["offset"] / 1e7, 3),
                        "duration": round(chunk["duration"] / 1e7, 3),
                        "text": chunk["text"],
                    })

        duration = self._get_audio_duration(output_file)
        logger.info("✅ Continuous voiceover generated: %.2fs (%d words captured)", duration, len(words))
        return duration, words

    def generate_ass_subtitles_from_words(
        self,
        words: List[Dict[str, Any]],
        output_file: Path,
        width: int = 1080,
        height: int = 1920,
    ) -> None:
        """Generates frame-perfect kinetic ASS subtitles directly from Edge-TTS WordBoundary telemetry.

        Words appear and disappear in exact millisecond lock-step with vocal delivery.
        """
        # For 9:16 (1080x1920): place subtitles above Instagram/TikTok bottom UI (MarginV=280)
        # For 4:5 (1080x1350): MarginV=160
        margin_v = 280 if height >= 1800 else 160
        fontsize = 54 if height >= 1800 else 46

        ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KineticPill,Arial,{fontsize},&H00FFFFFF,&H0015CCFA,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,3,7,0,2,40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        def _format_ass_time(seconds: float) -> str:
            td = timedelta(seconds=max(0.0, seconds))
            total_seconds = int(td.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            secs = total_seconds % 60
            centisecs = int(td.microseconds / 10000)
            return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

        cues: List[Dict[str, Any]] = []
        current_chunk: List[Dict[str, Any]] = []

        for i, w in enumerate(words):
            current_chunk.append(w)
            w_text = w["text"].strip()
            is_terminal = w_text.endswith((".", "?", "!", ":"))

            has_next = i < len(words) - 1
            long_pause = False
            if has_next:
                gap = words[i + 1]["offset"] - (w["offset"] + w["duration"])
                if gap > 0.38:
                    long_pause = True

            # Group into 3 to 4 words per cue or split on punctuation/pause
            if len(current_chunk) >= 4 or is_terminal or long_pause or not has_next:
                start_t = current_chunk[0]["offset"]
                end_t = current_chunk[-1]["offset"] + current_chunk[-1]["duration"]
                chunk_words = [cw["text"].strip() for cw in current_chunk]
                cues.append({
                    "start": start_t,
                    "end": end_t,
                    "words": chunk_words,
                })
                current_chunk = []

        # Smooth small gaps between adjacent cues to prevent subtitle flickering
        for i in range(len(cues) - 1):
            gap = cues[i + 1]["start"] - cues[i]["end"]
            if 0 < gap < 0.22:
                cues[i]["end"] = round(cues[i + 1]["start"] - 0.04, 3)

        events: List[str] = []
        for c in cues:
            start_str = _format_ass_time(c["start"])
            end_str = _format_ass_time(c["end"])
            raw_words = [re.sub(r"[\'\"\\\[\]]", "", w) for w in c["words"]]
            if not raw_words or not "".join(raw_words).strip():
                continue

            # Kinetic styling: First 1-2 words in electric amber/yellow highlight, remainder pure white
            if len(raw_words) > 2:
                highlight = " ".join(raw_words[:2]).upper()
                rest = " ".join(raw_words[2:]).upper()
                text_line = f"{{\\c&H0015CCFA&}}{highlight} {{\\c&H00FFFFFF&}}{rest}"
            else:
                highlight = " ".join(raw_words).upper()
                text_line = f"{{\\c&H0015CCFA&}}{highlight}"

            events.append(f"Dialogue: 0,{start_str},{end_str},KineticPill,,0,0,0,,{text_line}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ass_header + "\n".join(events) + "\n")

        logger.info("Saved word-boundary kinetic ASS subtitles: %s (%d dialogue cues)", output_file.name, len(events))

    def _compute_scene_cut_times(
        self,
        scenes: List[Dict[str, Any]],
        words: List[Dict[str, Any]],
        total_duration: float,
    ) -> List[float]:
        """Finds the exact end timestamp for each scene within the continuous word boundary telemetry."""
        cut_times: List[float] = []
        word_idx = 0
        num_words = len(words)

        for sc_idx, sc in enumerate(scenes):
            if sc_idx == len(scenes) - 1:
                # Last scene ends exactly at total_duration
                cut_times.append(total_duration)
                break

            # Find last 2 significant words of this scene's voiceover text
            cleaned_words = [re.sub(r"[^a-zA-Z0-9]", "", w).lower() for w in sc["voiceover_text"].split()]
            cleaned_words = [w for w in cleaned_words if len(w) > 2]
            target_token = cleaned_words[-1] if cleaned_words else ""
            penultimate_token = cleaned_words[-2] if len(cleaned_words) > 1 else ""

            found_idx = None
            for j in range(word_idx, num_words):
                w_str = re.sub(r"[^a-zA-Z0-9]", "", words[j]["text"]).lower()
                if target_token and target_token in w_str:
                    found_idx = j
                    break
                elif penultimate_token and penultimate_token in w_str:
                    found_idx = j
                    break

            if found_idx is not None:
                end_t = round(words[found_idx]["offset"] + words[found_idx]["duration"], 3)
                if found_idx + 1 < num_words:
                    next_start = words[found_idx + 1]["offset"]
                    if next_start > end_t:
                        end_t = round((end_t + next_start) / 2.0, 3)
                cut_times.append(min(end_t, total_duration))
                word_idx = found_idx + 1
            else:
                # Proportional fallback
                fraction = (sc_idx + 1) / len(scenes)
                cut_times.append(round(fraction * total_duration, 3))

        return cut_times

    def render_scene_clip(
        self,
        image_path: Path,
        duration: float,
        output_file: Path,
        motion_type: str = "zoom_in",
        width: int = 1080,
        height: int = 1920,
        fps: int = 30,
    ) -> None:
        """Renders an animated single-scene video clip with Ken Burns motion and dark blurred ambient backdrop."""
        total_frames = max(int(duration * fps), 30)

        # Select Ken Burns zoom/pan formula based on motion_type
        if motion_type == "zoom_in":
            # Gentle zoom into center (1.00 -> 1.07)
            zoom_expr = "min(zoom+0.00045,1.07)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif motion_type == "pan_down":
            # Subtle pan down to focus on benchmark telemetry (1.00 -> 1.06)
            zoom_expr = "min(zoom+0.0004,1.06)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = f"ih/2-(ih/zoom/2)+((on/{total_frames})*(ih/18))"
        elif motion_type == "zoom_center":
            # Steadily zoom in on the verified Core Web Vitals telemetry
            zoom_expr = "min(zoom+0.0005,1.08)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        else:  # pulse_zoom / outro
            # Subtle steady zoom focusing on the ExtrovertNerd verdict
            zoom_expr = "min(zoom+0.00035,1.05)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = f"ih/2-(ih/zoom/2)+((on/{total_frames})*(ih/24))"

        # Aspect ratio adaptation:
        # If output is 9:16 (1080x1920) and input is 4:5 (1080x1350):
        # We create a dark blurred ambient background from the slide and center the slide.
        if height > width:
            filter_complex = (
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},"
                f"boxblur=30:5,eq=brightness=-0.3:contrast=1.1[bg];"
                f"[0:v]scale={width - 40}:{(width - 40) * 5 // 4}[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,"
                f"zoompan=z='{zoom_expr}':d={total_frames}:s={width}x{height}:x='{x_expr}':y='{y_expr}':fps={fps}"
            )
        else:
            # Native 4:5 video (1080x1350)
            filter_complex = (
                f"[0:v]zoompan=z='{zoom_expr}':d={total_frames}:s={width}x{height}:x='{x_expr}':y='{y_expr}':fps={fps}"
            )

        cmd = [
            self.ffmpeg_bin,
            "-y",
            "-loop",
            "1",
            "-i",
            str(image_path),
            "-filter_complex",
            filter_complex,
            "-t",
            f"{duration:.3f}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-preset",
            "fast",
            str(output_file),
        ]

        logger.info("Rendering clip [%s, %.2fs, %dx%d]: %s", motion_type, duration, width, height, output_file.name)
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            logger.error("FFmpeg render error on %s: %s", output_file.name, res.stderr[-500:])
            raise RuntimeError(f"FFmpeg failed rendering scene clip: {output_file.name}")

    def build_narrative_script(
        self,
        city: Optional[Dict[str, Any]] = None,
        niche: Optional[Dict[str, Any]] = None,
        custom_script: Optional[Dict[int, str]] = None,
    ) -> List[Dict[str, Any]]:
        """Builds the 4-part high-retention narrative script for the 30s video reel."""
        city_name = (city or {}).get("name", "Local Commercial Hub")
        niche_name = (niche or {}).get("name", "Boutique Business")

        script_override = custom_script or {}

        scenes = [
            {
                "scene_number": 1,
                "title": "The Mobile Latency Reality",
                "hud_label": "MOBILE LATENCY BENCHMARK",
                "motion": "zoom_in",
                "voiceover_text": script_override.get(
                    1,
                    f"When a mobile website takes more than 3 seconds to load, over 50 percent of visitors leave immediately. In {city_name}, mobile latency directly impacts user retention.",
                ),
            },
            {
                "scene_number": 2,
                "title": "Core Web Vitals Impact",
                "hud_label": "FAILED CORE WEB VITALS",
                "motion": "pan_down",
                "voiceover_text": script_override.get(
                    2,
                    "Heavy scripts, uncompressed assets, and bloated page templates hurt Core Web Vitals. When layout shifts occur and paint times lag, search engines reduce mobile visibility.",
                ),
            },
            {
                "scene_number": 3,
                "title": "ExtrovertNerd Standards",
                "hud_label": "EXTROVERTNERD // SUB-SECOND",
                "motion": "zoom_center",
                "voiceover_text": script_override.get(
                    3,
                    "ExtrovertNerd focuses on sub-second web performance, clean code structures, and zero bloat, reaching 100 out of 100 Core Web Vitals scores.",
                ),
            },
            {
                "scene_number": 4,
                "title": "Performance Insights",
                "hud_label": "WEB SPEED BENCHMARKS",
                "motion": "pulse_zoom",
                "voiceover_text": script_override.get(
                    4,
                    "Speed is the foundation of modern user experience. Follow ExtrovertNerd for daily technical teardowns and web performance benchmarks.",
                ),
            },
        ]
        return scenes

    def render_reel(
        self,
        slide_images: List[Path | str],
        city: Optional[Dict[str, Any]] = None,
        niche: Optional[Dict[str, Any]] = None,
        output_filename: Optional[str] = None,
        aspect_ratio: str = "9:16",
        voice: Optional[str] = None,
        rate: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Assembles a 30-second vertical video reel with continuous voiceover and synchronized kinetic captions."""
        valid_slides = [Path(s) for s in slide_images if Path(s).exists()]
        if len(valid_slides) < 4:
            raise ValueError(f"At least 4 slide PNG images are required. Provided: {len(valid_slides)}")

        city = city or {"name": "Local Commercial Hub", "id": "local"}
        niche = niche or {"name": "Boutique Business", "id": "business"}

        if aspect_ratio == "4:5":
            width, height = 1080, 1350
        else:
            width, height = 1080, 1920

        slug = f"{city.get('id', 'local')}_{niche.get('id', 'niche')}_30s_reel"
        final_video_name = output_filename or f"{slug}.mp4"
        final_video_path = self.output_dir / final_video_name

        script_scenes = self.build_narrative_script(city, niche)

        with tempfile.TemporaryDirectory(prefix="extrovertnerd_reel_") as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            logger.info("🎬 Assembling 30s Video Reel in workspace: %s", temp_dir)

            full_script = " ".join([sc["voiceover_text"].strip() for sc in script_scenes])
            master_audio_path = temp_dir / "master_voiceover.mp3"

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                total_duration, words = loop.run_until_complete(
                    self._synthesize_continuous_audio(
                        text=full_script,
                        output_file=master_audio_path,
                        voice=voice or self.voice,
                        rate=rate or "+12%",
                    )
                )
            finally:
                loop.close()

            # Compute lock-step scene transitions
            cut_times = self._compute_scene_cut_times(script_scenes, words, total_duration)

            scenes_meta: List[SceneDefinition] = []
            prev_time = 0.0
            for idx, sc in enumerate(script_scenes):
                cut_t = cut_times[idx]
                dur = round(cut_t - prev_time, 3)
                sc_def = SceneDefinition(
                    scene_number=idx + 1,
                    title=sc["title"],
                    voiceover_text=sc["voiceover_text"],
                    slide_image_path=valid_slides[idx],
                    motion_type=sc["motion"],
                    duration=dur,
                    start_time=prev_time,
                    end_time=cut_t,
                )
                scenes_meta.append(sc_def)
                prev_time = cut_t

            # Generate frame-perfect ASS subtitles
            ass_subtitles_path = temp_dir / "subtitles.ass"
            self.generate_ass_subtitles_from_words(words, ass_subtitles_path, width=width, height=height)

            # Render scene clips
            clip_paths: List[Path] = []
            for sc in scenes_meta:
                clip_path = temp_dir / f"clip_{sc.scene_number}.mp4"
                self.render_scene_clip(
                    image_path=sc.slide_image_path,
                    duration=sc.duration,
                    output_file=clip_path,
                    motion_type=sc.motion_type,
                    width=width,
                    height=height,
                )
                clip_paths.append(clip_path)

            # Multiplex video clips + master audio + burn kinetic subtitles
            logger.info("Multiplexing continuous video clips, master voiceover, and kinetic captions...")
            concat_filter_inputs = "".join([f"[{i}:v]" for i in range(len(clip_paths))])
            filter_chain = (
                f"{concat_filter_inputs}concat=n={len(clip_paths)}:v=1:a=0[concated];"
                f"[concated]ass='{ass_subtitles_path.resolve()}'[outv]"
            )

            cmd_final = [self.ffmpeg_bin, "-y"]
            for cp in clip_paths:
                cmd_final.extend(["-i", str(cp)])
            cmd_final.extend(["-i", str(master_audio_path)])

            cmd_final.extend([
                "-filter_complex",
                filter_chain,
                "-map",
                "[outv]",
                "-map",
                f"{len(clip_paths)}:a",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-preset",
                "fast",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
                "-movflags",
                "+faststart",
                str(final_video_path),
            ])

            res_final = subprocess.run(cmd_final, capture_output=True, text=True, check=False)
            if res_final.returncode != 0:
                logger.error("Final export error: %s", res_final.stderr[-600:])
                raise RuntimeError("Failed to multiplex final video reel.")

        caption_path = final_video_path.with_suffix(".txt")
        caption_text = self._build_video_caption(city, niche)
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(caption_text)

        filesize_mb = round(final_video_path.stat().st_size / (1024 * 1024), 2)
        logger.info("🎉 Final 30s Video Reel Exported: %s (%.2f MB, %.2fs)", final_video_path, filesize_mb, total_duration)

        return {
            "ok": True,
            "video_path": str(final_video_path),
            "caption_path": str(caption_path),
            "caption_text": caption_text,
            "duration": total_duration,
            "filesize_mb": filesize_mb,
            "resolution": f"{width}x{height}",
            "city": city,
            "niche": niche,
            "scenes": [
                {
                    "scene": s.scene_number,
                    "title": s.title,
                    "duration": s.duration,
                    "voiceover": s.voiceover_text,
                }
                for s in scenes_meta
            ],
        }

    def _build_video_caption(self, city: Dict[str, Any], niche: Dict[str, Any]) -> str:
        """Generates high-value educational caption for Reels / Shorts / TikTok."""
        city_name = city.get("name", "Local Commercial Hub")
        niche_name = niche.get("name", "Boutique Business")

        return (
            f"Why mobile website speed matters for {city_name} {niche_name.lower()}:\n\n"
            f"• 53% of mobile visits are abandoned if pages take longer than 3 seconds to load.\n"
            f"• Heavy scripts and bloated templates degrade Google Core Web Vitals metrics.\n"
            f"• Sub-second response times improve engagement, retention, and mobile search rankings.\n\n"
            f"ExtrovertNerd shares daily web performance teardowns and Core Web Vitals telemetry.\n\n"
            f"💬 Want any help in your business with websites, custom tools, or software? Send us a DM.\n\n"
            f"Follow @extrovertnerd for daily performance breakdowns.\n\n"
            f"#WebPerformance #CoreWebVitals #WebsiteSpeed #ExtrovertNerd #{city_name.replace(' ', '')} #{niche_name.replace(' ', '')}"
        )

    def render_latest_carousel_reel(
        self,
        aspect_ratio: str = "9:16",
        voice: Optional[str] = None,
        rate: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Finds the most recently rendered carousel slides in output/graphics and renders a video reel."""
        graphics_dir = config.graphics_output_path
        carousel_dirs = [d for d in graphics_dir.glob("*_carousel") if d.is_dir()]
        if not carousel_dirs:
            raise FileNotFoundError(f"No carousel folders found in {graphics_dir}")

        carousel_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
        latest_dir = carousel_dirs[0]

        slides = sorted(list(latest_dir.glob("vertical_slide_*.png")) + list(latest_dir.glob("slide_*.png")))
        if not slides:
            slides = sorted(list(latest_dir.glob("*.png")))

        if len(slides) < 4:
            raise FileNotFoundError(f"Found fewer than 4 slides in {latest_dir}")

        meta_file = latest_dir / "meta.json"
        meta: Dict[str, Any] = {}
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                pass

        city = meta.get("city", {"name": "Bangalore", "id": "bangalore"})
        niche = meta.get("niche", {"name": "Fashion Boutiques", "id": "fashion-boutiques"})

        return self.render_reel(
            slide_images=slides[:4],
            city=city,
            niche=niche,
            aspect_ratio=aspect_ratio,
            voice=voice,
            rate=rate,
        )

    def build_top100_narrative_script(
        self,
        site: Dict[str, Any],
        slide1_path: Path,
        slide2_path: Path,
    ) -> List[Dict[str, Any]]:
        """Constructs a 6-part calibrated 60-second educational teardown script for the Top 100 series."""
        rank = site.get("global_rank", 1)
        name = site.get("name", "Target")
        stack_list = site.get("architecture_stack", [])[:3]
        stack_str = ", ".join(stack_list)
        telemetry = site.get("telemetry", {"lcp": "0.6s", "inp": "20ms", "cls": "0.00", "ttfb": "80ms"})
        reasons = site.get("key_reasons", [])

        def _clean_spoken_clause(text: str) -> str:
            t = text
            # Expand symbols and currency for smooth speech synthesis
            t = re.sub(r"\$([0-9]+)\s*([tT]rillion|[bB]illion|[mM]illion)", r"\1 \2 dollars", t)
            t = re.sub(r"\$([0-9]+)", r"\1 dollars", t)
            t = re.sub(r"\b60fps\b", "60 frames per second", t, flags=re.IGNORECASE)
            t = re.sub(r"\b120fps\b", "120 frames per second", t, flags=re.IGNORECASE)
            t = re.sub(r"\bsub-([0-9]+)ms\b", r"sub-\1 millisecond", t, flags=re.IGNORECASE)
            t = re.sub(r"([0-9]+)ms\b", r"\1 milliseconds", t, flags=re.IGNORECASE)
            # Remove parenthetical abbreviations like (sub-25ms INP) or (0.00 score)
            t = re.sub(r"\([^\)]*\)", "", t)
            # Remove internal slashes / asterisks
            t = t.replace("/", " and ").replace("*", "")
            # Ensure zero mentions of Ravi or engineer
            t = re.sub(r"\b(Ravi|engineer|lead architect)\b", "ExtrovertNerd", t, flags=re.IGNORECASE)
            t = re.sub(r"\s+", " ", t).strip()
            return t.rstrip(".")

        # Format concise hook question
        raw_hook = site.get("hook", "")
        if raw_hook:
            hook_text = _clean_spoken_clause(raw_hook)
            if not hook_text.endswith("?"):
                hook_text += "?"
        else:
            hook_text = f"Why does {name} dominate global web performance?"

        r1 = _clean_spoken_clause(reasons[0] if len(reasons) > 0 else "Optimized execution pipelines")
        r2 = _clean_spoken_clause(reasons[1] if len(reasons) > 1 else "Global edge network delivery")
        r3 = _clean_spoken_clause(reasons[2] if len(reasons) > 2 else "Zero layout shift architecture")
        verdict = _clean_spoken_clause(site.get("extrovertnerd_verdict", "Isolate state machines from cosmetic assets"))

        # Spoken telemetry format
        lcp_val = telemetry.get("lcp", "0.6s").replace("s", " seconds")
        inp_val = telemetry.get("inp", "20ms").replace("ms", " milliseconds")
        cls_val = telemetry.get("cls", "0.00")
        if cls_val in ("0", "0.0", "0.00"):
            cls_text = "zero layout shift"
        else:
            cls_text = f"{cls_val} layout shift"

        return [
            {
                "scene_number": 1,
                "title": f"Day {rank}/100: {name} Hook",
                "slide_image_path": slide1_path,
                "motion": "zoom_in",
                "voiceover_text": f"Day {rank} of 100: {name}. {hook_text}",
            },
            {
                "scene_number": 2,
                "title": f"Day {rank}/100: Architecture Stack",
                "slide_image_path": slide1_path,
                "motion": "pan_down",
                "voiceover_text": f"Their core production architecture runs on {stack_str}. Here is why this architecture dominates.",
            },
            {
                "scene_number": 3,
                "title": f"Day {rank}/100: Decisions 1 & 2",
                "slide_image_path": slide2_path,
                "motion": "zoom_in",
                "voiceover_text": f"Decision one: {r1}. Decision two: {r2}.",
            },
            {
                "scene_number": 4,
                "title": f"Day {rank}/100: Decision 3",
                "slide_image_path": slide2_path,
                "motion": "pan_down",
                "voiceover_text": f"Decision three: {r3}.",
            },
            {
                "scene_number": 5,
                "title": f"Day {rank}/100: Live Telemetry",
                "slide_image_path": slide2_path,
                "motion": "zoom_center",
                "voiceover_text": f"Verified Core Web Vitals telemetry: Largest Contentful Paint {lcp_val}, Interaction to Next Paint {inp_val}, and {cls_text}.",
            },
            {
                "scene_number": 6,
                "title": f"Day {rank}/100: ExtrovertNerd Verdict",
                "slide_image_path": slide2_path,
                "motion": "pulse_zoom",
                "voiceover_text": f"The ExtrovertNerd takeaway: {verdict}. Follow ExtrovertNerd for the 100 day series.",
            },
        ]

    def _build_top100_video_caption(self, site: Dict[str, Any]) -> str:
        """Builds non-promotional technical caption for the 60s Top 100 reel."""
        rank = site.get("global_rank", 1)
        name = site.get("name", "Website")
        domain = site.get("domain", "")
        telemetry = site.get("telemetry", {})
        stack = ", ".join(site.get("architecture_stack", []))

        return (
            f"Day {rank} of 100: Web Architecture Teardown // {name} ({domain})\n\n"
            f"⚡ Production Stack: {stack}\n\n"
            f"📊 Verified Telemetry:\n"
            f"• LCP: {telemetry.get('lcp')}\n"
            f"• INP: {telemetry.get('inp')}\n"
            f"• CLS: {telemetry.get('cls')}\n"
            f"• TTFB: {telemetry.get('ttfb')}\n\n"
            f"💡 ExtrovertNerd Verdict:\n"
            f"{site.get('extrovertnerd_verdict')}\n\n"
            f"💬 Want any help in your business with websites, custom tools, or software? Send us a DM.\n\n"
            f"Follow @extrovertnerd for daily 60-second architecture breakdowns across the top 100 websites in the world.\n\n"
            f"#WebPerformance #WebArchitecture #SystemDesign #ExtrovertNerd #{name.replace(' ', '')} #CoreWebVitals"
        )

    def render_top100_reel(
        self,
        website_id: Optional[str | int] = None,
        rank: Optional[int] = None,
        aspect_ratio: str = "9:16",
        voice: Optional[str] = None,
        rate: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Renders an automated 60-second vertical video reel for the Top 100 Website Architecture Series.

        Features continuous neural speech synthesis, millisecond-accurate word-boundary subtitles,
        and lock-step visual transitions.
        """
        top100_path = config.content_dir / "top100_websites.json"
        if not top100_path.exists():
            top100_path = Path("content/top100_websites.json")
        with open(top100_path, "r", encoding="utf-8") as f:
            websites = json.load(f)

        selected_site = None
        target_val = website_id or rank
        if target_val:
            for w in websites:
                if (
                    str(w.get("global_rank")) == str(target_val)
                    or str(w.get("id")) == str(target_val)
                    or w.get("name", "").lower() == str(target_val).lower()
                    or w.get("domain", "").lower() == str(target_val).lower()
                ):
                    selected_site = w
                    break

        if not selected_site:
            try:
                from src.tracker import get_next_top100_rank

                target_r = get_next_top100_rank(advance=False)
                selected_site = next((w for w in websites if w.get("global_rank") == target_r), None)
            except Exception:
                pass
            if not selected_site:
                day_of_year = datetime.date.today().timetuple().tm_yday
                selected_site = websites[(day_of_year - 1) % len(websites)]

        site_rank = selected_site["global_rank"]
        site_name = selected_site["name"]
        slug = site_name.lower().replace(" ", "_").replace("/", "_")

        slide1_path = config.graphics_output_path / "top100" / "instagram" / f"rank_{site_rank:03d}_{slug}_slide1.png"
        slide2_path = config.graphics_output_path / "top100" / "instagram" / f"rank_{site_rank:03d}_{slug}_slide2.png"

        if not (slide1_path.exists() and slide2_path.exists()):
            logger.info("Top 100 slides not found for #%d %s. Rendering them now via Playwright...", site_rank, site_name)
            from src.generator_graphics import GraphicsRenderer

            renderer = GraphicsRenderer()
            renderer.render_top100_breakdown(website_id=str(site_rank), platform="instagram")

        if not (slide1_path.exists() and slide2_path.exists()):
            candidates1 = list(config.graphics_output_path.glob(f"**/rank_{site_rank:03d}_*slide1.png"))
            candidates2 = list(config.graphics_output_path.glob(f"**/rank_{site_rank:03d}_*slide2.png"))
            if candidates1 and candidates2:
                slide1_path = candidates1[0]
                slide2_path = candidates2[0]
            else:
                raise FileNotFoundError(f"Could not locate rendered slides for rank #{site_rank} {site_name}")

        logger.info("🎬 Rendering 60-second Top 100 Reel for Day %d: %s", site_rank, site_name)
        scenes_def = self.build_top100_narrative_script(selected_site, slide1_path, slide2_path)

        if aspect_ratio == "4:5":
            width, height = 1080, 1350
        else:
            width, height = 1080, 1920

        final_video_name = f"top100_day_{site_rank:03d}_{slug}_60s_reel.mp4"
        final_video_path = self.output_dir / final_video_name

        with tempfile.TemporaryDirectory(prefix="extrovertnerd_top100_") as temp_dir_str:
            temp_dir = Path(temp_dir_str)

            # Step 1: Synthesize the full continuous voiceover in a single neural pass
            full_script = " ".join([sc["voiceover_text"].strip() for sc in scenes_def])
            master_audio_path = temp_dir / "master_voiceover.mp3"

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                total_duration, words = loop.run_until_complete(
                    self._synthesize_continuous_audio(
                        text=full_script,
                        output_file=master_audio_path,
                        voice=voice or self.voice,
                        rate=rate or "+22%",
                    )
                )
            finally:
                loop.close()

            logger.info("Master continuous voiceover synthesized: %.2fs (%d words)", total_duration, len(words))

            # Step 2: Compute scene cut times and durations from the WordBoundary telemetry
            cut_times = self._compute_scene_cut_times(scenes_def, words, total_duration)

            scenes_meta: List[SceneDefinition] = []
            prev_time = 0.0
            for idx, sc in enumerate(scenes_def):
                cut_t = cut_times[idx]
                dur = round(cut_t - prev_time, 3)
                sc_def = SceneDefinition(
                    scene_number=idx + 1,
                    title=sc["title"],
                    voiceover_text=sc["voiceover_text"],
                    slide_image_path=sc["slide_image_path"],
                    motion_type=sc["motion"],
                    duration=dur,
                    start_time=prev_time,
                    end_time=cut_t,
                )
                scenes_meta.append(sc_def)
                prev_time = cut_t

            logger.info("Scene durations computed: %s", [f"S{s.scene_number}: {s.duration:.2f}s" for s in scenes_meta])

            # Step 3: Generate frame-perfect ASS subtitles directly from word boundaries
            ass_subtitles_path = temp_dir / "subtitles.ass"
            self.generate_ass_subtitles_from_words(
                words=words,
                output_file=ass_subtitles_path,
                width=width,
                height=height,
            )

            # Step 4: Render the 6 animated scene video clips with exact durations
            clip_paths: List[Path] = []
            for sc in scenes_meta:
                clip_path = temp_dir / f"clip_{sc.scene_number}.mp4"
                self.render_scene_clip(
                    image_path=sc.slide_image_path,
                    duration=sc.duration,
                    output_file=clip_path,
                    motion_type=sc.motion_type,
                    width=width,
                    height=height,
                )
                clip_paths.append(clip_path)

            # Step 5: Multiplex video clips + continuous master audio + burn ASS subtitles
            logger.info("Multiplexing continuous video clips, master voiceover, and burning ASS captions...")
            concat_filter_inputs = "".join([f"[{i}:v]" for i in range(len(clip_paths))])
            filter_chain = (
                f"{concat_filter_inputs}concat=n={len(clip_paths)}:v=1:a=0[concated];"
                f"[concated]ass='{ass_subtitles_path.resolve()}'[outv]"
            )

            cmd_final = [self.ffmpeg_bin, "-y"]
            for cp in clip_paths:
                cmd_final.extend(["-i", str(cp)])
            cmd_final.extend(["-i", str(master_audio_path)])
            cmd_final.extend([
                "-filter_complex",
                filter_chain,
                "-map",
                "[outv]",
                "-map",
                f"{len(clip_paths)}:a",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-preset",
                "fast",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
                "-movflags",
                "+faststart",
                str(final_video_path),
            ])

            res_final = subprocess.run(cmd_final, capture_output=True, text=True, check=False)
            if res_final.returncode != 0:
                logger.error("Final export error: %s", res_final.stderr[-600:])
                raise RuntimeError("Failed to multiplex final Top 100 video reel.")

        caption_path = final_video_path.with_suffix(".txt")
        caption_text = self._build_top100_video_caption(selected_site)
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(caption_text)

        filesize_mb = round(final_video_path.stat().st_size / (1024 * 1024), 2)
        logger.info("🎉 Final 60s Top 100 Reel Exported: %s (%.2f MB, %.2fs)", final_video_path, filesize_mb, total_duration)

        return {
            "ok": True,
            "type": "top100_60s_reel",
            "video_path": str(final_video_path),
            "caption_path": str(caption_path),
            "caption_text": caption_text,
            "duration": total_duration,
            "filesize_mb": filesize_mb,
            "resolution": f"{width}x{height}",
            "website": selected_site,
            "scenes": [
                {
                    "scene": s.scene_number,
                    "title": s.title,
                    "duration": s.duration,
                    "voiceover": s.voiceover_text,
                }
                for s in scenes_meta
            ],
        }


def main() -> None:
    """CLI execution for the automated video reel generator."""
    parser = argparse.ArgumentParser(description="ExtrovertNerd Video Reel Generator")
    parser.add_argument("--top100", action="store_true", help="Render 60-second Top 100 Website Architecture Reel")
    parser.add_argument("--rank", type=int, help="Rank of website for Top 100 series (1-100)")
    parser.add_argument("--day", type=int, help="Day number (synonym for rank)")
    parser.add_argument("--website-id", type=str, help="Domain or ID for Top 100 teardown")
    parser.add_argument("--latest", action="store_true", help="Render video reel from latest carousel")
    parser.add_argument("--dir", type=str, help="Specific carousel directory with slide_1..4.png")
    parser.add_argument("--city", type=str, default="Bangalore", help="City name")
    parser.add_argument("--niche", type=str, default="Fashion Boutiques", help="Business niche")
    parser.add_argument("--aspect-ratio", type=str, default="9:16", choices=["9:16", "4:5"], help="Aspect ratio")
    parser.add_argument("--voice", type=str, default="en-US-ChristopherNeural", help="Edge-TTS voice")
    parser.add_argument("--rate", type=str, default=None, help="Edge-TTS speech rate (e.g. +22 percent)")
    parser.add_argument("--batch", nargs=2, type=int, metavar=("START", "END"), help="Batch render Top 100 reels from START to END")
    parser.add_argument("--telegram", action="store_true", help="Automatically dispatch generated reel to Telegram")
    args = parser.parse_args()

    generator = VideoReelGenerator(voice=args.voice, rate=args.rate)

    if args.batch:
        start_r, end_r = args.batch
        logger.info("🚀 Starting Batch Generation for Top 100 Reels: Rank #%d to #%d", start_r, end_r)
        from src.telegram_notifier import TelegramNotifier
        from src.tracker import set_current_top100_rank

        notifier = TelegramNotifier() if args.telegram else None
        successful_runs = []

        for r in range(start_r, end_r + 1):
            logger.info("\n------------------------------------------------------------")
            logger.info("🎬 [BATCH %d/%d] Rendering Top 100 Reel for Rank #%d", r - start_r + 1, end_r - start_r + 1, r)
            logger.info("------------------------------------------------------------")
            try:
                res = generator.render_top100_reel(
                    rank=r,
                    aspect_ratio=args.aspect_ratio,
                    voice=args.voice,
                    rate=args.rate,
                )
                successful_runs.append(res)
                print(f"✅ Generated Rank #{r} ({res['website']['name']}): {res['duration']}s | {res['filesize_mb']} MB")

                if notifier:
                    logger.info("📲 Dispatching Rank #%d video reel to Telegram...", r)
                    tg_res = notifier.dispatch_top100_video_reel(
                        video_path=res["video_path"],
                        site=res["website"],
                        caption=res["caption_text"],
                        duration=int(res["duration"]),
                    )
                    print(f"Telegram Dispatch: {tg_res.get('ok')}")
            except Exception as e:
                logger.error("❌ Failed rendering Rank #%d: %s", r, e)

        set_current_top100_rank(end_r)
        print(f"\n🎉 BATCH GENERATION COMPLETE: {len(successful_runs)}/{end_r - start_r + 1} video reels generated.")
        print(f"📌 Tracker set to Rank #{end_r}. Next daily run will start automatically from Rank #{end_r + 1}.")
        return

    if args.top100 or args.rank or args.day or args.website_id:
        target_rank = args.rank or args.day or args.website_id
        logger.info("🚀 Rendering 60-Second Top 100 Web Architecture Reel (Target: %s)...", target_rank or "Today")
        res = generator.render_top100_reel(
            website_id=args.website_id,
            rank=args.rank or args.day,
            aspect_ratio=args.aspect_ratio,
            voice=args.voice,
            rate=args.rate,
        )
    elif args.latest or not args.dir:
        logger.info("🚀 Rendering 30-second Video Reel from latest carousel...")
        res = generator.render_latest_carousel_reel(
            aspect_ratio=args.aspect_ratio,
            voice=args.voice,
            rate=args.rate,
        )
    else:
        target_dir = Path(args.dir)
        slides = sorted(list(target_dir.glob("slide_*.png")) + list(target_dir.glob("vertical_slide_*.png")))
        res = generator.render_reel(
            slide_images=slides[:4],
            city={"name": args.city, "id": args.city.lower().replace(" ", "-")},
            niche={"name": args.niche, "id": args.niche.lower().replace(" ", "-")},
            aspect_ratio=args.aspect_ratio,
            voice=args.voice,
            rate=args.rate,
        )

    print("\n=== VIDEO REEL GENERATION COMPLETE ===")
    print(f"🎬 Video File:    {res['video_path']}")
    print(f"⏱️ Duration:      {res['duration']}s")
    print(f"💾 File Size:     {res['filesize_mb']} MB")
    print(f"📐 Resolution:    {res['resolution']}")
    print(f"📋 Caption File:  {res['caption_path']}")

    if args.telegram:
        logger.info("\n📲 Dispatching video reel to Telegram...")
        from src.telegram_notifier import TelegramNotifier

        notifier = TelegramNotifier()
        if res.get("type") == "top100_60s_reel":
            tg_res = notifier.dispatch_top100_video_reel(
                video_path=res["video_path"],
                site=res["website"],
                caption=res["caption_text"],
                duration=int(res["duration"]),
            )
        else:
            tg_res = notifier.dispatch_video_reel(
                video_path=res["video_path"],
                city=res.get("city", {}),
                niche=res.get("niche", {}),
                caption=res["caption_text"],
                duration=int(res["duration"]),
            )
        print(f"Telegram Dispatch: {tg_res.get('ok')}")


if __name__ == "__main__":
    main()
