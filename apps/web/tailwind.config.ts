import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#cc785c",
        "primary-active": "#a9583e",
        ink: "#141413",
        body: "#3d3d3a",
        muted: "#6c6a64",
        canvas: "#faf9f5",
        "surface-card": "#efe9de",
        "surface-dark": "#181715",
        "surface-dark-elevated": "#252320",
        hairline: "#e6dfd8",
        warning: "#d4a017",
        error: "#c64545",
        success: "#5db872"
      },
      fontFamily: {
        display: ["Copernicus", "Tiempos Headline", "serif"],
        sans: ["StyreneB", "Inter", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"]
      },
      borderRadius: {
        lgx: "16px"
      }
    }
  },
  plugins: []
};

export default config;
