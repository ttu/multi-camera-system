import { useEffect, useState } from "react";
import * as api from "../api";
import { RouteInfo } from "../types";

const CameraStreams = () => {
  const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  useEffect(() => {
    api.getRouteInfos().then((infos) => setRoutes(infos));
  }, []);

  return (
    <>
      <h1>Camera Streams</h1>
      <div>
        TODO
      </div>
    </>
  );
};

export default CameraStreams;
