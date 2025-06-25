import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import EnhancedChatInterface from './components/EnhancedChatInterface';
import ChatFocusedLayout from './components/layout/ChatFocusedLayout';
import { ConversationProvider } from './contexts/ConversationContext';
import { NavigationProvider } from './contexts/NavigationContext';
import { ChatModeProvider } from './contexts/ChatModeContext';
import ResponsiveLayout from './components/layout/ResponsiveLayout';
import './App.css';
import './components/DemoPhase4.css';
import './styles/responsive.css';
import './styles/enhanced-chat.css';
import './styles/chat-focused.css';

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
        <Route path="/cleanrooms" element={<Cleanrooms />} />
        <Route path="/health" element={<SystemHealth />} />
        <Route path="/api-explorer" element={<ApiExplorer />} />
        <Route path="/architecture" element={<Architecture />} />
      </Routes>
    </div>
  );
};

const ChatPage: React.FC = () => {
  // For the chat page, we want full viewport without sidebar
  return <ChatFocusedLayout />;
};

function App() {
  return (
    <Router>
      <NavigationProvider>
        <ConversationProvider>
          <ChatModeProvider>
            <Routes>
              {/* Chat page gets full viewport without sidebar */}
              <Route path="/" element={<ChatPage />} />
              
              {/* Other pages use responsive layout with sidebar */}
              <Route path="/*" element={
                <ResponsiveLayout navItems={navItems}>
                  <MainContent />
                </ResponsiveLayout>
              } />
            </Routes>
          </ChatModeProvider>
        </ConversationProvider>
      </NavigationProvider>
    </Router>
  );
}

export default App;