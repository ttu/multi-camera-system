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
