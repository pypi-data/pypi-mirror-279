import type { StorybookConfig } from "storybook-solidjs-vite";
import { mergeConfig } from "vite";
import solid_svg from 'vite-plugin-solid-svg';

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@chromatic-com/storybook",
    "@storybook/addon-interactions",
  ],
  framework: {
    name: "storybook-solidjs-vite",
    options: {},
  },
  docs: {
    autodocs: "tag",
  },
  viteFinal: config => mergeConfig(config, {
    plugins: [solid_svg()]
  })

};
export default config;
