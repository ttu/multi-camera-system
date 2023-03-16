import { useEffect, useState } from "react";
import * as api from "../api";
import { VideoFile } from "../types";

const VideoPlayer = () => {
  const [files, setfiles] = useState<VideoFile[]>();

  useEffect(() => {
    api.getVideoFiles().then((resp) => setfiles(resp));
  }, []);

  return (
    <>
      <h1>Video Player</h1>
      <select>
        {files?.map((file) => (
          <option>{file.name}</option>
        ))}
      </select>
    </>
  );
};

export default VideoPlayer;
