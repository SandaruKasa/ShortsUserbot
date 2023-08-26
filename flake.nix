{
  description = "A Telegram userbot that converts all YouTube Shorts link to normal videos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
  };

  outputs = { self, nixpkgs }:
    let
      allSystems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });

      selectPython = pkgs: pkgs.python311;
      selectPythonPackages = pypkgs: with pypkgs; [
        pyrogram
        tgcrypto
      ];
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default =
          let
            python = selectPython pkgs;
            devPackages = with pkgs; [
              nixpkgs-fmt
              black
              mypy
            ];
          in
          pkgs.mkShellNoCC {
            packages = [ (python.withPackages selectPythonPackages) ] ++ devPackages;
          };
      });
      packages = forAllSystems ({ pkgs }: {
        default =
          let
            python = selectPython pkgs;
            pythonPkgs = python.pkgs;
          in
          pythonPkgs.buildPythonApplication {
            name = "shorts-userbot";
            format = "pyproject";
            buildInputs = with pythonPkgs; [ setuptools ];
            propagatedBuildInputs = selectPythonPackages pythonPkgs;
            src = ./.;
          };
      });
    };
}
