import React, { useState } from 'react';

interface MessageActionsProps {
  messageId: string;
  messageContent: string;
  messageType: 'user' | 'assistant';
  onCopy?: (content: string) => void;
  onRegenerate?: (messageId: string) => void;
  onFeedback?: (messageId: string, feedback: 'positive' | 'negative', comment?: string) => void;
}

const MessageActions: React.FC<MessageActionsProps> = ({
  messageId,
  messageContent,
  messageType,
  onCopy,
  onRegenerate,
  onFeedback
}) => {
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    if (onCopy) {
      onCopy(messageContent);
    } else {
      try {
        await navigator.clipboard.writeText(messageContent);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (error) {
        console.error('Failed to copy:', error);
      }
    }
  };

  const handleFeedback = (type: 'positive' | 'negative') => {
    if (type === 'negative') {
      setShowFeedbackForm(true);
    } else {
      onFeedback?.(messageId, type);
    }
  };

  const submitFeedback = () => {
    onFeedback?.(messageId, 'negative', feedbackComment);
    setShowFeedbackForm(false);
    setFeedbackComment('');
  };

  return (
    <div className="message-actions">
      <div className="action-buttons">
        <button
          className="action-button copy-button"
          onClick={handleCopy}
          title="Copy message"
        >
          {copied ? '✅ Copied!' : '📋 Copy'}
        </button>
        
        {messageType === 'assistant' && onRegenerate && (
          <button
            className="action-button regenerate-button"
            onClick={() => onRegenerate(messageId)}
            title="Regenerate response"
          >
            🔄 Regenerate
          </button>
        )}
        
        {messageType === 'assistant' && onFeedback && (
          <>
            <button
              className="action-button feedback-button positive"
              onClick={() => handleFeedback('positive')}
              title="This response was helpful"
            >
              👍
            </button>
            <button
              className="action-button feedback-button negative"
              onClick={() => handleFeedback('negative')}
              title="This response needs improvement"
            >
              👎
            </button>
          </>
        )}
      </div>

      {showFeedbackForm && (
        <div className="feedback-form">
          <div className="feedback-form-header">
            <h4>Help us improve</h4>
            <button 
              className="close-button"
              onClick={() => setShowFeedbackForm(false)}
            >
              ✕
            </button>
          </div>
          <textarea
            className="feedback-textarea"
            placeholder="What could be improved about this response?"
            value={feedbackComment}
            onChange={(e) => setFeedbackComment(e.target.value)}
            rows={3}
          />
          <div className="feedback-form-actions">
            <button
              className="submit-feedback-button"
              onClick={submitFeedback}
            >
              Submit Feedback
            </button>
            <button
              className="cancel-feedback-button"
              onClick={() => setShowFeedbackForm(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageActions;