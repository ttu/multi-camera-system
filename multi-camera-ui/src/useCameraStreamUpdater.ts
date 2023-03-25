import React from "react";

const useCameraStreamUpdater = (cameraId: number, callback: (cameraId: number, frameUrl: string) => void) => {
  React.useEffect(() => {
    const camera_ws = new WebSocket(`ws://localhost:8000/camera-stream/${cameraId}`);

    camera_ws.onopen = () => {
      console.log("camera_ws.onopen", cameraId);
    };

    camera_ws.onmessage = (event) => {
      console.log("camera_ws.onmessage", { cameraId, event });
      if (!event?.data) return;
      if (event.data instanceof Blob) {
        const frameUrl = URL.createObjectURL(event.data);
        console.log("camera_ws.onmessage", { cameraId, frameUrl });
        callback(cameraId, frameUrl);
      }
    };

    return () => {
      console.log("camera_ws.onclose", cameraId);
      camera_ws.close();
    };
  }, []);
};

export default useCameraStreamUpdater;
