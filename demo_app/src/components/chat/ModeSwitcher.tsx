import React from 'react';
import { ChatMode, CHAT_MODE_CONFIGS } from '../../types/ChatModes';
import { useChatMode } from '../../contexts/ChatModeContext';
import './ModeSwitcher.css';

const ModeSwitcher: React.FC = () => {
  const { modeState, switchMode, getCurrentModeConfig } = useChatMode();
  const currentConfig = getCurrentModeConfig();

  const handleModeSwitch = (mode: ChatMode) => {
    if (mode !== modeState.currentMode) {
      switchMode(mode);
    }
  };

  return (
    <div className="mode-switcher">
      <div className="mode-switcher-header">
        <h3>AI Assistant Mode</h3>
        <div className="current-mode-indicator">
          <span className="mode-icon">{currentConfig.icon}</span>
          <span className="mode-name">{currentConfig.name}</span>
        </div>
      </div>
      
      <div className="mode-options">
        {Object.values(CHAT_MODE_CONFIGS).map((config) => (
          <button
            key={config.mode}
            className={`mode-option ${modeState.currentMode === config.mode ? 'active' : ''}`}
            onClick={() => handleModeSwitch(config.mode)}
            title={config.description}
          >
            <div className="mode-option-content">
              <div className="mode-option-header">
                <span className="mode-option-icon">{config.icon}</span>
                <span className="mode-option-name">{config.name}</span>
              </div>
              <p className="mode-option-description">{config.description}</p>
              
              <div className="mode-capabilities">
                {config.capabilities.slice(0, 3).map((capability, index) => (
                  <span key={index} className="capability-tag">
                    {capability}
                  </span>
                ))}
                {config.capabilities.length > 3 && (
                  <span className="capability-more">
                    +{config.capabilities.length - 3} more
                  </span>
                )}
              </div>
            </div>
            
            {modeState.currentMode === config.mode && (
              <div className="active-indicator">
                <span>✓</span>
              </div>
            )}
          </button>
        ))}
      </div>
      
      <div className="mode-context-info">
        {modeState.currentMode === ChatMode.MANAGER && modeState.businessContext && (
          <div className="business-context">
            <h4>📊 Current Status</h4>
            <div className="context-stats">
              <div className="stat">
                <span className="stat-value">{modeState.businessContext.cleanroomCount}</span>
                <span className="stat-label">Cleanrooms</span>
              </div>
              <div className="stat">
                <span className="stat-value">{modeState.businessContext.activeQueries}</span>
                <span className="stat-label">Active Queries</span>
              </div>
              <div className="stat">
                <span className="stat-value">{modeState.businessContext.pendingExports}</span>
                <span className="stat-label">Pending Exports</span>
              </div>
            </div>
          </div>
        )}
        
        {modeState.currentMode === ChatMode.API_EXPERT && modeState.apiContext && (
          <div className="api-context">
            <h4>🔧 API Status</h4>
            <div className="context-info">
              <div className="api-stat">
                <span className="api-label">Available Tools:</span>
                <span className="api-value">{modeState.apiContext.availableTools.length}</span>
              </div>
              <div className="api-stat">
                <span className="api-label">API Version:</span>
                <span className="api-value">{modeState.apiContext.apiVersion}</span>
              </div>
              {modeState.apiContext.recentChanges.length > 0 && (
                <div className="api-stat">
                  <span className="api-label">Recent Updates:</span>
                  <span className="api-value">{modeState.apiContext.recentChanges.length} changes</span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ModeSwitcher;