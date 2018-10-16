# Quena Console

## What is it?
Quena Console is a CLI for [Quena Web](https://github.com/zelton/quena), a self-hosted knowledge management tool. It helps you quickly look up your notes and thanks to [ConsoleMD](https://github.com/kneufeld/consolemd) it outputs proper Markdown.

## How can I run it?
1. Install Python, pip and [pipenv](https://github.com/pypa/pipenv).
2. Run `pipenv install` and then `pyinstaller quena.spec`.
3. The application will be built under `dist/` directory. Move it where you like and add to `PATH` to have global access.
4. Run `quena` in your terminal!

```bash
$ quena --help
Usage: quena [OPTIONS] [PHRASE]

Options:
  --url           Show the API base URL and exit.
  --set-url TEXT  Set the API base URL and exit. Example:
                  https://quena.yourdomain.com
  --help          Show this message and exit.
```

```bash
$ quena 'running tests'

Running tests for Quena Web
---------------------------
$ composer test

Running tests for Quena Console
-------------------------------
$ pytest
```

```bash
$ quena
What are you looking for? running tests

Running tests for Quena Web
---------------------------
$ composer test

Running tests for Quena console
-------------------------------
$ pytest
```
