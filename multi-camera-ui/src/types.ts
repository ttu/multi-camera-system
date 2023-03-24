export interface RouteInfo {
  routeId: number;
  name: string;
  cameras: CameraInfo[];
}

export interface CameraStatausUpdate {
  routeId: number;
  cameraId: number;
  status: string;
  type: string;
}

export interface CameraInfo {
  cameraId: number;
  name: string;
  status: string;
}

export interface VideoFiles {
  files: string[];
}

export type VideoFile = {
  title: string;
  name: string;
};

export interface CameraControlState {
  cameraId: number;
  state: string;
}

export interface RouteControlState {
  routeId: number;
  state: string;
}
