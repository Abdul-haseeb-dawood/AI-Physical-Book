// docusaurus-plugin-chat/src/chat-widget.js

import React from 'react';
import { useDoc } from '@docusaurus/theme-common/internal';
import ChatWidget from '../../frontend/src/components/ChatWidget/ChatWidget';

// This component will be injected into Docusaurus pages
const ChatWidgetInjector = () => {
  const { metadata } = useDoc();

  // Only show the chat widget on docs pages, not on blog or other pages
  if (metadata && metadata.editUrl) {
    return <ChatWidget />;
  }

  return null;
};

export default ChatWidgetInjector;