import { useQuery } from "react-query";
import { CameraControlState, RouteControlState, RouteInfo, VideoFile, VideoFiles } from "./types";

export const fetchRouteInfos = async () => {
  const response = await fetch("/api/route-info/");
  console.log("fetch", "/api/route-info/");
  return (await response.json()) as RouteInfo[];
};

export const getRouteInfos = () => useQuery("routes", fetchRouteInfos);

export const getVideoFiles = async (): Promise<VideoFile[]> => {
  const response = await fetch("/api/video-files/");
  console.log("fetch", "/video-files/");
  const content = (await response.json()) as VideoFiles;
  const files = content.files.map((f) => ({
    title: f,
    name: f,
  }));
  return files;
};

export const controlCamera = async (cameraId: number, state: string): Promise<CameraControlState> => {
  const response = await fetch("/api/control-camera/", {
    method: "post",
    body: JSON.stringify({ camera_id: cameraId, state }),
  });
  const content = (await response.json()) as CameraControlState;
  return content;
};

export const controlRoute = async (routeId: number, state: string): Promise<RouteControlState> => {
  const response = await fetch("/api/control-route/", {
    method: "post",
    body: JSON.stringify({ route_id: routeId, state }),
  });
  const content = (await response.json()) as RouteControlState;
  return content;
};
