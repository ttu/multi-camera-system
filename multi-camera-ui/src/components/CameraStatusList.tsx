import { RouteInfo } from "../types";

interface RoutesProps {
  routes: RouteInfo[];
}

interface RouteProps {
  route: RouteInfo;
}

const CameraStatusList: React.FC<RoutesProps> = ({ routes }) => {
  return (
    <>
      <h1>Camera Status List</h1>
      {routes?.map((route) => (
        <Route key={route.routeId} route={route} />
      ))}
    </>
  );
};

const Route: React.FC<RouteProps> = ({ route }) => {
  return (
    <div>
      <h4>{route.name}</h4>
      {Object.values(route.cameras).map((camera) => (
        <div key={camera.cameraId}>{`${camera.name}: ${camera.status}`}</div>
      ))}
    </div>
  );
};

export default CameraStatusList;
