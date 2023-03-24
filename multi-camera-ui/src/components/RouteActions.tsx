import { RouteInfo } from "../types";

interface Props {
  route: RouteInfo;
  controlRoute: (routeId: number, action: string) => void;
}

const RouteActions: React.FC<Props> = ({ route, controlRoute }) => {
  const handleStartRoute = () => controlRoute(route.routeId, "start");
  const handleStopRoute = () => controlRoute(route.routeId, "stop");

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
