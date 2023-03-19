import { RouteInfo } from "../types";

const CameraStatusList = (props: { routes: RouteInfo[] }) => {
  const { routes } = props;

  return (
    <div>
      <h1>Camera Status List</h1>
      {routes?.map((route) => (
        <Route key={route.route_id} route={route} />
      ))}
    </div>
  );
};

const Route = (props: { route: RouteInfo }) => {
  return (
    <div>
      <h4>{props.route.name}</h4>
      {Object.values(props.route.cameras).map((camera) => (
        <div>{`${camera.name} : ${camera.status}`}</div>
      ))}
    </div>
  );
};

export default CameraStatusList;
