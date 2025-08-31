import { configSujets0DataOnly, loadModuleDynamically } from "./config.js";
import { S0, setInState, getFromState } from "./state.js";

export async function ensurePcaLoaderLoaded() {
  if (!getFromState("pca.loaderClass")) {
    const module = await loadModuleDynamically(
      configSujets0DataOnly.v4PyJsPCAGraphLoaderUrl
    );
    setInState("pca.loaderClass", module.PCAGraphLoader);
  }
}

export async function ensurePcaLoaderInstance(config = {}) {
  await ensurePcaLoaderLoaded();
  let instance = getFromState("pca.loaderInstance", null);
  const LoaderClass = getFromState("pca.loaderClass", null);
  if (!instance && LoaderClass) {
    instance = new LoaderClass({
      debug: false,
      graphConfig: config,
      pcaVersion: "v0.0.27",
    });
    await instance.initialize();
    setInState("pca.loaderInstance", instance);
  } else if (instance && config && Object.keys(config).length > 0) {
    instance.updateConfig(config);
  }
  return instance;
}

export async function buildPCAGraph(graphKey, config = {}) {
  try {
    const loader = await ensurePcaLoaderInstance(config);
    const result = await loader.renderGraph(graphKey);
    return result;
  } catch (error) {
    console.error("PCA Graph Error:", error);
    return { svg: "<svg></svg>", graphDict: {} };
  }
}


