import { useRef } from "react";
import { CameraInfo } from "../types";
import useCameraStreamUpdater from "../useCameraStreamUpdater";

interface Props {
  cameras: CameraInfo[];
}

const CameraStreams: React.FC<Props> = ({ cameras }) => {
  return (
    <>
      <h1>Camera Streams</h1>
      <div>
        {cameras.map((camera) => (
          <CameraStream key={camera.cameraId} camera={camera} />
        ))}
      </div>
    </>
  );
};

interface CameraProps {
  camera: CameraInfo;
}

const CameraStream: React.FC<CameraProps> = ({ camera }) => {
  const imageRef = useRef<HTMLImageElement>(null);

  useCameraStreamUpdater(camera.cameraId, (id, url) => {
    if (!imageRef.current) return;
    imageRef.current.src = url;
  });

  return (
    <div key={camera.cameraId}>
      <div>{camera.name}</div>
      <img ref={imageRef} id={`frame_${camera.cameraId}`} />
    </div>
  );
};

export default CameraStreams;
