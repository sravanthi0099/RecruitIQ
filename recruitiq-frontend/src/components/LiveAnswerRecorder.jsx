import { useEffect, useRef, useState } from 'react';
import { Video, Mic, Square, Loader2, AlertCircle } from 'lucide-react';
import { evaluateVoiceAnswer } from '../api/endpoints';

/**
 * LiveAnswerRecorder
 * ------------------
 * Candidate-facing recorder: shows a live camera preview, records the
 * candidate's spoken answer, and submits it for AI transcription +
 * evaluation. Camera video itself is never uploaded or stored — only a
 * best-effort, client-side "eye contact" percentage (derived from the
 * browser's native FaceDetector API where available) is sent alongside
 * the audio, purely as a minor signal for the confidence score.
 *
 * Props:
 *  - candidateId, jobId, question: strings, same as the text-answer flow
 *  - onEvaluated(result): called with the evaluation result on success
 */
export default function LiveAnswerRecorder({ candidateId, jobId, question, onEvaluated }) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const faceCheckIntervalRef = useRef(null);
  const faceDetectorRef = useRef(null);
  const faceSamplesRef = useRef({ seen: 0, total: 0 });

  const [phase, setPhase] = useState('idle'); // idle | requesting | recording | uploading | error
  const [seconds, setSeconds] = useState(0);
  const [error, setError] = useState('');
  const timerRef = useRef(null);

  useEffect(() => {
    return () => stopStream();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const stopStream = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    if (timerRef.current) clearInterval(timerRef.current);
    if (faceCheckIntervalRef.current) clearInterval(faceCheckIntervalRef.current);
  };

  const startRecording = async () => {
    setError('');
    setPhase('requesting');

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      // Best-effort eye-contact heuristic. `FaceDetector` is only
      // available in some Chromium browsers — if it's missing we simply
      // skip this signal rather than fake a number.
      if ('FaceDetector' in window) {
        try {
          faceDetectorRef.current = new window.FaceDetector({ fastMode: true });
          faceSamplesRef.current = { seen: 0, total: 0 };
          faceCheckIntervalRef.current = setInterval(async () => {
            if (!videoRef.current) return;
            try {
              const faces = await faceDetectorRef.current.detect(videoRef.current);
              faceSamplesRef.current.total += 1;
              if (faces.length > 0) faceSamplesRef.current.seen += 1;
            } catch { /* ignore a single failed sample */ }
          }, 1000);
        } catch { /* FaceDetector present but unsupported config — skip */ }
      }

      const audioOnlyStream = new MediaStream(stream.getAudioTracks());
      const recorder = new MediaRecorder(audioOnlyStream);
      mediaRecorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.start();
      setPhase('recording');
      setSeconds(0);
      timerRef.current = setInterval(() => setSeconds((s) => s + 1), 1000);
    } catch (err) {
      setError('Camera/microphone access was denied or unavailable. Please allow permissions and try again.');
      setPhase('error');
      stopStream();
    }
  };

  const stopAndSubmit = async () => {
    const recorder = mediaRecorderRef.current;
    if (!recorder) return;

    setPhase('uploading');
    if (timerRef.current) clearInterval(timerRef.current);
    if (faceCheckIntervalRef.current) clearInterval(faceCheckIntervalRef.current);

    const stopped = new Promise((resolve) => {
      recorder.onstop = resolve;
    });
    recorder.stop();
    await stopped;

    stopStream();

    const blob = new Blob(chunksRef.current, { type: 'audio/webm' });

    const { seen, total } = faceSamplesRef.current;
    const eyeContactScore = total > 0 ? Math.round((seen / total) * 100) : null;

    try {
      const res = await evaluateVoiceAnswer(candidateId, jobId, question, blob, eyeContactScore);
      if (res.data.error) {
        setError(res.data.error);
        setPhase('error');
        return;
      }
      onEvaluated(res.data);
      setPhase('idle');
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload or evaluation failed. Please try again.');
      setPhase('error');
    }
  };

  const mm = String(Math.floor(seconds / 60)).padStart(2, '0');
  const ss = String(seconds % 60).padStart(2, '0');

  return (
    <div className="card" style={{ background: 'var(--bg3)' }}>
      <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start', flexWrap: 'wrap' }}>
        <div
          style={{
            width: 200,
            height: 150,
            borderRadius: 'var(--radius-sm)',
            overflow: 'hidden',
            background: '#000',
            flexShrink: 0,
            position: 'relative',
          }}
        >
          <video
            ref={videoRef}
            autoPlay
            muted
            playsInline
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: phase === 'recording' || phase === 'uploading' ? 'block' : 'none' }}
          />
          {phase !== 'recording' && phase !== 'uploading' && (
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text3)' }}>
              <Video size={28} />
            </div>
          )}
          {phase === 'recording' && (
            <div style={{ position: 'absolute', top: 8, left: 8, display: 'flex', alignItems: 'center', gap: 6, background: 'rgba(0,0,0,0.55)', padding: '3px 8px', borderRadius: 20 }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#ff4d4f', display: 'inline-block' }} />
              <span style={{ color: '#fff', fontSize: 12, fontFamily: 'monospace' }}>{mm}:{ss}</span>
            </div>
          )}
        </div>

        <div style={{ flex: 1, minWidth: 200 }}>
          <div style={{ fontSize: 13, color: 'var(--text2)', marginBottom: 10 }}>
            {phase === 'idle' && 'Answer this question out loud using your camera and microphone.'}
            {phase === 'requesting' && 'Requesting camera and microphone access…'}
            {phase === 'recording' && 'Recording your answer — click stop when finished.'}
            {phase === 'uploading' && 'Transcribing and evaluating your answer…'}
            {phase === 'error' && 'Something went wrong.'}
          </div>

          {error && (
            <div className="alert alert-danger" style={{ marginBottom: 10 }}>
              <AlertCircle size={15} style={{ flexShrink: 0 }} />
              <div>{error}</div>
            </div>
          )}

          <div className="flex gap-2">
            {phase === 'idle' || phase === 'error' ? (
              <button className="btn btn-primary btn-sm" onClick={startRecording}>
                <Mic size={13} /> Start Live Answer
              </button>
            ) : phase === 'recording' ? (
              <button className="btn btn-primary btn-sm" onClick={stopAndSubmit}>
                <Square size={13} /> Stop & Submit
              </button>
            ) : (
              <button className="btn btn-secondary btn-sm" disabled>
                <Loader2 size={13} className="spin" /> {phase === 'requesting' ? 'Starting…' : 'Evaluating…'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}