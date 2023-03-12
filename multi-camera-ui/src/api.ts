import { CameraControlState, RouteControlState, RouteInfo, VideoFile, VideoFiles } from "./types";

export const getRouteInfos = async () => {
  const response = await fetch("/api/camera-info/");
  return (await response.json()) as RouteInfo[];
};

export const getVideoFiles = async (): Promise<VideoFile[]> => {
  const response = await fetch("/video-files/");
  const content = (await response.json()) as VideoFiles;
  const files = content.files.map((f) => ({
    title: f,
    name: f,
  }));
  return files;
};

export const controlCamera = async (cameraId: number, state: string): Promise<CameraControlState> => {
  const response = await fetch("/control-camera/", {
    method: "post",
    body: JSON.stringify({ camera_id: cameraId, state }),
  });
  const content = (await response.json()) as CameraControlState;
  return content;
};

export const controlRoute = async (routeId: number, state: string): Promise<RouteControlState> => {
  const response = await fetch("/control-route/", {
    method: "post",
    body: JSON.stringify({ route_id: routeId, state }),
  });
  const content = (await response.json()) as RouteControlState;
  return content;
};
