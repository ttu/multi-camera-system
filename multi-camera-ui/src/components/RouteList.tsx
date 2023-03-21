import React from "react";
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

const RouteList: React.FC<RoutesProps> = ({ routes, selectedRoute, selectRoute }) => {
  return (
    <>
      <h1>Routes</h1>
      <div>
        {routes?.map((route) => (
          <Route
            key={route.route_id}
            isSelected={selectedRoute?.route_id === route.route_id}
            route={route}
            selectRoute={selectRoute}
          />
        ))}
      </div>
    </>
  );
};

const Route: React.FC<RouteProps> = ({ route, isSelected, selectRoute }) => {
  return (
    <div>
      {isSelected && <b>X</b>}
      <h2>{`${route.route_id}: ${route.name}`}</h2>
      <button onClick={() => selectRoute(route.route_id)}>Select</button>
    </div>
  );
};

export default RouteList;
