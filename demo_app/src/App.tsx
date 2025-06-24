import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import { ConversationProvider } from './contexts/ConversationContext';
import { NavigationProvider } from './contexts/NavigationContext';
import { ChatModeProvider } from './contexts/ChatModeContext';
import ResponsiveLayout from './components/layout/ResponsiveLayout';
import './App.css';
import './components/DemoPhase4.css';
import './styles/responsive.css';

// Direct imports instead of lazy loading for debugging
import Cleanrooms from './pages/Cleanrooms';
import SystemHealth from './pages/SystemHealth';
import ApiExplorer from './pages/ApiExplorer';
import Architecture from './pages/Architecture';

// Navigation configuration
const navItems = [
  { path: '/', icon: '💬', label: 'AI Assistant' },
  { path: '/cleanrooms', icon: '🏛️', label: 'Cleanrooms' },
  { path: '/health', icon: '📈', label: 'System Health' },
  { path: '/api-explorer', icon: '⚙️', label: 'API Explorer' },
  { path: '/architecture', icon: '📐', label: 'Architecture' },
];

const MainContent: React.FC = () => {
  return (
    <div className="page-content">
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/cleanrooms" element={<Cleanrooms />} />
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
      <NavigationProvider>
        <ConversationProvider>
          <ChatModeProvider>
            <ResponsiveLayout navItems={navItems}>
              <MainContent />
            </ResponsiveLayout>
          </ChatModeProvider>
        </ConversationProvider>
      </NavigationProvider>
    </Router>
  );
}

export default App;