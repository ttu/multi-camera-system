import { useEffect, useState } from "react";
import "./App.css";

import CameraActions from "./components/CameraActions";
import CameraStatusList from "./components/CameraStatusList";
import CameraStreams from "./components/CameraStreams";
import RouteActions from "./components/RouteActions";
import RouteCameras from "./components/RouteCameras";
import RouteList from "./components/RouteList";
import VideoPlayer from "./components/VideoPlayer";
import useCameraStatusUpdater from "./useCameraStatusUpdater";
import * as api from "./api";
import { RouteInfo } from "./types";
import useCameraStatusUpdaterNotify from "./useCameraStatusUpdaterNotify";

const MainComponent = () => {
  // const _ = useCameraStatusUpdater();
  // const { data: routeInfo } = api.getRouteInfos();
  
  useCameraStatusUpdaterNotify((data) => {
    console.log(data);
  });

  const [routeInfo, setRouteInfo] = useState<RouteInfo[]>([]);
  const [selectedRoute, setSelectedRoute] = useState<RouteInfo>();

  console.log(selectedRoute)
  if (!routeInfo) return <div>Loading...</div>;

  useEffect(() => {
    console.log("fetching route info");
    api.fetchRouteInfos().then((data) => setRouteInfo(data));
  }, []);

  const selectRoute = (routeId: any) => {
    const selectedRoute = routeInfo.find((route) => route.route_id === routeId);
    setSelectedRoute(selectedRoute);
  };

  const controlRoute = (routeId: number, action: string) => api.controlRoute(routeId, action);

  const controlCamera = (cameraId: number, action: string) => api.controlCamera(cameraId, action);

  return (
    <div className="App">
      <CameraStatusList routes={routeInfo} />
      <RouteList routes={routeInfo} selectedRoute={selectedRoute} selectRoute={selectRoute} />
      {selectedRoute && <RouteCameras route={selectedRoute} />}
      {selectedRoute && <RouteActions route={selectedRoute} controlRoute={controlRoute} />}
      {selectedRoute && <CameraActions route={selectedRoute} controlCamera={controlCamera} />}
      {selectedRoute && <CameraStreams route={selectedRoute} />}
      <VideoPlayer />
    </div>
  );
};

export default MainComponent;
