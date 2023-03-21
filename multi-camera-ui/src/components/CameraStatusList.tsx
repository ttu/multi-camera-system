import { RouteInfo } from "../types";

interface RoutesProps {
  routes: RouteInfo[];
}

interface RouteProps {
  route: RouteInfo;
}

const CameraStatusList: React.FC<RoutesProps> = ({ routes }) => {
  return (
    <div>
      <h1>Camera Status List</h1>
      {routes?.map((route) => (
        <Route key={route.route_id} route={route} />
      ))}
    </div>
  );
};

const Route: React.FC<RouteProps> = ({ route }) => {
  return (
    <div>
      <h4>{route.name}</h4>
      {Object.values(route.cameras).map((camera) => (
        <div key={camera.camera_id}>{`${camera.name}: ${camera.status}`}</div>
      ))}
    </div>
  );
};

export default CameraStatusList;
