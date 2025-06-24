import React, { useState, useEffect } from 'react';
import { useNavigation } from '../../contexts/NavigationContext';
import HamburgerMenu from '../navigation/HamburgerMenu';
import DesktopSidebar from '../navigation/DesktopSidebar';
import './ResponsiveLayout.css';

interface NavItem {
  path: string;
  icon: string;
  label: string;
}

interface ResponsiveLayoutProps {
  children: React.ReactNode;
  navItems: NavItem[];
}

const ResponsiveLayout: React.FC<ResponsiveLayoutProps> = ({ children, navItems }) => {
  const { isMobile, closeMobileMenu } = useNavigation();
  const [showDesktopSidebar, setShowDesktopSidebar] = useState(false);

  // Determine if we should show desktop sidebar vs hamburger menu
  useEffect(() => {
    const checkScreenSize = () => {
      // Show desktop sidebar on screens wider than 1200px
      setShowDesktopSidebar(window.innerWidth >= 1200);
    };

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  return (
    <div className="responsive-layout">
      {/* Desktop Sidebar for large screens */}
      {showDesktopSidebar && !isMobile && (
        <DesktopSidebar navItems={navItems} />
      )}
      
      {/* Hamburger Menu for mobile and smaller desktop screens */}
      {(!showDesktopSidebar || isMobile) && (
        <HamburgerMenu navItems={navItems} onClose={closeMobileMenu} />
      )}
      
      {/* Main Content Area */}
      <main className={`main-content-area ${isMobile ? 'mobile' : 'desktop'} ${showDesktopSidebar ? 'with-sidebar' : ''}`}>
        {children}
      </main>
    </div>
  );
};

export default ResponsiveLayout;