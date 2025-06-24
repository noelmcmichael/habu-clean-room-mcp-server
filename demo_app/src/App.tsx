import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import { ConversationProvider } from './contexts/ConversationContext';
import './App.css';
import './components/DemoPhase4.css';

// Lazy load pages for better bundle splitting
const Cleanrooms = lazy(() => import('./pages/Cleanrooms'));
const SystemHealth = lazy(() => import('./pages/SystemHealth'));
const ApiExplorer = lazy(() => import('./pages/ApiExplorer'));
const Architecture = lazy(() => import('./pages/Architecture'));

// Loading component for lazy-loaded pages
const PageLoader: React.FC = () => (
  <div className="page-loader">
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p>Loading page...</p>
    </div>
  </div>
);

const Navigation: React.FC = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: '💬', label: 'AI Assistant' },
    { path: '/cleanrooms', icon: '🏛️', label: 'Cleanrooms' },
    { path: '/health', icon: '📈', label: 'System Health' },
    { path: '/api-explorer', icon: '⚙️', label: 'API Explorer' },
    { path: '/architecture', icon: '📐', label: 'Architecture' },
  ];

  return (
    <div className="sidebar-content">
      <div className="sidebar-header">
        <Link to="/" className="logo-link">
          <div className="logo">
            <span className="logo-icon">🏠</span>
            <span className="logo-text">ICDC</span>
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
            <span className="status-dot real"></span>
            <span>Real API</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const MainContent: React.FC = () => {
  return (
    <div className="main-content">
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/cleanrooms" element={<Cleanrooms />} />
          <Route path="/health" element={<SystemHealth />} />
          <Route path="/api-explorer" element={<ApiExplorer />} />
          <Route path="/architecture" element={<Architecture />} />
        </Routes>
      </Suspense>
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
      <ConversationProvider>
        <div className="app">
          <div className="app-layout">
            <aside className="sidebar">
              <Navigation />
            </aside>
            <MainContent />
          </div>
        </div>
      </ConversationProvider>
    </Router>
  );
}

export default App;