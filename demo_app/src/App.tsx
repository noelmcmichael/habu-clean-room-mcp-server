import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import SystemHealth from './pages/SystemHealth';
import './App.css';

const Navigation: React.FC = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: '🤖', label: 'AI Assistant' },
    { path: '/health', icon: '📊', label: 'System Health' },
    { path: '/api-explorer', icon: '🔧', label: 'API Explorer' },
    { path: '/architecture', icon: '🏗️', label: 'Architecture' },
  ];

  return (
    <nav className="sidebar-nav">
      {navItems.map((item) => (
        <Link 
          key={item.path}
          to={item.path} 
          className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
        >
          <span className="nav-icon">{item.icon}</span>
          <span className="nav-label">{item.label}</span>
        </Link>
      ))}
    </nav>
  );
};

const MainContent: React.FC = () => {
  return (
    <div className="main-content">
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/health" element={<SystemHealth />} />
        <Route path="/api-explorer" element={<ComingSoonPage title="API Explorer" />} />
        <Route path="/architecture" element={<ComingSoonPage title="Architecture" />} />
      </Routes>
    </div>
  );
};

const ChatPage: React.FC = () => {
  return (
    <div className="chat-page">
      <div className="chat-header">
        <h1>🤖 AI Assistant</h1>
        <p>Powered by OpenAI GPT-4 | Model Context Protocol Integration</p>
      </div>
      <ChatInterface />
    </div>
  );
};

const ComingSoonPage: React.FC<{ title: string }> = ({ title }) => {
  return (
    <div className="coming-soon">
      <h1>{title}</h1>
      <p>This page is coming soon as part of our phased development plan.</p>
      <div className="features-preview">
        <h3>Planned Features:</h3>
        <ul>
          {title === 'API Explorer' && (
            <>
              <li>Interactive Habu API endpoint testing</li>
              <li>Real-time request/response debugging</li>
              <li>Authentication status monitoring</li>
              <li>Cleanroom discovery tools</li>
            </>
          )}
          {title === 'Architecture' && (
            <>
              <li>System architecture diagrams</li>
              <li>Data flow visualization</li>
              <li>Component interaction maps</li>
              <li>Technology stack documentation</li>
            </>
          )}
        </ul>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <div className="logo-section">
              <h1>ICDC</h1>
              <span className="tagline">🧹 AI Assistant</span>
            </div>
            <div className="status-indicators">
              <span className="status-badge production">Production</span>
              <span className="status-badge mock-data">Mock Data</span>
            </div>
          </div>
        </header>

        <div className="app-layout">
          <aside className="sidebar">
            <Navigation />
          </aside>
          <MainContent />
        </div>
      </div>
    </Router>
  );
}

export default App;