"""Automated Video Generation Pipeline for ExtrovertNerd.

Transforms rendered static Playwright carousels and tech-tip graphics into
high-retention, 30-second vertical video reels (1080x1920 / 1080x1350) optimized
for Instagram Reels, YouTube Shorts, and TikTok.

Pipeline Features:
1. Hyper-realistic neural voiceover synthesis via Edge-TTS (en-IN / en-US).
2. Dynamic 4-part narrative arc (Hook -> Benchmark Failure -> ExtrovertNerd Rebuild -> WhatsApp CTA).
3. Smooth Ken Burns pan/zoom motion effects on high-res Playwright PNG slides.
4. Blurred ambient background styling with high-contrast centered presentation.
5. High-contrast kinetic subtitle overlays with word highlights (ASS subtitles).
6. Direct export to output/videos/ and one-click dispatch to Telegram.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import shutil
import subprocess
import sys
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
    """Represents a single scene in the 30-second video reel."""

    scene_number: int
    title: str
    voiceover_text: str
    slide_image_path: Path
    motion_type: str = "zoom_in"
    duration: float = 7.5
    start_time: float = 0.0
    end_time: float = 7.5
    audio_path: Optional[Path] = None


class VideoReelGenerator:
    """Orchestrates Edge-TTS voiceover synthesis, Ken Burns animations,

    kinetic subtitles, and video export for social media reels.
    """

    def __init__(
        self,
        output_dir: Optional[Path | str] = None,
        voice: Optional[str] = None,
        rate: Optional[str] = None,
    ):
        self.output_dir = Path(output_dir or config.video_output_path)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.voice = voice or getattr(config, "default_tts_voice", "en-IN-PrabhatNeural")
        self.rate = rate or getattr(config, "default_tts_rate", "+16%")
        self.ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

    def build_narrative_script(
        self,
        city: Optional[Dict[str, Any]] = None,
        niche: Optional[Dict[str, Any]] = None,
        custom_script: Optional[Dict[int, str]] = None,
    ) -> List[Dict[str, Any]]:
        """Builds the 4-part high-retention narrative script for the video reel."""
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

    async def _synthesize_scene_audio(
        self,
        text: str,
        output_file: Path,
        voice: Optional[str] = None,
        rate: Optional[str] = None,
    ) -> float:
        """Synthesizes voiceover speech for a single scene and returns duration in seconds."""
        v = voice or self.voice
        r = rate or self.rate
        logger.info("Synthesizing voiceover [%s @ %s]: %s...", v, r, text[:45])

        comm = edge_tts.Communicate(text, v, rate=r)
        await comm.save(str(output_file))

        # Get exact audio duration using ffprobe
        duration = self._get_audio_duration(output_file)
        logger.info("Generated voiceover clip (%.2fs): %s", duration, output_file.name)
        return duration

    def _get_audio_duration(self, audio_file: Path) -> float:
        """Measures audio file duration in seconds via MoviePy or ffprobe."""
        try:
            from moviepy import AudioFileClip
            clip = AudioFileClip(str(audio_file))
            dur = float(clip.duration)
            clip.close()
            if dur > 0.5:
                return round(dur, 2)
        except Exception:
            pass

        ffprobe_bin = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
        if os.path.exists(ffprobe_bin):
            cmd = [
                ffprobe_bin,
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
        return 9.5

    def generate_ass_subtitles(
        self,
        scenes: List[SceneDefinition],
        output_file: Path,
        width: int = 1080,
        height: int = 1920,
    ) -> None:
        """Generates an Advanced SubStation Alpha (ASS) subtitle file with kinetic word highlighting."""
        ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KineticPill,Arial,52,&H00FFFFFF,&H0000FFFF,&H00000000,&HD0050811,-1,0,0,0,100,100,0,0,3,10,0,2,40,40,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events: List[str] = []

        def _format_ass_time(seconds: float) -> str:
            td = timedelta(seconds=seconds)
            total_seconds = int(td.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            secs = total_seconds % 60
            centisecs = int(td.microseconds / 10000)
            return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

        for sc in scenes:
            text = sc.voiceover_text.strip()
            # Clean special characters
            cleaned_text = re.sub(r'[\'"]', "", text)
            words = cleaned_text.split()
            if not words:
                continue

            # Split into kinetic cues of 4-6 words
            words_per_cue = 5
            chunks = []
            for i in range(0, len(words), words_per_cue):
                chunks.append(words[i : i + words_per_cue])

            cue_duration = sc.duration / len(chunks)

            for idx, chunk in enumerate(chunks):
                c_start = sc.start_time + (idx * cue_duration)
                c_end = c_start + cue_duration
                # Small safety margin between cues
                c_end = min(c_end, sc.end_time)

                start_str = _format_ass_time(c_start)
                end_str = _format_ass_time(c_end)

                # Format kinetic styling: First 1-2 words in vivid cyan/yellow highlight, remainder white
                if len(chunk) > 2:
                    highlight = " ".join(chunk[:2])
                    normal = " ".join(chunk[2:])
                    cue_text = f"{{\\c&H00F0FF00&}}{highlight.upper()} {{\\c&H00FFFFFF&}}{normal.upper()}"
                else:
                    cue_text = f"{{\\c&H00F0FF00&}}{' '.join(chunk).upper()}"

                events.append(f"Dialogue: 0,{start_str},{end_str},KineticPill,,0,0,0,,{cue_text}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ass_header + "\n".join(events) + "\n")

        logger.info("Saved kinetic ASS subtitles: %s (%d dialogue cues)", output_file.name, len(events))

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
        """Renders an animated single-scene video clip with Ken Burns zoom/pan and blurred backdrop."""
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
            # Steadily zoom in on the 100/100 verified speedometer
            zoom_expr = "min(zoom+0.0005,1.08)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        else:  # pulse_zoom / cta
            # Subtle steady zoom focusing on the WhatsApp link
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

        logger.info("Rendering scene clip [%s, %.2fs, %dx%d]: %s", motion_type, duration, width, height, output_file.name)
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            logger.error("FFmpeg render error on %s: %s", output_file.name, res.stderr[-500:])
            raise RuntimeError(f"FFmpeg failed rendering scene clip: {output_file.name}")

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
        """Assembles the complete 30-second vertical video reel with voiceover and kinetic subtitles."""
        valid_slides = [Path(s) for s in slide_images if Path(s).exists()]
        if len(valid_slides) < 4:
            raise ValueError(f"At least 4 slide PNG images are required. Provided: {len(valid_slides)}")

        city = city or {"name": "Local Commercial Hub", "id": "local"}
        niche = niche or {"name": "Boutique Business", "id": "business"}

        # Dimensions: 9:16 (1080x1920) for Reels/Shorts/TikTok, or 4:5 (1080x1350) for Feed
        if aspect_ratio == "4:5":
            width, height = 1080, 1350
        else:
            width, height = 1080, 1920

        slug = f"{city.get('id', 'local')}_{niche.get('id', 'niche')}_30s_reel"
        final_video_name = output_filename or f"{slug}.mp4"
        final_video_path = self.output_dir / final_video_name

        script_scenes = self.build_narrative_script(city, niche)

        # Work inside a clean temporary workspace
        with tempfile.TemporaryDirectory(prefix="extrovertnerd_reel_") as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            logger.info("🎬 Assembling 30s Video Reel in workspace: %s", temp_dir)

            # Step 1: Synthesize voiceover for all 4 scenes
            scenes_meta: List[SceneDefinition] = []
            audio_files: List[Path] = []
            current_time = 0.0

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                for idx, sc_dict in enumerate(script_scenes):
                    slide_path = valid_slides[idx]
                    audio_path = temp_dir / f"voice_scene_{idx + 1}.mp3"

                    # Synthesize audio chunk
                    dur = loop.run_until_complete(
                        self._synthesize_scene_audio(
                            text=sc_dict["voiceover_text"],
                            output_file=audio_path,
                            voice=voice,
                            rate=rate,
                        )
                    )
                    # Add tiny 0.15s breathing room between scenes
                    dur = round(dur + 0.15, 3)

                    sc_def = SceneDefinition(
                        scene_number=idx + 1,
                        title=sc_dict["title"],
                        voiceover_text=sc_dict["voiceover_text"],
                        slide_image_path=slide_path,
                        motion_type=sc_dict["motion"],
                        duration=dur,
                        start_time=round(current_time, 3),
                        end_time=round(current_time + dur, 3),
                        audio_path=audio_path,
                    )
                    scenes_meta.append(sc_def)
                    audio_files.append(audio_path)
                    current_time += dur
            finally:
                loop.close()

            total_duration = round(current_time, 3)
            logger.info("Total Reel Duration: %.2f seconds across 4 scenes", total_duration)

            # Step 2: Concatenate audio into master track
            master_audio_path = temp_dir / "master_voiceover.mp3"
            concat_audio_txt = temp_dir / "audio_list.txt"
            with open(concat_audio_txt, "w", encoding="utf-8") as f:
                for af in audio_files:
                    f.write(f"file '{af.resolve()}'\n")

            cmd_audio = [
                self.ffmpeg_bin,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_audio_txt),
                "-c",
                "copy",
                str(master_audio_path),
            ]
            subprocess.run(cmd_audio, check=True, capture_output=True)

            # Step 3: Generate styled ASS subtitles
            ass_subtitles_path = temp_dir / "subtitles.ass"
            self.generate_ass_subtitles(scenes_meta, ass_subtitles_path, width=width, height=height)

            # Step 4: Render each scene video clip
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

            # Step 5: Multiplex video clips + master audio + burn kinetic subtitles
            logger.info("Multiplexing master video, voiceover, and kinetic captions...")
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

        # Step 6: Generate platform-ready caption companion file
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
        category = site.get("category", "Web Platform")
        stack_str = ", ".join(site.get("architecture_stack", [])[:3])
        telemetry = site.get("telemetry", {"lcp": "0.6s", "inp": "20ms", "cls": "0.00", "ttfb": "80ms"})
        reasons = site.get("key_reasons", [])

        # Format concise hook question
        hook = site.get("hook", "").split("?")[0]
        if hook:
            hook_words = hook.split()
            if len(hook_words) > 14:
                hook_words = hook_words[:14]
            hook_text = " ".join(hook_words) + "?"
        else:
            hook_text = f"Why does {name} dominate global web performance?"

        # Short clean clauses for audio clarity & strictly ~58-60s timing
        def _concise(text: str, max_words: int = 10) -> str:
            cleaned = re.sub(r'[\(\)]', '', text)
            words = cleaned.split()
            if len(words) <= max_words:
                return cleaned.rstrip(".")
            return " ".join(words[:max_words]).rstrip(".")

        r1 = _concise(reasons[0] if len(reasons) > 0 else "Optimized execution pipelines", 9)
        r2 = _concise(reasons[1] if len(reasons) > 1 else "Global edge network delivery", 9)
        r3 = _concise(reasons[2] if len(reasons) > 2 else "Zero layout shift architecture", 9)
        verdict = _concise(site.get("extrovertnerd_verdict", "Isolate state machines from cosmetic assets"), 10)

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
                "voiceover_text": f"Verified Core Web Vitals telemetry: Largest Contentful Paint {telemetry.get('lcp')}, Interaction to Next Paint {telemetry.get('inp')}, and {telemetry.get('cls')} Layout Shift.",
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
        """Renders an automated 60-second vertical video reel for the Top 100 Website Architecture Series."""
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

            # Pass 1: Synthesize all 6 audio clips and measure exact speech duration
            raw_durs: List[float] = []
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                for idx, sc in enumerate(scenes_def):
                    raw_audio_path = temp_dir / f"voice_top100_raw_{idx + 1}.mp3"
                    dur = loop.run_until_complete(
                        self._synthesize_scene_audio(
                            text=sc["voiceover_text"],
                            output_file=raw_audio_path,
                            voice=voice or self.voice,
                            rate=rate or "+18%",
                        )
                    )
                    raw_durs.append(dur)
            finally:
                loop.close()

            # Pass 2: Calibrate durations to target exactly 59.5s (~60 seconds)
            target_total = 59.5
            total_raw = sum(raw_durs)
            if total_raw < target_total:
                pad_per_scene = (target_total - total_raw) / len(scenes_def)
            else:
                pad_per_scene = 0.2

            scenes_meta: List[SceneDefinition] = []
            audio_files: List[Path] = []
            current_time = 0.0

            for idx, sc in enumerate(scenes_def):
                raw_path = temp_dir / f"voice_top100_raw_{idx + 1}.mp3"
                padded_path = temp_dir / f"voice_top100_{idx + 1}.mp3"
                scene_dur = round(raw_durs[idx] + pad_per_scene, 2)

                # Pad audio to match scene_dur
                cmd_pad = [
                    self.ffmpeg_bin, "-y", "-i", str(raw_path),
                    "-af", f"apad=whole_dur={scene_dur}",
                    str(padded_path)
                ]
                subprocess.run(cmd_pad, check=True, capture_output=True)

                sc_def = SceneDefinition(
                    scene_number=idx + 1,
                    title=sc["title"],
                    voiceover_text=sc["voiceover_text"],
                    slide_image_path=sc["slide_image_path"],
                    motion_type=sc["motion"],
                    duration=scene_dur,
                    start_time=round(current_time, 2),
                    end_time=round(current_time + scene_dur, 2),
                    audio_path=padded_path,
                )
                scenes_meta.append(sc_def)
                audio_files.append(padded_path)
                current_time += scene_dur

            total_duration = round(current_time, 2)
            logger.info("Total Top 100 Reel Duration: %.2f seconds across 6 scenes", total_duration)

            master_audio_path = temp_dir / "master_voiceover.mp3"
            concat_audio_txt = temp_dir / "audio_list.txt"
            with open(concat_audio_txt, "w", encoding="utf-8") as f:
                for af in audio_files:
                    f.write(f"file '{af.resolve()}'\n")

            cmd_audio = [
                self.ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_audio_txt),
                "-c", "copy", str(master_audio_path)
            ]
            subprocess.run(cmd_audio, check=True, capture_output=True)

            ass_subtitles_path = temp_dir / "subtitles.ass"
            self.generate_ass_subtitles(scenes_meta, ass_subtitles_path, width=width, height=height)

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
                "-filter_complex", filter_chain,
                "-map", "[outv]",
                "-map", f"{len(clip_paths)}:a",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "fast",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                "-movflags", "+faststart",
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
    parser.add_argument("--voice", type=str, default="en-IN-PrabhatNeural", help="Edge-TTS voice")
    parser.add_argument("--rate", type=str, default="+18%", help="Edge-TTS speech rate")
    parser.add_argument("--telegram", action="store_true", help="Automatically dispatch generated reel to Telegram")
    args = parser.parse_args()

    generator = VideoReelGenerator(voice=args.voice, rate=args.rate)

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
        res = generator.render_latest_carousel_reel(aspect_ratio=args.aspect_ratio, voice=args.voice)
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

