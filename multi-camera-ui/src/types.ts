export interface RouteInfo {
  route_id: number;
  name: string;
  cameras: CameraInfo[];
}

export interface CameraStatausUpdate {
  route_id: number;
  camera_id: number;
  status: string;
  type: string;
}

export interface CameraInfo {
  camera_id: number;
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
  camera_id: number;
  state: string;
}

export interface RouteControlState {
  route_id: number;
  state: string;
}
