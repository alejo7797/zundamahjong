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
      { lib, ... }: {

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
                myOverlay = _: prev: {
                  zundamahjong = prev.zundamahjong.overrideAttrs (oldAttrs: {
                    outputs = [
                      "out" "doc"
                    ];

                    nativeBuildInputs = oldAttrs.nativeBuildInputs ++ [
                      python.pkgs.sphinxHook
                    ];

                    preBuildSphinx = ''
                      export PYTHONPATH=${lib.makeSearchPath python.sitePackages [
                        (pythonSet.mkVirtualEnv "zundamahjong-deps" (
                          { sphinx-rtd-theme = [ ]; } // pythonSet.zundamahjong.dependencies
                        )) "$out" # This "fix" is pretty cursed :(
                      ]}
                    '';

                    preBuild = ''
                      cp -r ${self'.packages.zundamahjong-client} client_build
                      chmod -R u+w client_build
                    '';
                  });
                };

                inherit (pkgs.callPackages inputs.pyproject-nix.build.util { }) mkApplication;
                distPythonSet = pythonSet.overrideScope myOverlay;
              in

              {
                default = self'.packages.zundamahjong;

                venv = distPythonSet.mkVirtualEnv "venv" (
                  workspace.deps.optionals // { gunicorn = [ ]; }
                );

                zundamahjong-client = pkgs.buildNpmPackage {
                  name = "zundamahjong-client";
                  src = ./client;

                  npmDepsHash = "sha256-nAUdwnayf0CtYmXfKEfudBztMq7LLBUi3eFudHAO+Ak=";
                  npmPackFlags = [ "--ignore-scripts" ];

                  installPhase = ''
                    runHook preInstall
                    mkdir -p $out && cp -r ../client_build/. $out
                    runHook postInstall
                  '';
                };

                zundamahjong = (
                  mkApplication {
                    package = distPythonSet.zundamahjong;
                    inherit (self'.packages) venv;
                  }
                ).overrideAttrs {
                  passthru = {
                    inherit (distPythonSet.zundamahjong) doc;
                    inherit (self'.packages) venv;
                  };
                };
              };

          };

      }
    );

}
