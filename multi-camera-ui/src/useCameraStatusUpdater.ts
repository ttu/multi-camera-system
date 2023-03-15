import React from "react";
import { useQueryClient } from "react-query";
import { CameraStatausUpdate } from "./types";

const useCameraStatusUpdater = () => {
  const queryClient = useQueryClient();
  React.useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8000/status-updates");
    websocket.onopen = () => {
      console.log("connected");
    };
    websocket.onmessage = (event) => {
      if (!event?.data) return;
      const payload = JSON.parse(event.data) as CameraStatausUpdate;
      if (payload.type == "status") {
        queryClient.invalidateQueries("routes")
        console.log(payload);
      }
    };

    return () => {
      if (websocket.readyState == 0) return;
      websocket.close();
    };
  }, [queryClient]);
};

export default useCameraStatusUpdater;
