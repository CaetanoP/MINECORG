JUST_CONFIG_TEMPLATE = """
import {{ argv, parallel, series, task, tscTask }} from "just-scripts";
import {{
  BundleTaskParameters,
  CopyTaskParameters,
  bundleTask,
  cleanTask,
  cleanCollateralTask,
  copyTask,
  coreLint,
  mcaddonTask,
  setupEnvironment,
  ZipTaskParameters,
  STANDARD_CLEAN_PATHS,
  DEFAULT_CLEAN_DIRECTORIES,
  getOrThrowFromProcess,
  watchTask,
}} from "@minecraft/core-build-tasks";
import path from "path";
setupEnvironment(path.resolve(__dirname, ".env"));
const projectName = getOrThrowFromProcess("PROJECT_NAME");
const bundleTaskOptions: BundleTaskParameters = {{
  entryPoint: path.join(__dirname, "./scripts/main.ts"),
  external: ["@minecraft/server", "@minecraft/server-ui"],
  outfile: path.resolve(__dirname, "./dist/scripts/main.js"),
  minifyWhitespace: false,
  sourcemap: true,
  outputSourcemapPath: path.resolve(__dirname, "./dist/debug"),
}};
const copyTaskOptions: CopyTaskParameters = {{
  copyToBehaviorPacks: [`./behavior_packs/${{projectName}}`],
  copyToScripts: ["./dist/scripts"],
  copyToResourcePacks: [`./resource_packs/${{projectName}}`],
}};
const mcaddonTaskOptions: ZipTaskParameters = {{
  ...copyTaskOptions,
  outputFile: `./dist/packages/${{projectName}}.mcaddon`,
}};
task("lint", coreLint(["scripts/**/*.ts"], argv().fix));
task("typescript", tscTask());
task("bundle", bundleTask(bundleTaskOptions));
task("build", series("typescript", "bundle"));
task("clean-local", cleanTask(DEFAULT_CLEAN_DIRECTORIES));
task("clean-collateral", cleanCollateralTask(STANDARD_CLEAN_PATHS));
task("clean", parallel("clean-local", "clean-collateral"));
task("copyArtifacts", copyTask(copyTaskOptions));
task("package", series("clean-collateral", "copyArtifacts"));
task(
  "local-deploy",
  watchTask(
    ["scripts/**/*.ts", "behavior_packs/**/*.{{json,lang,tga,ogg,png}}", "resource_packs/**/*.{{json,lang,tga,ogg,png}}"],
    series("clean-local", "build", "package")
  )
);
task("createMcaddonFile", mcaddonTask(mcaddonTaskOptions));
task("mcaddon", series("clean-local", "build", "createMcaddonFile"));
"""
ESLINT_CONFIG_TEMPLATE = """
import minecraftLinting from "eslint-plugin-minecraft-linting";
import tsParser from "@typescript-eslint/parser";
import ts from "@typescript-eslint/eslint-plugin";
export default [
  {
    files: ["scripts/**/*.ts"],
    languageOptions: {
      parser: tsParser,
      ecmaVersion: "latest",
    },
    plugins: {
      ts,
      "minecraft-linting": minecraftLinting,
    },
    rules: {
      "minecraft-linting/avoid-unnecessary-command": "error",
    },
  },
];
"""
TS_CONFIG_TEMPLATE = """{
  "compilerOptions": {
    "target": "es6",
    "moduleResolution": "Node",
    "module": "ES2020",
    "declaration": false,
    "noLib": false,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "sourceMap": true,
    "pretty": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "allowUnreachableCode": true,
    "allowUnusedLabels": true,
    "noImplicitAny": true,
    "noImplicitReturns": false,
    "noImplicitUseStrict": false,
    "outDir": "lib",
    "rootDir": ".",
    "baseUrl": "behavior_packs/",
    "listFiles": false,
    "noEmitHelpers": true,
    "skipLibCheck": true
  },
  "include": [
    "scripts/**/*"
  ],
  "exclude": [
    "lib",
    "dist",
    "node_modules"
  ],
  "compileOnSave": false
}
"""