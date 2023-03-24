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
          <button onClick={() => controlCamera(camera.cameraId, "start")}>Start</button>
          <button onClick={() => controlCamera(camera.cameraId, "stop")}>Stop</button>
          <button onClick={() => controlCamera(camera.cameraId, "record")}>Record</button>
          <button onClick={() => controlCamera(camera.cameraId, "pause")}>Pause</button>
        </div>
      ))}
    </>
  );
};

export default CameraActions;
