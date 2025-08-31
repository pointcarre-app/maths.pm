import { configSujets0DataOnly, isSafari } from "./config.js";

// Global state singleton for sujets0-data-only
// Always reference and mutate through this object to keep a single source of truth.
export const S0 = (function ensureGlobalState() {
  if (window.S0 && window.S0.__isSujets0DataOnlyState) {
    return window.S0;
  }

  const initialState = {
    __isSujets0DataOnlyState: true,
    config: configSujets0DataOnly,
    env: {
      isSafari: isSafari(),
    },
    assets: {
      domtoimage: null,
    },
    pca: {
      loaderClass: null,
      loaderInstance: null,
    },
    nagini: {
      module: null,
      manager: null,
      ready: false,
    },
    results: {
      questionResults: [],
    },
    ui: {
      tableElement: null,
    },
  };

  window.S0 = initialState;
  return window.S0;
})();

export function setInState(path, value) {
  // Minimal helper to set shallow properties using a dot path
  const segments = path.split(".");
  let cursor = S0;
  for (let i = 0; i < segments.length - 1; i++) {
    const key = segments[i];
    if (!(key in cursor) || typeof cursor[key] !== "object") {
      cursor[key] = {};
    }
    cursor = cursor[key];
  }
  cursor[segments[segments.length - 1]] = value;
}

export function getFromState(path, fallback = undefined) {
  const segments = path.split(".");
  let cursor = S0;
  for (let i = 0; i < segments.length; i++) {
    const key = segments[i];
    if (!(key in cursor)) return fallback;
    cursor = cursor[key];
  }
  return cursor;
}


