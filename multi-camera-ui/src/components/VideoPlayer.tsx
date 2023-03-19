import { useEffect, useRef, useState } from "react";
import * as api from "../api";
import { VideoFile } from "../types";

const VideoPlayer = () => {
  const videoRef = useRef();
  const [files, setfiles] = useState<VideoFile[]>();
  const [selectedVideoUrl, setSelectedVideoUrl] = useState<string>();

  useEffect(() => {
    api.getVideoFiles().then((videoFiles) => {
      setfiles(videoFiles);
      if (videoFiles.length > 0) setSelectedVideoUrl(`/api/video/${videoFiles[0].name}`);
    });
  }, []);

  const setVideoUrl = (e: any) => {
    setSelectedVideoUrl(`/api/video/${e.target.value}`);
  };

  useEffect(() => {
    videoRef.current?.load();
  }, [selectedVideoUrl]);

  return (
    <>
      <h1>Video Player</h1>
      <select onChange={setVideoUrl}>
        {files?.map((file) => (
          <option value={file.name}>{file.title}</option>
        ))}
      </select>
      <div>
        <video ref={videoRef} width="360" controls>
          <source src={selectedVideoUrl} type="video/mp4" />
        </video>
      </div>
    </>
  );
};

export default VideoPlayer;
