# Agent Session Context

This file provides context for new sessions/agents working on the `cursor-usage-menubar` project.

## Recent Work
- **April 19, 2026**: GitHub publication prep.
  - Expanded `.gitignore` (`.venv`, caches, etc.).
  - Added `SECURITY.md`, `CONTRIBUTING.md`; README updated (disclaimer, renewal feature, publish steps).
  - Initialized git on `main` with an initial commit (ready for `git remote add` / `git push`).
- **April 18, 2026**: Initial creation of the application.
  - Implemented `src/app.py` using `rumps` and `urllib` to hit the `api2.cursor.sh` DashboardService endpoint.
  - Used read-only SQLite connections to avoid WAL locks when reading `cursorAuth/accessToken`.
  - Generated and processed an AI application icon (`assets/icon.png` -> `assets/icon.icns`).
  - Packaged the project for macOS using `py2app` inside `setup.py` (LSUIElement set to True to hide the dock icon).
  - Adjusted UI to remove the "Cursor: " prefix and keep items fully opaque using dummy callbacks.
  - Restructured root folder for open-source GitHub publishing (`src`, `assets`, `scripts`, `README.md`, `LICENSE`, `.gitignore`, `requirements.txt`).

## Key Paths & Commands
- **App Logic**: `src/app.py`
- **Build Config**: `setup.py`
- **Build Script**: `build.sh` (Runs the build process, clears old instances, copies to `/Applications`, and starts the new instance).
- **Environment**: To install dependencies: `pip install -r requirements.txt`.