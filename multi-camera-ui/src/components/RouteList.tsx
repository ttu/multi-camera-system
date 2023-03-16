import { RouteInfo, RouteProps, RoutesProps } from "../types";

const RouteList = (props: RoutesProps) => {
  const { routes } = props;

  return (
    <>
      <h1>Routes</h1>
      <div>
        {routes?.map((route) => (
          <Route key={route.route_id} route={route} />
        ))}
      </div>
    </>
  );
};

const Route = (props: RouteProps) => {
  return <h2>{`${props.route.route_id}: ${props.route.name}`}</h2>;
};

export default RouteList;
