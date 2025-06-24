import React from 'react';
import { useNavigation } from '../../contexts/NavigationContext';
import HamburgerMenu from '../navigation/HamburgerMenu';
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

  return (
    <div className="responsive-layout">
      {/* Hamburger Menu - Always present */}
      <HamburgerMenu navItems={navItems} onClose={closeMobileMenu} />
      
      {/* Main Content Area */}
      <main className={`main-content-area ${isMobile ? 'mobile' : 'desktop'}`}>
        {children}
      </main>
    </div>
  );
};

export default ResponsiveLayout;