import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import SystemHealth from './pages/SystemHealth';
import ApiExplorer from './pages/ApiExplorer';
import Architecture from './pages/Architecture';
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
    <div className="sidebar-content">
      <div className="sidebar-header">
        <Link to="/" className="logo-link">
          <div className="logo">
            <span className="logo-icon">🤖</span>
            <span className="logo-text">Habu MCP</span>
          </div>
        </Link>
      </div>
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
      <div className="sidebar-footer">
        <div className="status-info">
          <div className="status-item">
            <span className="status-dot production"></span>
            <span>Production</span>
          </div>
          <div className="status-item">
            <span className="status-dot mock"></span>
            <span>Mock Data</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const MainContent: React.FC = () => {
  return (
    <div className="main-content">
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/health" element={<SystemHealth />} />
        <Route path="/api-explorer" element={<ApiExplorer />} />
        <Route path="/architecture" element={<Architecture />} />
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