import { useState, useEffect } from 'react'
import { CopilotKit } from '@copilotkit/react-core'
import { CopilotPopup } from '@copilotkit/react-ui'
import '@copilotkit/react-ui/styles.css'
import MagenticWorkflow from './components/MagenticWorkflow'
import './App.css'

function App() {
  return (
    <CopilotKit runtimeUrl="/copilotkit">
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <h1>🤖 Magentic Multi-Agent Workflow</h1>
            <p>Collaborate with AI agents to solve complex tasks</p>
          </div>
        </header>
        
        <main className="app-main">
          <MagenticWorkflow />
        </main>
        
        <footer className="app-footer">
          <p>Powered by Microsoft Agent Framework & CopilotKit</p>
        </footer>
        
        {/* CopilotKit Popup for chat interface */}
        <CopilotPopup
          instructions="You are a helpful assistant coordinating a team of AI agents. You can help users create complex tasks for research and analysis."
          labels={{
            title: "Magentic Assistant",
            initial: "Hi! I can help you create tasks for our AI agent team. What would you like to research or analyze?",
          }}
        />
      </div>
    </CopilotKit>
  )
}

export default App
