import { RouteInfo } from "../types";

interface Props {
  route: RouteInfo;
}

const CameraStreams: React.FC<Props> = ({ route }) => {
  return (
    <>
      <h1>Camera Streams</h1>
      <div>
        {route.cameras.map((camera) => (
          <div key={camera.cameraId}>{camera.name}</div>
        ))}
      </div>
    </>
  );
};

export default CameraStreams;
