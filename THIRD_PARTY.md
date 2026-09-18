# Third-party components and references

This repository does not vendor entire upstream projects by default. External projects are used as references, optional dependencies, or sources of architectural patterns only when they solve a concrete need.

## Current references

### FFmpeg
Repository: `FFmpeg/FFmpeg`
Role: primary media processing and rendering engine.
License note: primarily LGPL with optional GPL components depending on build configuration.

### PySceneDetect
Repository: `Breakthrough/PySceneDetect`
Role: scene detection and footage indexing.

### OpenAI Whisper
Repository: `openai/whisper`
Role: transcription, timestamps and language recognition.

### auto-editor
Repository: `WyattBlue/auto-editor`
Role: optional assisted rough cut.

### ForwrdCut
Repository: `bussiomedia-sys/forwrdcut`
Reference snapshot reviewed: `3f61f8c51896c830d81bf17fe009e39f0704bf97`
License: MIT.
Patterns adopted conceptually: local-first workflow, contact sheets, non-destructive editing, Edit Decision Plan, render QC and agent-oriented media workflow.
No full-project copy has been imported.

### Agentic Video Editor
Repository: `poseljacob/agentic-video-editor`
Reference snapshot reviewed: `47248b577046b0563e57e78edad86a3106c6faab`
License: MIT.
Patterns adopted conceptually: preprocess → director → trim refiner → editor → reviewer, declarative pipeline, versioned retries and review feedback loop.
No full-project copy has been imported.

### Remotion Skills
Repository: `remotion-dev/skills`
Reference snapshot reviewed: `9ae8048a84690098b1059f7f5d30e6d05833b824`
Patterns adopted conceptually: modular routing for creation, multimedia, captions and rendering; timestamped caption structures.

### Remotion
Repository: `remotion-dev/remotion`
Role: optional programmatic renderer to evaluate case by case.
License note: special two-tier license. Individuals and eligible small organizations may use it for free; other for-profit organizations may require a company license. Review current terms before commercial adoption.

## Review 2026-09-18

See [verified tool selection](docs/TOOL_SELECTION_2026-09.md). No third-party source code was vendored in this revision. The local renderer calls FFmpeg; the optional transcription adapter calls faster-whisper's public API (MIT). The validator uses python-jsonschema (MIT). Model weights, fonts, media, optional libraries and FFmpeg builds retain their own terms.

An API license label is not sufficient by itself: ForwrdCut's LICENSE was read to resolve its Other classification. Remotion has a separate commercial eligibility policy. No open-source license is granted for this repository's own code by this document.

## Incorporation rule

Before copying or adapting third-party code:

1. verify license and compatibility;
2. identify the exact operational need;
3. prefer a dependency or adapter over vendoring;
4. preserve attribution when required;
5. avoid importing sample assets, fonts, media or model weights unless their license is separately verified;
6. record the upstream repository and commit used as reference.

The absence of a project from this file means it has not yet been approved for incorporation.
