import { RouteInfo } from "../types";

interface Props {
  route: RouteInfo;
}

const RouteCameras: React.FC<Props> = ({ route }) => {
  return (
    <div>
      <h1>{route.name}</h1>
      {Object.values(route.cameras).map((camera) => (
        <div key={camera.camera_id}>{`${camera.name}: ${camera.status}`}</div>
      ))}
    </div>
  );
};

export default RouteCameras;
