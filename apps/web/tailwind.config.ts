import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0066cc",
        "primary-focus": "#0071e3",
        "primary-on-dark": "#2997ff",
        ink: "#1d1d1f",
        body: "#1d1d1f",
        "body-on-dark": "#ffffff",
        "body-muted": "#cccccc",
        "ink-muted-80": "#333333",
        "ink-muted-48": "#7a7a7a",
        "divider-soft": "#f0f0f0",
        hairline: "#e0e0e0",
        canvas: "#ffffff",
        "canvas-parchment": "#f5f5f7",
        "surface-pearl": "#fafafc",
        "surface-tile-1": "#272729",
        "surface-tile-2": "#2a2a2c",
        "surface-tile-3": "#252527",
        "surface-black": "#000000",
        "surface-chip": "#d2d2d7",
        "on-primary": "#ffffff",
        "on-dark": "#ffffff",
        warning: "#d4a017",
        error: "#c64545",
        success: "#5db872"
      },
      fontFamily: {
        display: ["SF Pro Display", "system-ui", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        sans: ["SF Pro Text", "system-ui", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ["SF Mono", "ui-monospace", "monospace"]
      },
      fontSize: {
        "hero-display": ["56px", { lineHeight: "1.07", letterSpacing: "-0.28px", fontWeight: "600" }],
        "display-lg": ["40px", { lineHeight: "1.1", letterSpacing: "0", fontWeight: "600" }],
        "display-md": ["34px", { lineHeight: "1.47", letterSpacing: "-0.374px", fontWeight: "600" }],
        "lead": ["28px", { lineHeight: "1.14", letterSpacing: "0.196px", fontWeight: "400" }],
        "lead-airy": ["24px", { lineHeight: "1.5", letterSpacing: "0", fontWeight: "300" }],
        "tagline": ["21px", { lineHeight: "1.19", letterSpacing: "0.231px", fontWeight: "600" }],
        "body-strong": ["17px", { lineHeight: "1.24", letterSpacing: "-0.374px", fontWeight: "600" }],
        "body": ["17px", { lineHeight: "1.47", letterSpacing: "-0.374px", fontWeight: "400" }],
        "dense-link": ["17px", { lineHeight: "2.41", letterSpacing: "0", fontWeight: "400" }],
        "caption": ["14px", { lineHeight: "1.43", letterSpacing: "-0.224px", fontWeight: "400" }],
        "caption-strong": ["14px", { lineHeight: "1.29", letterSpacing: "-0.224px", fontWeight: "600" }],
        "btn-large": ["18px", { lineHeight: "1.0", letterSpacing: "0", fontWeight: "300" }],
        "btn-utility": ["14px", { lineHeight: "1.29", letterSpacing: "-0.224px", fontWeight: "400" }],
        "fine-print": ["12px", { lineHeight: "1.0", letterSpacing: "-0.12px", fontWeight: "400" }],
        "micro-legal": ["10px", { lineHeight: "1.3", letterSpacing: "-0.08px", fontWeight: "400" }],
        "nav-link": ["12px", { lineHeight: "1.0", letterSpacing: "-0.12px", fontWeight: "400" }]
      },
      borderRadius: {
        xs: "5px",
        sm: "8px",
        md: "11px",
        lg: "18px",
        pill: "9999px"
      },
      spacing: {
        "xxs": "4px",
        "section": "80px"
      },
      boxShadow: {
        "product": "rgba(0, 0, 0, 0.22) 3px 5px 30px 0px"
      },
      maxWidth: {
        "content": "980px",
        "grid": "1440px"
      }
    }
  },
  plugins: []
};

export default config;
