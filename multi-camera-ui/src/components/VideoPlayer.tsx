import { useQueryClient } from "react-query";
import * as api from "../api";

const VideoPlayer = () => {
  const queryClient = useQueryClient();
  const { data } = api.getRouteInfos();

  // const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  // useEffect(() => {
  //   api.getRouteInfos().then((infos) => setRoutes(infos));
  // }, []);

  return (
    <>
      <h1>Video Player</h1>
      <div>TODO</div>
    </>
  );
};

export default VideoPlayer;
