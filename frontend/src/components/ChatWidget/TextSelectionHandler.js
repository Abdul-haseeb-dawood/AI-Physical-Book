// Text selection handler for detecting selected text on the page
class TextSelectionHandler {
  constructor(onSelectionCallback) {
    this.onSelectionCallback = onSelectionCallback;
    this.init();
  }

  init() {
    // Listen for mouse up event to detect text selection
    document.addEventListener('mouseup', this.handleSelection.bind(this));
    // Also listen for touchend for mobile devices
    document.addEventListener('touchend', this.handleSelection.bind(this));
  }

  handleSelection() {
    // Get the selected text
    const selectedText = window.getSelection().toString().trim();
    
    // Only trigger callback if there's actual selected text
    if (selectedText) {
      this.onSelectionCallback(selectedText);
    }
  }

  // Method to get the current selection with additional context
  getCurrentSelectionWithContext() {
    const selection = window.getSelection();
    if (!selection.toString().trim()) {
      return null;
    }

    // Get the surrounding context of the selection
    const range = selection.getRangeAt(0);
    const startContainer = range.startContainer;
    
    // Try to find the nearest heading to provide context
    let contextElement = startContainer.parentElement;
    let chapter = 'Unknown Chapter';
    
    // Look up the DOM tree to find a heading element
    while (contextElement && contextElement !== document.body) {
      if (contextElement.tagName && ['H1', 'H2', 'H3'].includes(contextElement.tagName)) {
        chapter = contextElement.textContent;
        break;
      }
      contextElement = contextElement.parentElement;
    }
    
    return {
      text: selection.toString().trim(),
      chapter: chapter,
      page: window.location.pathname
    };
  }
}

export default TextSelectionHandler;