import "./App.css";
import CameraActions from "./components/CameraActions";
import CameraStatusList from "./components/CameraStatusList";
import CameraStreams from "./components/CameraStreams";
import RouteActions from "./components/RouteActions";
import RouteList from "./components/RouteList";
import VideoPlayer from "./components/VideoPlayer";
import * as api from "./api";
import useCameraStatusUpdater from "./useCameraStatusUpdater";

const MainComponent = () => {
  const status = useCameraStatusUpdater();
  const { data: routeInfo } = api.getRouteInfos();

  if (!routeInfo) return <div>No data</div>;

  return (
    <div className="App">
      <RouteList routes={routeInfo} />
      <CameraStatusList routes={routeInfo} />
      <CameraStreams routes={routeInfo} />
      <RouteActions routes={routeInfo} />
      <CameraActions routes={routeInfo} />
      <VideoPlayer />
    </div>
  );
};

export default MainComponent;
