import "./App.css";
import CameraActions from "./components/CameraActions";
import CameraStatusList from "./components/CameraStatusList";
import CameraStreams from "./components/CameraStreams";
import RouteActions from "./components/RouteActions";
import RouteList from "./components/RouteList";
import VideoPlayer from "./components/VideoPlayer";

function App() {
  return (
    <div className="App">
      <RouteList />
      <CameraStatusList />
      <CameraStreams />
      <RouteActions />
      <CameraActions />
      <VideoPlayer />
    </div>
  );
}

export default App;
