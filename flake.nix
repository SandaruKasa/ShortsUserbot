{
  description = "A Telegram userbot that converts all YouTube Shorts link to normal videos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    nixpkgs-lib.url = "github:NixOS/nixpkgs/nixos-24.11?dir=lib";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs = {
        nixpkgs-lib.follows = "nixpkgs-lib";
      };
    };
    pre-commit-hooks-nix = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs = inputs @ { nixpkgs, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.pre-commit-hooks-nix.flakeModule
      ];

      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem = { pkgs, config, ... }:
        let
          takeAttrs = attrList: x: (map (attr: x."${attr}") attrList);

          python = pkgs.python311;
          pythonPkgs = python.pkgs;
          pythonDeps = [
            "pyrogram"
            "tgcrypto"
          ];
          pythonDevDeps = [
            "black"
            "mypy"
            "isort"
          ];
        in
        {
          packages.default =
            pythonPkgs.buildPythonApplication {
              name = "shorts-userbot";
              format = "pyproject";
              buildInputs = with pythonPkgs; [ setuptools ];
              propagatedBuildInputs = takeAttrs pythonDeps pythonPkgs;
              src = ./.;
            };


          devShells.default =
            pkgs.mkShellNoCC {
              inherit (config.pre-commit.devShell) shellHook;
              packages = [
                (python.withPackages (takeAttrs (pythonDeps ++ pythonDevDeps)))
              ];
            };

          pre-commit.settings = {
            hooks = {
              black.enable = true;
              isort.enable = true;
              nixpkgs-fmt.enable = true;
            };

            settings = {
              isort.profile = "black";
            };
          };

          formatter = pkgs.nixpkgs-fmt;
        };
    };
}
    