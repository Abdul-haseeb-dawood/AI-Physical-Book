// docusaurus-plugin-chat/src/index.js
const path = require('path');

module.exports = function (context, options) {
  return {
    name: 'docusaurus-plugin-chat',
    
    getClientModules() {
      return [path.resolve(__dirname, './chat-widget.js')];
    },
    
    configureWebpack(config, isServer, utils) {
      return {
        resolve: {
          alias: {
            '@chat-widget': path.resolve(__dirname, './chat-widget.js'),
          },
        },
      };
    },
  };
};