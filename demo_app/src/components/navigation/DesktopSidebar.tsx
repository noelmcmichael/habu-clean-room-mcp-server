import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './DesktopSidebar.css';

interface NavItem {
  path: string;
  icon: string;
  label: string;
}

interface DesktopSidebarProps {
  navItems: NavItem[];
}

const DesktopSidebar: React.FC<DesktopSidebarProps> = ({ navItems }) => {
  const location = useLocation();

  return (
    <aside className="desktop-sidebar">
      {/* Sidebar Header */}
      <div className="sidebar-header">
        <Link to="/" className="sidebar-logo">
          <span className="logo-icon">🏠</span>
          <span className="logo-text">ICDC</span>
        </Link>
      </div>

      {/* Navigation Items */}
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar-nav-item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </Link>
        ))}
      </nav>

      {/* Sidebar Footer */}
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
    </aside>
  );
};

export default DesktopSidebar;