import React, { useState, useEffect, useCallback } from 'react';

interface DemoError {
  id: string;
  type: 'api' | 'network' | 'auth' | 'timeout' | 'server' | 'unknown';
  message: string;
  originalError?: string;
  timestamp: Date;
  resolved: boolean;
  autoRetryAttempts: number;
  maxRetryAttempts: number;
}

interface DemoErrorHandlerProps {
  onError: (error: DemoError) => void;
  onRetry: () => Promise<boolean>;
  children: React.ReactNode;
}

interface ErrorRecoveryProps {
  error: DemoError;
  onRetry: () => void;
  onDismiss: () => void;
  onSwitchToDemo: () => void;
}

const ErrorRecovery: React.FC<ErrorRecoveryProps> = ({ 
  error, 
  onRetry, 
  onDismiss, 
  onSwitchToDemo 
}) => {
  const getErrorIcon = (type: DemoError['type']): string => {
    switch (type) {
      case 'api': return '🔌';
      case 'network': return '🌐';
      case 'auth': return '🔐';
      case 'timeout': return '⏱️';
      case 'server': return '🖥️';
      default: return '⚠️';
    }
  };

  const getErrorTitle = (type: DemoError['type']): string => {
    switch (type) {
      case 'api': return 'API Connection Issue';
      case 'network': return 'Network Connectivity Problem';
      case 'auth': return 'Authentication Error';
      case 'timeout': return 'Request Timeout';
      case 'server': return 'Server Error';
      default: return 'Unexpected Error';
    }
  };

  const getSuggestions = (type: DemoError['type']): string[] => {
    switch (type) {
      case 'api':
        return [
          'Check if the MCP server is running',
          'Verify API endpoints are accessible',
          'Switch to demo mode for presentation'
        ];
      case 'network':
        return [
          'Check your internet connection',
          'Try refreshing the page',
          'Use demo mode for offline presentation'
        ];
      case 'auth':
        return [
          'Verify API credentials are configured',
          'Check authentication tokens',
          'Contact administrator for access'
        ];
      case 'timeout':
        return [
          'Server may be experiencing high load',
          'Try again in a few moments',
          'Use demo mode for immediate presentation'
        ];
      case 'server':
        return [
          'Server is temporarily unavailable',
          'Check server logs for details',
          'Switch to demo mode for presentation'
        ];
      default:
        return [
          'Try refreshing the page',
          'Check browser console for details',
          'Use demo mode as fallback'
        ];
    }
  };

  return (
    <div className="error-recovery-panel">
      <div className="error-header">
        <span className="error-icon">{getErrorIcon(error.type)}</span>
        <h3>{getErrorTitle(error.type)}</h3>
      </div>

      <div className="error-message">
        <p>{error.message}</p>
        {error.originalError && (
          <details className="error-details">
            <summary>Technical Details</summary>
            <pre>{error.originalError}</pre>
          </details>
        )}
      </div>

      <div className="error-suggestions">
        <h4>💡 Suggested Actions:</h4>
        <ul>
          {getSuggestions(error.type).map((suggestion, index) => (
            <li key={index}>{suggestion}</li>
          ))}
        </ul>
      </div>

      <div className="recovery-actions">
        <button 
          className="retry-btn primary"
          onClick={onRetry}
          disabled={error.autoRetryAttempts >= error.maxRetryAttempts}
        >
          🔄 Retry ({error.autoRetryAttempts}/{error.maxRetryAttempts})
        </button>
        
        <button 
          className="demo-mode-btn secondary"
          onClick={onSwitchToDemo}
        >
          🎬 Switch to Demo Mode
        </button>
        
        <button 
          className="dismiss-btn tertiary"
          onClick={onDismiss}
        >
          ✕ Dismiss
        </button>
      </div>

      <div className="error-timestamp">
        Occurred at: {error.timestamp.toLocaleString()}
      </div>
    </div>
  );
};

const DemoErrorHandler: React.FC<DemoErrorHandlerProps> = ({ 
  onError, 
  onRetry, 
  children 
}) => {
  const [currentError, setCurrentError] = useState<DemoError | null>(null);
  const [isRetrying, setIsRetrying] = useState(false);
  const [isDemoMode, setIsDemoMode] = useState(false);

  const createError = (
    type: DemoError['type'],
    message: string,
    originalError?: string
  ): DemoError => {
    return {
      id: Date.now().toString(),
      type,
      message,
      originalError,
      timestamp: new Date(),
      resolved: false,
      autoRetryAttempts: 0,
      maxRetryAttempts: 3
    };
  };

  const handleError = useCallback((error: any) => {
    let demoError: DemoError;

    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      demoError = createError(
        'network',
        'Unable to connect to the demo server. This might be due to network issues or server unavailability.',
        error.message
      );
    } else if (error.status === 401 || error.status === 403) {
      demoError = createError(
        'auth',
        'Authentication failed. Please check your API credentials or contact support.',
        error.message
      );
    } else if (error.status === 404) {
      demoError = createError(
        'api',
        'API endpoint not found. The demo server may not be properly configured.',
        error.message
      );
    } else if (error.status >= 500) {
      demoError = createError(
        'server',
        'The demo server is experiencing issues. This is temporary and should resolve shortly.',
        error.message
      );
    } else if (error.name === 'AbortError' || error.message.includes('timeout')) {
      demoError = createError(
        'timeout',
        'The request timed out. The server may be busy processing your request.',
        error.message
      );
    } else {
      demoError = createError(
        'unknown',
        'An unexpected error occurred during the demo. Please try again or switch to demo mode.',
        error.message
      );
    }

    setCurrentError(demoError);
    onError(demoError);
  }, [onError]);

  const handleRetry = async () => {
    if (!currentError || isRetrying) return;

    setIsRetrying(true);
    
    try {
      const success = await onRetry();
      if (success) {
        setCurrentError(null);
      } else {
        setCurrentError(prev => prev ? {
          ...prev,
          autoRetryAttempts: prev.autoRetryAttempts + 1
        } : null);
      }
    } catch (error) {
      handleError(error);
    } finally {
      setIsRetrying(false);
    }
  };

  const handleSwitchToDemo = () => {
    setIsDemoMode(true);
    setCurrentError(null);
    // You would implement demo mode switching logic here
    console.log('Switching to demo mode for presentation');
  };

  const handleDismiss = () => {
    setCurrentError(null);
  };

  // Global error handler for the demo
  useEffect(() => {
    const handleGlobalError = (event: ErrorEvent) => {
      handleError(event.error);
    };

    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      handleError(event.reason);
    };

    window.addEventListener('error', handleGlobalError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.removeEventListener('error', handleGlobalError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, [handleError]);

  return (
    <div className="demo-error-handler">
      {currentError && (
        <div className="error-overlay">
          <ErrorRecovery
            error={currentError}
            onRetry={handleRetry}
            onDismiss={handleDismiss}
            onSwitchToDemo={handleSwitchToDemo}
          />
        </div>
      )}
      
      {isDemoMode && (
        <div className="demo-mode-banner">
          <span className="demo-mode-icon">🎬</span>
          <span>Demo Mode Active - Using simulated responses for presentation</span>
          <button onClick={() => setIsDemoMode(false)}>
            Exit Demo Mode
          </button>
        </div>
      )}
      
      {isRetrying && (
        <div className="retry-indicator">
          <span className="retry-spinner">🔄</span>
          <span>Retrying connection...</span>
        </div>
      )}
      
      {children}
    </div>
  );
};

export default DemoErrorHandler;