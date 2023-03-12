import { useQueryClient } from "react-query";
import * as api from "../api";

const CameraStreams = () => {
  const queryClient = useQueryClient()
  const { data } = api.getRouteInfos();

  // const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  // useEffect(() => {
  //   api.getRouteInfos().then((infos) => setRoutes(infos));
  // }, []);

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
