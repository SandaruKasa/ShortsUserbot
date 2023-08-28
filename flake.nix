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


      takeAttrs = attrList: x: (map (attr: x."${attr}") attrList);

      selectPython = pkgs: pkgs.python311;
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
            propagatedBuildInputs = takeAttrs pythonDeps pythonPkgs;
            src = ./.;
          };
      });

      devShells = forAllSystems ({ pkgs }: {
        default =
          let
            python = (selectPython pkgs).withPackages
              (takeAttrs (pythonDeps ++ pythonDevDeps));
          in
          pkgs.mkShellNoCC {
            packages = [
              python
              pkgs.nixpkgs-fmt
            ];
          };
      });
    };
}
