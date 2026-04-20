# Contributing

Thanks for your interest in improving this project.

## Development setup

1. Clone the repo and create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the app from source (menu bar app; quit with Activity Monitor or the app’s Quit item after a local run):
   ```bash
   python src/app.py
   ```

3. Build the macOS app bundle and install to `/Applications`:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

## Pull requests

- Keep changes focused and match existing style in `src/app.py`.
- Do not commit `venv/`, `dist/`, or `build/` (they are gitignored).
- Do not commit machine-specific notes, agent handoff files, or internal docs: `AGENT_SESSION_CONTEXT.md`, `docs/internal/`, and `*.local.md` are intentionally ignored. Keep those only on your machine.
- Never commit real tokens, cookies, or database copies from Cursor’s `state.vscdb`.
- If you change behavior or dependencies, update `README.md` and `requirements.txt` as needed.
