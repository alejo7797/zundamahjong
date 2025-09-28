{
  description = "Web-based Mahjong game by faraplay";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {

      systems = [
        "x86_64-linux" "aarch64-darwin"
        "aarch64-linux" "x86_64-darwin"
      ];

      perSystem = { pkgs, ... }: {

        devShells.default = pkgs.mkShell {
          packages = [ pkgs.nodejs_22 pkgs.python313 ];
        };

      };

    };
}
