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
        <div key={camera.camera_id}>
          <span>{camera.name}</span>
          <button onClick={() => controlCamera(camera.camera_id, "start")}>Start</button>
          <button onClick={() => controlCamera(camera.camera_id, "stop")}>Stop</button>
          <button onClick={() => controlCamera(camera.camera_id, "record")}>Record</button>
          <button onClick={() => controlCamera(camera.camera_id, "pause")}>Pause</button>
        </div>
      ))}
    </>
  );
};

export default CameraActions;
