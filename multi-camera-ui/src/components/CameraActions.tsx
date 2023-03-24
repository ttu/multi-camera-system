import { RouteInfo } from "../types";

interface CameraActionsProps {
  route: RouteInfo;
  controlCamera: (cameraId: number, action: string) => void;
}

const CameraActions: React.FC<CameraActionsProps> = ({ route, controlCamera }) => {
  return (
    <>
      <h1>Camera Actions</h1>

      {Object.values(route.cameras).map((camera) => (
        <div key={camera.cameraId}>
          <span>{camera.name}</span>
          <button onClick={() => controlCamera(camera.cameraId, "CAMERA_COMMAND_PREPARE")}>Start</button>
          <button onClick={() => controlCamera(camera.cameraId, "CAMERA_COMMAND_TURNOFF")}>Stop</button>
          <button onClick={() => controlCamera(camera.cameraId, "CAMERA_COMMAND_RECORD")}>Record</button>
          <button onClick={() => controlCamera(camera.cameraId, "CAMERA_COMMAND_STOP_RECORD")}>Pause</button>
        </div>
      ))}
    </>
  );
};

export default CameraActions;
