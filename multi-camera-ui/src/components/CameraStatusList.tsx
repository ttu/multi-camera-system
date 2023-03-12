import { useEffect, useState } from "react";
import * as api from "../api";
import { RouteInfo } from "../types";

const CameraStatusList = () => {
  const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  useEffect(() => {
    api.getRouteInfos().then((infos) => setRoutes(infos));
  }, []);

  return (
    <div>
      <h1>Camera Status List</h1>
      {routeInfo?.map((route) => (
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
