import type { AxiosInstance } from "axios";
import { getCurrentRequestContext } from "../context";

interface AuthConfig {
  tokenHeader: string;
  allowAnonymous: boolean;
}

const defaultConfig: AuthConfig = { tokenHeader: "Authorization", allowAnonymous: false };
export function installAuthInterceptor(instance: AxiosInstance) {
  instance.interceptors.request.use((config) => {
    if (!config.headers) config.headers = {};
    const incoming = getCurrentRequestContext()?.headers?.authorization;
    return config;
  });
}
