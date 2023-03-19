import "./App.css";
import CameraActions from "./components/CameraActions";
import CameraStatusList from "./components/CameraStatusList";
import CameraStreams from "./components/CameraStreams";
import RouteActions from "./components/RouteActions";
import RouteList from "./components/RouteList";
import VideoPlayer from "./components/VideoPlayer";
import * as api from "./api";
import useCameraStatusUpdater from "./useCameraStatusUpdater";
import { useState } from "react";
import { RouteInfo } from "./types";
import RouteCameras from "./components/RouteCameras";

const MainComponent = () => {
  console.log("refresh");
  const _ = useCameraStatusUpdater();
  const { data: routeInfo } = api.getRouteInfos();
  const [selectedRoute, setSelectedRoute] = useState<RouteInfo>();

  if (!routeInfo) return <div>Loading...</div>;

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
      <CameraStreams routes={routeInfo} />
      <VideoPlayer />
    </div>
  );
};

export default MainComponent;
