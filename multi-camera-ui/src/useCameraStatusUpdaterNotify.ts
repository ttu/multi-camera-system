import React from "react";
import { CameraStatausUpdate } from "./types";

const useCameraStatusUpdaterNotify = (notify: (data: CameraStatausUpdate) => void) => {
  React.useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8000/status-updates");
    websocket.onopen = () => {
      console.log("connected");
    };
    websocket.onmessage = (event) => {
      if (!event?.data) return;
      const payload = JSON.parse(event.data) as CameraStatausUpdate;
      if (payload.type == "status") {
        console.log(payload);
        notify(payload);
      }
    };

    return () => {
      if (websocket.readyState == 0) return;
      websocket.close();
    };
  }, []);
};

export default useCameraStatusUpdaterNotify;
