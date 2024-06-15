import path from "path"
import { defineConfig } from 'vitest/config';
import solid_plugin from "vite-plugin-solid";
import solid_svg from "vite-plugin-solid-svg";
import prism from "vite-plugin-prismjs";
// import devtools from "solid-devtools/vite";

export default defineConfig({
  plugins: [
    /* 
    Uncomment the following line to enable solid-devtools.
    For more info see https://github.com/thetarnav/solid-devtools/tree/main/packages/extension#readme
    */
    // devtools(),
    solid_plugin(),
    solid_svg(),
    prism({
      languages: ["python", "json"],
      plugins: ["line-numbers", "line-highlight"], // "toolbar", "copy-to-clipboard"],
      theme: "okaidia", // "okaidia", // "default"
      css: true,
    })
  ],
  test: { 
    globals: true, 
    testTransformMode: { 
        web: ['tsx', 'ts'], 
    }, 
  },
  resolve: {
    alias: {
      "@src": path.resolve(__dirname, "./src"),
    }
  },
  css: {
    preprocessorOptions: {
      styl: {
        paths: [path.resolve(__dirname, "./src"), path.resolve(__dirname, "./node_modules")]
      }
    }
  },
  server: {
    port: 3000,
  },
  build: {
    target: "esnext",
  },
});
