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
            key={route.routeId}
            isSelected={selectedRoute?.routeId === route.routeId}
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
      <h2>{`${route.routeId}: ${route.name}`}</h2>
      <button onClick={() => selectRoute(route.routeId)}>Select</button>
    </div>
  );
};

export default RouteList;
