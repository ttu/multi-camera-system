import { RouteInfo } from "../types";

interface CameraActionsProps {
  route: RouteInfo;
  controlCamera: (cameraId: number, action: string) => void;
}

const CameraActions = (props: CameraActionsProps) => {
  const { route, controlCamera } = props;

  const startCamera = (cameraId: number) => controlCamera(cameraId, "start");
  const stopCamera = (cameraId: number) => controlCamera(cameraId, "stop");
  const recordCamera = (cameraId: number) => controlCamera(cameraId, "record");
  const pauseCamera = (cameraId: number) => controlCamera(cameraId, "pause");

  return (
    <>
      <h1>Camera Actions</h1>

      {Object.values(route.cameras).map((camera) => (
        <div>
          <span>{camera.name}</span>
          <button onClick={() => startCamera(camera.camera_id)}>Start</button>
          <button onClick={() => stopCamera(camera.camera_id)}>Stop</button>
          <button onClick={() => recordCamera(camera.camera_id)}>Record</button>
          <button onClick={() => pauseCamera(camera.camera_id)}>Pause</button>
        </div>
      ))}
    </>
  );
};

export default CameraActions;
