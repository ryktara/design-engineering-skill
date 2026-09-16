import { build } from "esbuild";
await build({
  entryPoints: ["src/main.jsx"],
  bundle: true,
  outfile: "public/bundle.js",
  jsx: "automatic",
  define: { "process.env.NODE_ENV": '"production"' },
  minify: false,
  sourcemap: false,
  logLevel: "info",
});
