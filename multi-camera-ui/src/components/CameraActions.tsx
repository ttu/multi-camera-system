import { useQueryClient } from "react-query";
import * as api from "../api";

const CameraActions = () => {
  const queryClient = useQueryClient()
  const { data } = api.getRouteInfos();

  // const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  // useEffect(() => {
  //   api.getRouteInfos().then((infos) => setRoutes(infos));
  // }, []);

  return (
    <>
      <h1>Camera Actions</h1>
      <div>
        TODO
      </div>
    </>
  );
};

export default CameraActions;
