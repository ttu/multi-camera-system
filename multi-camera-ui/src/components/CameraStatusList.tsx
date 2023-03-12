import { useQueryClient } from "react-query";
import * as api from "../api";
import { RouteInfo } from "../types";

const CameraStatusList = () => {
  const queryClient = useQueryClient()
  const { data } = api.getRouteInfos();

  // const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  // useEffect(() => {
  //   api.getRouteInfos().then((infos) => setRoutes(infos));
  // }, []);

  return (
    <div>
      <h1>Camera Status List</h1>
      {data?.map((route) => (
        <Route key={route.route_id} route={route} />
      ))}
    </div>
  );
};

const Route = (props: { route: RouteInfo }) => {
  return (
    <div>
      <h4>{props.route.name}</h4>
      {Object.values(props.route.cameras).map((camera) => (
        <div>{`${camera.name} : ${camera.status}`}</div>
      ))}
    </div>
  );
};

export default CameraStatusList;
