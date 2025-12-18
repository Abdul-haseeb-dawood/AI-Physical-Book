import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

// Layout wrapper to add the chat widget to every page
const LayoutWrapper = ({ children }) => {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
};

export default LayoutWrapper;