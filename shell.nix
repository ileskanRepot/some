{ pkgs ? import <nixpkgs> {}}:
  pkgs.mkShell {
    nativeBuildInputs = let
      env = pyPkgs : with pyPkgs; [
        fastapi
        uvicorn
      ];
    in with pkgs; [
      (python311.withPackages env)
      nodejs
      nodePackages.npm
      vite
  ];
}
