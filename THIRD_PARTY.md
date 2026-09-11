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
Patterns adopted conceptually: local-first workflow, contact sheets, non-destructive editing, Edit Decision Plan, render QC and agent-oriented media workflow.
No full-project copy has been imported.

### Agentic Video Editor
Repository: `poseljacob/agentic-video-editor`
Patterns adopted conceptually: preprocess → director → trim refiner → editor → reviewer, declarative pipeline, versioned retries and review feedback loop.
No full-project copy has been imported.

### Remotion Skills
Repository: `remotion-dev/skills`
Patterns adopted conceptually: modular routing for creation, multimedia, captions and rendering; timestamped caption structures.

### Remotion
Repository: `remotion-dev/remotion`
Role: optional programmatic renderer to evaluate case by case.
License note: review current terms before commercial adoption.

## Incorporation rule

Before copying or adapting third-party code:

1. verify license and compatibility;
2. identify the exact operational need;
3. prefer a dependency or adapter over vendoring;
4. preserve attribution when required;
5. avoid importing sample assets, fonts, media or model weights unless their license is separately verified;
6. record the upstream repository and commit used as reference.

The absence of a project from this file means it has not yet been approved for incorporation.
