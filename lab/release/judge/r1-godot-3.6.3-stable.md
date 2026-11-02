# Judge file r1-godot-3.6.3-stable

## PUBLISHED RELEASE NOTES (written by the maintainers)

**Godot 3.6.3** is a maintenance release addressing stability and usability issues, and fixing all sorts of bugs. Maintenance releases are compatible with previous releases and are recommended for adoption.

Report bugs on GitHub after checking that they haven't been reported:
- https://github.com/godotengine/godot/issues

----

- [Release notes](https://godotengine.org/article/maintenance-release-godot-3-6-3/)
- [Complete changelog](https://godotengine.github.io/godot-interactive-changelog/#3.6.3)
- [Curated changelog](https://github.com/godotengine/godot/blob/3.6.3-stable/CHANGELOG.md)

----

- **Download (GitHub):** Expand **Assets** below

## COMMIT SUBJECTS between the previous tag and the release

Bump version to 3.6.3-rc
Fix new CI compiler warnings
[3.x] Linux/TTS: Fix speechd deadlock
[3.x] GDScript: Fix missing function signature hint
FTI - Optimize non-interpolated 2D items
Preserve the output from the gradle build command
Make physics interpolation compatible with separate-thread rendering
Add proper flags when using external recast
mbedTLS: Update to 3.6.7
core: Backport OS::get_entropy from 4.x
mbedTLS: Always use Godot's OS as entropy source
[3.x] Android versions bump for 2026
Fix audio crackling issues due to incorrect WASAPI buffer size
Merge pull request #122094 from lawnjelly/3_6_3_cherrypicks_A
Suppress error when device is invalidated after `IAudioClient::GetBufferSize`
Minor BVH correctness fixes
[iOS] Bump min. version to 15.0, remove 32-bit code, add min. target export option.
[Buildsystem] Ping `master` cache after saving cache
Merge pull request #122488 from lawnjelly/3_6_3_cherrypicks_B
libpng: Update to 1.6.58
Merge pull request #122507 from lawnjelly/3_6_3_cherrypick_libpng
Changelog for 3.6.3
Merge pull request #122545 from lawnjelly/3_6_3_changelog
Add internal `get_entropy()` javascript function for web build
[iOS] Fix x86_64 simulator build.
Update Changelog with final changes for 3.6.3
Merge pull request #122700 from lawnjelly/3_6_3_cherrypicks_C
Bump version to 3.6.3-stable \o/

# CANDIDATE A

# Godot 3.6.3-stable

Godot 3.6.3 is a maintenance release of the 3.6 branch. It contains bug fixes, security-related dependency updates, a few performance improvements and platform updates for Android, iOS, Web, Windows and Linux.

## Breaking changes

- **iOS:** The minimum supported iOS version is now 15.0 (was 12.0). ([#122324](https://github.com/godotengine/godot/pull/122324))
- **iOS:** 32-bit (`armv7`/`i386`) support is removed, so the `architectures/armv7` export option is gone and only `arm64` is exported (plus `x86_64` for simulator builds). ([#122324](https://github.com/godotengine/godot/pull/122324))
- **Android:** Custom builds now target SDK 36 by default (was 35). Check that your project works with it. ([#120883](https://github.com/godotengine/godot/pull/120883))

## New features

- **iOS:** Added an `application/min_ios_version` export option so you can choose the minimum iOS version, which defaults to 15.0. ([#122324](https://github.com/godotengine/godot/pull/122324))

## Improvements

- **2D:** Physics interpolation now skips non-moving items, which makes it cheaper. ([#111195](https://github.com/godotengine/godot/pull/111195))
- **Android:** Gradle build errors now include the actual build output in the export error message. ([#120612](https://github.com/godotengine/godot/pull/120612))
- **Android:** Updated the build tooling to compileSdk/targetSdk 36, build-tools 36.1.0, Kotlin 2.1.21 and NDK 29. ([#120883](https://github.com/godotengine/godot/pull/120883))
- **GDScript:** The editor now shows the function signature hint for calls to script methods that were missing it. ([#68449](https://github.com/godotengine/godot/pull/68449))
- **Build:** Building with an external Recast library now uses the proper compiler flags. ([#112029](https://github.com/godotengine/godot/pull/112029))

## Fixes

- **Physics/Rendering:** Physics interpolation now works when the renderer runs on a separate thread. ([#114211](https://github.com/godotengine/godot/pull/114211))
- **Physics:** Fixed a few small BVH correctness issues, including missing locking in some accessors and an unsigned loop counter. ([#121501](https://github.com/godotengine/godot/pull/121501))
- **Audio (Windows):** Fixed audio crackling caused by an incorrect WASAPI buffer size. ([#122117](https://github.com/godotengine/godot/pull/122117))
- **Audio (Windows):** Removed a spurious error when the audio device is invalidated while the driver is starting. ([#122467](https://github.com/godotengine/godot/pull/122467))
- **Text-to-speech (Linux):** Fixed a deadlock with speech-dispatcher by handling its callbacks on the main thread. ([#110481](https://github.com/godotengine/godot/pull/110481))
- **iOS:** Fixed the x86_64 simulator build. ([#122639](https://github.com/godotengine/godot/pull/122639))
- **Core:** Fixed several uninitialized-data and buffer-overrun issues in `Image`, `MessageQueue`, `AudioEffectPitchShift` and the Windows DirectInput joypad code. ([#120627](https://github.com/godotengine/godot/pull/120627))

## Security and dependencies

- Updated mbedTLS to 3.6.7. ([#121110](https://github.com/godotengine/godot/pull/121110))
- Updated libpng to 1.6.58. ([#122506](https://github.com/godotengine/godot/pull/122506))
- mbedTLS now always uses Godot's own OS-provided entropy source, via a new internal `OS::get_entropy()`. ([#121894](https://github.com/godotengine/godot/pull/121894))
- **Web:** Added an internal `get_entropy()` JavaScript function so mbedTLS can get entropy in Web exports. ([#122647](https://github.com/godotengine/godot/pull/122647))

## Other

- CI: Updated the cache action to `v6`, changed its cache path, and pinged the `master` cache after saving. ([#122267](https://github.com/godotengine/godot/pull/122267))
- Updated the changelog and bumped the version to 3.6.3.


# CANDIDATE B

# Godot 3.6.3-stable

Godot 3.6.3 is a maintenance release of the 3.6 branch. It updates bundled libraries, raises the Android and iOS targets to current store requirements, and fixes bugs in audio, physics interpolation, text-to-speech and the script editor. It is based on 3.6.2-stable and should be a drop-in upgrade for 3.6.x projects.

Most changes were cherry-picked from the master branch in batches: [#122094](https://github.com/godotengine/godot/pull/122094), [#122488](https://github.com/godotengine/godot/pull/122488), [#122507](https://github.com/godotengine/godot/pull/122507) and [#122700](https://github.com/godotengine/godot/pull/122700). The changelog was added in [#122545](https://github.com/godotengine/godot/pull/122545). Individual fixes only link to a batch PR where the original PR number is not recorded in the history.

## Breaking changes

- **iOS:** The minimum supported iOS version is now 15.0 ([#122488](https://github.com/godotengine/godot/pull/122488)).
- **iOS:** 32-bit (armv7) support is removed, so iOS builds and exports are 64-bit only (arm64, plus x86_64 for the simulator) ([#122488](https://github.com/godotengine/godot/pull/122488)).
- **iOS:** The `architectures/*` options are removed from the iOS export preset ([#122488](https://github.com/godotengine/godot/pull/122488)).
- **Custom modules and platforms:** `OS` has a new pure virtual method `get_entropy()`. Custom platform ports must implement it, or they will not build ([#122094](https://github.com/godotengine/godot/pull/122094)).
- **Custom modules and platforms:** `VisualServer` has two new pure virtual methods, `sync_and_halt()` and `thaw()`. Custom `VisualServer` implementations must provide them ([#122094](https://github.com/godotengine/godot/pull/122094)).

## Added

### Export

- iOS: Add an `application/min_ios_version` export option, which defaults to `15.0` ([#122488](https://github.com/godotengine/godot/pull/122488)).

## Changed

### Android

- Target and compile against Android API 36 by default, and use NDK r29 (29.0.14206865), build tools 36.1.0 and Kotlin 2.1.21 ([#122094](https://github.com/godotengine/godot/pull/122094)).
- Handle the back button through the Android back-pressed dispatcher instead of the deprecated `onBackPressed()` override ([#122094](https://github.com/godotengine/godot/pull/122094)).
- Show the gradle output in the error message when an Android export fails to build or to copy the binary ([#122094](https://github.com/godotengine/godot/pull/122094)).
- Print the gradle output in verbose mode when an Android export succeeds ([#122094](https://github.com/godotengine/godot/pull/122094)).

### Networking and security

- Update mbedTLS to 3.6.7 ([#122094](https://github.com/godotengine/godot/pull/122094)).
- mbedTLS now always takes its random data from the operating system through the new `OS::get_entropy()`, with implementations for all platforms including the web ([#122094](https://github.com/godotengine/godot/pull/122094)).
- Web: Fall back to `crypto.getRandomValues()` for entropy when building with Emscripten older than 2.0.5 ([#122700](https://github.com/godotengine/godot/pull/122700)).

### Thirdparty

- Update libpng to 1.6.58 ([#122507](https://github.com/godotengine/godot/pull/122507)).

### Rendering

- 2D physics interpolation: Make non-interpolated canvas items cheaper to render ([#122094](https://github.com/godotengine/godot/pull/122094)).

## Fixed

### Audio

- Windows: Fix audio crackling caused by using the wrong WASAPI buffer size ([#122094](https://github.com/godotengine/godot/pull/122094)).
- Windows: Don't print an error when the audio device is removed or changed while its buffer size is being read ([#122488](https://github.com/godotengine/godot/pull/122488)).
- Fix a compiler warning about the Pitch Shift effect's frame size, and ignore invalid frame sizes with an error message ([#122094](https://github.com/godotengine/godot/pull/122094)).

### Editor

- GDScript: Show the argument hint when calling a method defined in the current script ([#122094](https://github.com/godotengine/godot/pull/122094)).

### Physics

- Fix physics interpolation breaking or glitching when rendering runs on a separate thread ([#122094](https://github.com/godotengine/godot/pull/122094)).
- Fix thread-safety, overflow and uninitialized-value issues in the BVH used for 3D culling and physics broadphase ([#122488](https://github.com/godotengine/godot/pull/122488)).

### Platforms

- Linux: Fix a deadlock in text-to-speech with speech-dispatcher ([#122094](https://github.com/godotengine/godot/pull/122094)).
- Windows: Initialize the DirectInput joypad device and GUID fields to avoid reading uninitialized memory ([#122094](https://github.com/godotengine/godot/pull/122094)).
- macOS: Link the `Security` framework, which the new entropy source needs ([#122094](https://github.com/godotengine/godot/pull/122094)).
- iOS: Fix building the x86_64 simulator ([#122700](https://github.com/godotengine/godot/pull/122700)).

### Core

- Fix `Image.fix_alpha_edges()` possibly reading an uninitialized colour ([#122094](https://github.com/godotengine/godot/pull/122094)).
- Fix the message queue destructor using a message after destroying it ([#122094](https://github.com/godotengine/godot/pull/122094)).

### Buildsystem

- Linux and server builds: Pass the correct compiler and linker flags when building with `builtin_recast=no` ([#122094](https://github.com/godotengine/godot/pull/122094)).

## Other

- Fix new compiler warnings reported by CI.
- Make the CI build cache update the `master` cache after saving.
- Update the bundled license information (`COPYRIGHT.txt`) and version numbers.
- Update the changelog and bump the version to 3.6.3.

