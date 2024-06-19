{
  nixpkgs,
  python_version,
  pythonOverrideUtils,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    inherit (nixpkgs."${python_version}".pkgs) buildPythonPackage;
    inherit (nixpkgs.python3Packages) fetchPypi;
  };

  utils = pythonOverrideUtils;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;

  layer_1 = python_pkgs:
    python_pkgs
    // {
      grimp = import ./grimp {
        inherit lib python_pkgs;
      };
      types-deprecated = import ./deprecated/stubs.nix lib;
    };

  python_pkgs = utils.compose [layer_1] nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
