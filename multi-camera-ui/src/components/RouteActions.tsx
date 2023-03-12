import { useQueryClient } from "react-query";
import * as api from "../api";

const RouteActions = () => {
  const queryClient = useQueryClient()
  const { data } = api.getRouteInfos();

  // const [routeInfo, setRoutes] = useState<RouteInfo[]>();

  // useEffect(() => {
  //   api.getRouteInfos().then((infos) => setRoutes(infos));
  // }, []);

  return (
    <>
      <h1>Route Actions</h1>
      <div>
        TODO
      </div>
    </>
  );
};

export default RouteActions;
