import { useEffect, useRef, useState } from "react";
import * as api from "../api";
import { VideoFile } from "../types";

const VideoPlayer = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [files, setfiles] = useState<VideoFile[]>([]);
  const [selectedVideoUrl, setSelectedVideoUrl] = useState<string>("");

  useEffect(() => {
    api.getVideoFiles().then((videoFiles) => {
      setfiles(videoFiles);
      if (videoFiles.length > 0) setSelectedVideoUrl(`/api/video/${videoFiles[0].name}`);
    });
  }, []);

  useEffect(() => {
    videoRef.current?.load();
  }, [selectedVideoUrl]);

  const handleFileSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedVideoUrl(`/api/video/${e.target.value}`);
  };

  return (
    <div>
      <h1>Video Player</h1>
      <select onChange={handleFileSelectChange}>
        {files?.map((file) => (
          <option key={file.name} value={file.name}>
            {file.title}
          </option>
        ))}
      </select>
      <div>
        <video ref={videoRef} width="360" controls>
          <source src={selectedVideoUrl} type="video/mp4" />
        </video>
      </div>
    </div>
  );
};

export default VideoPlayer;
