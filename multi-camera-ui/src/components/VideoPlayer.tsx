import { useEffect, useState } from "react";
import * as api from "../api";
import { RouteInfo } from "../types";

const VideoPlayer = () => {
  const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  useEffect(() => {
    api.getRouteInfos().then((infos) => setRoutes(infos));
  }, []);

  return (
    <>
      <h1>Video Player</h1>
      <div>
        TODO
      </div>
    </>
  );
};

export default VideoPlayer;
