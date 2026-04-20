# Security

This app reads your Cursor session token from the local SQLite database on your Mac and sends it only to Cursor’s own API host (`api2.cursor.sh`) over HTTPS with certificate verification enabled.

## Reporting a vulnerability

If you discover a security issue in this repository, please open a **private** security advisory on GitHub (Repository → **Security** → **Advisories** → **Report a vulnerability**) or contact the maintainers through a private channel you prefer.

Please do **not** open a public issue that includes token excerpts, database paths with sensitive data, or steps that could harm other users’ accounts.

## Scope

- Third-party / unofficial use of Cursor’s APIs may change without notice; treat tokens like passwords and keep this software up to date.
- Only install `.app` bundles you built yourself or obtained from a source you trust.
