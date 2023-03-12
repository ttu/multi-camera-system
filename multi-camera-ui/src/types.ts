export interface RouteInfo {
  route_id: string;
  name: string;
  cameras: CameraInfo[];
}

export interface CameraInfo {
  cameraId: string;
  name: string;
  status: string;
}

export interface VideoFiles {
  files: string[];
}

export type VideoFile = {
  title: string;
  name: string;
}

export interface CameraControlState {
  camera_id: number;
  state: string;
}

export interface RouteControlState {
  route_id: number;
  state: string;
}
