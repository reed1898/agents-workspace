import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0f172a",
        surface: "#111827",
        accent: "#22c55e",
        warn: "#f59e0b",
        danger: "#ef4444"
      },
      fontFamily: {
        sans: ["'Space Grotesk'", "'IBM Plex Sans'", "ui-sans-serif", "system-ui"]
      }
    }
  },
  plugins: []
};

export default config;
