import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

// source ~/myenv/bin/activate

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [videoTitle, setVideoTitle] = useState("");
  const [videoSummary, setVideoSummary] = useState("");
  const [thumbnailUrl, setThumbnailUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [transcript, setTranscript] = useState("");
  const summaryRef = useRef(null);
  const [lines, setLines] = useState(4);

  const summarizeText = async () => {
    const options = {
      method: "POST",
      url: "https://gpt-summarization.p.rapidapi.com/summarize",
      headers: {
        "content-type": "application/json",
        "X-RapidAPI-Key": "09477c5ab1msh7c0a9742a41a0bcp1e3717jsnd5171e48c278",
        "X-RapidAPI-Host": "gpt-summarization.p.rapidapi.com",
      },
      data: {
        text: transcript,
        num_sentences: lines,
      },
    };

    try {
      const response = await axios.request(options);
      setVideoSummary(response.data.summary);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const summarizeVideo = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/summarize", {
        youtube_video_url: youtubeUrl,
      });

      setVideoTitle(response.data.video_title);
      setTranscript(response.data.transcript);
      setThumbnailUrl(response.data.thumbnail_url);
      if (summaryRef.current) {
        summaryRef.current.scrollIntoView({ behavior: "smooth" });
      }
    } catch (error) {
      console.error(error);
      setVideoTitle("");
      setTranscript("Error: Unable to fetch video summary.");
      setThumbnailUrl("");
    } finally {
      setLoading(true);
    }
  };
  useEffect(() => {
    if (transcript) {
      summarizeText();
    }
  }, [transcript]);

  return (
    <div className="main">
      <h1>YouTube Video Summarizer</h1>
      <div className="btn-container">
        <div>
          <h3>YouTube url</h3>
          <input
            className="inp"
            type="text"
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
            placeholder="Enter YouTube video URL"
          />
        </div>
        <div>
          <h3>Enter length for summary</h3>
          <input
            className="inp"
            type="number"
            value={lines}
            onChange={(e) => setLines(e.target.value)}
            placeholder="Enter no. of lines for summary"
          />
        </div>

        <button className="btn" onClick={summarizeVideo} disabled={loading}>
          Summarize
        </button>
      </div>
      {loading && (
        <div className="out-div-container">
          <h2>Video Title: {videoTitle} </h2>

          <div className="out-div">
            <div className="out-image-container">
              <img className="img" src={thumbnailUrl} alt="Thumbnail" />
              <div className="s1"></div>
              <div className="s2"></div>
              <div className="s3"></div>
            </div>
          </div>

          {videoSummary ? (
            <p>{videoSummary}</p>
          ) : (
            <div ref={summaryRef} className="loader-container">
              <div className="loader">
                <div className="inner one"></div>
                <div className="inner two"></div>
                <div className="inner three"></div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;

// 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
