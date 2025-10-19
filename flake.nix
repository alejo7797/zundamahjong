{
  description = "Web-based Mahjong game by faraplay";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        pyproject-nix.follows = "pyproject-nix";
        uv2nix.follows = "uv2nix";
      };
    };
  };

  outputs =
    inputs@{ flake-parts, uv2nix, ... }:

    let
      workspace = uv2nix.lib.workspace.loadWorkspace {
        workspaceRoot = ./.;
      };

      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      editableOverlay = workspace.mkEditablePyprojectOverlay {
        root = "$REPO_ROOT";
      };
    in

    flake-parts.lib.mkFlake { inherit inputs; } (
      { lib, getSystem, ... }: {

        systems = [
          "x86_64-linux" "aarch64-darwin"
          "aarch64-linux" "x86_64-darwin"
        ];

        perSystem =
          { pkgs, self', ... }:

          let
            python = pkgs.python313;

            pythonSet =
              (pkgs.callPackage inputs.pyproject-nix.build.packages {
                inherit python;
              }).overrideScope (lib.composeManyExtensions [
                inputs.pyproject-build-systems.overlays.wheel overlay
              ]);
          in

          {
            devShells.default =

              let
                devPythonSet = pythonSet.overrideScope editableOverlay;
                virtualenv = devPythonSet.mkVirtualEnv "zundamahjong-dev-env" workspace.deps.all;
              in

              pkgs.mkShell {

                packages = [
                  pkgs.nodejs virtualenv
                ];

                env = {
                  UV_NO_SYNC = "1";
                  UV_PYTHON = devPythonSet.python.interpreter;
                  UV_PYTHON_DOWNLOADS = "never";
                };

                shellHook = ''
                  unset PYTHONPATH
                  export REPO_ROOT=$(git rev-parse --show-toplevel)
                '';

              };

            packages =

              let
                version = "0.2.0a2";
              in

              rec {

                zundamahjong = pkgs.callPackage (
                  {
                    python3Packages,
                    zundamahjong-client,
                  }:

                  python3Packages.buildPythonPackage {
                    pname = "zundamahjong";
                    inherit version;
                    format = "pyproject";

                    outputs = [
                      "doc"
                      "out"
                    ];

                    src = ./.;

                    build-system = with python3Packages; [
                      setuptools
                      setuptools-scm
                    ];

                    nativeBuildInputs = [
                      python3Packages.sphinxHook
                    ];

                    dependencies = with python3Packages; [
                      flask
                      flask-socketio
                      pydantic
                      sqlalchemy
                    ];

                    preBuild = ''
                      cp -r ${zundamahjong-client} client_build
                      chmod -R u+w client_build
                    '';

                    pythonImportsCheck = [
                      "zundamahjong"
                    ];

                    nativeCheckInputs = [
                      python3Packages.pytestCheckHook
                    ];

                    meta = {
                      description = "Web-based Mahjong game";
                      homepage = "https://github.com/faraplay/zundamahjong";
                      license = lib.licenses.mit;
                    };
                  }
                )
                {
                  inherit (self'.packages) zundamahjong-client;
                };

                zundamahjong-client = pkgs.callPackage (
                  { buildNpmPackage }:

                  buildNpmPackage {
                    pname = "zundamahjong-client";
                    inherit version;

                    src = ./client;

                    npmDepsHash = "sha256-nAUdwnayf0CtYmXfKEfudBztMq7LLBUi3eFudHAO+Ak=";
                    npmPackFlags = [ "--ignore-scripts" ];

                    installPhase = ''
                      runHook preInstall
                      mkdir -p $out && cp -r ../client_build/. $out
                      runHook postInstall
                    '';
                  }
                ) { };

                default = zundamahjong;

              };

          };

        flake.overlays.default =
          final: prev:

          let
            config = getSystem prev.stdenv.hostPlatform.system;

            pythonOverlay = python-final: python-prev: {
              zundamahjong = config.packages.zundamahjong.override { python3Packages = python-final; };
            };
          in

          {
            pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [ pythonOverlay ];
          };

      }
    );

}
