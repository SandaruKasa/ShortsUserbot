{
  description = "A Telegram userbot that converts all YouTube Shorts link to normal videos";

  outputs = inputs @ { nixpkgs, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem = { pkgs, ... }:
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
              packages = [
                (python.withPackages (takeAttrs (pythonDeps ++ pythonDevDeps)))
                pkgs.nixpkgs-fmt
              ];
            };
        };
    };
}
    