import { RouteInfo } from "../types";

interface RouteActionsProps {
  route: RouteInfo;
  controlRoute: (routeId: number, action: string) => void;
}

const RouteActions = (props: RouteActionsProps) => {
  const { route, controlRoute } = props;

  const startRouteCameras = () => controlRoute(route.route_id, "start");
  const stopRouteCameras = () => controlRoute(route.route_id, "stop");

  return (
    <>
      <h1>Route Actions</h1>
      <div>
        <button onClick={startRouteCameras}>Start</button>
        <button onClick={stopRouteCameras}>Stop</button>
      </div>
    </>
  );
};

export default RouteActions;
