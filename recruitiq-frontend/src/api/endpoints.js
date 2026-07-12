import api from './client';

// ============ Auth ============
export const login = (email, password) =>
  api.post('/auth/login', { email, password });

export const registerUser = (data) =>
  api.post('/auth/register', data);

export const getMe = () => api.get('/auth/me');

export const logoutServer = () => api.post('/auth/logout');

// ============ Candidates ============
export const getCandidates = (page = 1, limit = 10) =>
  api.get('/candidates/', { params: { page, limit } });

export const getCandidate = (candidateId) =>
  api.get(`/candidates/${candidateId}`);

export const createCandidate = (data) =>
  api.post('/candidates/', data);

export const updateCandidate = (candidateId, data) =>
  api.patch(`/candidates/${candidateId}`, data);

export const deleteCandidate = (candidateId) =>
  api.delete(`/candidates/${candidateId}`);

export const uploadResume = (candidateId, file) => {
  const fd = new FormData();
  fd.append('file', file);
  return api.post(`/candidates/${candidateId}/upload-resume`, fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

// ============ Jobs ============
export const getJobs = (page = 1, limit = 100) => api.get(`/jobs/?page=${page}&limit=${limit}`);
export const getJob = (jobId) => api.get(`/jobs/${jobId}`);
export const createJob = (data) => api.post('/jobs/', data);
export const updateJob = (jobId, data) => api.patch(`/jobs/${jobId}`, data);
export const deleteJob = (jobId) => api.delete(`/jobs/${jobId}`);

// ============ Matching ============
export const findMatches = (jobId, candidateIds, topK = 10, minScore = 0.5) =>
  api.post('/matching/find', { job_id: jobId, candidate_ids: candidateIds, top_k: topK, min_score: minScore });

export const getMatchResults = (jobId) =>
  api.get(`/matching/results/${jobId}`);

// ============ Full Analysis ============
export const runAnalysis = (candidateId, jobId) =>
  api.post(`/agents/full-analysis?candidate_id=${candidateId}&job_id=${jobId}`);

export const getAnalysis = (analysisId) =>
  api.get(`/agents/analysis/${analysisId}`);

// ============ Resume / Bias / Salary Agents ============
export const analyzeResume = (resumeText) =>
  api.post('/agents/resume/analyze', { resume_text: resumeText });

export const auditBiasForJob = (jobId) =>
  api.post(`/agents/bias/audit?job_id=${jobId}`);

export const estimateSalaryAgent = (jobTitle, experienceYears) =>
  api.post('/agents/salary/estimate', { job_title: jobTitle, experience_years: experienceYears });

// ============ Interview Questions & Evaluation ============
export const generateQuestions = (candidateId, jobId, difficulty = 'medium', numQuestions = 5) =>
  api.post('/agents/interview/generate-questions', {
    candidate_id: candidateId,
    job_id: jobId,
    difficulty,
    num_questions: numQuestions,
  });

export const evaluateAnswer = (candidateId, jobId, question, answer) =>
  api.post(
    `/interview/evaluate-answer?candidate_id=${candidateId}&job_id=${jobId}&question=${encodeURIComponent(question)}&answer=${encodeURIComponent(answer)}`
  );

// Live Voice + Camera Interview Evaluation
export const evaluateVoiceAnswer = (candidateId, jobId, question, audioBlob, eyeContactScore) => {
  const fd = new FormData();
  fd.append('candidate_id', candidateId);
  fd.append('job_id', jobId);
  fd.append('question', question);
  fd.append('audio', audioBlob, 'answer.webm');
  if (eyeContactScore !== null && eyeContactScore !== undefined) {
    fd.append('eye_contact_score', eyeContactScore);
  }
  return api.post('/interview/evaluate-voice-answer', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getInterviewReport = (candidateId) =>
  api.get(`/interview/report/${candidateId}`);

export const sendInterviewInvite = (candidateId, jobId, scheduledAt) =>
  api.post('/agents/interview/invite', {
    candidate_id: candidateId,
    job_id: jobId,
    scheduled_at: scheduledAt,
  });

// ============ Email ============
export const sendEmail = (to, subject, body) =>
  api.post('/agents/email/send', { to, subject, body });

// ============ Recruiter Copilot & Shortlist ============
export const askCopilot = (question) =>
  api.post(`/agents/recruiter/copilot?question=${encodeURIComponent(question)}`);

export const getShortlist = (jobId) =>
  api.get(`/recruiter/shortlist/${jobId}`);

// ============ Analytics ============
export const getHiringFunnel = () =>
  api.get('/analytics/hiring-funnel');

export const getFunnel = (jobId) =>
  api.get('/analytics/funnel', { params: jobId ? { job_id: jobId } : {} });

export const getBiasAudit = (jobId) =>
  api.get('/analytics/bias-audit', { params: jobId ? { job_id: jobId } : {} });

export const getSalaryIntelligence = (jobTitle, location) =>
  api.get('/analytics/salary', { params: { job_title: jobTitle, location } });

export const getRecruiterDashboard = () =>
  api.get('/analytics/recruiter-dashboard');

export const getSkillGapAnalytics = () =>
  api.get('/analytics/skill-gap-analytics');