import { RouteInfo } from "../types";

const RouteCameras = (props: { route: RouteInfo }) => {
  const { route } = props;

  return (
    <div>
      <h1>{route.name}</h1>
      {Object.values(route.cameras).map((camera) => (
        <div>{`${camera.name} : ${camera.status}`}</div>
      ))}
    </div>
  );
};

export default RouteCameras;
