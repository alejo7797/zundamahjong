[doc("Show this help message and exit")]
help:
    @just --list


# Hacking on Zundamahjong

[doc("Run the debug Werkzeug server")]
debug-server:
    uv run -m zundamahjong --debug

[doc("Run the debug Vite client")]
debug-client:
    npm --prefix=client run dev

# Formatting code

[doc("Format client source code")]
format-client:
    npm --prefix=client run lint:format

[doc("Format server source code")]
format-server:
    ruff format

[doc("Format all code")]
format-all: format-client format-server

# Running checks on code

[doc("Lint client source code")]
lint-client:
    npm --prefix=client run build:check
    npm --prefix=client run lint

[doc("Check client source code formatting")]
check-format-client:
    npm --prefix=client run format:check

[doc("Run client tests")]
test-client:
    npm --prefix=client run test

[doc("Build client")]
build-client:
    npm --prefix=client run build

[doc("Run all client checks")]
check-client: lint-client check-format-client test-client

[doc("Lint server source code")]
lint-server:
    basedpyright
    mypy
    ruff check

[doc("Check server source code formatting")]
check-format-server:
    ruff format --check

[doc("Run server tests")]
test-server:
    pytest

[doc("Run all server checks")]
check-server: lint-server check-format-server test-server

[doc("Run all checks")]
check-all: check-client check-server

# Generating client pattern data

[doc("Generate client pattern data")]
gen-pattern:
    python src/zundamahjong/mahjong/pattern/print_ts.py > client/src/types/pattern.ts
    npx --prefix=client prettier --write client/src/types/pattern.ts

# Working with the Sphinx docs

[doc("Clean existing doc builds")]
docs-clean:
    ! [[ -d docs/build ]] || rm -r docs/build

[doc("Build developer documentation")]
docs: docs-clean
    sphinx-build -M html docs/source/ docs/build/

[doc("Build auto-reloading developer documentation")]
docs-auto: docs-clean
    sphinx-autobuild docs/source docs/build/html --watch src
