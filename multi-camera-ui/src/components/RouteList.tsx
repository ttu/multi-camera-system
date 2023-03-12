import { useQueryClient } from "react-query";
import * as api from "../api";
import { RouteInfo } from "../types";

const RouteList = () => {
  const queryClient = useQueryClient();
  const { data } = api.getRouteInfos();

  // const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  // useEffect(() => {
  //   api.getRouteInfos().then((infos) => setRoutes(infos));
  // }, []);

  return (
    <>
      <h1>Routes</h1>
      <div>
        {data?.map((route) => (
          <Route key={route.route_id} route={route} />
        ))}
      </div>
    </>
  );
};

const Route = (props: { route: RouteInfo }) => {
  return <h2>{`${props.route.route_id}: ${props.route.name}`}</h2>;
};

export default RouteList;
