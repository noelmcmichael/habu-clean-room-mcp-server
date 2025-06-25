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
    <div className="mode-switcher-simple">
      <div className="current-mode-display">
        <span className="current-mode-label">Mode: </span>
        <span className="current-mode-icon">{currentConfig.icon}</span>
        <span className="current-mode-name">{currentConfig.name}</span>
      </div>
      
      <div className="mode-toggle-buttons">
        {Object.values(CHAT_MODE_CONFIGS).map((config) => (
          <button
            key={config.mode}
            className={`mode-toggle ${modeState.currentMode === config.mode ? 'active' : ''}`}
            onClick={() => handleModeSwitch(config.mode)}
            title={config.description}
          >
            <span className="toggle-icon">{config.icon}</span>
            <span className="toggle-name">{config.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default ModeSwitcher;