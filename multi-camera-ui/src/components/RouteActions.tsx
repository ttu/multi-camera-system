import { useEffect, useState } from "react";
import * as api from "../api";
import { RouteInfo } from "../types";

const RouteActions = () => {
  const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  useEffect(() => {
    api.getRouteInfos().then((infos) => setRoutes(infos));
  }, []);

  return (
    <>
      <h1>Route Actions</h1>
      <div>
        TODO
      </div>
    </>
  );
};

export default RouteActions;
