import { RouteInfo } from "./types";

export const getRouteInfos = async () => {
  const response = await fetch("/api/camera-info/");
  return (await response.json()) as RouteInfo[];
};
