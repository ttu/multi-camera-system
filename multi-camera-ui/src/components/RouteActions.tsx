import { RouteInfo } from "../types";

interface Props {
  route: RouteInfo;
  controlRoute: (routeId: number, action: string) => void;
}

const RouteActions: React.FC<Props > = ({ route, controlRoute }) => {

  const handleStartRoute = () => controlRoute(route.route_id, "start");
  const handleStopRoute = () => controlRoute(route.route_id, "stop");

  return (
    <>
      <h1>Route Actions</h1>
      <div>
        <button onClick={handleStartRoute}>Start</button>
        <button onClick={handleStopRoute}>Stop</button>
      </div>
    </>
  );
};

export default RouteActions;
