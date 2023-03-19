import { RouteInfo } from "../types";

interface RoutesProps {
  routes: RouteInfo[];
  selectedRoute?: RouteInfo;
  selectRoute: (routeId: number) => void;
}

interface RouteProps {
  route: RouteInfo;
  isSelected: boolean;
  selectRoute: (routeId: number) => void;
}

const RouteList = (props: RoutesProps) => {
  const { routes } = props;

  return (
    <>
      <h1>Routes</h1>
      <div>
        {routes?.map((route) => (
          <Route
            key={route.route_id}
            isSelected={props.selectedRoute?.route_id == route.route_id}
            route={route}
            selectRoute={props.selectRoute}
          />
        ))}
      </div>
    </>
  );
};

const Route = (props: RouteProps) => {
  return (
    <div>
      {props.isSelected && <b>X</b>}
      <h2>{`${props.route.route_id}: ${props.route.name}`}</h2>{" "}
      <button onClick={() => props.selectRoute(props.route.route_id)}>Select</button>
    </div>
  );
};

export default RouteList;
