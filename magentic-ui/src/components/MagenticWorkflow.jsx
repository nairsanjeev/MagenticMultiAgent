import { useState, useEffect } from 'react'
import { useCopilotAction, useCopilotReadable } from '@copilotkit/react-core'
import axios from 'axios'
import { Sparkles, Users, Play, Clock, CheckCircle, XCircle, Loader } from 'lucide-react'
import './MagenticWorkflow.css'

function MagenticWorkflow() {
  const [task, setTask] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [examples, setExamples] = useState([])
  const [activityLog, setActivityLog] = useState([])
  const [showActivityLog, setShowActivityLog] = useState(true)
  const [models, setModels] = useState([])
  const [researcherModel, setResearcherModel] = useState('gpt-4o')
  const [coderModel, setCoderModel] = useState('gpt-4o')
  const [managerModel, setManagerModel] = useState('gpt-4o')
  const [reviewerModel, setReviewerModel] = useState('gpt-4o')

  // Load example tasks and available models
  useEffect(() => {
    axios.get('/api/examples')
      .then(response => setExamples(response.data.examples))
      .catch(err => console.error('Failed to load examples:', err))
    
    axios.get('/api/models')
      .then(response => setModels(response.data.models))
      .catch(err => console.error('Failed to load models:', err))
  }, [])

  // Make workflow context available to Copilot
  useCopilotReadable({
    description: "Current task being processed by the Magentic workflow",
    value: task,
  })

  useCopilotReadable({
    description: "Latest result from the Magentic multi-agent workflow",
    value: result,
  })

  // Define Copilot action for executing tasks
  useCopilotAction({
    name: "executeMagenticTask",
    description: "Execute a task using the Magentic multi-agent workflow (Researcher + Coder + Manager)",
    parameters: [
      {
        name: "task",
        type: "string",
        description: "The task to execute using multiple AI agents",
        required: true,
      },
    ],
    handler: async ({ task }) => {
      setTask(task)
      await handleExecute(task)
      return "Task executed successfully"
    },
  })

  const handleExecute = async (taskText = task) => {
    if (!taskText.trim()) {
      setError('Please enter a task')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    setActivityLog([])
    setShowActivityLog(true)

    // Add initial log entry
    addActivityLog('system', '🚀 Task submitted - Agents initializing...', '�')

    try {
      const response = await axios.post('/api/execute', {
        task: taskText,
        max_rounds: 20,
        researcher_model: researcherModel,
        coder_model: coderModel,
        manager_model: managerModel,
        reviewer_model: reviewerModel
      })

      if (response.data.status === 'success') {
        // Clear the initial message and show REAL backend activity log
        setActivityLog([])
        
        // Add all detailed backend activity logs
        if (response.data.activity_log && response.data.activity_log.length > 0) {
          response.data.activity_log.forEach(log => {
            addActivityLog(log.type, log.message, log.icon)
          })
        } else {
          // Fallback if no activity log
          addActivityLog('system', '✅ Task completed successfully', '✅')
        }
        
        setResult(response.data.result)
      } else {
        setError(response.data.error || 'Task execution failed')
        addActivityLog('error', response.data.error || 'Task execution failed', '❌')
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to execute task'
      setError(errorMsg)
      addActivityLog('error', errorMsg, '❌')
    } finally {
      setLoading(false)
    }
  }

  const addActivityLog = (type, message, icon) => {
    const timestamp = new Date().toLocaleTimeString()
    setActivityLog(prev => [...prev, { type, message, icon, timestamp }])
  }

  const loadExample = (example) => {
    setTask(example.task)
    setResult(null)
    setError(null)
    setActivityLog([])
  }

  return (
    <div className="magentic-workflow">
      {/* Agents Info Card with Model Selection */}
      <div className="agents-card">
        <h2><Users size={24} /> Multi-Agent AI Team</h2>
        <div className="agents-grid">
          <div className="agent-badge researcher">
            <span className="agent-icon">🔍</span>
            <div className="agent-info">
              <div className="agent-name">Researcher</div>
              <div className="agent-role">Information Gathering</div>
              <select 
                className="model-select"
                value={researcherModel}
                onChange={(e) => setResearcherModel(e.target.value)}
                disabled={loading}
              >
                {models.map(model => (
                  <option key={model.id} value={model.id}>{model.name}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="agent-badge coder">
            <span className="agent-icon">💻</span>
            <div className="agent-info">
              <div className="agent-name">Coder</div>
              <div className="agent-role">Analysis & Computation</div>
              <select 
                className="model-select"
                value={coderModel}
                onChange={(e) => setCoderModel(e.target.value)}
                disabled={loading}
              >
                {models.map(model => (
                  <option key={model.id} value={model.id}>{model.name}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="agent-badge reviewer">
            <span className="agent-icon">🔎</span>
            <div className="agent-info">
              <div className="agent-name">Reviewer</div>
              <div className="agent-role">Quality Assurance</div>
              <select 
                className="model-select"
                value={reviewerModel}
                onChange={(e) => setReviewerModel(e.target.value)}
                disabled={loading}
              >
                {models.map(model => (
                  <option key={model.id} value={model.id}>{model.name}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="agent-badge manager">
            <span className="agent-icon">🎯</span>
            <div className="agent-info">
              <div className="agent-name">Manager</div>
              <div className="agent-role">Team Coordination</div>
              <select 
                className="model-select"
                value={managerModel}
                onChange={(e) => setManagerModel(e.target.value)}
                disabled={loading}
              >
                {models.map(model => (
                  <option key={model.id} value={model.id}>{model.name}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Task Input Section */}
      <div className="task-section">
        <h2><Sparkles size={24} /> Create Your Task</h2>
        <textarea
          className="task-input"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Enter a complex task that requires research and analysis..."
          rows={6}
        />
        
        <button 
          className="execute-btn"
          onClick={() => handleExecute()}
          disabled={loading || !task.trim()}
        >
          {loading ? (
            <>
              <Loader className="spin" size={20} />
              Agents Working...
            </>
          ) : (
            <>
              <Play size={20} />
              Execute with AI Team
            </>
          )}
        </button>
      </div>

      {/* Example Tasks */}
      {examples.length > 0 && !result && (
        <div className="examples-section">
          <h3>💡 Example Tasks</h3>
          <div className="examples-grid">
            {examples.map((example, idx) => (
              <div 
                key={idx}
                className="example-card"
                onClick={() => loadExample(example)}
              >
                <h4>{example.title}</h4>
                <p>{example.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Status Messages */}
      {loading && (
        <div className="status-card loading">
          <Clock size={20} />
          <span>Agents are collaborating... This may take 1-3 minutes.</span>
        </div>
      )}

      {error && (
        <div className="status-card error">
          <XCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Activity Log */}
      {activityLog.length > 0 && (
        <div className="activity-log-section">
          <div className="activity-log-header">
            <h3>
              <Users size={20} />
              Agent Activity Log
            </h3>
            <button 
              className="toggle-log-btn"
              onClick={() => setShowActivityLog(!showActivityLog)}
            >
              {showActivityLog ? '▼ Hide' : '▶ Show'}
            </button>
          </div>
          
          {showActivityLog && (
            <div className="activity-log-content">
              {activityLog.map((log, idx) => (
                <div key={idx} className={`activity-item ${log.type}`}>
                  <span className="activity-icon">{log.icon}</span>
                  <div className="activity-details">
                    <span className="activity-message">{log.message}</span>
                    <span className="activity-timestamp">{log.timestamp}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="result-section">
          <div className="result-header">
            <CheckCircle size={24} />
            <h2>Results</h2>
          </div>
          <div className="result-content">
            <pre>{result}</pre>
          </div>
          <button 
            className="new-task-btn"
            onClick={() => {
              setTask('')
              setResult(null)
              setError(null)
            }}
          >
            Create New Task
          </button>
        </div>
      )}
    </div>
  )
}

export default MagenticWorkflow
