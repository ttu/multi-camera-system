import { QueryClient, QueryClientProvider } from "react-query";
import "./App.css";
import CameraActions from "./components/CameraActions";
import CameraStatusList from "./components/CameraStatusList";
import CameraStreams from "./components/CameraStreams";
import RouteActions from "./components/RouteActions";
import RouteList from "./components/RouteList";
import VideoPlayer from "./components/VideoPlayer";

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
        <RouteList />
        <CameraStatusList />
        <CameraStreams />
        <RouteActions />
        <CameraActions />
        <VideoPlayer />
      </div>
    </QueryClientProvider>
  );
}

export default App;
