import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './HamburgerMenu.css';

interface NavItem {
  path: string;
  icon: string;
  label: string;
}

interface HamburgerMenuProps {
  navItems: NavItem[];
  onClose?: () => void;
}

const HamburgerMenu: React.FC<HamburgerMenuProps> = ({ navItems, onClose }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const menuRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // Close menu when route changes
  useEffect(() => {
    setIsOpen(false);
    onClose?.();
  }, [location.pathname, onClose]);

  // Handle click outside to close menu
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        isOpen &&
        menuRef.current &&
        buttonRef.current &&
        !menuRef.current.contains(event.target as Node) &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
        onClose?.();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen, onClose]);

  // Handle escape key
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        setIsOpen(false);
        onClose?.();
        buttonRef.current?.focus();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Prevent body scroll when menu is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleLinkClick = () => {
    setIsOpen(false);
    onClose?.();
  };

  return (
    <>
      {/* Hamburger Button */}
      <button
        ref={buttonRef}
        className={`hamburger-button ${isOpen ? 'open' : ''}`}
        onClick={toggleMenu}
        aria-label={isOpen ? 'Close navigation menu' : 'Open navigation menu'}
        aria-expanded={isOpen}
        aria-controls="navigation-menu"
      >
        <span className="hamburger-line"></span>
        <span className="hamburger-line"></span>
        <span className="hamburger-line"></span>
      </button>

      {/* Backdrop */}
      {isOpen && <div className="hamburger-backdrop" onClick={() => setIsOpen(false)} />}

      {/* Navigation Menu */}
      <nav
        ref={menuRef}
        id="navigation-menu"
        className={`hamburger-nav ${isOpen ? 'open' : ''}`}
        aria-hidden={!isOpen}
      >
        {/* Menu Header */}
        <div className="hamburger-header">
          <Link to="/" className="hamburger-logo" onClick={handleLinkClick}>
            <span className="logo-icon">🏠</span>
            <span className="logo-text">ICDC</span>
          </Link>
        </div>

        {/* Menu Items */}
        <div className="hamburger-menu-items">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`hamburger-nav-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={handleLinkClick}
              tabIndex={isOpen ? 0 : -1}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </Link>
          ))}
        </div>

        {/* Menu Footer */}
        <div className="hamburger-footer">
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
      </nav>
    </>
  );
};

export default HamburgerMenu;